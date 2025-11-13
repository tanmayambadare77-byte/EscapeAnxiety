from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..routers.users import get_current_user

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/", response_model=list[schemas.GameOut])
def get_games(db: Session = Depends(get_db)):
    return crud.list_games(db)


@router.post("/score", response_model=schemas.GameScoreOut)
def submit_score(score_in: schemas.GameScoreCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Validate game exists (optional)
    return crud.create_game_score(db, user_id=current_user.id, game_id=score_in.game_id, score=score_in.score)
