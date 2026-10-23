import sys
sys.path.insert(0, "src")

from trustmed.rag.retriever import Retriever
from trustmed.rag.prompts import build_messages

chunks = Retriever().search("Does trastuzumab improve survival in HER2-positive breast cancer?", k=2)
messages = build_messages("Does trastuzumab improve survival in HER2-positive breast cancer?", chunks)

print("=== SYSTEM ===\n", messages[0]["content"])
print("\n=== USER ===\n", messages[1]["content"][:1500], "...")