from pydantic import BaseModel, Field


class QueryOutput(BaseModel):
    query: str = Field(
        description="Effective PubMed search query string joining core medical concepts with AND"
    )
    target_scenario: str = Field(
        description="The primary clinical condition, disease, or target scenario (e.g., 'sepsis', 'type 2 diabetes', 'heart failure')"
    )
