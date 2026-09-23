from typing import Annotated, List, Optional
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from src.types.features import Feature
from src.types.clinical_rules import ClinicalRule


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    generated_query: str
    target_class: str
    prior_collection_exists: bool
    collection_to_be_used: str
    dataset_path: str
    features: List[Feature]
    clinical_rules: List[ClinicalRule]