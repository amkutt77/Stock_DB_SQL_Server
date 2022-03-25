CREATE TABLE stock_price_data (
    ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    Ticker_ VARCHAR(255),
    Date_ Date,
    Open_ Float,
    High_ Float,
	Low_ Float,
	Close_ Float,
	Adj_Close_ Float,
	Volume_ Float
);