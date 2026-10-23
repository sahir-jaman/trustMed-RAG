import sys
sys.path.insert(0, "src")

from trustmed.pipeline import TrustMedPipeline

ICON = {"supported": "✅", "partial": "🟡", "unsupported": "⚠️", "unknown": "❓",
        "no_citation": "⚠️", "skip": "  "}

result = TrustMedPipeline().ask("Does trastuzumab improve survival in HER2-positive breast cancer?")

print("SEARCHED FOR:", result.get("search_query"))
print("WARNINGS:", result["warnings"])
print("\nANSWER (checked sentence by sentence):")
for c in result["claims"]:
    print(f"  {ICON[c['status']]} {c['sentence']}")
print("\nSOURCES:")
for s in result["sources"]:
    print(f"  [{s['n']}] {s['badge']:12} {s['section']:12} {s['title'][:60]} ({s['year']})")
print("\n", result["disclaimer"])