"""The TrustMed pipeline: the baseline RAG plus trust features."""
import re
from .rag.retriever import Retriever
from .rag.prompts import build_messages
from .rag.llm import LLM
from .trust.retraction import SAFE_ONLY, retraction_warnings
from .trust.safety_layer import SafetyChecker, REFUSAL, DISCLAIMER
from .trust.reranker import rerank, BADGE
from .trust.evidence_check import check_evidence, NOT_ENOUGH


class TrustMedPipeline:
    def __init__(self, k=5):
        self.retriever = Retriever()
        self.llm = LLM()
        self.safety = SafetyChecker()
        self.k = k

    def ask(self, question):
        warnings = []

        # Feature 2: safety layer (check BEFORE searching or answering)
        if self.safety.is_personal_advice(question):
            return {"question": question, "answer": REFUSAL, "sources": [],
                    "warnings": ["🛑 Personal medical-advice question: no answer given."],
                    "disclaimer": DISCLAIMER}

        # Feature 1: retraction filter
        # Feature 3: fetch 20 safe candidates, then re-rank by evidence and section
        candidates = self.retriever.search(question, k=20, where=SAFE_ONLY)
        chunks = rerank(candidates, k=self.k)
        # Feature 4: "not enough evidence" rule
        enough, evidence_warnings = check_evidence(chunks)
        if not enough:
            return {"question": question, "answer": NOT_ENOUGH, "sources": [],
                    "warnings": warnings + ["🔍 No relevant evidence found in the database."],
                    "disclaimer": DISCLAIMER}
        warnings += evidence_warnings
        warnings += retraction_warnings(self.retriever, question, k=self.k)

        answer = self.llm.generate(build_messages(question, chunks))
        answer = re.sub(r"【(\d+)[^】]*】", r"[\1]", answer)

        sources = [{
            "n": i,
            "title": c["title"],
            "journal": c["journal"],
            "year": c["year"],
            "section": c["section"],
            "evidence_level": c["evidence_level"],
            "badge": BADGE[c["evidence_level"]],
            "retracted": c["retracted"],
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{c['pmid']}/",
        } for i, c in enumerate(chunks, start=1)]

        return {"question": question, "answer": answer,
                "sources": sources, "warnings": warnings,
                "disclaimer": DISCLAIMER}