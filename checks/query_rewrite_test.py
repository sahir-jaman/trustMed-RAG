import sys
sys.path.insert(0, "src")

from trustmed.rag.retriever import Retriever
from trustmed.trust.query_rewrite import QueryRewriter

r, rw = Retriever(), QueryRewriter()
SAFE = {"retracted": False}

questions = [
    "Does a cold cap stop hair falling out from chemo?",
    "Can drugs that target the HER2 protein help women whose cancer grows fast?",
    "Does working out help breast cancer survivors feel less tired?",
    "Is the pill that blocks oestrogen worth the hot flushes?",
    "Can a blood test for tumour DNA show if treatment is working?",
]

for q in questions:
    new_q = rw.rewrite(q)
    before = r.search(q, k=1, where=SAFE)[0]
    after = r.search(new_q, k=1, where=SAFE)[0]
    print("=" * 90)
    print("ORIGINAL :", q)
    print("REWRITTEN:", new_q)
    print(f"  before {before['score']}  {before['title'][:70]}")
    print(f"  after  {after['score']}  {after['title'][:70]}")



"""
#For checking the pipeline workinng end to end. 



import sys
sys.path.insert(0, "src")

from trustmed.pipeline import TrustMedPipeline

result = TrustMedPipeline().ask("Is the pill that blocks oestrogen worth the hot flushes?")

print("SEARCHED FOR:", result.get("search_query"))
print("WARNINGS:", result["warnings"])
print("ANSWER:", result["answer"][:400])
print("SOURCES:", len(result["sources"]))
"""