import pytest
import numpy as np
import pandas as pd

from app.use_cases.portifolios import (
    StockDataProvider,
    StockReturn,
    StockMetricsCalculate,
)


# Test StockDataProvider
@pytest.fixture
def stock_data_provider():
    return StockDataProvider(["AAPL", "GOOGL"], "SPY", "1y")


def test_download_stock_data(stock_data_provider):
    stock_data = stock_data_provider.download_stock_data()
    assert isinstance(stock_data, pd.DataFrame)
    assert not stock_data.empty


def test_download_index_data(stock_data_provider):
    index_data = stock_data_provider.download_index_data()
    assert isinstance(index_data, pd.DataFrame)
    assert not index_data.empty


# Test StockReturn
@pytest.fixture
def sample_data():
    dates = pd.date_range(start="2022-01-01", periods=5, freq="D")
    data = {"AAPL": [150, 151, 152, 153, 154], "GOOGL": [2800, 2820, 2840, 2805, 2810]}
    return pd.DataFrame(data, index=dates)


@pytest.fixture
def stock_return(sample_data):
    return StockReturn(sample_data)


def test_calculate_portfolio_returns(stock_return):
    log_returns = stock_return.calculate_portfolio_returns()
    assert isinstance(log_returns, pd.Series)
    assert not log_returns.empty


def test_calculate_index_return(stock_return):
    index_returns = stock_return.calculate_index_return()
    assert isinstance(index_returns, pd.Series)
    assert not index_returns.empty


# Test StockMetricsCalculate
@pytest.fixture
def stock_metrics_calculator(sample_data):
    weights = [0.5, 0.5]
    log_return = np.log(sample_data / sample_data.shift(1)).dropna()
    index_return = pd.Series([0.01, 0.02, 0.03, 0.01, 0.02], index=log_return.index)
    risk_rate = 0.02
    return StockMetricsCalculate(weights, log_return, index_return, risk_rate)


def test_calculate_volatility_return(stock_metrics_calculator):
    volatility = stock_metrics_calculator.calculate_volatility_return(annualized=True)
    assert isinstance(volatility, str)
    assert float(volatility) > 0


def test_calculate_sharpe_ratio(stock_metrics_calculator):
    sharpe_ratio = stock_metrics_calculator.calculate_sharpe_ratio()
    assert isinstance(sharpe_ratio, str)
    assert float(sharpe_ratio) >= 0


def test_calculate_beta(stock_metrics_calculator):
    beta = stock_metrics_calculator.calculate_beta(annualized=True)
    assert isinstance(beta, str)
    assert float(beta) >= 0


def test_calculate_kurtosis(stock_metrics_calculator):
    kurtosis = stock_metrics_calculator.calculate_kurtosis()
    assert isinstance(kurtosis, str)
    assert float(kurtosis) >= 0


if __name__ == "__main__":
    pytest.main()
