import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from src.types.state import State
from src.tools.pubmed import search_pubmed_pmids, fetch_article_metadata, print_article_metadata
from src.variables import PUBMED_RETMAX, EMBEDDING_MODEL_NAME


def knowledge_base_node(state: State) -> dict:
    """Builds knowledge base (vector db) from PubMed articles."""
    query = state["generated_query"]
    collection_name = query.replace(" ", "_")
    print(f"[Node: Knowledge Base] Fetching articles from PubMed and building collection '{collection_name}'...")

    pmids = search_pubmed_pmids(query, retmax=PUBMED_RETMAX)

    chroma_client = chromadb.PersistentClient()
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME, 
        device="cpu"
    )
    collection = chroma_client.get_or_create_collection(
        name=collection_name, 
        embedding_function=embedding_function
    )
    
    for article_id in pmids:
        try:
            metadata = fetch_article_metadata(article_id)
            collection.add(
                documents=[metadata["title"] + ". " + metadata["abstract"]],
                metadatas=[metadata],
                ids=[str(article_id)]
            )
        except Exception as e:
            pass
    
    return {"collection_to_be_used": collection_name}
