"""Find the chunks most related to a question."""
import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "dataset/chroma_db"
COLLECTION = "trustmed_chunks"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"   # Model I got highest result from Notebook


class Retriever:
    def __init__(self, db_path=DB_PATH):
        self.model = SentenceTransformer(EMBED_MODEL)
        client = chromadb.PersistentClient(path=db_path)
        self.collection = client.get_collection(COLLECTION)

    def search(self, question, k=5, where=None):
        """Returning the top-k chunks for a question, with their labels."""
        q = self.model.encode([question], normalize_embeddings=True).tolist()
        res = self.collection.query(query_embeddings=q, n_results=k, where=where)

        results = []
        for cid, text, meta, dist in zip(res["ids"][0], res["documents"][0],
                                         res["metadatas"][0], res["distances"][0]):
            results.append({"chunk_id": cid, "text": text,
                            "score": round(1 - dist, 3),   # higher = more similar
                            **meta})
        return results