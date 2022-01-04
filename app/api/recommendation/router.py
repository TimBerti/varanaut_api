from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.api.recommendation.main import calculate_recommendation


router = APIRouter()


@router.post("/")
def get_recommendation(request: Dict, db: Session = Depends(deps.get_db)):
    return calculate_recommendation(db, request["portfolio"])
