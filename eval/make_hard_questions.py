import json
from pathlib import Path

DOCS = Path("data/fastapi")

# (question, reponse_attendue, source_attendue)
HARD_EN = [
    ("How can I execute code after the response has been sent to the client?", "Use BackgroundTasks.", "tutorial/background-tasks.md"),
    ("How do I let a browser on another domain call my API?", "Configure CORSMiddleware.", "tutorial/cors.md"),
    ("How do I accept a file sent by a client?", "Use File or UploadFile.", "tutorial/request-files.md"),
    ("How do I make my endpoint return an error with a 404?", "Raise HTTPException.", "tutorial/handling-errors.md"),
    ("How do I share logic between several endpoints?", "Use dependencies with Depends.", "tutorial/dependencies/index.md"),
    ("How do I validate the length of a string in the URL query?", "Use Query with max_length.", "tutorial/query-params-str-validations.md"),
    ("How do I check that my endpoints work without starting a server?", "Use TestClient.", "tutorial/testing.md"),
    ("How do I organize routes across several modules?", "Use APIRouter.", "tutorial/bigger-applications.md"),
    ("How do I choose the HTTP status returned on success?", "Use status_code in the decorator.", "tutorial/response-status-code.md"),
    ("How do I hide some fields of my data from the response?", "Use response_model.", "tutorial/response-model.md"),
]

HARD_FR = [
    ("Comment exécuter une tâche après avoir envoyé la réponse ?", "Utiliser BackgroundTasks.", "tutorial/background-tasks.md"),
    ("Comment autoriser les requêtes d'un autre domaine ?", "Configurer CORSMiddleware.", "tutorial/cors.md"),
    ("Comment recevoir un fichier envoyé par l'utilisateur ?", "Utiliser File ou UploadFile.", "tutorial/request-files.md"),
    ("Comment renvoyer une erreur HTTP ?", "Lever une HTTPException.", "tutorial/handling-errors.md"),
    ("Comment utiliser l'injection de dépendances ?", "Utiliser Depends.", "tutorial/dependencies/index.md"),
    ("Comment tester mon application ?", "Utiliser TestClient.", "tutorial/testing.md"),
    ("Comment découper mon application en plusieurs fichiers ?", "Utiliser APIRouter.", "tutorial/bigger-applications.md"),
    ("Comment lire un paramètre de requête ?", "Déclarer un paramètre de fonction.", "tutorial/query-params.md"),
    ("Comment déclarer le corps d'une requête ?", "Utiliser un modèle Pydantic.", "tutorial/body.md"),
    ("Comment servir des fichiers statiques ?", "Utiliser StaticFiles.", "tutorial/static-files.md"),
]

rows, manquants = [], []
for groupe, items in (("hard_en", HARD_EN), ("fr", HARD_FR)):
    for q, a, s in items:
        if (DOCS / s).exists():
            rows.append({"question": q, "reponse_attendue": a, "source_attendue": s,
                         "type": "answerable", "groupe": groupe})
        else:
            manquants.append(s)

with open("eval/questions_hard.jsonl", "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows), "questions difficiles écrites")
if manquants:
    print("Pages introuvables :", manquants)