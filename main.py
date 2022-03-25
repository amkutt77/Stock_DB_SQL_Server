from stock_data import stockData
import datetime as dt
import pandas as pd

sp500 = pd.read_excel("SP500.xlsx")
tickers = sp500["Symbol"].tolist()

st = dt.datetime(2015,3,1)
et = dt.datetime(2022,3,15)

for ticker in tickers:
    my_ticker = stockData(ticker)
    my_ticker.pull_data_and_push_data(st = st, et = et)

