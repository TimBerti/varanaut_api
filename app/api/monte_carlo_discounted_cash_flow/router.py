from typing import Dict
from fastapi import APIRouter
from app.api.monte_carlo_discounted_cash_flow.main import monte_carlo_discounted_cash_flow


router = APIRouter()


@router.post("/")
def get_monte_carlo_discounted_cash_flow(request: Dict):
    return monte_carlo_discounted_cash_flow(**request)
