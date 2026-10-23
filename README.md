# TrustMed RAG

A trustworthy medical research assistant for breast cancer. It answers questions
from 5,000+ open-access research papers and shows how much each answer can be
trusted: it excludes retracted papers, rates evidence strength, and checks every
claim against its source.

🚧 Work in progress

## Project structure

```
scripts/        data pipeline, numbered in run order
checks/         small scripts to inspect the data
src/trustmed/   application code (retrieval, LLM, trust features)
notebooks/      data exploration and charts
tests/          tests
dataset/        local data (not committed)
```

## Data pipeline

Run from the project root:

```bash
pip install -r requirements.txt
python scripts/01_download_papers.py     # full text from PubMed Central (BioC API)
python scripts/02_download_metadata.py   # title, year, journal, DOI, study type
git clone https://gitlab.com/crossref/retraction-watch-data dataset/raw/retraction-watch-data
python scripts/03_clean_papers.py        # clean sections, evidence + retraction labels
python scripts/04_make_chunks.py         # ~400-word overlapping chunks
```

Current dataset: 5,319 papers → 69,282 chunks (13 retracted papers flagged).


baseline question 8 issue: 
![alt text](image.png)
