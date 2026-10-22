import json, random

required = ["chunk_id", "pmid", "section", "text", "evidence_level", "retraction_status", "retracted"]
chunks = [json.loads(line) for line in open("dataset/processed/chunks.jsonl", encoding="utf-8")]

problems = [c["chunk_id"] for c in chunks if any(c.get(k) in (None, "") for k in required)]
retracted = {c["pmid"] for c in chunks if c["retracted"]}

print(f"Total chunks: {len(chunks)}")
print(f"Chunks with missing fields: {len(problems)}")
print(f"Retracted papers in chunks: {len(retracted)}")

# 20 random chunks to read by eye
for c in random.sample(chunks, 20):
    print(f"\n[{c['section']} | {c['evidence_level']} | {c['year']}] {c['title'][:70]}")
    print(c["text"][:200], "...")