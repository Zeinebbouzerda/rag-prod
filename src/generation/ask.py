import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "retrieval"))

from google import genai
from google.genai import types
from search import search, client as qdrant

LLM_MODEL = "gemini-3.8-flash"
K = 5

SYSTEM = """Tu es un assistant qui répond à des questions sur la documentation FastAPI.
Règles strictes :
- Réponds UNIQUEMENT à partir des extraits fournis.
- Cite les extraits utilisés avec leur numéro entre crochets, par exemple [1] ou [2][3].
- Si les extraits ne contiennent pas la réponse, dis clairement : "Je ne trouve pas la réponse dans la documentation fournie." N'invente rien.
- Réponds dans la langue de la question.
- Sois concis et donne un exemple de code si les extraits en contiennent un."""

llm = genai.Client()  # lit GEMINI_API_KEY


def build_context(hits):
    blocs = []
    for i, h in enumerate(hits, start=1):
        blocs.append(f"[{i}] (source : {h['source']})\n{h['texte']}")
    return "\n\n---\n\n".join(blocs)


def ask(question: str):
    hits = search(question, k=K)
    user_msg = f"Extraits :\n\n{build_context(hits)}\n\nQuestion : {question}"
    resp = llm.models.generate_content(
        model=LLM_MODEL,
        contents=user_msg,
        config=types.GenerateContentConfig(system_instruction=SYSTEM, max_output_tokens=800),
    )
    return resp.text, hits, resp.usage_metadata


if __name__ == "__main__":
    question = " ".join(sys.argv[1:])
    answer, hits, usage = ask(question)
    print("\n" + answer)
    print("\nSources :")
    for i, h in enumerate(hits, start=1):
        print(f"  [{i}] {h['source']}")
    print(f"\n(tokens : {usage.prompt_token_count} entrée, {usage.candidates_token_count} sortie)")
    qdrant.close()