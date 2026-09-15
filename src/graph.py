from langgraph.graph import StateGraph, START, END
from src.types.state import State
from src.nodes.knowledge_base_node import build_knowledge_base_node

builder = StateGraph(State)

builder.add_node("build_knowledge_base", build_knowledge_base_node)

builder.add_edge(START, "build_knowledge_base")
builder.add_edge("build_knowledge_base", END)

graph = builder.compile()
