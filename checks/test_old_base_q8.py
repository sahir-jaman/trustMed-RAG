import sys
sys.path.insert(0, "src")

from trustmed.pipeline import TrustMedPipeline

result = TrustMedPipeline().ask("Is albumin-bound paclitaxel more effective than docetaxel?")

print("WARNINGS:")
for w in result["warnings"]:
    print(" ", w)

print("\nANSWER:\n", result["answer"])

print("\nSOURCES:")
for s in result["sources"]:
    flag = "🔴 RETRACTED" if s["retracted"] else "✅"
    print(f"[{s['n']}] {flag} {s['title'][:80]} ({s['year']})")