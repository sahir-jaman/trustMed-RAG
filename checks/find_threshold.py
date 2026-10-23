import sys
sys.path.insert(0, "src")

from trustmed.rag.retriever import Retriever

r = Retriever()

in_scope = [
    "Does trastuzumab improve survival in HER2-positive breast cancer?",
    "What are the common side effects of tamoxifen?",
    "Does exercise reduce fatigue in breast cancer survivors?",
    "Is hypofractionated radiotherapy as effective as conventional radiotherapy?",
    "Can scalp cooling prevent hair loss during chemotherapy?",
]
out_of_scope = [
    "What is the best treatment for lung cancer?",
    "How do I fix a flat bicycle tyre?",
    "Does vitamin C cure the common cold?",
    "What causes type 2 diabetes?",
    "Is prostate cancer screening worth it?",
]

for label, questions in [("IN SCOPE", in_scope), ("OUT OF SCOPE", out_of_scope)]:
    print(f"\n{label}:")
    for q in questions:
        best = r.search(q, k=1, where={"retracted": False})[0]["score"]
        print(f"  {best}  {q}")