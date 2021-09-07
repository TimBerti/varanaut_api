from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api import deps
from app.api.portfolio_creator.src.main import optimal_portfolio


router = APIRouter()


@router.post("/")
def set_portfolio(body: dict = Body(...), db: Session = Depends(deps.get_db)):

    portfolio = optimal_portfolio(body["risk_coefficient"], db)

    return JSONResponse(content=portfolio)
