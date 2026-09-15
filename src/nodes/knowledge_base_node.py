import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from src.types.state import State
from src.tools.pubmed import search_pubmed_pmids, fetch_article_metadata, print_article_metadata
from src.variables import PUBMED_RETMAX, EMBEDDING_MODEL_NAME


def knowledge_base_node(state: State) -> dict:
    """Builds knowledge base (vector db) from PubMed articles."""
    query = state["generated_query"]
    
    collection_name = query.replace(" ", "_")

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
    
    for idx, article_id in enumerate(pmids, 1):
        try:
            print(f"================ Article {idx}/{len(pmids)} [PMID: {article_id}] ================")
            metadata = fetch_article_metadata(article_id)
            print_article_metadata(metadata)
            print("=" * 70 + "\n")
            
            collection.add(
                documents=[metadata["title"] + ". " + metadata["abstract"]],
                metadatas=[metadata],
                ids=[str(article_id)]
            )
        except Exception as e:
            print(f"[{idx}/{len(pmids)}] Error fetching PMID {article_id}: {e}\n")
    
    return {"collection_to_be_used": collection_name}
