from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from app.api.monte_carlo_discounted_cash_flow.main import monte_carlo_discounted_cash_flow


router = APIRouter()


class Item(BaseModel):

    n_trials: Optional[int] = Field(
        100000, ge=1, le=100000
    )
    n_periods: Optional[int] = Field(
        10, ge=1, le=20
    )

    r_0: Optional[float] = Field(
        1.3, ge=0.1, le=5
    )
    dr_0: Optional[float] = Field(
        0.3, ge=0.001, le=5
    )

    r_n: Optional[float] = Field(
        1.04, ge=0.1, le=5
    )
    dr_n: Optional[float] = Field(
        0.16, ge=0.001, le=5
    )

    C_0: Optional[float] = Field(
        10, gt=0, le=100000
    )

    discount_rate: Optional[float] = Field(
        0.1, ge=0, le=9
    )

    terminal_multiple: Optional[float] = Field(
        15, ge=0, le=100
    )


@router.post("/")
def get_monte_carlo_discounted_cash_flow(request: Item):
    return monte_carlo_discounted_cash_flow(**request.dict())
