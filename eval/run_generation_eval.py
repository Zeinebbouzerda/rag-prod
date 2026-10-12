import json
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "generation"))
from ask import ask, build_context, llm, LLM_MODEL, qdrant
from google.genai import types

LIMITE = 5  # nombre de questions answerable ; mets None pour tout tester plus tard

rows = [json.loads(l) for l in open("eval/questions.jsonl", encoding="utf-8")]
ans = [r for r in rows if r["type"] == "answerable"]
una = [r for r in rows if r["type"] == "unanswerable"]
if LIMITE:
    ans = ans[:LIMITE]
    una = una[:5]
rows = ans + una

JUGE = """Contexte (extraits) :
{ctx}

Réponse à évaluer :
{rep}

La réponse est-elle entièrement appuyée par les extraits, sans information inventée ?
Réponds uniquement en JSON : {{"fidele": true ou false, "raison": "..."}}"""

PHRASES_REFUS = [
    "je ne trouve pas",
    "i cannot find",
    "i can't find",
    "i couldn't find",
    "could not find",
    "not found in the",
    "does not contain",
    "do not contain",
    "not covered",
    "no information",
]


def appel(fn):
    for _ in range(4):
        try:
            return fn()
        except Exception as e:
            print("  erreur, nouvel essai :", str(e)[:80])
            time.sleep(10)
    return None


fideles, n_fid = 0, 0
refus_ok, n_refus = 0, 0

for r in rows:
    out = appel(lambda: ask(r["question"]))
    if out is None:
        print("  abandon pour :", r["question"])
        continue
    answer, hits, _ = out
    refuse = any(p in answer.lower() for p in PHRASES_REFUS)

    if r["type"] == "unanswerable":
        n_refus += 1
        refus_ok += refuse
        print(f"[hors sujet] refus={refuse} | {r['question']}")
    else:
        n_fid += 1
        verdict = appel(lambda: llm.models.generate_content(
            model=LLM_MODEL,
            contents=JUGE.format(ctx=build_context(hits), rep=answer),
            config=types.GenerateContentConfig(
                response_mime_type="application/json", max_output_tokens=1000),
        ))
        try:
            v = json.loads(verdict.text)
            fideles += bool(v["fidele"])
            print(f"[fidele={v['fidele']}] {r['question']}")
            if not v["fidele"]:
                print("    raison :", v["raison"][:150])
        except Exception:
            n_fid -= 1
            print("  verdict illisible pour :", r["question"])
    time.sleep(6)  # reste sous la limite par minute du quota gratuit

print(f"\nFidélité : {fideles}/{n_fid}")
print(f"Refus corrects sur hors-sujet : {refus_ok}/{n_refus}")
qdrant.close()