import pandas as pd

def is_categorical(series: pd.Series) -> bool:
    col = series.dropna()

    if not pd.api.types.is_numeric_dtype(col) or pd.api.types.is_bool_dtype(col):
        return True

    unique_count = col.nunique()
    if unique_count <= 10:  #asumming no more than 10 classes exist :p
        return True

    return False

