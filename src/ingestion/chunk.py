import json
from pathlib import Path

DOCS_FILE = Path("data/docs.jsonl")
OUT_FILE = Path("data/chunks.jsonl")
CHUNK_WORDS = 300
OVERLAP_WORDS = 50


def split_words(text: str, size: int, overlap: int):
    words = text.split()
    step = size - overlap
    for start in range(0, len(words), step):
        piece = words[start:start + size]
        if len(piece) < 30:
            break
        yield start, " ".join(piece)


def main():
    n = 0
    with OUT_FILE.open("w", encoding="utf-8") as out:
        for line in DOCS_FILE.open(encoding="utf-8"):
            doc = json.loads(line)
            for i, (start, text) in enumerate(split_words(doc["texte"], CHUNK_WORDS, OVERLAP_WORDS)):
                chunk = {
                    "chunk_id": f'{doc["id"]}::{i}',
                    "doc_id": doc["id"],
                    "titre": doc["titre"],
                    "source": doc["source"],
                    "position": i,
                    "texte": text,
                }
                out.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                n += 1
    print(f"{n} chunks écrits dans {OUT_FILE}")


if __name__ == "__main__":
    main()