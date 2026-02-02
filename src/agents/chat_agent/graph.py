from langgraph.graph import StateGraph, END
from src.agents.chat_agent.states.chat_agent_state import ChatAgentState
from src.agents.chat_agent.nodes.chat_node import chat_node
from langsmith import traceable

@traceable
def chat_node(state):
    return state



builder = StateGraph(ChatAgentState)

builder.add_node("chat", chat_node)
builder.set_entry_point("chat")
builder.add_edge("chat", END)

chat_graph = builder.compile()  
