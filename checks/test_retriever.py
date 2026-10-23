import sys
sys.path.insert(0, "src")          # lets Python find the trustmed package

from trustmed.rag.retriever import Retriever

r = Retriever()
for c in r.search("trastuzumab in HER2-positive breast cancer"):
    print(f"{c['score']}  [{c['evidence_level']} | {c['section']} | {c['year']}]  {c['title'][:80]}")
