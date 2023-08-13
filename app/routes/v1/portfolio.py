import logging
from fastapi import APIRouter
from typing import Dict
from app.domain.dto.portifolio import UserRequest, UserResponse
from app.controller.main import ControllerAnalyzer 
from app.use_cases.portifolios import RequestMetrics

router = APIRouter()

@router.post("/status")
async def get_portfolio_status(user_request: UserRequest) -> Dict:
    period = user_request.period
    tickers = user_request.tickers
    index = user_request.index
    weights = user_request.weights
    risk_rate = user_request.risk_rate

    response_controller = ControllerAnalyzer(period, tickers, index, weights, risk_rate).controller_stock_analyzer().execute()

    return {
        "volatility": response_controller.volatility,
        "sharpe_ratio": response_controller.sharpe_ratio,
        "beta": response_controller.beta,
        "kurtosis": response_controller.kurtosis
    }

@router.get("/health")
async def get_health():
    return {"message": "Healthy"}
