import logging
from fastapi import APIRouter
from typing import List, Dict
from app.dto.portifolio import UserRequest, UserResponse
from app.use_cases.portifolios import RequestMetrics

router = APIRouter()

@router.post("/status")
async def get_portifolio_status(request: UserRequest) -> Dict:
    # You can access the request data through the `request` parameter
    period  = request.period
    tickers = request.tickers
    index   = request.index
    weights = request.weights

    print(request)

    metrics_calculator = RequestMetrics(period, tickers, index, weights)
    response = metrics_calculator.execute()

    response_metric = {
        "volatility": response.volatility,
        "sharpe_ratio": response.sharpe_ratio,
        "beta": response.beta,
        "kurtosis": response.kurtosis
    }

    return response_metric

@router.get("/health")
async def get_health():
    return {"message": "Healthy"}
