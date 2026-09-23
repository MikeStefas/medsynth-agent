from pydantic import BaseModel, Field
from typing import List
from src.types.clinical_rules import ClinicalRule


class QueryOutput(BaseModel):
    query: str = Field(
        description="Effective PubMed search query string joining core medical concepts with AND"
    )
    target_class: str = Field(
        description="The primary clinical condition, disease, or target minority class (e.g., 'sepsis', 'type 2 diabetes and heart failure')"
    )

class ClinicalRuleExtractorOutput(BaseModel):
    clinical_rules: List[ClinicalRule] = Field(
        description="List of clinical rules extracted from the literature"
    )


    