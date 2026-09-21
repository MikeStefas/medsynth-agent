import pandas as pd
from typing import List, Dict, Any
from src.types import State, Feature, ContinuousFeature, CategoricalFeature


def dataset_analyzer_node(state: State) -> dict:
    print("[Node: Dataset Analyzer] Analyzing dataset schema and extracting features...")
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

    return {"features": features}


def is_categorical(series: pd.Series) -> bool:
    col = series.dropna()

    if not pd.api.types.is_numeric_dtype(col) or pd.api.types.is_bool_dtype(col):
        return True

    unique_count = col.nunique()
    if unique_count <= 10:  # e.g. binary indicators or small ordinal scales
        return True

    return False

