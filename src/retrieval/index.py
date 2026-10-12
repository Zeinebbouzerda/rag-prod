import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

MODEL = "BAAI/bge-m3"
COLLECTION = "fastapi_docs_bge"

chunks = [json.loads(l) for l in open("data/chunks.jsonl", encoding="utf-8")]
print(len(chunks), "chunks à indexer")

model = SentenceTransformer(MODEL)
# e5 demande le préfixe "passage: " pour les documents
texts = [c["titre"] + "\n" + c["texte"] for c in chunks]
vectors = model.encode(texts, batch_size=32, normalize_embeddings=True, show_progress_bar=True)

client = QdrantClient(path="data/qdrant")
if client.collection_exists(COLLECTION):
    client.delete_collection(COLLECTION)
client.create_collection(
    COLLECTION,
    vectors_config=VectorParams(size=vectors.shape[1], distance=Distance.COSINE),
)
client.upsert(
    COLLECTION,
    points=[PointStruct(id=i, vector=v.tolist(), payload=c)
            for i, (c, v) in enumerate(zip(chunks, vectors))],
)
print("Indexation terminée :", client.count(COLLECTION).count, "points")
client.close()