from typing import List, Dict, Any
from pydantic import BaseModel, Field
from src.types.features import Feature


class DatasetMetadata(BaseModel):
    dataset_name: str
    total_records: int
    target_column: str
    minority_class_label: Any
    minority_prevalence: float               # e.g., 0.32 for 32% deceased
    features: List[Feature]
    covariance_anchor_matrix: Dict[str, Dict[str, float]] = Field(default_factory=dict)  # Real Pearson correlation matrix Σ
