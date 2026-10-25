"""Upload the app code to the Hugging Face Space. HF then builds it with the Dockerfile."""
import os
from dotenv import load_dotenv
from huggingface_hub import HfApi

load_dotenv()
SPACE_ID = "sahir-zaman/trustmed"

api = HfApi(token=os.getenv("HF_TOKEN"))      # your WRITE token from .env
api.upload_folder(
    folder_path=".",
    repo_id=SPACE_ID,
    repo_type="space",
    ignore_patterns=[".venv/*", "dataset/*", ".env", ".git/*", "**/__pycache__/*",
                     "notebooks/*", "results/*", "eval/*", "checks/*", "project_plan.txt"],
)
print(f"Uploaded! Watch the build at https://huggingface.co/spaces/{SPACE_ID}")