"""
Train a simple mood classification model.

It trains a TF-IDF + LogisticRegression model on mood-labeled text.
If there are mood entries in DB with labels, it will use them.
Otherwise it uses a small built-in sample set.

Outputs to MODEL_PATH configured in app/config.py
"""
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from pathlib import Path
from ..config import settings
from ..database import SessionLocal
from .. import models
import pandas as pd

DEFAULT_LABELS = ["calm", "neutral", "anxious"]

SAMPLE_DATA = [
    ("I feel very nervous and worried about exams", "anxious"),
    ("My heart races and I cannot sleep", "anxious"),
    ("I am okay and relaxed today", "calm"),
    ("Feeling peaceful and calm right now", "calm"),
    ("I finished my tasks and feel fine", "neutral"),
    ("Today was average, nothing special", "neutral"),
    ("I feel overwhelmed and tense", "anxious"),
    ("Breathing exercises helped me calm down", "calm"),
]


def load_data_from_db(limit: int = 1000):
    db = SessionLocal()
    try:
        q = db.query(models.MoodEntry).filter(models.MoodEntry.label != None).limit(limit).all()
        data = [(m.text, m.label) for m in q]
        return data
    finally:
        db.close()


def train_and_save(model_path: str = settings.MODEL_PATH):
    data = load_data_from_db()
    if not data:
        print("No labeled data in DB. Using sample data.")
        data = SAMPLE_DATA

    df = pd.DataFrame(data, columns=["text", "label"])
    X = df["text"].values
    y = df["label"].values

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X, y)
    p = Path(model_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, p)
    print(f"Model saved to {p}")


if __name__ == "__main__":
    train_and_save()
