---
title: TrustMed
emoji: 🩺
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# 🩺 TrustMed

**A breast cancer research assistant that shows you how far to trust each answer.**

TrustMed answers questions from **5,319 open-access breast cancer papers** (69,282 passages).
Unlike a standard "chat with PubMed" app, it:

- 🔴 **excludes retracted papers** and warns you when one was relevant
- 🏅 **rates evidence strength** for every source (strong / moderate / weak)
- ✅ **checks every sentence** of the answer against the source it cites
- 🛑 **refuses personal medical advice** and says when there isn't enough evidence

> 🚧 Work in progress: the evaluation on 98 test questions is running.

---

## Why this matters: a real example

I asked a standard RAG pipeline (my **baseline**):
*"Is albumin-bound paclitaxel more effective than docetaxel?"*

![Baseline answer to question 8](docs/images/baseline_q8.png)

**What went wrong:** 3 of its 5 sources came from a **retracted** meta-analysis, and its answer
(*"the evidence is mixed"*) relied on that study, with no warning to the user.

**TrustMed on the same question:**

| | Baseline | TrustMed |
|---|---|---|
| Retracted passages used | **3** | **0** |
| Warning shown | none | ⚠️ *"Excluded 1 relevant paper because it was RETRACTED"* |
| Conclusion | "the evidence is mixed" | based only on the remaining trials |

**One retracted study changed the answer.** That is the problem TrustMed is built to catch.

---

## How it works

```
Question
   │
   ├─ 1. Safety check ─────────── personal medical advice? → polite refusal
   ├─ 2. Query rewriting ──────── "cold cap" → "scalp cooling", "chemo" → "chemotherapy"
   ├─ 3. Retrieval ────────────── top 20 passages from ChromaDB, retracted papers excluded
   ├─ 4. Evidence re-ranking ──── prefer strong studies and results/conclusion sections
   ├─ 5. Evidence check ───────── nothing relevant? → "not enough evidence" (no guessing)
   ├─ 6. Answer generation ────── LLM answers ONLY from the sources, citing [1], [2]…
   └─ 7. Claim checking ───────── each sentence: ✅ supported · 🟡 partial · ⚠️ unsupported
```

## Design decisions (measured, not assumed)

**1. Embedding model**: tested on 20 questions (share of top-5 results containing the key term):

| Model | Type | Score |
|---|---|---|
| `bge-small-en-v1.5` | general | **94%** ← chosen (also reads full 512-token passages) |
| `all-MiniLM-L6-v2` | general | 92% |
| `pubmedbert-base-embeddings` | medical | 71% |

The medical model found the right *topic* but often the wrong *drug*.

**2. "Not enough evidence" threshold**: best-match similarity scores:
in-scope questions **0.858–0.903**, out-of-scope **0.522–0.767**. The threshold was set at **0.80**, in the gap.
Lung cancer and prostate screening questions are now declined instead of answered from breast cancer papers.

**3. Query rewriting**: plain-language questions found better sources:
*"Is the pill that blocks oestrogen worth the hot flushes?"* scored **0.773 → 0.827** after rewriting,
moving above the threshold and from an unrelated paper to the right one.

**4. Claim checker**: an NLI model (`nli-deberta-v3-small`) was tried first, but it labelled
correct multi-fact sentences as 99.6% "neutral". It was replaced by an LLM judge, which was confirmed
to flag fabricated claims (e.g. *"trastuzumab cures every breast cancer within one week"* → ⚠️).

**5. Evidence re-ranking**: for *"Does trastuzumab improve survival in HER2-positive breast cancer?"*
the baseline's 5 sources were **all introductions**. After re-ranking: **0 introductions**, all strong studies,
from abstract / results / discussion sections.

## Evaluation (in progress)

98 questions in 6 groups, each testing a feature:

| Group | Questions | Expected behaviour |
|---|---|---|
| Research questions | 25 | answer with supported citations |
| MedQuAD (NIH) questions | 20 | answer |
| Plain-language questions | 10 | answer (tests query rewriting) |
| Personal advice | 15 | refuse |
| Out of scope | 15 | decline |
| Retracted-paper topics | 13 | answer without retracted sources |

Results table: coming soon.

## Tech stack

| Part | Tool |
|---|---|
| Data | PubMed Central Open Access (BioC API), PubMed metadata, Retraction Watch |
| Embeddings | `BAAI/bge-small-en-v1.5` |
| Vector database | ChromaDB |
| LLM | `gpt-oss-120b` (answers) and `gpt-oss-20b` (safety, rewriting, claim checking) via Groq |
| Backend | FastAPI |
| Frontend | Streamlit |
| Deployment | Docker, Hugging Face Spaces |

## Project structure

```
scripts/          data pipeline and evaluation, numbered in run order
src/trustmed/
  ├── rag/        baseline RAG: retriever, prompts, LLM, pipeline (frozen as baseline-v1)
  ├── trust/      trust features: retraction, safety, re-ranking, evidence check, rewriting, verifier
  └── pipeline.py the full TrustMed pipeline
src/app/          FastAPI backend (api.py) and Streamlit frontend (ui.py)
checks/           test scripts for each component
eval/             evaluation questions
results/          baseline and TrustMed outputs
notebooks/        embedding model comparison
```

## Run it locally

```bash
pip install -r requirements.txt
# add GROQ_API_KEY and HF_TOKEN to a .env file
uvicorn app.api:app --app-dir src          # terminal 1: API
streamlit run src/app/ui.py                # terminal 2: website
```

## Rebuild the data

```bash
python scripts/01_download_papers.py     # full text from PubMed Central (BioC API)
python scripts/02_download_metadata.py   # title, year, journal, DOI, study type
git clone https://gitlab.com/crossref/retraction-watch-data dataset/raw/retraction-watch-data
python scripts/03_clean_papers.py        # clean sections, evidence + retraction labels
python scripts/04_make_chunks.py         # ~400-word overlapping chunks
```

## Limitations

- Covers **breast cancer only**, and only open-access papers (2015–2026).
- Evidence levels come from PubMed publication types, not a full quality appraisal.
- The claim checker is itself an LLM and can make mistakes.
- Runs on Groq's free tier, so answers can be slow or temporarily unavailable.

## Disclaimer

TrustMed summarises published research for educational purposes. **It is not medical advice.**
Always talk to your doctor about your own care.