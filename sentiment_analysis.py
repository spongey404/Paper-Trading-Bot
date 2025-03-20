from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device_int = 0 if torch.cuda.is_available() else -1

load_dotenv()
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
ALPACA_URL = os.getenv("ALPACA_ENDPOINT")


# ticker must be entered all caps
class NewsSentimentAnalyser:
    def __init__(self, ticker):
        self.newsClient = NewsClient(api_key=API_KEY, secret_key=API_SECRET)
        self.ticker = ticker

        self.pipe = pipeline("text-classification", model="ProsusAI/finbert", device=device_int)
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)

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
    
    def get_sentiment(self):
        newsList = self.get_news()

        if not newsList:
            return ()

        texts = [f"{headline}: {summary}" for headline, summary in newsList]

        results = self.pipe(inputs=texts) # 4gb vram
        
        sentimentNum = {
            "negative": -1,
            "neutral": 0,
            "positive": 1
        }

        weightedTotalSentiment = 0
        confidenceTotal = 0

        for article in results:
            weightedTotalSentiment += sentimentNum[article["label"]] * article["score"]
            confidenceTotal += article["score"]

        # <-0.4 means negative, >0.4 means positive, in between means neutral?
        return weightedTotalSentiment/len(results), confidenceTotal/len(results)


x = NewsSentimentAnalyser("NVDA")
print(x.get_sentiment())
