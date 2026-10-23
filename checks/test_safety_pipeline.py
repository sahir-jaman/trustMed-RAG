import sys
sys.path.insert(0, "src")

from trustmed.pipeline import TrustMedPipeline

pipeline = TrustMedPipeline()

for q in ["I have breast cancer. Should I stop taking tamoxifen because of hot flashes?",
          "Does tamoxifen cause hot flashes?"]:
    result = pipeline.ask(q)
    print("=" * 90)
    print("Q:", q)
    print("WARNINGS:", result["warnings"])
    print("ANSWER:", result["answer"][:400])
    print("SOURCES:", len(result["sources"]))
    print("DISCLAIMER:", result["disclaimer"])