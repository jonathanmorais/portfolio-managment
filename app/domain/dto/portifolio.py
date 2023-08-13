from pydantic import BaseModel
from typing import List

class UserRequest(BaseModel):
    period: str
    tickers: List[str]
    index: str
    weights: List[float]
    risk_rate: float

class UserResponse(BaseModel):
    volatility: str
    sharpe_ratio: str
    beta: str
    kurtosis: str

class MetricsResponse(BaseModel):
    volatility: str
    sharpe_ratio: str
    beta: str
    kurtosis: str