from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    preferences = Column(Text, nullable=True)

    activities = relationship("ActivityProgress", back_populates="user")
    mood_entries = relationship("MoodEntry", back_populates="user")
    game_scores = relationship("GameScore", back_populates="user")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    activity_type = Column(String(100), nullable=True)  # breathing, meditation, audio, game, etc.
    content_url = Column(String(1024), nullable=True)


class ActivityProgress(Base):
    __tablename__ = "activity_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activities")
    # Optionally: relationship to Activity


class MotivationalContent(Base):
    __tablename__ = "motivational_content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content_type = Column(String(50), default="text")  # text, video, audio
    text = Column(Text, nullable=True)
    url = Column(String(1024), nullable=True)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    # hint to front end how to run simple games (or link)


class GameScore(Base):
    __tablename__ = "game_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    score = Column(Float, nullable=False)
    played_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="game_scores")


class MoodEntry(Base):
    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    text = Column(Text, nullable=False)
    label = Column(String(64), nullable=True)  # e.g., "anxious", "calm", "neutral", for training
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="mood_entries")
