"""Evidence re-ranking: prefer strong studies and finding-rich sections."""

EVIDENCE_BONUS = {"strong": 0.05, "moderate": 0.025, "weak": 0.0}
SECTION_BONUS = {"results": 0.03, "conclusion": 0.03, "abstract": 0.03,
                 "discussion": 0.01, "introduction": 0.0, "methods": 0.0}
BADGE = {"strong": "🟢 Strong", "moderate": "🟡 Moderate", "weak": "🟠 Weak"}


def rerank(chunks, k=5, max_per_paper=2):
    """Re-score chunks, then keep the top-k with at most max_per_paper per paper."""
    for c in chunks:
        c["final_score"] = round(c["score"]
                                 + EVIDENCE_BONUS.get(c["evidence_level"], 0)
                                 + SECTION_BONUS.get(c["section"], 0), 3)

    picked, per_paper = [], {}
    for c in sorted(chunks, key=lambda c: c["final_score"], reverse=True):
        if per_paper.get(c["pmid"], 0) >= max_per_paper:
            continue
        picked.append(c)
        per_paper[c["pmid"]] = per_paper.get(c["pmid"], 0) + 1
        if len(picked) == k:
            break
    return picked