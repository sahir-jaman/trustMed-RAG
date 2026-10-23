"""The baseline RAG pipeline: retrieve -> prompt -> LLM -> answer + sources."""
import re 
from .retriever import Retriever
from .prompts import build_messages
from .llm import LLM


class Pipeline:
    def __init__(self, k=5):
        self.retriever = Retriever()
        self.llm = LLM()
        self.k = k

    def ask(self, question):
        chunks = self.retriever.search(question, k=self.k)
        answer = self.llm.generate(build_messages(question, chunks))
        answer = re.sub(r"【(\d+)[^】]*】", r"[\1]", answer)   # 【1†L4-L7】 -> [1]

        sources = []
        for i, c in enumerate(chunks, start=1):
            sources.append({
                "n": i,
                "title": c["title"],
                "journal": c["journal"],
                "year": c["year"],
                "section": c["section"],
                "evidence_level": c["evidence_level"],
                "retracted": c["retracted"],
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{c['pmid']}/",
            })
        return {"question": question, "answer": answer, "sources": sources}