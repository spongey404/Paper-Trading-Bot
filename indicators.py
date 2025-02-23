import ta
import pandas as pd
import ta.momentum
import ta.trend
class TechnicalIndicators:
    def __init__(self):
        pass

    def get_indicators(self, dataframe):
        closeSeries = dataframe['Close'].squeeze()
        # window_slow = longer EMA period, window_fast = shorter EMA period, window_sign = signal line period
        macd = ta.trend.MACD(close=closeSeries, window_slow=26, window_fast=12, window_sign=9, fillna=True)
        rsi = ta.momentum.RSIIndicator(close=closeSeries, window=14, fillna=True)
        sma = ta.trend.SMAIndicator(close=closeSeries, window=20, fillna=True)
        ema = ta.trend.EMAIndicator(close=closeSeries, window=20, fillna=True)

        dataframe['MACD'] = macd.macd()
        dataframe['MACD_Signal'] = macd.macd_signal()
        dataframe['MACD_Diff'] = macd.macd_diff()
        dataframe['RSI'] = rsi.rsi()
        dataframe['SMA20'] = sma.sma_indicator()
        dataframe['EMA20'] = ema.ema_indicator()

        return dataframe

if __name__ == '__main__':
    from historical_data_retriever import DataRetriever

    fetcher = DataRetriever(period='60d', interval='15m')
    data = fetcher.get_data('AAPL')
    
    calculator = TechnicalIndicators()
    data_with_indicators = calculator.get_indicators(data) 
    print(data_with_indicators)