from abc import ABC, abstractmethod

class AbstractStockDataProvider(ABC):
    @abstractmethod
    def download_stock_data(self):
        pass

    @abstractmethod
    def download_index_data(self):
        pass

class AbstractStockReturn(ABC):
    @abstractmethod
    def calculate_portfolio_returns(self):
        pass

    @abstractmethod
    def calculate_index_return(self):
        pass

class AbstractStockMetricsCalculate(ABC):
    @abstractmethod
    def calculate_volatility_return(self, annualized=True):
        pass

    @abstractmethod
    def calculate_sharpe_ratio(self):
        pass

    @abstractmethod
    def calculate_beta(self):
        pass

    @abstractmethod
    def calculate_kurtosis(self):
        pass

class AbstractStockMetricsResponse(ABC):
    @abstractmethod
    def formal_response(self, annualized=True):
        pass
