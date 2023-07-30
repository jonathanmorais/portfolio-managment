import pandas as pd
import quantstats as qs
from scipy.stats import kurtosis
import numpy as np
import yfinance as yf
from typing import List

from .base import AbstractStockDataProvider, AbstractStockMetricsCalculate, AbstractStockReturn, AbstractStockMetricsResponse
from app.dto.portifolio import UserRequest, UserResponse

class StockDataProvider(AbstractStockDataProvider):
    def __init__(self, tickers, index, period):
        self.tickers = tickers
        self.index = index
        self.period = period

    def download_stock_data(self):
        stock_data = yf.download(tickers=self.tickers, period=self.period)
        return stock_data['Adj Close']

    def download_index_data(self):
        idx_data = yf.download(tickers=self.index, period=self.period)
        return idx_data['Adj Close']

class StockReturn(AbstractStockReturn):
    def __init__(self, data_provided) -> None:
        self.data_provided = data_provided

    def calculate_portfolio_returns(self):
        return np.log(self.data_provided / self.data_provided.shift(1)).dropna()

    def calculate_index_return(self):
        return self.data_provided.pct_change(1).dropna()

class StockMetricsCalculate(AbstractStockMetricsCalculate):
    def __init__(self, weights, log_return, index_return, risk_rate):
        self.weights = weights
        self.log_return = log_return
        self.index_return = index_return
        self.risk_rate = risk_rate

    def calculate_volatility_return(self, annualized=True):
        log_ret = self.log_return
        portfolio_cov = log_ret.cov() * 252

        if annualized:
            portfolio_weights = np.array(self.weights)
            portfolio_std = np.sqrt(np.dot(portfolio_weights.T, np.dot(portfolio_cov, portfolio_weights)))
            volatility = round(portfolio_std * np.sqrt(252), 3)
            return str(volatility)

    def calculate_sharpe_ratio(self):
        sharpe_ratio = np.round(qs.stats.sharpe(self.log_return, rf=self.risk_rate), decimals=2)
        sharpe_ratio = round(sharpe_ratio.mean(), 2)
        return str(sharpe_ratio)

    def calculate_beta(self, annualized=True):
        log_ret = self.log_return
        portfolio_cov = log_ret.cov()
        if annualized:
            annual_cov = portfolio_cov * 252
            covariance_port = annual_cov.iloc[0, 1]
            benchmark_index = self.index_return
            market_variance = benchmark_index.var() * 252

            beta = covariance_port / market_variance
            return str(beta)

    def calculate_kurtosis(self):
        kurt_median = qs.stats.kurtosis(self.log_return).mean()
        kurt        = round(kurt_median, 2)
        return str(kurt)

class RequestMetrics:
    def __init__(self, period: str, tickers: List[str], index: str, weights: List[float], risk_rate: float):
        self.period  = period
        self.tickers = tickers
        self.index   = index
        self.weights = weights
        self.risk_rate = risk_rate

    def execute(self) -> UserResponse:
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
            kurtosis=stock_analyzer.calculate_kurtosis()
        )

        return response