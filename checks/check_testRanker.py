import sys
sys.path.insert(0, "src")

from trustmed.rag.retriever import Retriever
from trustmed.trust.reranker import rerank, BADGE

question = "Does trastuzumab improve survival in HER2-positive breast cancer?"
rtrv = Retriever()

print("BEFORE (similarity only):")
for c in rtrv.search(question, k=5, where={"retracted": False}):
    print(f"  {c['score']}  {BADGE[c['evidence_level']]:12} {c['section']:13} {c['title'][:60]}")

print("\nAFTER (re-ranked):")
for c in rerank(rtrv.search(question, k=20, where={"retracted": False}), k=5):
    print(f"  {c['score']} → {c['final_score']}  {BADGE[c['evidence_level']]:12} {c['section']:13} {c['title'][:60]}")