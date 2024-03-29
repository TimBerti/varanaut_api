from fastapi import APIRouter

from app.api.portfolio_creator import router as portfolio_creator_router
from app.api.recommendation import router as recommendation_router
from app.api.monte_carlo_discounted_cash_flow import router as dcf_router

api_router = APIRouter()

api_router.include_router(portfolio_creator_router.router,
                          prefix="/portfolio-creator")

api_router.include_router(recommendation_router.router,
                          prefix="/recommendation")

api_router.include_router(dcf_router.router,
                          prefix="/dcf")
