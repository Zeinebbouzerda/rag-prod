import sys
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

MODEL = "intfloat/multilingual-e5-small"
COLLECTION = "fastapi_docs"

model = SentenceTransformer(MODEL)
client = QdrantClient(path="data/qdrant")


def search(question: str, k: int = 5):
    # e5 demande le préfixe "query: " pour les questions
    vec = model.encode("query: " + question, normalize_embeddings=True).tolist()
    hits = client.query_points(COLLECTION, query=vec, limit=k).points
    return [{"score": h.score, **h.payload} for h in hits]


if __name__ == "__main__":
    question = " ".join(sys.argv[1:])
    for r in search(question):
        print(f"{r['score']:.3f} | {r['source']} | {r['titre']}")
    client.close()  # évite l'erreur msvcrt à la fermeture