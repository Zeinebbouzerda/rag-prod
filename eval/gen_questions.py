import json
import random
import time
from google import genai
from google.genai import types

LLM_MODEL = "gemini-3.8-flash"
N = 60  # on en génère 60 pour en garder ~50 après relecture

chunks = [json.loads(l) for l in open("data/chunks.jsonl", encoding="utf-8")]
random.seed(42)
sample = random.sample(chunks, N)

llm = genai.Client()

PROMPT = """Voici un extrait de la documentation FastAPI :

{texte}

Écris UNE question qu'un développeur pourrait poser et dont la réponse se trouve dans cet extrait.
Règles :
- La question doit se comprendre seule, sans mentionner "l'extrait" ni "le texte".
- Écris la question en anglais.
- Donne aussi une réponse courte (1 à 3 phrases) basée uniquement sur l'extrait.
Réponds uniquement en JSON : {{"question": "...", "reponse_attendue": "..."}}"""

out = open("eval/questions_raw.jsonl", "w", encoding="utf-8")
ok = 0
for c in sample:
    for essai in range(3):
        try:
            resp = llm.models.generate_content(
                model=LLM_MODEL,
                contents=PROMPT.format(texte=c["texte"][:2500]),
                config=types.GenerateContentConfig(
                    response_mime_type="application/json", max_output_tokens=2000),
            )
            qa = json.loads(resp.text)
            qa["source_attendue"] = c["source"]
            qa["chunk_id"] = c["chunk_id"]
            qa["type"] = "answerable"
            out.write(json.dumps(qa, ensure_ascii=False) + "\n")
            ok += 1
            break
        except Exception as e:
            print("erreur, nouvel essai :", str(e)[:80])
            time.sleep(5)
    time.sleep(1)  # on reste sous les limites du quota gratuit
out.close()
print(ok, "questions écrites dans eval/questions_raw.jsonl")