from typing import List, Dict, Optional, Union, Literal, Annotated
from pydantic import BaseModel, Field
from src.types.stat_results import KSResult, TVDResult


class BaseFeature(BaseModel):
    name: str
    clinical_description: Optional[str] = None
    unit: Optional[str] = None
    is_target: bool = False


class ContinuousFeature(BaseFeature):
    data_type: Literal["continuous"] = "continuous"
    min_val: float
    max_val: float
    typical_value: Optional[float] = None  # (median anchor)
    non_negative: bool = True

    # Audit result (filled after Tester / Quality Gate runs)
    ks_evaluation: Optional[KSResult] = None


class CategoricalFeature(BaseFeature):
    data_type: Literal["categorical"] = "categorical"
    is_binary: bool = False
    categories: List[Union[str, int]]
    category_frequencies: Dict[str, float]

    # Audit result (filled after Tester / Quality Gate runs)
    tvd_evaluation: Optional[TVDResult] = None


# Polymorphic Discriminated Union
Feature = Annotated[
    Union[ContinuousFeature, CategoricalFeature],
    Field(discriminator="data_type"),
]
