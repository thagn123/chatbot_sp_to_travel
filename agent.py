import os
import json
import logging
from typing import Annotated, List, Union, TypedDict
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from tools.tools import tools_list
from config.settings import settings

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# --- State Definition ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# --- Node Implementations ---
# Khởi tạo Gemini thay vì OpenAI
llm = ChatGoogleGenerativeAI(
    api_key=settings.GEMINI_API_KEY,
    model=settings.MODEL_NAME,
    temperature=settings.TEMPERATURE
)
llm_with_tools = llm.bind_tools(tools_list)

# Load system prompt
SYSTEM_PROMPT_PATH = "prompts/system_prompt.txt"
if os.path.exists(SYSTEM_PROMPT_PATH):
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt_content = f.read()
else:
    system_prompt_content = "Bạn là TravelBuddy, trợ lý du lịch thông minh."

def call_model(state: AgentState) -> dict:
    """LLM Node: Quyết định hành động tiếp theo."""
    logger.info("Node: call_model")
    messages = state['messages']
    
    # Ensure system prompt is present
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=system_prompt_content)] + messages
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def execute_tools(state: AgentState) -> dict:
    """Tool Node: Thực thi tool calls từ LLM."""
    logger.info("Node: execute_tools")
    messages = state['messages']
    last_message = messages[-1]
    
    tool_outputs = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
        
        # Find the tool
        selected_tool = next((t for t in tools_list if t.name == tool_name), None)
        if selected_tool:
            try:
                result = selected_tool.invoke(tool_args)
                tool_outputs.append(
                    ToolMessage(tool_call_id=tool_call["id"], content=str(result))
                )
            except Exception as e:
                logger.error(f"Tool execution failed: {e}")
                tool_outputs.append(
                    ToolMessage(
                        tool_call_id=tool_call["id"], 
                        content=json.dumps({"success": False, "error": str(e)})
                    )
                )
        else:
            logger.warning(f"Tool {tool_name} not found.")
            
    return {"messages": tool_outputs}

def router(state: AgentState) -> str:
    """Decision Node: Chuyển hướng luồng chạy."""
    messages = state['messages']
    last_message = messages[-1]
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

# --- Graph Construction ---
def create_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", execute_tools)
    
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        router,
        {
            "tools": "tools",
            "end": END
        }
    )
    workflow.add_edge("tools", "agent")
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

# Final Agent Instance
travel_agent = create_graph()

def log_to_file(text: str):
    """Lưu log hội thoại vào file test_results.md"""
    try:
        with open("test_results.md", "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception as e:
        logger.error(f"Failed to log to file: {e}")

# --- Execution Helper ---
def run_travel_buddy():
    print("="*50)
    print("Chào mừng bạn đến với TravelBuddy! (Gõ 'quit' hoặc 'exit' để thoát)")
    print("="*50 + "\n")
    
    log_to_file("\n" + "="*50)
    log_to_file("Khởi tạo phiên chat mới")
    log_to_file("="*50 + "\n")
    
    config = {"configurable": {"thread_id": "user_session_1"}}
    
    while True:
        try:
            query = input("Bạn: ")
            log_to_file(f"Bạn: {query}")
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Tạm biệt! Chúc bạn một ngày vui vẻ.")
                log_to_file("Tạm biệt! Chúc bạn một ngày vui vẻ.\n")
                break
            
            if not query.strip():
                continue
                
            inputs = {"messages": [HumanMessage(content=query)]}
            
            final_output = None
            for event in travel_agent.stream(inputs, config=config, stream_mode="values"):
                final_output = event
                
            if final_output:
                print("\n" + "="*50)
                print("TRAVELBUDDY:")
                print("="*50)
                content = final_output['messages'][-1].content
                if isinstance(content, list):
                    # Extract text from the list of dicts returned by some LLMs
                    text_blocks = [item.get('text', '') for item in content if isinstance(item, dict) and 'text' in item]
                    response_text = "\n".join(text_blocks)
                else:
                    response_text = str(content)
                print(response_text)
                print("="*50 + "\n")
                
                # Cập nhật log
                log_to_file("\n" + "="*50)
                log_to_file("TRAVELBUDDY:")
                log_to_file("="*50)
                log_to_file(response_text)
                log_to_file("="*50 + "\n")
                
        except KeyboardInterrupt:
            print("\nTạm biệt!")
            log_to_file("Tạm biệt!\n")
            break
        except Exception as e:
            logger.error(f"Lỗi: {e}")

if __name__ == "__main__":
    import sys
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    run_travel_buddy()
