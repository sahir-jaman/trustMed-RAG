"""Run the baseline and TrustMed on every evaluation question.
Safe to stop and re-run: questions already answered are skipped."""
import json, os, sys, time
sys.path.insert(0, "src")

from trustmed.rag.pipeline import Pipeline
from trustmed.pipeline import TrustMedPipeline

QUESTIONS = [json.loads(l) for l in open("eval/questions.jsonl", encoding="utf-8")]
OUT = {"baseline": "results/eval_baseline.jsonl", "trustmed": "results/eval_trustmed.jsonl"}
os.makedirs("results", exist_ok=True)


def done_ids(path):
    if not os.path.exists(path):
        return set()
    return {json.loads(l)["id"] for l in open(path, encoding="utf-8")}


def ask_baseline(p, question):
    result = p.ask(question)
    chunks = p.retriever.search(question, k=p.k)      # same search the baseline just did
    for s, c in zip(result["sources"], chunks):
        s["text"] = c["text"]
    return result


def ask_trustmed(p, question):
    return p.ask(question)


def timed_with_retry(fn, p, question, tries=5):
    for attempt in range(1, tries + 1):
        try:
            start = time.time()
            result = fn(p, question)
            result["seconds"] = round(time.time() - start, 2)
            return result
        except Exception as e:
            wait = 30 * attempt
            print(f"   error ({type(e).__name__}): {str(e)} -> waiting {wait}s")
            time.sleep(wait)
    raise SystemExit("Too many errors (probably Groq's daily limit). "
                     "Re-run later - finished questions are saved.")


systems = {
    "baseline": (Pipeline(), ask_baseline),
    "trustmed": (TrustMedPipeline(), ask_trustmed),
}

for name, (pipeline, fn) in systems.items():
    done = done_ids(OUT[name])
    todo = [q for q in QUESTIONS if q["id"] not in done]
    print(f"\n=== {name}: {len(done)} done, {len(todo)} to go ===")

    with open(OUT[name], "a", encoding="utf-8") as f:
        for i, q in enumerate(todo, start=1):
            result = timed_with_retry(fn, pipeline, q["question"])
            f.write(json.dumps({**q, "system": name, **result}) + "\n")
            f.flush()                                   # saved immediately
            print(f"[{i}/{len(todo)}] {q['id']:20} {result['seconds']:6}s")
            time.sleep(2)                               # be gentle with the free tier

print("\nAll done.")