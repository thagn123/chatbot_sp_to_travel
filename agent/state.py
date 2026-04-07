from typing import Annotated, TypedDict, List, Union
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # The messages in the conversation
    messages: Annotated[List[BaseMessage], add_messages]
    # Current planning context
    budget: float
    flight_results: List[dict]
    hotel_results: List[dict]
    origin: str
    destination: str
    date: str
