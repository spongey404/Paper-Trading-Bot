from datetime import datetime, timedelta

def get_news_dates(self, days_back=3):
    today = datetime.now()
    endDate = today - timedelta(days=days_back)
    return today.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d")

print(get_news_dates(3))