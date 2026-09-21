import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from src.types import State
from src.variables import EMBEDDING_MODEL_NAME


def clinical_rule_extractor_node(state: State):
    print(f"[Node: Clinical Rule Extractor] Retrieving relevant literature from collection '{state.get('collection_to_be_used')}' for clinical rule extraction...")
    features = state.get("features", [])
    feature_names = [f.name if hasattr(f, "name") else f["name"] for f in features]
    target_scenario = state.get("target_scenario", state.get("generated_query", ""))

    search_query = (
        f"Clinical diagnostic criteria, biomarker cutoff thresholds, and laboratory reference ranges "
        f"in {target_scenario}. "
        f"Quantitative values, severe disease definitions, and mortality risk factors for: {', '.join(feature_names)}."
    )

    client = chromadb.PersistentClient()
    
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME, 
        device="cpu"
    )

    collection = client.get_collection(
        state["collection_to_be_used"],
        embedding_function=embedding_function
    ) 
    
    results = collection.query(
        query_texts=[search_query],
        n_results=30
    )   
    
    for result in results.get("metadatas")[0]:
        print(result)
        print("#" * 80)
    
    print(f"Total articles: {len(results.get('metadatas')[0])}")
    return {}