from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.api.portfolio_creator.main import portfolio_creator


router = APIRouter()


@router.post("/")
def set_portfolio(request: Dict, db: Session = Depends(deps.get_db)):
    return portfolio_creator(db, request)
