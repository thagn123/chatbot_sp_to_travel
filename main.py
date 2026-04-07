import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from agent.graph import travel_buddy

# Load environment variables
load_dotenv()

def run_agent(user_input: str):
    print(f"\n--- User: {user_input} ---")
    
    # Initial state
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "budget": 0,
        "flight_results": [],
        "hotel_results": [],
        "origin": "",
        "destination": "",
        "date": ""
    }
    
    # Run the graph
    final_state = travel_buddy.invoke(initial_state)
    
    # Get the last message (the final answer)
    final_answer = final_state['messages'][-1].content
    print(f"\nTravelBuddy:\n{final_answer}")
    return final_answer

if __name__ == "__main__":
    # Test Case 1: Full info
    run_agent("Tôi muốn đi Đà Nẵng từ Hà Nội cuối tuần này budget 5 triệu")
    
    # Test Case 2: Missing info
    # run_agent("Tôi muốn đi Đà Nẵng")
    
    # Test Case 3: Low budget
    # run_agent("Tôi muốn đi Đà Nẵng từ Sài Gòn với 1 triệu")
