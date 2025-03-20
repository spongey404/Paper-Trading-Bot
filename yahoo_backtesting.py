from lumibot.strategies.strategy import Strategy
from lumibot.backtesting import YahooDataBacktesting
from sentiment_analysis import NewsSentimentAnalyser

class SentimentStrategyTest(Strategy):
    def __init__(self, ticker):
        self.ticker = ticker
        self.sentimentAnalyser = NewsSentimentAnalyser(self.ticker)
