import chromadb
from langchain_core.messages import SystemMessage, HumanMessage

from src.types.state import State
from src.llms.clients import local_llm
from src.prompts import COLLECTION_DECIDER_SYSTEM_PROMPT




def collection_decision_node(state: State) -> dict:
    """Checks if existing knowledge bases (collections) are sufficient for the user's request."""
    print("⫘" * 60)
    print("⫘" * 60)
    print("3) checking for pre existing vector databases")
    generated_query = state["generated_query"]

    chroma_client = chromadb.PersistentClient()
    existing_collections = [collection.name for collection in chroma_client.list_collections()]

    if not existing_collections:
        return {
            "prior_collection_exists": False,
            "collection_to_be_used": generated_query,
        }

    decider_messages = [
        SystemMessage(content=COLLECTION_DECIDER_SYSTEM_PROMPT),
        HumanMessage(
            content=f"Query: {generated_query}\nExisting Collections: {existing_collections}"
        ),
    ]

    try:
        checker_response = local_llm.invoke(decider_messages)
        result = str(checker_response.content).strip().strip("'\"`")

        if result in existing_collections:
            return {
                "prior_collection_exists": True,
                "collection_to_be_used": result,
            }
    except Exception as e:
        print(f"Error evaluating collection match: {e}")

    return {
        "prior_collection_exists": False,
        "collection_to_be_used": generated_query,
    }