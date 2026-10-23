import sys
sys.path.insert(0, "src")

from trustmed.rag.pipeline import Pipeline

result = Pipeline().ask("Does trastuzumab improve survival in HER2-positive breast cancer?")

print("ANSWER:\n", result["answer"])
print("\nSOURCES:")
for s in result["sources"]:
    print(f"[{s['n']}] {s['title'][:80]} ({s['journal']}, {s['year']})")
    print("    ", s["url"])