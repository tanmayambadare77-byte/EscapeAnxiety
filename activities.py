from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..routers.users import get_current_user

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/", response_model=list[schemas.ActivityOut])
def get_activities(db: Session = Depends(get_db)):
    return crud.list_activities(db)


@router.post("/complete", response_model=schemas.ActivityProgressOut)
def complete_activity(progress_in: schemas.ActivityProgressCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Optionally validate activity exists
    return crud.create_activity_progress(db, user_id=current_user.id, activity_id=progress_in.activity_id)


@router.get("/progress", response_model=list[schemas.ActivityProgressOut])
def user_progress(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.list_user_progress(db, user_id=current_user.id)
