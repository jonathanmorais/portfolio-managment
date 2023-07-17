import re
import uuid

from pydantic import BaseModel, Field

class Portfolio(BaseModel):
    id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    volatility: float
    sharperatio: float
    beta: float
    kurtosis: float
