"""Claim checker: does the cited source really support each sentence?"""
import re
from sentence_transformers import CrossEncoder

NLI_MODEL = "cross-encoder/nli-deberta-v3-small"
ENTAILMENT = 1          # this model's labels: 0 contradiction, 1 entailment, 2 neutral
THRESHOLD = 0.5         # supported if entailment probability >= 0.5


def split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def windows(text, size=3, step=2):
    """Cut a chunk into overlapping windows of ~3 sentences."""
    sents = split_sentences(text)
    return [" ".join(sents[i:i + size]) for i in range(0, len(sents), step)] or [text]


class ClaimVerifier:
    def __init__(self):
        self.model = CrossEncoder(NLI_MODEL)

    def verify(self, answer, chunks):
        results = []
        for sentence in split_sentences(answer):
            cited = [int(n) for n in re.findall(r"\[(\d+)\]", sentence)]
            claim = re.sub(r"\s*\[\d+\]", "", sentence).strip()

            if len(claim.split()) < 4:                     # e.g. "Yes." -> nothing to check
                results.append({"sentence": sentence, "status": "skip", "score": None})
                continue

            premises = [w for n in cited if 1 <= n <= len(chunks)
                          for w in windows(chunks[n - 1]["text"])]
            if not premises:
                results.append({"sentence": sentence, "status": "no_citation", "score": 0.0})
                continue

            probs = self.model.predict([(p, claim) for p in premises], apply_softmax=True)
            best = float(max(row[ENTAILMENT] for row in probs))
            results.append({"sentence": sentence,
                            "status": "supported" if best >= THRESHOLD else "unsupported",
                            "score": round(best, 2)})
        return results