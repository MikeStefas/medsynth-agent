from typing import Optional, Union, List, Literal
from pydantic import BaseModel


class ClinicalRule(BaseModel):
    feature_name: str
    operator: Literal[">", "<", ">=", "<=", "=="]
    value: Union[float, int, List[float]]
    rationale: str
    pmid_source: Optional[str] = None
