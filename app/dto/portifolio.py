from pydantic import BaseModel
from pydantic import Field


class UserRequest(BaseModel):
    period: str
    tickers: list(str)
    index: str
    weights = list(int)


class UserResponse(BaseModel):
    volatility: float
    sharpe_ratio: float
    beta: float
    kurtosis: float
