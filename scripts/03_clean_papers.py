import csv, glob, json, os
from collections import Counter

PAPERS_DIR = "dataset/raw/papers"
OUT_FILE = "dataset/processed/papers.jsonl"
os.makedirs("dataset/processed", exist_ok=True)

# Sections we keep (everything else is thrown away)
KEEP = {"ABSTRACT": "abstract", "INTRO": "introduction", "METHODS": "methods",
        "RESULTS": "results", "DISCUSS": "discussion", "CONCL": "conclusion"}

# Study type -> evidence badge (checked in this order)
STUDY_TYPES = [
    ("Meta-Analysis", "strong"),
    ("Systematic Review", "strong"),
    ("Guideline", "strong"),
    ("Randomized Controlled Trial", "strong"),
    ("Clinical Trial", "moderate"),
    ("Observational Study", "weak"),
    ("Review", "weak"),
]

def get_study_type(pub_types):
    for name, level in STUDY_TYPES:
        if any(name in pt for pt in pub_types):
            return name, level
    return "Other", "weak"

# ---- 1) Load metadata ----
metadata = {}
with open("dataset/raw/metadata.jsonl", encoding="utf-8") as f:
    for line in f:
        m = json.loads(line)
        metadata[m["pmid"]] = m

# ---- 2) Load the retraction list (keep the most serious notice per paper) ----
SEVERITY = {"retraction": 3, "expression of concern": 2, "correction": 1}
LABEL = {"retraction": "retracted", "expression of concern": "expression_of_concern",
         "correction": "corrected"}
notices = {}

csv_path = glob.glob("dataset/raw/retraction-watch-data/*.csv")[0]
with open(csv_path, encoding="latin-1") as f:
    for row in csv.DictReader(f):
        nature = row.get("RetractionNature", "").strip().lower()
        if nature not in SEVERITY:
            continue
        keys = [(row.get("OriginalPaperDOI") or "").strip().lower(),
                (row.get("OriginalPaperPubMedID") or "").strip()]
        for key in keys:
            if key and key not in ("unavailable", "0"):
                if SEVERITY[nature] > SEVERITY.get(notices.get(key), 0):
                    notices[key] = nature

# ---- 3) Clean every paper ----
evidence_count, retraction_count = Counter(), Counter()
saved, skipped = 0, 0

with open(OUT_FILE, "w", encoding="utf-8") as out:
    for path in sorted(glob.glob(f"{PAPERS_DIR}/*.json")):
        pmid = os.path.basename(path).replace(".json", "")
        meta = metadata.get(pmid)
        if meta is None:
            skipped += 1
            continue

        try:
            data = json.load(open(path, encoding="utf-8"))
        except json.JSONDecodeError:
            print("Skipping", path, "(invalid JSON)")
            skipped += 1
            continue
        sections = []
        for p in data[0]["documents"][0]["passages"]:
            sec = p["infons"].get("section_type", "")
            ptype = p["infons"].get("type", "")
            text = (p.get("text") or "").strip()
            if sec not in KEEP:          # references, figures, tables...
                continue
            if "title" in ptype:         # headings like "Background", "Methods"
                continue
            if len(text.split()) < 10:   # tiny leftovers
                continue
            sections.append({"section": KEEP[sec], "text": text})

        if not sections:                 # nothing useful left
            skipped += 1
            continue

        study_type, evidence = get_study_type(meta["publication_types"])
        nature = notices.get(meta["doi"].lower()) or notices.get(pmid)
        status = LABEL.get(nature, "none")

        record = {**meta,
                  "study_type": study_type,
                  "evidence_level": evidence,
                  "retraction_status": status,
                  "retracted": status == "retracted",
                  "sections": sections}
        out.write(json.dumps(record) + "\n")

        saved += 1
        evidence_count[evidence] += 1
        retraction_count[status] += 1

print(f"Saved {saved} clean papers, skipped {skipped}")
print("Evidence levels:", dict(evidence_count))
print("Retraction labels:", dict(retraction_count))