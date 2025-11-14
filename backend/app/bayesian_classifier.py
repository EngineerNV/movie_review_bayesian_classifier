from __future__ import annotations

import math
import string
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence, Tuple

COMMON_WORDS = {
    "about",
    "all",
    "also",
    "and",
    "as",
    "at",
    "be",
    "because",
    "but",
    "by",
    "can",
    "come",
    "could",
    "day",
    "do",
    "even",
    "find",
    "first",
    "for",
    "from",
    "get",
    "give",
    "go",
    "have",
    "he",
    "her",
    "here",
    "him",
    "his",
    "how",
    "i",
    "if",
    "in",
    "into",
    "it",
    "its",
    "just",
    "know",
    "like",
    "look",
    "make",
    "man",
    "many",
    "me",
    "more",
    "my",
    "new",
    "no",
    "not",
    "now",
    "of",
    "on",
    "one",
    "only",
    "or",
    "other",
    "our",
    "out",
    "people",
    "say",
    "see",
    "she",
    "so",
    "some",
    "take",
    "tell",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "thing",
    "think",
    "this",
    "those",
    "time",
    "to",
    "two",
    "up",
    "use",
    "very",
    "want",
    "way",
    "we",
    "well",
    "what",
    "when",
    "which",
    "who",
    "will",
    "with",
    "would",
    "year",
    "you",
    "your",
}

TRANSLATION_TABLE = str.maketrans({key: " " for key in string.punctuation})


@dataclass
class TrainingSummary:
    fresh_token_count: int
    rotten_token_count: int
    vocabulary_size: int
    top_fresh_words: List[Tuple[str, float]]
    top_rotten_words: List[Tuple[str, float]]


@dataclass
class PredictionResult:
    label: str
    fresh_probability: float
    rotten_probability: float
    tokens_considered: List[str]


class TrainingRequiredError(RuntimeError):
    """Raised when predictions are requested before training."""


class BayesianClassifier:
    """A light-weight Naive Bayes classifier tailored for the movie review dataset."""

    def __init__(self) -> None:
        self.alpha: float = 1.0
        self._fresh_counts: Counter[str] = Counter()
        self._rotten_counts: Counter[str] = Counter()
        self._vocabulary: set[str] = set()
        self._fresh_tokens = 0
        self._rotten_tokens = 0
        self._fresh_reviews = 0
        self._rotten_reviews = 0
        self._trained = False

    @staticmethod
    def _tokenise(text: str) -> List[str]:
        cleaned = text.lower().translate(TRANSLATION_TABLE)
        tokens = [token for token in cleaned.split() if token and token not in COMMON_WORDS]
        return tokens

    @staticmethod
    def _load_reviews(path: Path) -> List[str]:
        if not path.exists():
            raise FileNotFoundError(path)
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            return [line.strip() for line in handle if line.strip()]

    def train(
        self,
        fresh_reviews: Sequence[str],
        rotten_reviews: Sequence[str],
        *,
        alpha: float = 1.0,
    ) -> TrainingSummary:
        if not fresh_reviews and not rotten_reviews:
            raise ValueError("At least one review is required to train the classifier.")

        self.alpha = alpha
        self._fresh_counts.clear()
        self._rotten_counts.clear()
        self._vocabulary.clear()
        self._fresh_tokens = 0
        self._rotten_tokens = 0
        self._fresh_reviews = len(fresh_reviews)
        self._rotten_reviews = len(rotten_reviews)

        for review in fresh_reviews:
            tokens = self._tokenise(review)
            self._fresh_counts.update(tokens)
            self._vocabulary.update(tokens)
            self._fresh_tokens += len(tokens)

        for review in rotten_reviews:
            tokens = self._tokenise(review)
            self._rotten_counts.update(tokens)
            self._vocabulary.update(tokens)
            self._rotten_tokens += len(tokens)

        self._trained = True

        return TrainingSummary(
            fresh_token_count=self._fresh_tokens,
            rotten_token_count=self._rotten_tokens,
            vocabulary_size=len(self._vocabulary),
            top_fresh_words=self._most_distinctive_words(self._fresh_counts, self._rotten_counts),
            top_rotten_words=self._most_distinctive_words(self._rotten_counts, self._fresh_counts),
        )

    def load_and_train(
        self,
        fresh_path: Path,
        rotten_path: Path,
        *,
        alpha: float = 1.0,
    ) -> TrainingSummary:
        fresh_reviews = self._load_reviews(fresh_path)
        rotten_reviews = self._load_reviews(rotten_path)
        return self.train(fresh_reviews, rotten_reviews, alpha=alpha)

    def predict(self, review: str) -> PredictionResult:
        if not self._trained:
            raise TrainingRequiredError("Train the classifier before making predictions.")

        tokens = self._tokenise(review)
        if not tokens:
            raise ValueError("No valid tokens found in the provided review.")

        fresh_log_prob = self._log_prior(self._fresh_reviews, self._rotten_reviews)
        rotten_log_prob = self._log_prior(self._rotten_reviews, self._fresh_reviews)

        vocab_size = max(len(self._vocabulary), 1)
        fresh_denominator = self._fresh_tokens + self.alpha * vocab_size
        rotten_denominator = self._rotten_tokens + self.alpha * vocab_size

        for token in tokens:
            fresh_count = self._fresh_counts.get(token, 0)
            rotten_count = self._rotten_counts.get(token, 0)
            fresh_log_prob += math.log((fresh_count + self.alpha) / fresh_denominator)
            rotten_log_prob += math.log((rotten_count + self.alpha) / rotten_denominator)

        fresh_probability, rotten_probability = self._normalise_log_probs(
            fresh_log_prob, rotten_log_prob
        )
        label = "Fresh" if fresh_probability > rotten_probability else "Rotten"

        return PredictionResult(
            label=label,
            fresh_probability=fresh_probability,
            rotten_probability=rotten_probability,
            tokens_considered=tokens,
        )

    def _most_distinctive_words(
        self,
        primary_counts: Counter[str],
        secondary_counts: Counter[str],
        *,
        limit: int = 8,
    ) -> List[Tuple[str, float]]:
        vocab_size = max(len(self._vocabulary), 1)
        primary_denominator = (self._fresh_tokens if primary_counts is self._fresh_counts else self._rotten_tokens) + self.alpha * vocab_size
        secondary_denominator = (self._rotten_tokens if secondary_counts is self._rotten_counts else self._fresh_tokens) + self.alpha * vocab_size

        scored: List[Tuple[str, float]] = []
        for word, count in primary_counts.items():
            primary_prob = (count + self.alpha) / primary_denominator
            secondary_prob = (secondary_counts.get(word, 0) + self.alpha) / secondary_denominator
            score = math.log(primary_prob / secondary_prob)
            scored.append((word, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:limit]

    @staticmethod
    def _normalise_log_probs(*log_probs: float) -> Tuple[float, ...]:
        max_log_prob = max(log_probs)
        exp_probs = [math.exp(lp - max_log_prob) for lp in log_probs]
        total = sum(exp_probs)
        return tuple(prob / total for prob in exp_probs)

    @staticmethod
    def _log_prior(class_count: int, other_class_count: int) -> float:
        total = class_count + other_class_count
        if total == 0:
            return math.log(0.5)
        return math.log(class_count / total if class_count else 1e-9)


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_dataset_paths() -> Tuple[Path, Path]:
    root = project_root()
    return root / "train_fresh.txt", root / "train_rotten.txt"
