:receipt: :bar_chart: :chart_with_upwards_trend: Generate common performance metrics to Portfolio.

## What Is Portfolio Management?
Portfolio management is the art and science of selecting and overseeing a group of investments that meet the long-term financial objectives and risk tolerance of a client, a company, or an institution.
[see https://www.investopedia.com/terms/p/portfoliomanagement.asp].


## Project
Given a data, this engine have a propols to be a engine to provide some metrics based on MPT (Modern Portfolio Theory).


## use
  

```

curl -i -X POST -H "Content-Type: application/json" -d '{
	"period": "5y",
	"tickers": ["UBER", "GOOGL", "MSFT"],
	"index": "^GSPC",
	"weights": [0.4, 0.4, 0.2],
	"risk_rate": 0
}' http://localhost:8000/v1/status

```

  

### Explanation

The service accept the parameters above, it will make some statiscal calculations around of the dataset called automaticly. For now, the service calculate the Volatility, Kurtosis, Shape Ratio and Beta coeficient.

  
## Response

The response from http call, should be something like:

```

{"volatility":"4.98","sharpe_ratio":"0.47","beta":"1.7539956706304167","kurtosis":"6.7"}

```