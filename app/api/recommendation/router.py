from typing import Dict
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api import deps
from app.api.recommendation.main import recommendation


router = APIRouter()


@router.post("/")
def set_portfolio(request: Dict, db: Session = Depends(deps.get_db)):

    portfolio = recommendation(db, request["portfolio"])

    return JSONResponse(content=portfolio)
