# Stock_DB_SQL_Server
Use multiprocessing to pull down daily stock price data and insert it into a SQL Server DB

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the below needed packages.

```bash
pip install pandas
```
```bash
pip install yfinance
```
```bash
pip install pyodbc
```

## Usage

First, I created a database in SQL Server called dbo.stock_price_data.  Then, using my stockData class, I can take a list of tickers, define a time period to 
pull daily price data, pull down the data with the Yahoo Finance API (yFinance), and then push it to my SQL Server DB using the pyodbc package. In this case, 
the tickers are saved down in an Excel file containing the ~500 Yahoo Finance tickers for the SP500. 

The interesting part about this script is how much faster it is to use multiprocessing vs standard processing.

### Standard Processing


This script below is the main.py file where I loop one at a time through each ticker.

```python
from stock_data import stockData
import datetime as dt
import pandas as pd

# Yahoo stock tickers
sp500 = pd.read_excel("SP500.xlsx")
tickers = sp500["Symbol"].tolist()

# Timeframe: start time and end time
st = dt.datetime(2015,3,1)
et = dt.datetime(2022,3,15)

# loop through list of tickers, initialize stockData class, pull down data and push data to db
for ticker in tickers:
    my_ticker = stockData(ticker)
    my_ticker.pull_data_and_push_data(st = st, et = et)
```

### Multiprocessing

Running through 500 tickers and pulling data for a long period one at a time can take a while. A faster approach to this is through using multiprocessing.
Instead of running through each ticker one at a time, I pull down and push data asynchronously by splitting it up among different processes. 
Normally, Python will run a script synchronously using one processor. Multiprocessing allows the computer to utilize multiple processors concurrently so that instead
I can pull and push data for multiple tickers at once.

```python
from stock_data import stockData
import datetime as dt
import pandas as pd
import concurrent.futures
import time

# Yahoo stock tickers
sp500 = pd.read_excel("SP500.xlsx")
tickers = sp500["Symbol"].tolist()

# Set up outer function
def multiprocessing_run(ticker):

    my_ticker = stockData(ticker)
    st = dt.datetime(2015,3,1)
    et = dt.datetime(2022,3,15) 
    my_ticker.pull_data_and_push_data(st = st, et = et)

# set up Process Pool Executor for multiprocessing
with concurrent.futures.ProcessPoolExecutor() as executor:
    if __name__ == '__main__':
        futures = [executor.submit(multiprocessing_run, ticker) for ticker in tickers]
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
```

## Results

When running a test on just 50 tickers over a seven year period, standard processing took 23 seconds to run. With multiprocessing, it took 7 seconds. 
This is a 70% decrease in execution time. 
