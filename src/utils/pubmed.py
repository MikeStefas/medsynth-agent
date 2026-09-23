import config 
from metapub import PubMedFetcher

fetcher = PubMedFetcher()

def fetch_article_metadata(pmid: str) -> dict:
    article = fetcher.article_by_pmid(pmid)
    authors = ', '.join([str(author) for author in article.author_list]) if article.author_list else 'N/A'
    mesh_tags = ', '.join(article.mesh) if article.mesh else 'N/A'
    keywords = ', '.join(article.keywords) if article.keywords else 'N/A'

    metadata = {
        "pmid": str(pmid),
        "title": str(article.title or "N/A"),
        "authors": authors,
        "year": str(article.year or "N/A"),
        "journal": str(article.journal or "N/A"),
        "mesh": mesh_tags,
        "keywords": keywords,
        "abstract": str(article.abstract or "N/A"),
    }
    return metadata

def print_article_metadata(metadata: dict) -> None:
    print(f"Title:    {metadata['title']}")
    print(f"Authors:  {metadata['authors']}")
    print(f"Year:     {metadata['year']}")
    print(f"Journal:  {metadata['journal']}")
    print(f"MESH:     {metadata['mesh']}")
    print(f"Keywords: {metadata['keywords']}")
    print(f"Abstract: {metadata['abstract']}")

GUIDELINE_FILTER = 'AND ("Practice Guideline"[Publication Type] OR "Consensus Development Conference"[Publication Type] OR "guideline"[Title] OR "consensus"[Title])'

def search_pubmed_pmids(query: str, retmax: int = 10) -> list[str]:
    filter_suffix = 'AND ("Practice Guideline"[Publication Type] OR "Consensus Development Conference"[Publication Type] OR "guideline"[Title] OR "consensus"[Title])'
    full_query = query.strip()
    if filter_suffix not in full_query:
        full_query = f"{full_query} {filter_suffix}"
    print(f"final pubmed query: {full_query}")
    return fetcher.pmids_for_query(full_query, retmax=retmax)

