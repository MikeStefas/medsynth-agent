import sys
from langchain_core.messages import SystemMessage
from src.types.state import State
from src.llms.clients import local_llm
from src.prompts import QUERY_GENERATOR_SYSTEM_PROMPT


def query_node(state: State) -> dict:
    """Generates a PubMed search query from user prompt messages."""
    print(state['features'])
    print("Node 1. Creating query...")
    try:
        messages = [
            SystemMessage(content=QUERY_GENERATOR_SYSTEM_PROMPT),
        ] + state["messages"]
        
        response = local_llm.invoke(messages)
        generated_query = str(response.content).strip()
    except Exception as err:
        print(f"Error generating query: {err}")
        sys.exit(1)
    
    print(f"Generated Query: {generated_query}")

    return {"generated_query": generated_query}

