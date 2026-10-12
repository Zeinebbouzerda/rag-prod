import sys
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

MODEL = "BAAI/bge-m3"
COLLECTION = "fastapi_docs_bge"

model = SentenceTransformer(MODEL)
client = QdrantClient(path="data/qdrant")


def search(question: str, k: int = 5):
    vec = model.encode(question, normalize_embeddings=True).tolist()
    hits = client.query_points(COLLECTION, query=vec, limit=k).points
    return [{"score": h.score, **h.payload} for h in hits]


if __name__ == "__main__":
    question = " ".join(sys.argv[1:])
    for r in search(question):
        print(f"{r['score']:.3f} | {r['source']} | {r['titre']}")
    client.close()