from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..ml.mood_model import MoodModel
from ..config import settings
from ..routers.users import get_current_user

router = APIRouter(prefix="/ml", tags=["ml"])
model = MoodModel(model_path=settings.MODEL_PATH)


@router.post("/mood", response_model=schemas.MoodPredictionOut)
def predict_mood(entry: schemas.MoodEntryCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Save mood entry without label
    me = crud.create_mood_entry(db, user_id=current_user.id, text=entry.text, label=entry.label)
    # Predict
    predicted, conf = model.predict(entry.text)
    return {"predicted_label": predicted, "confidence": conf}
