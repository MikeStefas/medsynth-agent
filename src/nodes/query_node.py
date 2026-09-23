import sys
from langchain_core.messages import SystemMessage
from src.types import State, QueryOutput
from src.llms.clients import local_llm
from src.prompts import QUERY_GENERATOR_SYSTEM_PROMPT




def query_node(state: State) -> dict:
    """Generates a PubMed search query and target class from user prompt messages."""
    print("⫘" * 60)
    print("⫘" * 60)
    print("2) generating query")
    try:
        messages = [
            SystemMessage(content=QUERY_GENERATOR_SYSTEM_PROMPT),
        ] + state["messages"]
        
        structured_llm = local_llm.with_structured_output(QueryOutput)
        result: QueryOutput = structured_llm.invoke(messages)
        
        generated_query = result.query.strip()
        target_class = result.target_class.strip()
        print(f"Generated_query: {generated_query}")
        print(f"Target_class: {target_class}")
    except Exception as err:
        print(f"Error generating query: {err}")
        sys.exit(1)

    return {
        "generated_query": generated_query,
        "target_class": target_class,
    }



