import yfinance as yf
import pandas as pd
import pyodbc
import secrets

class stockData():

    def __init__(self, ticker):
        
        self.ticker = ticker
        conn_string = f"Driver={secrets.DRIVER};Server={secrets.SERVER};Database={secrets.DATABASE};Trusted_Connection={secrets.TRUSTED_CONNECTION};" 
        self.conn = pyodbc.connect(conn_string)
        self.cursor = self.conn.cursor()

    def get_stock_data(self,st, et):

        self.data = yf.download(self.ticker, st, et)
        # replace NaN values with None so that it can be inserted into db
        self.data = self.data.where(self.data.notnull(), None) # Uses df value when condition is met, otherwise uses None
        self.data = self.data.reset_index()

        # add the ticker to the data dataframe
        idx = 0
        values = pd.Series([self.ticker for x in range(len(self.data.index))])
        self.data.insert(loc = idx, column = "Ticker", value = values)
        return self.data

    def column_check(self, d):
        '''Make sure the data matches the format needed for db'''
        data_cols = list(d.columns)
        required_cols = ["Ticker","Date","Open","High","Low","Close","Adj Close","Volume"]

        if not data_cols == required_cols:
            raise Exception("This data table is not suitable to be pushed.")

    def insert_price_data(self, d):
        '''pass in dataframe to be inserted into db'''

        check = self.column_check(d)
        print(f"Insert data for {self.ticker}...")
        
        sql = "INSERT INTO dbo.stock_price_data(Ticker_, Date_, Open_, High_, Low_, Close_, Adj_Close_, Volume_) VALUES (?,?,?,?,?,?,?,?);"
        params = []
        for index, row in d.iterrows():

            # we replaced NaN with None, and you can't round a None value. So if it errors our, just prep as is
            try:
                value = (row["Ticker"],row["Date"],round(row["Open"],2),round(row["High"],2),round(row["Low"],2),round(row["Close"],2),round(row["Adj Close"],2),round(row["Volume"],2))
            except:
                value = (row["Ticker"],row["Date"],row["Open"],row["High"],row["Low"],row["Close"],row["Adj Close"],row["Volume"])

            params.append(value)

        self.cursor.fast_executemany = True
        self.cursor.executemany(sql, params)
        self.conn.commit()

    def read_price_data_for_ticker(self):

        sql = f"SELECT * FROM dbo.stock_price_data WHERE Ticker_ = '{self.ticker}';"
        self.cursor.execute(sql)
        for row in self.cursor:
            print(f"row = {row}")

    def read_all_data(self):
        sql = f"SELECT * FROM dbo.stock_price_data;"
        self.cursor.execute(sql)
        for row in self.cursor:
            print(f"row = {row}")

    def table_cleanup(self):
        # delete duplicates by ticker and date. We only want daily data, so there should not be >1 date of data for each ticker
        sql = f'''WITH CTE AS (
                SELECT 
                    *,
                    RN = ROW_NUMBER() OVER (PARTITION BY Ticker_, Date_ ORDER BY ID Desc)
                FROM
                    dbo.stock_price_data
                )
                DELETE FROM CTE WHERE RN > 1;

            '''

        self.cursor.execute(sql)
        self.conn.commit()

    def pull_data_and_push_data(self, st, et):

        data = self.get_stock_data(st, et)
        self.insert_price_data(data)
            



    

        
    