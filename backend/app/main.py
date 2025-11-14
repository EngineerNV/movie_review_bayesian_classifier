from __future__ import annotations

import asyncio
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .bayesian_classifier import (
    BayesianClassifier,
    PredictionResult,
    TrainingRequiredError,
    TrainingSummary,
    default_dataset_paths,
)

app = FastAPI(
    title="Movie Review Mood Arcade",
    description=(
        "A playful FastAPI backend that powers an interactive Naive Bayes "
        "movie review experience."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TrainRequest(BaseModel):
    fresh_samples: List[str] = Field(default_factory=list, description="Positive review snippets.")
    rotten_samples: List[str] = Field(default_factory=list, description="Negative review snippets.")
    use_default_dataset: bool = Field(
        default=True,
        description="When true the classic training files bundled with the project are used as a base.",
    )
    alpha: float = Field(default=1.0, ge=0.1, le=10.0, description="Laplace smoothing factor.")


class TrainResponse(BaseModel):
    message: str
    fresh_token_count: int
    rotten_token_count: int
    vocabulary_size: int
    top_fresh_words: List[str]
    top_rotten_words: List[str]


class ClassifyRequest(BaseModel):
    review: str = Field(..., min_length=3)


class ClassifyResponse(BaseModel):
    label: str
    fresh_probability: float
    rotten_probability: float
    tokens_considered: List[str]


classifier = BayesianClassifier()
classifier_lock = asyncio.Lock()


async def _default_training() -> TrainingSummary:
    fresh_path, rotten_path = default_dataset_paths()
    return classifier.load_and_train(fresh_path, rotten_path)


@app.on_event("startup")
async def startup_event() -> None:
    async with classifier_lock:
        await _default_training()


@app.post("/train", response_model=TrainResponse)
async def train_endpoint(payload: TrainRequest) -> TrainResponse:
    async with classifier_lock:
        fresh_reviews = list(payload.fresh_samples)
        rotten_reviews = list(payload.rotten_samples)

        if payload.use_default_dataset:
            fresh_path, rotten_path = default_dataset_paths()
            fresh_reviews.extend(
                fresh_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            )
            rotten_reviews.extend(
                rotten_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            )

        summary = classifier.train(fresh_reviews, rotten_reviews, alpha=payload.alpha)

    return TrainResponse(
        message="Training complete! The mood arcade is freshly tuned.",
        fresh_token_count=summary.fresh_token_count,
        rotten_token_count=summary.rotten_token_count,
        vocabulary_size=summary.vocabulary_size,
        top_fresh_words=[word for word, _ in summary.top_fresh_words],
        top_rotten_words=[word for word, _ in summary.top_rotten_words],
    )


@app.post("/classify", response_model=ClassifyResponse)
async def classify_endpoint(payload: ClassifyRequest) -> ClassifyResponse:
    async with classifier_lock:
        try:
            prediction = classifier.predict(payload.review)
        except TrainingRequiredError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    return ClassifyResponse(
        label=prediction.label,
        fresh_probability=prediction.fresh_probability,
        rotten_probability=prediction.rotten_probability,
        tokens_considered=prediction.tokens_considered,
    )


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"status": "ok", "message": "The Movie Review Mood Arcade is online!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
