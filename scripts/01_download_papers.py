import os, time
import requests

OUT_DIR = "dataset/raw/papers"
os.makedirs(OUT_DIR, exist_ok=True)

QUERY = ('"breast neoplasms"[MeSH] AND pubmed pmc open access[filter] '
         'AND 2015:2026[dp] AND english[lang] AND (meta-analysis[pt] '
         'OR systematic review[pt] OR randomized controlled trial[pt] '
         'OR clinical trial[pt] OR practice guideline[pt] '
         'OR observational study[pt])')

# 1) Get the list of paper IDs from PubMed
r = requests.get(
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
    params={"db": "pubmed", "term": QUERY, "retmax": 6500, "retmode": "json"},
)
pmids = r.json()["esearchresult"]["idlist"]
print(f"Found {len(pmids)} papers")

with open("dataset/raw/pmids.txt", "w") as f:
    f.write("\n".join(pmids))

# 2) Download each paper's full text
URL = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{}/unicode"

ok, failed = 0, 0
for i, pmid in enumerate(pmids, 1):
    path = f"{OUT_DIR}/{pmid}.json"
    if os.path.exists(path):
        continue
    try:
        resp = requests.get(URL.format(pmid), timeout=30)
        if resp.status_code == 200 and resp.text.strip().startswith("["):
            with open(path, "w", encoding="utf-8") as f:
                f.write(resp.text)
            ok += 1
        else:
            failed += 1
    except requests.RequestException:
        failed += 1
    if i % 100 == 0:
        print(f"{i}/{len(pmids)}  saved={ok}  failed={failed}")
    time.sleep(0.35)

print(f"Done. Saved {ok}, failed {failed}")