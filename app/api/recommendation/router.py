from typing import Dict
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api import deps
from app.api.recommendation.diversification import diversification_recommendation
from app.api.recommendation.similar import similar_recommendation


router = APIRouter()


@router.post("/diversification")
def get_diversification_recommendation(request: Dict, db: Session = Depends(deps.get_db)):

    portfolio = diversification_recommendation(db, request["portfolio"])

    return JSONResponse(content=portfolio)


@router.post("/similar")
def get_similar_recommendation(request: Dict, db: Session = Depends(deps.get_db)):

    portfolio = similar_recommendation(db, request["portfolio"])

    return JSONResponse(content=portfolio)
