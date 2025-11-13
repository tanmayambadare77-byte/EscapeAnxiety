from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/motivational", response_model=list[schemas.MotivationalContentOut])
def get_motivational(db: Session = Depends(get_db)):
    return crud.list_motivational_content(db)
