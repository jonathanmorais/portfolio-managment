import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import riskfolio as rp
from IPython.display import display
import quantstats as qs


class StockDataProvider:
    def __init__(self, tickers, period):
        self.tickers = tickers
        self.period  = period

    def download_stock_data(self):
        stock_data = yf.download(tickers=self.tickers, period=self.period)
        return stock_data['Adj Close']

class StockReturn:
    def __init__(self, data_provided) -> None:
        self.data_provided    = data_provided

    def calculate_portfolio_returns(self):
        return np.log(self.data_provided / self.data_provided.shift(1)).dropna()

class StockMetricsCalculate:
    def __init__(self, log_return):
        self.log_return    = log_return

    def calculate_volatility_return(self, annualized=True):
        log_ret = self.log_return
        portfolio_cov = log_ret.cov() * 252

        if annualized:
            portfolio_weights= np.array([0.2,0.2,0.2,0.2,0.2])
            portfolio_std =np.sqrt(np.dot(portfolio_weights.T, np.dot(portfolio_cov, portfolio_weights)))
            
            volatility = portfolio_std * np.sqrt(252)


        return volatility
if __name__ == "__main__":
    start_date = "5y"
    tickers = ["PETR4.SA", "CPLE6.SA", "TAEE11.SA", "CMIG4.SA", "BRAP4.SA"]

    stock_data_provider = StockDataProvider(tickers, start_date)
    stock_return   = StockReturn(stock_data_provider.download_stock_data())
    stock_analyzer = StockMetricsCalculate(stock_return.calculate_portfolio_returns())

   # portfolio_returns = stock_analyzer.calculate_portfolio_optimization(stock_data_provider)

    print(stock_analyzer.calculate_volatility_return())

