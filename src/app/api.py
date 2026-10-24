"""FastAPI backend for TrustMed."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from groq import RateLimitError
from trustmed.pipeline import TrustMedPipeline
from app.checkORdownload_db import ensure_db

pipeline = None


@asynccontextmanager
async def lifespan(app):
    global pipeline
    ensure_db()  # download the database if it isn't here yet
    pipeline = TrustMedPipeline()      # load the models ONCE, when the server starts
    yield


app = FastAPI(title="TrustMed API", version="0.1", lifespan=lifespan)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)


@app.get("/")
def health():
    """Quick check that the server is running."""
    return {"status": "Welcome to Trust Med", "pipeline_loaded": pipeline is not None}


@app.post("/chat")
def ask(req: AskRequest):
    """Question in -> answer, checked claims, sources with badges, warnings out."""
    try:
        return pipeline.ask(req.question)
    except RateLimitError:
        raise HTTPException(status_code=503,
                            detail="The AI service is busy (usage limit reached). Please try again later.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {type(e).__name__}")