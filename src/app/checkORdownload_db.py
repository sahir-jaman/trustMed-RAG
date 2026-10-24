"""Download the ChromaDB database from Hugging Face if it isn't here yet."""
import os
from dotenv import load_dotenv
from huggingface_hub import snapshot_download

load_dotenv()
DB_REPO = os.getenv("DB_REPO", "sahir-zaman/trustmed-chroma")
DB_PATH = "dataset/chroma_db"


def ensure_db():
    if os.path.exists(os.path.join(DB_PATH, "chroma.sqlite3")):
        print("Database found locally.")
        return
    print(f"Database not found - downloading from {DB_REPO} (about 1.4 GB, first start only)...")
    snapshot_download(repo_id=DB_REPO, repo_type="dataset", local_dir=DB_PATH,
                      token=os.getenv("HF_TOKEN"))
    print("Database downloaded.")