import pandas as pd
from typing import List, Dict, Any
from rich import print as rprint
from src.types import State, Feature, ContinuousFeature, CategoricalFeature
from src.utils import is_categorical



def dataset_analyzer_node(state: State) -> dict:
    """Analyzes the dataset schema and extracts feature information."""
    print("⫘" * 60)
    print("⫘" * 60)
    print("1) analyzing dataset")
    df = pd.read_csv(state["dataset_path"])
    features: List[Feature] = []

    for col_name in df.columns:
        series = df[col_name].dropna()

        if is_categorical(series):
            freq_dict = series.value_counts(normalize=True).to_dict()
            features.append(
                CategoricalFeature(
                    name=col_name,
                    is_binary=(series.nunique() == 2),
                    categories=list(series.unique().tolist()),
                    category_frequencies={str(k): float(v) for k, v in freq_dict.items()},
                    is_target=(col_name.lower() in ["target", "outcome", "label", "class"]),
                )
            )
        else:
            features.append(
                ContinuousFeature(
                    name=col_name,
                    min_val=float(series.min()),
                    max_val=float(series.max()),
                    typical_value=float(series.median()),
                    non_negative=bool(series.min() >= 0),
                    is_target=(col_name.lower() in ["target", "outcome", "label", "class"]),
                )
            )

    rprint(features)
    return {"features": features}




