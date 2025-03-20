from historical_data_retriever import DataRetriever
from indicators import TechnicalIndicators
from technical_analysis import TechnicalAnalyser
from sentiment_analysis import NewsSentimentAnalyser
import pandas as pd

class TradingStrategy:
    def __init__(self, ticker, period="5d", interval="1h"):
        self.ticker = ticker
        self.period = period
        self.interval = interval

        self.dataRetriever = DataRetriever(period=self.period, interval=self.interval)
        self.indicatorCalc = TechnicalIndicators()
        self.technicalAnalysis = TechnicalAnalyser()
        self.sentimentAnalysis = NewsSentimentAnalyser(self.ticker)

        self.posSentimentThreshold = 0.2
        self.negSentimentThreshold = -0.2

    def run_analysis(self):
        histData = self.dataRetriever.get_data(self.ticker)
        indicatorData = self.indicatorCalc.get_indicators(histData)
        currentData = indicatorData.iloc[-1]

        techSignalsDict, techScore = self.technicalAnalysis.run_all_tech_analyses(current_data=currentData, historical_data=indicatorData)

        try:
            sentimentScore, confidence = self.sentimentAnalysis.get_sentiment()
        except Exception as e:
            print(f"Error calculating sentiment. It seems no news is available on Benzinga for {self.ticker}")
            sentimentScore, confidence = 0, 0
        
        combinedSignal = self.determine_signal(techScore, sentimentScore, confidence)

        result = {
            "ticker": self.ticker,
            "technical_signals": techSignalsDict,
            "technical_score": techScore,
            "sentiment_score": sentimentScore,
            "sentiment_confidence": confidence,
            "final_signal": combinedSignal
        }
        
        return result

    
    def determine_signal(self, tech_analysis_score, sent_analysis_score, sent_analysis_confidence):
        if sent_analysis_confidence < 0.6:
            techWeight, sentWeight = 0.9, 0.1
        else:
            techWeight, sentWeight = 0.7, 0.3

        # normalising technical analysis score since it can range from -8 to 8
        normalTechScore = tech_analysis_score / 8 

        combinedScore = (normalTechScore * techWeight) + (sent_analysis_score * sentWeight)

        if combinedScore > 0.4:
            return 1 # buy
        elif combinedScore < -0.4:
            return -1 # sell
        else:
            return 0 # hold


if __name__ == "__main__":
    strategy = TradingStrategy("NVDA", period="5d", interval="1h")
    analysis_result = strategy.run_analysis()

    print(f"Analysis for {analysis_result["ticker"]}")
    print(f"Technical Score: {analysis_result["technical_score"]:.2f}")
    print(f"Sentiment Score: {analysis_result["sentiment_score"]:.2f} (Confidence: {analysis_result["sentiment_confidence"]:.2f})")
    print(f"Final Signal: {analysis_result["final_signal"]}")
    print("\nTechnical Signals:")
    for key, value in analysis_result["technical_signals"].items():
        print(f"  {key}: {value}")