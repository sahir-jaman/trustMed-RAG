"""Retraction filter: never answer from retracted papers, but warn when one was relevant."""

SAFE_ONLY = {"retracted": False}   # ChromaDB filter: keep non-retracted chunks only


def retraction_warnings(retriever, question, k=5):
    """Search WITHOUT the filter. If retracted papers appear in the top-k,
    they would have been used, so return a warning about them."""
    results = retriever.search(question, k=k)
    retracted_titles = {c["title"] for c in results if c["retracted"]}

    if not retracted_titles:
        return []
    return [
        f"⚠️ Excluded {len(retracted_titles)} relevant paper(s) because they were RETRACTED: "
        + "; ".join(t[:100] for t in retracted_titles)
    ]