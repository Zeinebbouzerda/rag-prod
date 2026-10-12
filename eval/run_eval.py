import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "retrieval"))
from search import search, client

rows = [json.loads(l) for l in open("eval/questions.jsonl", encoding="utf-8")]
answerable = [r for r in rows if r["type"] == "answerable"]

hits_ok = 0
rates = []
for r in answerable:
    res = search(r["question"], k=5)
    sources = [x["source"] for x in res]
    found = r["source_attendue"] in sources
    hits_ok += found
    if not found:
        rates.append((r["question"], r["source_attendue"], sources[:3]))

print(f"\nrecall@5 = {hits_ok}/{len(answerable)} = {hits_ok/len(answerable):.1%}")
print("\nQuestions ratées :")
for q, att, got in rates:
    print(f"- {q}\n    attendu : {att}\n    obtenu  : {got}")
client.close()