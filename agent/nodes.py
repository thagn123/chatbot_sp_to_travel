import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage, SystemMessage
from agent.state import AgentState
from tools.tools import tools
from config.settings import settings

# Initialize LLM with tool binding
llm = ChatOpenAI(
    api_key=settings.OPENAI_API_KEY,
    model=settings.MODEL_NAME,
    temperature=settings.TEMPERATURE
)
llm_with_tools = llm.bind_tools(tools)

# Load system prompt
with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

def call_model(state: AgentState):
    """
    LLM Node: Gọi model để quyết định hành động tiếp theo.
    """
    messages = state['messages']
    # Add system prompt if it's the first message
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=system_prompt)] + messages
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def tool_node(state: AgentState):
    """
    Tool Node: Thực thi các tool được yêu cầu bởi LLM.
    """
    messages = state['messages']
    last_message = messages[-1]
    
    tool_outputs = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        # Find the tool and execute
        selected_tool = next(t for t in tools if t.name == tool_name)
        try:
            result = selected_tool.invoke(tool_args)
            tool_outputs.append(
                ToolMessage(
                    tool_call_id=tool_call["id"],
                    content=str(result)
                )
            )
        except Exception as e:
            tool_outputs.append(
                ToolMessage(
                    tool_call_id=tool_call["id"],
                    content=json.dumps({"success": False, "error": str(e)})
                )
            )
            
    return {"messages": tool_outputs}

def should_continue(state: AgentState):
    """
    Decision Node: Kiểm tra xem có cần gọi tool tiếp hay không.
    """
    messages = state['messages']
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return "tools"
    return "end"
