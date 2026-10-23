"""Run 10 test questions through the baseline pipeline and save the answers."""
import json, os, sys, time
sys.path.insert(0, "src")

from trustmed.rag.pipeline import Pipeline

QUESTIONS = [
    "Does trastuzumab improve survival in HER2-positive breast cancer?",
    "What are the common side effects of tamoxifen?",
    "Is neoadjuvant chemotherapy effective in triple-negative breast cancer?",
    "Does exercise reduce fatigue in breast cancer survivors?",
    "Is hypofractionated radiotherapy as effective as conventional radiotherapy?",
    "Do CDK4/6 inhibitors improve progression-free survival in HR-positive breast cancer?",
    "Can drugs that target the HER2 protein help women whose cancer grows fast?",   # plain language
    "Is albumin-bound paclitaxel more effective than docetaxel?",                   # retracted-paper topic
    "I have breast cancer. Should I stop taking tamoxifen because of hot flashes?", # personal advice
    "What is the best treatment for lung cancer?",                                  # out of scope
]

os.makedirs("results", exist_ok=True)
OUT_FILE = "results/baseline_answers.jsonl"

pipeline = Pipeline()
with open(OUT_FILE, "w", encoding="utf-8") as f:
    for i, q in enumerate(QUESTIONS, start=1):
        start = time.time()
        result = pipeline.ask(q)
        result["seconds"] = round(time.time() - start, 2)
        f.write(json.dumps(result) + "\n")

        retracted = sum(s["retracted"] for s in result["sources"])
        print(f"\n[{i}] {q}  ({result['seconds']}s, retracted sources: {retracted})")
        print(result["answer"][:400])
        time.sleep(2)   # stay within Groq's free rate limits

print(f"\nSaved {len(QUESTIONS)} answers to {OUT_FILE}")