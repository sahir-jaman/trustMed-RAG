import json, os, time
import requests
import xml.etree.ElementTree as ET

PAPERS_DIR = "dataset/raw/papers"
OUT_FILE = "dataset/raw/metadata.jsonl"

# Only get metadata for papers we actually downloaded
pmids = [f.replace(".json", "") for f in os.listdir(PAPERS_DIR) if f.endswith(".json")]
print(f"Getting metadata for {len(pmids)} papers")

URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH = 200   # ask for 200 papers at a time

def get_text(el):
    return "".join(el.itertext()).strip() if el is not None else ""

count = 0
with open(OUT_FILE, "w", encoding="utf-8") as out:
    for start in range(0, len(pmids), BATCH):
        batch = pmids[start:start + BATCH]
        resp = requests.post(URL, data={"db": "pubmed", "id": ",".join(batch),
                                        "retmode": "xml"}, timeout=60)
        root = ET.fromstring(resp.content)

        for art in root.findall(".//PubmedArticle"):
            pmid = art.findtext(".//MedlineCitation/PMID")

            # Year (PubMed stores it in a few different places)
            year = art.findtext(".//JournalIssue/PubDate/Year")
            if not year:
                medline_date = art.findtext(".//JournalIssue/PubDate/MedlineDate") or ""
                year = medline_date[:4]

            authors = []
            for a in art.findall(".//AuthorList/Author"):
                last, initials = a.findtext("LastName"), a.findtext("Initials")
                if last:
                    authors.append(f"{last} {initials or ''}".strip())

            record = {
                "pmid": pmid,
                "title": get_text(art.find(".//ArticleTitle")),
                "journal": art.findtext(".//Journal/Title") or "",
                "year": int(year) if year.isdigit() else None,
                "doi": art.findtext(".//ArticleId[@IdType='doi']") or "",
                "pmcid": art.findtext(".//ArticleId[@IdType='pmc']") or "",
                "authors": authors,
                "publication_types": [p.text for p in art.findall(".//PublicationType")],
            }
            out.write(json.dumps(record) + "\n")
            count += 1

        print(f"{min(start + BATCH, len(pmids))}/{len(pmids)} done")
        time.sleep(0.4)

print(f"Finished. Saved metadata for {count} papers to {OUT_FILE}")