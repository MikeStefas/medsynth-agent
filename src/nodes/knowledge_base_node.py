import sys
from langchain_core.messages import SystemMessage
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from src.types.state import State
from src.llms.clients import local_llm
from src.prompts import QUERY_GENERATOR_SYSTEM_PROMPT
from src.tools.pubmed import search_pubmed_pmids, fetch_article_metadata, print_article_metadata


def build_knowledge_base_node(state: State) -> dict:
    # Step 1: Generate PubMed query string from user messages
    try:
        messages = [
            SystemMessage(content=QUERY_GENERATOR_SYSTEM_PROMPT),
        ] + state["messages"]
        
        response = local_llm.invoke(messages)
        query = str(response.content).strip()
    except Exception as err:
        print(f"Error generating query: {err}")
        sys.exit(1)
    
    print("=" * 50)
    print(f"Generated Query: {query}")
    print("=" * 50)

    # Step 2: Fetch PubMed PMIDs & metadata, then embed into Chroma Vector DB
    pmids = search_pubmed_pmids(query, retmax=500)
    print(f"Fetched {len(pmids)} PMIDs. Embedding into Knowledge Base...\n")

    chroma_client = chromadb.PersistentClient()
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="NeuML/pubmedbert-base-embeddings", 
        device="cpu"
    )
    collection = chroma_client.get_or_create_collection(
        name=query.replace(" ", "_"), 
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
    
    return {"query": query}
