import config  # ensures NCBI_API_KEY is set before metapub import
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

def search_pubmed_pmids(query: str, retmax: int = 10) -> list[str]:
    return fetcher.pmids_for_query(query, retmax=retmax)
