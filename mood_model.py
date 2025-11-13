import joblib
from pathlib import Path
from typing import Tuple
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from .train_model import DEFAULT_LABELS


class MoodModel:
    def __init__(self, model_path: str = "app/ml/mood_model.pkl"):
        self.model_path = Path(model_path)
        self.pipeline: Pipeline | None = None
        self._load()

    def _load(self):
        if self.model_path.exists():
            self.pipeline = joblib.load(self.model_path)
        else:
            # fallback: create a default pipeline with simple mapping
            self.pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
                ("clf", LogisticRegression(max_iter=1000))
            ])
            # For safety we do not train here. Use train_model.py to produce model file.

    def predict(self, text: str) -> Tuple[str, float]:
        if self.pipeline is None:
            raise RuntimeError("Model pipeline not loaded")
        probs = self.pipeline.predict_proba([text])[0]
        idx = probs.argmax()
        label = self.pipeline.classes_[idx]
        confidence = float(probs[idx])
        return label, confidence
