from typing import List, Dict
from src.types.features import BaseFeature

def format_pubmed_abstracts(metadatas: List[Dict[str, str | int]]) -> str:
    abstracts = []
    for meta in metadatas:
        abstract = meta["abstract"]
        if abstract and abstract != "N/A":
            pmid = meta["pmid"]
            title = meta["title"]
            abstracts.append(f"PMID: {pmid} \nTitle: {title}\nAbstract: {abstract}")

    return "\n\n".join(abstracts)


def format_column_info(feature: BaseFeature) -> str:
    columns_info = []
    name = feature.name
    data_type = feature.data_type

    if data_type == "continuous":
        min_val = feature.min_val
        max_val = feature.max_val
        bounds = f" (range: {min_val} to {max_val})"
    else:
        categories = feature.categories
        bounds = f" (allowed categories: {categories})"

    columns_info.append(f"Name: {name} \nType: {data_type} \nBounds: {bounds}")

    return "\n".join(columns_info)
