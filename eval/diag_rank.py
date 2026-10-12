import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "retrieval"))
from search import search, client

rows = [json.loads(l) for l in open("eval/questions_hard.jsonl", encoding="utf-8")]
for r in rows:
    if r["groupe"] != "hard_en":
        continue
    sources = [x["source"] for x in search(r["question"], k=30)]
    rang = sources.index(r["source_attendue"]) + 1 if r["source_attendue"] in sources else None
    print(f"rang={rang} | {r['question']}")
client.close()