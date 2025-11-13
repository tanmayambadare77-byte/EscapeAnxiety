from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# User
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Activities
class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    activity_type: Optional[str] = None
    content_url: Optional[str] = None


class ActivityOut(ActivityBase):
    id: int

    class Config:
        orm_mode = True


# Progress
class ActivityProgressCreate(BaseModel):
    activity_id: int


class ActivityProgressOut(BaseModel):
    id: int
    activity_id: int
    completed_at: datetime

    class Config:
        orm_mode = True


# Motivational content
class MotivationalContentOut(BaseModel):
    id: int
    title: str
    content_type: str
    text: Optional[str] = None
    url: Optional[str] = None

    class Config:
        orm_mode = True


# Games
class GameOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class GameScoreCreate(BaseModel):
    game_id: int
    score: float


class GameScoreOut(BaseModel):
    id: int
    game_id: int
    score: float
    played_at: datetime

    class Config:
        orm_mode = True


# Mood
class MoodEntryCreate(BaseModel):
    text: str
    label: Optional[str] = None


class MoodPredictionOut(BaseModel):
    predicted_label: str
    confidence: float
