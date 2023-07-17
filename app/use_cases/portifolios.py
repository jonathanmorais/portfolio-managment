import pandas as pd
import quantstats as qs
from scipy.stats import kurtosis
import numpy as np
import yfinance as yf

from .base import AbstractStockDataProvider, AbstractStockMetricsCalculate, AbstractStockReturn

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
    def __init__(self, weight, log_return, index_return):
        self.weight = weight
        self.log_return = log_return
        self.index_return = index_return

    def calculate_volatility_return(self, annualized=True):
        log_ret = self.log_return
        portfolio_cov = log_ret.cov() * 252

        if annualized:
            portfolio_weights = np.array(self.weight)
            portfolio_std = np.sqrt(np.dot(portfolio_weights.T, np.dot(portfolio_cov, portfolio_weights)))
            volatility = portfolio_std * np.sqrt(252)
            return volatility

    def calculate_sharpe_ratio(self):
        returns = self.log_return * 252
        sharpe_ratio = qs.stats.sharpe(returns, rf=0)
        sharpe_ratio_rounded = np.round(sharpe_ratio, decimals=2)
        return sharpe_ratio_rounded

    def calculate_beta(self):
        portfolio_cov = self.log_return.cov()
        benchmark_index = self.index_return
        annual_cov = portfolio_cov * 252
        covariance_port = annual_cov.iloc[0, 1]

        portfolio_benchmark = benchmark_index.pct_change(1).dropna()
        market_variance = portfolio_benchmark.var() * 252

        beta_rounded = format(covariance_port / market_variance, 'f')
        return beta_rounded

    def calculate_kurtosis(self):
        kurt = kurtosis(self.log_return, fisher=False)
        return kurt

    def execute(self):
        stock_data_provider = StockDataProvider(self.tickers, self.index, self.period)
        stock_data = stock_data_provider.download_stock_data()
        index_data = stock_data_provider.download_index_data()

        stock_return_calculator = StockReturn(stock_data)
        stock_log_return = stock_return_calculator.calculate_portfolio_returns()
        index_return = stock_return_calculator.calculate_index_return()

        status_portfolio_report = StockMetricsCalculate()

        return stock_log_return, index_return