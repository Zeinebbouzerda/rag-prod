import json
from pathlib import Path

DOCS = Path("data/fastapi")

ANSWERABLE = [
    ("How do I declare a query parameter with a default value?", "Declare it as a function parameter that is not in the path, with a default value.", "tutorial/query-params.md"),
    ("How do I declare a path parameter with a type?", "Use the same syntax as Python format strings and add a type annotation to the function parameter.", "tutorial/path-params.md"),
    ("How do I declare a request body with Pydantic?", "Create a Pydantic model class and declare it as a parameter of the path operation function.", "tutorial/body.md"),
    ("How can I add CORS to my application?", "Add CORSMiddleware with the allowed origins.", "tutorial/cors.md"),
    ("How do I run a task after returning a response?", "Use BackgroundTasks and add_task.", "tutorial/background-tasks.md"),
    ("How do I upload files?", "Declare a parameter of type File or UploadFile.", "tutorial/request-files.md"),
    ("How do I read form data?", "Use Form parameters; this requires python-multipart.", "tutorial/request-forms.md"),
    ("How do I return an HTTP error to the client?", "Raise an HTTPException with a status code and detail.", "tutorial/handling-errors.md"),
    ("How do I read a header from the request?", "Declare a parameter with Header.", "tutorial/header-params.md"),
    ("How do I read a cookie?", "Declare a parameter with Cookie.", "tutorial/cookie-params.md"),
    ("How do I limit the response fields with a response model?", "Use the response_model parameter in the path operation decorator.", "tutorial/response-model.md"),
    ("How do I set the status code of a response?", "Use the status_code parameter in the path operation decorator.", "tutorial/response-status-code.md"),
    ("How do I add validation constraints to a query parameter, like max length?", "Use Query with parameters like max_length.", "tutorial/query-params-str-validations.md"),
    ("How do I validate a path parameter with greater than or less than?", "Use Path with gt, ge, lt, le.", "tutorial/path-params-numeric-validations.md"),
    ("How do I use dependency injection?", "Declare a function and use Depends in the parameters.", "tutorial/dependencies/index.md"),
    ("How do I serve static files?", "Mount StaticFiles on a path.", "tutorial/static-files.md"),
    ("How do I write tests for my application?", "Use TestClient.", "tutorial/testing.md"),
    ("How do I set the title and description of my API?", "Pass metadata parameters when creating the FastAPI app.", "tutorial/metadata.md"),
    ("How do I add a custom middleware?", "Use the @app.middleware('http') decorator on a function.", "tutorial/middleware.md"),
    ("How do I split my application into multiple files?", "Use APIRouter.", "tutorial/bigger-applications.md"),
    ("How do I connect to a SQL database?", "Use SQLModel with an engine and a session dependency.", "tutorial/sql-databases.md"),
    ("How do I add OAuth2 password authentication?", "Use OAuth2PasswordBearer.", "tutorial/security/first-steps.md"),
    ("How do I define nested models in a request body?", "Use a Pydantic model as the type of an attribute of another model.", "tutorial/body-nested-models.md"),
    ("How do I add extra validation inside a Pydantic model field?", "Use Field with validation parameters.", "tutorial/body-fields.md"),
    ("How do I declare multiple body parameters?", "Declare several Pydantic model parameters, or use Body.", "tutorial/body-multiple-params.md"),
    ("How do I build a Docker image for my application?", "Write a Dockerfile based on a Python image.", "deployment/docker.md"),
    ("How do I handle websockets?", "Use the WebSocket class and a websocket route.", "advanced/websockets.md"),
]

UNANSWERABLE = [
    "How do I deploy with Helm on Kubernetes?",
    "How do I use Django ORM migrations?",
    "How do I train a neural network with PyTorch?",
    "What is the capital of Morocco?",
    "How do I configure an Nginx reverse proxy for PHP?",
    "How do I use React hooks?",
    "How to set up a MongoDB replica set?",
    "How do I use pandas groupby?",
    "How to configure Redis Sentinel?",
    "How do I write a Rust macro?",
]

rows, manquants = [], []
for q, a, s in ANSWERABLE:
    if (DOCS / s).exists():
        rows.append({"question": q, "reponse_attendue": a,
                     "source_attendue": s, "type": "answerable"})
    else:
        manquants.append(s)
for q in UNANSWERABLE:
    rows.append({"question": q, "reponse_attendue": None,
                 "source_attendue": None, "type": "unanswerable"})

with open("eval/questions.jsonl", "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(len(rows) - len(UNANSWERABLE), "questions answerable,", len(UNANSWERABLE), "hors sujet")
if manquants:
    print("Pages introuvables (questions retirées) :", manquants)