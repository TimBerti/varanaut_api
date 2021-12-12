from typing import Dict
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api import deps
from app.api.portfolio_creator.main import portfolio_creator


router = APIRouter()


@router.post("/")
def set_portfolio(request: Dict, db: Session = Depends(deps.get_db)):

    portfolio = portfolio_creator(
        db, request["risk_coefficient"], request["n_positions"])

    return JSONResponse(content=portfolio)
