from alpaca_trade_api import REST
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
ALPACA_URL = os.getenv("ALPACA_ENDPOINT")

# ticker must be entered all caps
class NewsSentimentAnalyser:
    def __init__(self, ticker):
        self.api = REST(key_id=API_KEY, secret_key=API_SECRET, base_url=ALPACA_URL)
        self.ticker = ticker

    def get_news(self, days_prior=3):
        startDate, endDate = self.get_news_dates(days_prior)
        news = self.api.get_news(symbol=self.ticker, start=startDate, end=endDate)
        news = [(ev.headline, ev.summary) for ev in news]
        return news

    def get_news_dates(self, days_back=3):
        today = datetime.now()
        startDate = today - timedelta(days=days_back)
        return startDate.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

    
x = NewsSentimentAnalyser("GME")
print(x.get_news())
