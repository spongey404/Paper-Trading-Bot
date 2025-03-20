import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.volatility import BollingerBands, AverageTrueRange
class TechnicalIndicators:
    def __init__(self):
        pass

    def get_indicators(self, data):
        IndicatorDF = data.copy()

        closeSeries = data['Close'].squeeze() # turns df to series
        highSeries = data['High'].squeeze()
        lowSeries = data['Low'].squeeze()
        
        # trend indicators
        macd = MACD(close=closeSeries, window_slow=26, window_fast=12, window_sign=9)
        sma20 = SMAIndicator(close=closeSeries, window=20)
        ema20 = EMAIndicator(close=closeSeries, window=20)
        sma50 = SMAIndicator(close=closeSeries, window=50)
        sma200 = SMAIndicator(close=closeSeries, window=200)
        
        # momentum indicators
        rsi = RSIIndicator(close=closeSeries, window=14)
        stoch = StochasticOscillator(high=highSeries, low=lowSeries, close=closeSeries, window=14)
        
        # volatility indicators
        bb = BollingerBands(close=closeSeries, window=20, window_dev=2)
        atr = AverageTrueRange(high=highSeries, low=lowSeries, close=closeSeries, window=14        )
        
        
        IndicatorDF['MACD'] = macd.macd()
        IndicatorDF['MACD_Signal'] = macd.macd_signal()
        IndicatorDF['MACD_Hist'] = macd.macd_diff()
        IndicatorDF['RSI'] = rsi.rsi()
        IndicatorDF['SMA20'] = sma20.sma_indicator()
        IndicatorDF['EMA20'] = ema20.ema_indicator()
        IndicatorDF['SMA50'] = sma50.sma_indicator()
        IndicatorDF['SMA200'] = sma200.sma_indicator()
        IndicatorDF['Stoch_K'] = stoch.stoch()
        IndicatorDF['Stoch_D'] = stoch.stoch_signal()
        IndicatorDF['BB_Upper'] = bb.bollinger_hband()
        IndicatorDF['BB_Middle'] = bb.bollinger_mavg()
        IndicatorDF['BB_Lower'] = bb.bollinger_lband()
        IndicatorDF['ATR'] = atr.average_true_range()
        
        return IndicatorDF

if __name__ == "__main__":
    from historical_data_retriever import DataRetriever

    fetcher = DataRetriever(period="1mo", interval="15m")
    data = fetcher.get_data("AAPL")
    
    calculator = TechnicalIndicators()
    data_with_indicators = calculator.get_indicators(data) 
    print(data_with_indicators)