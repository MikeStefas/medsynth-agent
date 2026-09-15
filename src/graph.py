from langgraph.graph import StateGraph, START, END
from src.types.state import State
from src.nodes.query_node import query_node
from src.nodes.collection_decision_node import collection_decision_node
from src.nodes.knowledge_base_node import knowledge_base_node


def should_build_knowledge_base(state: State) -> str:
    # If a prior collection already exists, skip building the knowledge base
    if state.get("prior_collection_exists", False):
        return END
    return "knowledge_base_node"


builder = StateGraph(State)

builder.add_node("query_node", query_node)
builder.add_node("collection_decision_node", collection_decision_node)
builder.add_node("knowledge_base_node", knowledge_base_node)

builder.add_edge(START, "query_node")
builder.add_edge("query_node", "collection_decision_node")

builder.add_conditional_edges(
    "collection_decision_node",
    should_build_knowledge_base
)

builder.add_edge("knowledge_base_node", END)

graph = builder.compile()
