from app.domain.dto.portifolio import UserResponse
from app.use_cases.portifolios import RequestMetrics

class ControllerAnalyzer:
    def __init__(self, period, tickers, index, weights, risk_rate):
        self.period = period
        self.tickers = tickers
        self.index = index
        self.weights = weights
        self.risk_rate = risk_rate

    def controller_stock_analyzer(self):
        metrics_calculator = RequestMetrics(self.period, self.tickers, self.index, self.weights, self.risk_rate)
        return metrics_calculator
