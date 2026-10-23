import sys
sys.path.insert(0, "src")

from trustmed.pipeline import TrustMedPipeline

pipeline = TrustMedPipeline()
for q in ["What is the best treatment for lung cancer?",
          "Is prostate cancer screening worth it?",
          "Can scalp cooling prevent hair loss during chemotherapy?"]:
    result = pipeline.ask(q)
    print("=" * 90)
    print("Q:", q)
    print("WARNINGS:", result["warnings"])
    print("ANSWER:", result["answer"][:300])
    print("SOURCES:", len(result["sources"]))