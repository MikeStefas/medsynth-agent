import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_core.messages import SystemMessage, HumanMessage

from src.types import State, ClinicalRuleExtractorOutput
from src.variables import EMBEDDING_MODEL_NAME
from src.llms.clients import local_llm
from src.prompts import (
    CLINICAL_RULE_EXTRACTOR_SYSTEM_PROMPT,
    clinical_rule_extractor_user_prompt,
)
from src.utils import (
    format_pubmed_abstracts,
    format_column_info,
)




def clinical_rule_extractor_node(state: State) -> dict:
    print("⫘" * 60)
    print("⫘" * 60)
    print("5)extracting clinical rules")
    collection_name = state["collection_to_be_used"]
    
    features = state["features"]
    target_class = state["target_class"]
    
    client = chromadb.PersistentClient()
        
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME, 
        device="cpu"
    )

    collection = client.get_collection(
        collection_name,
        embedding_function=embedding_function
    ) 

    clin_rule_extractor = local_llm.with_structured_output(ClinicalRuleExtractorOutput)


    for feature in features:
            
        search_query = (
            f"Clinical diagnostic criteria, abnormal reference range, and cutoff thresholds "
            f"for {feature.name} in {target_class}. "
            f"Quantitative values, laboratory assays, risk factors, and disease definitions."
        )
        results = collection.query(
            query_texts=[search_query],
            n_results=15
        )   
        metadatas = results["metadatas"][0]
        pubmed_relevant_abstracts_block = format_pubmed_abstracts(metadatas)
        columns_info_str = format_column_info(feature)

        user_prompt = clinical_rule_extractor_user_prompt(
            target_class=target_class,
            feature_name=feature.name,
            column_info_str=columns_info_str,
            pubmed_relevant_abstracts_block=pubmed_relevant_abstracts_block,
        )
        clin_rule_extractor = local_llm.with_structured_output(ClinicalRuleExtractorOutput)
        messages = [
            SystemMessage(content=CLINICAL_RULE_EXTRACTOR_SYSTEM_PROMPT),
            HumanMessage(content=user_prompt),
            ]
        extraction_output= clin_rule_extractor.invoke(messages)

        for clinical_rule in extraction_output.clinical_rules:
            print(clinical_rule)
            print()
        print("_"* 50)

