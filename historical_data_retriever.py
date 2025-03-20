import yfinance as yf
import pandas as pd

class DataRetriever:
    def __init__(self, period="60d", interval="15m"):
        self.period = period
        self.interval = interval

    def get_data(self, ticker):
        data = yf.download(ticker, period=self.period, interval=self.interval)
        data.dropna(inplace=True)
        return data
        
if __name__=="__main__":
    retriever = DataRetriever(period="3mo", interval="1d")
    data = retriever.get_data("AAPL")
    print(data)