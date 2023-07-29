import re
import uuid

from pydantic import BaseModel, Field

class Portfolio(BaseModel):
    volatility: float
    sharperatio: float
    beta: float
    kurtosis: float
