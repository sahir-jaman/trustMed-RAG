import csv, glob, json

csv_path = glob.glob("dataset/raw/retraction-watch-data/*.csv")[0]
print("Using:", csv_path)

retracted_dois, retracted_pmids = set(), set()
with open(csv_path, encoding="latin-1") as f:
    for row in csv.DictReader(f):
        doi = (row.get("OriginalPaperDOI") or "").strip().lower()
        pmid = (row.get("OriginalPaperPubMedID") or "").strip()
        if doi and doi != "unavailable":
            retracted_dois.add(doi)
        if pmid and pmid != "0":
            retracted_pmids.add(pmid)

print(f"Retraction list has {len(retracted_dois)} retracted papers")

matches = []
with open("dataset/raw/metadata.jsonl", encoding="utf-8") as f:
    for line in f:
        paper = json.loads(line)
        if paper["doi"].lower() in retracted_dois or paper["pmid"] in retracted_pmids:
            matches.append(paper)

print(f"Retracted papers in YOUR dataset: {len(matches)}")
for p in matches:
    print(" -", p["pmid"], p["year"], p["title"][:80])