import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "retrieval"))
from search import search, client

rows = [json.loads(l) for l in open("eval/questions_hard.jsonl", encoding="utf-8")]
stats = {}
for r in rows:
    sources = [x["source"] for x in search(r["question"], k=5)]
    ok = r["source_attendue"] in sources
    s = stats.setdefault(r["groupe"], [0, 0])
    s[0] += ok
    s[1] += 1
    if not ok:
        print(f"RATÉ [{r['groupe']}] {r['question']}\n    attendu : {r['source_attendue']}\n    obtenu  : {sources[:3]}")

print()
for g, (ok, n) in stats.items():
    print(f"{g} : recall@5 = {ok}/{n} = {ok/n:.0%}")
client.close()