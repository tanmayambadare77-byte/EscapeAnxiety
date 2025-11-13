from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash, verify_password
from typing import Optional
from datetime import datetime


# Users
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    hashed = get_password_hash(user_in.password)
    db_user = models.User(email=user_in.email, full_name=user_in.full_name, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Activities & progress
def list_activities(db: Session):
    return db.query(models.Activity).all()


def create_activity_progress(db: Session, user_id: int, activity_id: int) -> models.ActivityProgress:
    progress = models.ActivityProgress(user_id=user_id, activity_id=activity_id, completed_at=datetime.utcnow())
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def list_user_progress(db: Session, user_id: int):
    return db.query(models.ActivityProgress).filter(models.ActivityProgress.user_id == user_id).all()


# Motivational content
def list_motivational_content(db: Session):
    return db.query(models.MotivationalContent).all()


# Games
def list_games(db: Session):
    return db.query(models.Game).all()


def create_game_score(db: Session, user_id: int, game_id: int, score: float) -> models.GameScore:
    gs = models.GameScore(user_id=user_id, game_id=game_id, score=score)
    db.add(gs)
    db.commit()
    db.refresh(gs)
    return gs


# Mood entries
def create_mood_entry(db: Session, user_id: Optional[int], text: str, label: Optional[str] = None) -> models.MoodEntry:
    me = models.MoodEntry(user_id=user_id, text=text, label=label)
    db.add(me)
    db.commit()
    db.refresh(me)
    return me


def list_mood_entries(db: Session, limit: int = 100):
    return db.query(models.MoodEntry).limit(limit).all()
