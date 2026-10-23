"""Claim checker: an LLM judge checks each sentence against the source(s) it cites.
(We first tried an NLI model - see verifier_nli.py - but it marked almost every
multi-fact medical sentence as 'neutral', even when the source stated the facts.)"""
import re
from ..rag.llm import LLM

JUDGE_PROMPT = """You check whether each sentence of an answer is supported by the source(s) it cites.
For each numbered sentence, give ONE verdict:
SUPPORTED   - the cited source(s) state this claim (paraphrasing is fine)
PARTIAL     - the cited source(s) state only part of the claim
UNSUPPORTED - the cited source(s) do not state this claim
Judge ONLY against the cited sources, never your own knowledge.
Reply with one line per sentence, in exactly this format:
1: SUPPORTED
2: PARTIAL"""


def split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


class ClaimVerifier:
    def __init__(self):
        self.llm = LLM(model="openai/gpt-oss-20b")

    def verify(self, answer, chunks):
        results, to_judge = [], []
        for sentence in split_sentences(answer):
            cited = [int(n) for n in re.findall(r"\[(\d+)\]", sentence)]
            claim = re.sub(r"\s*\[\d+\]", "", sentence).strip()
            if len(claim.split()) < 4:                     # e.g. "Yes."
                results.append({"sentence": sentence, "status": "skip"})
            elif not cited:
                results.append({"sentence": sentence, "status": "no_citation"})
            else:
                results.append({"sentence": sentence, "status": None})
                to_judge.append(len(results) - 1)

        if not to_judge:
            return results

        sources = "\n\n".join(f"[{i}] {c['text']}" for i, c in enumerate(chunks, start=1))
        numbered = "\n".join(f"{j}: {results[idx]['sentence']}"
                             for j, idx in enumerate(to_judge, start=1))
        reply = self.llm.generate(
            [{"role": "system", "content": JUDGE_PROMPT},
             {"role": "user", "content": f"Sources:\n\n{sources}\n\nSentences:\n{numbered}"}],
            temperature=0, max_tokens=2048) or ""

        verdicts = dict(re.findall(r"(\d+)\s*:\s*(SUPPORTED|PARTIAL|UNSUPPORTED)", reply.upper()))
        for j, idx in enumerate(to_judge, start=1):
            results[idx]["status"] = verdicts.get(str(j), "UNKNOWN").lower()
        return results