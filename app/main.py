import numpy as np
import pandas as pd
import yfinance as yf
import quantstats as qs
from scipy import stats


class StockDataProvider:
    def __init__(self, tickers, index, period):
        self.tickers = tickers
        self.index   = index
        self.period  = period

    def download_stock_data(self):
        stock_data = yf.download(tickers=self.tickers, period=self.period)
        return stock_data['Adj Close']

    def download_index_data(self):
        idx_data = yf.download(tickers=self.index, period=self.period)
        return idx_data['Adj Close']

class StockReturn:
    def __init__(self, data_provided) -> None:
        self.data_provided    = data_provided

    def calculate_portfolio_returns(self):
        return np.log(self.data_provided / self.data_provided.shift(1)).dropna()

    def calculate_index_return(self):
        return self.data_provided.pct_change(1).dropna()    

class StockMetricsCalculate:
    def __init__(self, log_return, index_return):
        self.log_return    = log_return
        self.index_return   = index_return

    def calculate_volatility_return(self, annualized=True):
        log_ret = self.log_return
        portfolio_cov = log_ret.cov() * 252

        if annualized:
            portfolio_weights= np.array([0.2,0.2,0.2,0.2,0.2])
            portfolio_std =np.sqrt(np.dot(portfolio_weights.T, np.dot(portfolio_cov, portfolio_weights)))
            
            volatility = portfolio_std * np.sqrt(252)

        return volatility

    def calculate_sharpe_ratio(self):
        returns = self.log_return * 252 
        shar_rt = qs.stats.sharpe(returns, rf=0)
        shar_rt_rounded = np.round(shar_rt, decimals=2)

        return shar_rt_rounded
    
    def calculate_beta(self):

        portfolio_cov = self.log_return.cov()
        benchmark_index = self.index_return
        annual_cov    = portfolio_cov * 252
        covariance_port = annual_cov.iloc[0,1]

        portfolio_benchmark = benchmark_index.pct_change(1).dropna()
        market_variance = portfolio_benchmark.var() * 252

        beta_rounded = format(covariance_port / market_variance, 'f')           
        
        return beta_rounded
                        

if __name__ == "__main__":
    start_date = "5y"
    tickers = ["PETR4.SA", "CPLE6.SA", "TAEE11.SA", "CMIG4.SA", "BRAP4.SA"]
    index   = "^BVSP"

    stock_data_provider = StockDataProvider(tickers, index, start_date)
    stock_index_provider  = StockDataProvider(tickers, index, start_date)
    stock_return        = StockReturn(stock_data_provider.download_stock_data())
    stock_return_index  = StockReturn(stock_index_provider.download_index_data())
    stock_analyzer      = StockMetricsCalculate(stock_return.calculate_portfolio_returns(), stock_return_index.calculate_index_return())

   # portfolio_returns = stock_analyzer.calculate_portfolio_optimization(stock_data_provider)

    print(stock_analyzer.calculate_beta())
