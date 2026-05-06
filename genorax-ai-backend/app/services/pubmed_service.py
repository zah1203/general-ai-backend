from Bio import Entrez

Entrez.email = "zah1203@gmail.com"


def search_pubmed(query: str, max_results: int = 3):
    try:
        handle = Entrez.esearch(
            db="pubmed",
            term=query,
            retmax=max_results,
            sort="relevance"
        )
        record = Entrez.read(handle)
        ids = record.get("IdList", [])

        if not ids:
            return []

        summary_handle = Entrez.esummary(db="pubmed", id=",".join(ids))
        summaries = Entrez.read(summary_handle)

        papers = []
        for item in summaries:
            papers.append({
                "pmid": str(item.get("Id", "")),
                "title": str(item.get("Title", "")),
                "journal": str(item.get("FullJournalName", "")),
                "pubdate": str(item.get("PubDate", ""))
            })

        return papers

    except Exception as e:
        return [{"error": str(e)}]
