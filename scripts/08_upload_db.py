"""Upload the ChromaDB folder to a private Hugging Face dataset repo."""
import os
from dotenv import load_dotenv
from huggingface_hub import HfApi

load_dotenv()
REPO_ID = "sahir-zaman/trustmed-chroma"     # <- change to your Hugging Face username

api = HfApi(token=os.getenv("HF_TOKEN"))
api.create_repo(REPO_ID, repo_type="dataset", private=True, exist_ok=True)
api.upload_folder(folder_path="dataset/chroma_db", repo_id=REPO_ID, repo_type="dataset")
print(f"Uploaded! See it at https://huggingface.co/datasets/{REPO_ID}")