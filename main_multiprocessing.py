from stock_data import stockData
import datetime as dt
import pandas as pd
import concurrent.futures
import time

sp500 = pd.read_excel("SP500.xlsx")
tickers = sp500["Symbol"].tolist()

start = time.time()

def multiprocessing_run(ticker):

    my_ticker = stockData(ticker)
    st = dt.datetime(2015,3,1)
    et = dt.datetime(2022,3,15) 
    my_ticker.pull_data_and_push_data(st = st, et = et)


with concurrent.futures.ProcessPoolExecutor() as executor:
    if __name__ == '__main__':
        futures = [executor.submit(multiprocessing_run, ticker) for ticker in tickers]
        for future in concurrent.futures.as_completed(futures):
            data = future.result()

        end = time.time()
        print(end - start) 

