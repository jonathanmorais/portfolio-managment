from typing import List

from app.domain.dto.portifolio import UserResponse, MetricsResponse
from app.domain.entities.entity import StockDataProvider, StockReturn, StockMetricsCalculate

class RequestMetrics:
    def __init__(self, period: str, tickers: List[str], index: str, weights: List[float], risk_rate: float):
        self.period = period
        self.tickers = tickers
        self.index = index
        self.weights = weights
        self.risk_rate = risk_rate

    def execute(self) -> object:
        """
        Executes the function and returns a UserResponse object.

        Returns:
            UserResponse: The response object containing the calculated metrics.

        Raises:
            ValueError: If there is an error executing the function.
        """
        stock_data_provider = StockDataProvider(self.tickers, self.index, self.period)
        stock_data = stock_data_provider.download_stock_data()
        index_data = stock_data_provider.download_index_data()

        stock_return_calculator = StockReturn(stock_data)
        index_return_calculator = StockReturn(index_data)

        stock_log_return = stock_return_calculator.calculate_portfolio_returns()
        index_return = index_return_calculator.calculate_index_return()

        stock_analyzer = StockMetricsCalculate(self.weights, stock_log_return, index_return, self.risk_rate)

        response = UserResponse(
            volatility=stock_analyzer.calculate_volatility_return(),
            sharpe_ratio=stock_analyzer.calculate_sharpe_ratio(),
            beta=stock_analyzer.calculate_beta(),
            kurtosis=stock_analyzer.calculate_kurtosis(),
        )

        return response
