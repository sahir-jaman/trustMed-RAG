import json, random
from collections import Counter

IN_FILE = "dataset/processed/papers.jsonl"
OUT_FILE = "dataset/processed/chunks.jsonl"

CHUNK_SIZE = 400   # words per chunk
OVERLAP = 50       # words repeated from the previous chunk
MIN_WORDS = 30     # drop tiny leftover chunks

def split_words(words):
    """Cut a list of words into overlapping windows."""
    if len(words) <= CHUNK_SIZE:
        return [words]
    step = CHUNK_SIZE - OVERLAP
    chunks = []
    for start in range(0, len(words), step):
        piece = words[start:start + CHUNK_SIZE]
        if len(piece) < MIN_WORDS and chunks:   # tiny tail: already covered by overlap
            break
        chunks.append(piece)
        if start + CHUNK_SIZE >= len(words):
            break
    return chunks

total, section_count, lengths = 0, Counter(), []
all_chunks = []

with open(IN_FILE, encoding="utf-8") as f_in, open(OUT_FILE, "w", encoding="utf-8") as f_out:
    for line in f_in:
        paper = json.loads(line)

        # Join the paragraphs of each section together (keeping the paper's order)
        by_section = {}
        for s in paper["sections"]:
            by_section.setdefault(s["section"], []).append(s["text"])

        n = 0
        for section, paragraphs in by_section.items():
            words = " ".join(paragraphs).split()
            for piece in split_words(words):
                if len(piece) < MIN_WORDS:
                    continue
                chunk = {
                    "chunk_id": f"{paper['pmid']}_{n}",
                    "pmid": paper["pmid"],
                    "section": section,
                    "text": " ".join(piece),
                    "title": paper["title"],
                    "journal": paper["journal"],
                    "year": paper["year"],
                    "doi": paper["doi"],
                    "pmcid": paper["pmcid"],
                    "authors": paper["authors"][:3],
                    "study_type": paper["study_type"],
                    "evidence_level": paper["evidence_level"],
                    "retraction_status": paper["retraction_status"],
                    "retracted": paper["retracted"],
                }
                f_out.write(json.dumps(chunk) + "\n")
                all_chunks.append(chunk)
                n += 1
                total += 1
                section_count[section] += 1
                lengths.append(len(piece))

print(f"Created {total} chunks")
print(f"Average length: {sum(lengths) // len(lengths)} words")
print("Chunks per section:", dict(section_count))

# Show one random chunk so you can see what it looks like
c = random.choice(all_chunks)
print("\n--- Example chunk ---")
print(f"{c['chunk_id']} | {c['section']} | {c['evidence_level']} | {c['year']}")
print(c["title"])
print(c["text"][:600], "...")