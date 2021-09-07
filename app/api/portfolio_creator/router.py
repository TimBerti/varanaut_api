from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api import deps
from app.api.portfolio_creator.src.main import optimal_portfolio


router = APIRouter()


@router.post("/")
def set_portfolio(risk_coefficient: float = Form(..., ge=0, le=5), db: Session = Depends(deps.get_db)):

    portfolio = optimal_portfolio(risk_coefficient, db)

    return JSONResponse(content=portfolio)
