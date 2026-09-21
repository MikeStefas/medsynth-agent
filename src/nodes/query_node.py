import sys
from langchain_core.messages import SystemMessage
from src.types import State, QueryOutput
from src.llms.clients import local_llm
from src.prompts import QUERY_GENERATOR_SYSTEM_PROMPT


def query_node(state: State) -> dict:
    """Generates a PubMed search query and target clinical scenario from user prompt messages."""
    print("[Node: Query Generator] Extracting PubMed query and target clinical scenario from user request...")
    try:
        messages = [
            SystemMessage(content=QUERY_GENERATOR_SYSTEM_PROMPT),
        ] + state["messages"]
        
        structured_llm = local_llm.with_structured_output(QueryOutput)
        result: QueryOutput = structured_llm.invoke(messages)
        
        generated_query = result.query.strip()
        target_scenario = result.target_scenario.strip()
    except Exception as err:
        print(f"Error generating query: {err}")
        sys.exit(1)

    return {
        "generated_query": generated_query,
        "target_scenario": target_scenario,
    }


