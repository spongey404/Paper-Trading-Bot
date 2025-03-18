from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
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
        self.newsClient = NewsClient(api_key=API_KEY, secret_key=API_SECRET, )
        self.ticker = ticker

    def get_news(self, days_prior=3):
        startDate, endDate = self.get_news_dates(days_prior)
        newsParam = NewsRequest(symbols=self.ticker, start=startDate, end=endDate)
        news = self.newsClient.get_news(newsParam)
        newsDF = news.df
        usefulNews = [(row["headline"], row["summary"]) for index, row in newsDF.iterrows()]
        return usefulNews

    def get_news_dates(self, days_back=3):
        today = datetime.now()
        startDate = today - timedelta(days=days_back)
        return startDate.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

    
x = NewsSentimentAnalyser("NVDA")
print(x.get_news())
