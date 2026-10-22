import json, sys

pmid = sys.argv[1]
data = json.load(open(f"dataset/raw/papers/{pmid}.json"))

for passage in data[0]["documents"][0]["passages"]:
    section = passage["infons"].get("section_type", "")
    text = passage.get("text", "")
    if section in ("TITLE", "ABSTRACT", "INTRO", "RESULTS", "CONCL"):
        print(f"\n=== {section} ===")
        print(text[:500])