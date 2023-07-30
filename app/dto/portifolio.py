from pydantic import BaseModel
from pydantic import Field
from typing import List, Optional
import pandas as pd

class UserRequest(BaseModel):
    period: str
    tickers: List[str]
    index: str
    weights: List[float]

class UserResponse(BaseModel):
    volatility: str
    sharpe_ratio: str
    beta: str
    kurtosis: str
