import sys
sys.path.insert(0, "src")

from trustmed.rag.retriever import Retriever
from trustmed.rag.prompts import build_messages
from trustmed.rag.llm import LLM
from trustmed.trust.verifier import ClaimVerifier

ICON = {"supported": "✅", "partial": "🟡", "unsupported": "⚠️", "unknown": "❓",
        "no_citation": "⚠️ (no citation)", "skip": "  "}

q = "Does trastuzumab improve survival in HER2-positive breast cancer?"
chunks = Retriever().search(q, k=5, where={"retracted": False})
answer = LLM().generate(build_messages(q, chunks)).replace("【", "[").replace("】", "]")

for r in ClaimVerifier().verify(answer, chunks):
    print(f"{ICON[r['status']]}  {r['sentence']}\n")



print("\n--- Sanity check: fake claims ---")
fake = ("Trastuzumab cures every type of breast cancer within one week [5]. "
        "Trastuzumab was approved in 1998 and improved survival in HER2-positive disease [1].")
for r in ClaimVerifier().verify(fake, chunks):
    print(f"{ICON[r['status']]}  {r['sentence']}\n")