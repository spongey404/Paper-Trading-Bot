import pandas as pd
class TechnicalAnalyser:
    def __init__(self):
        self.signals = {}
        self.score = 0

    def _series_to_scalar(self, data):
        return float(data)

    def macd_analysis(self, data):
        macd = self._series_to_scalar(data["MACD"])
        macdSignal = self._series_to_scalar(data["MACD_Signal"])
        macdHist = self._series_to_scalar(data["MACD_Hist"])

        if macd > macdSignal:
            self.signals["MACD"] = "bullish"
            self.score += 1
        elif macd < macdSignal:
            self.signals["MACD"] = "bearish"
            self.score -= 1
        else:
            self.signals["MACD"] = "neutral"

        if macdHist > 0:
            self.signals["MACD_momentum"] = "up"
            self.score += 0.5
        else:
            self.signals["MACD_momentum"] = "down"
            self.score -= 0.5
    

    def rsi_analysis(self, data):
        rsi = self._series_to_scalar(data["RSI"])

        if rsi < 30:
            self.signals["RSI"] = "oversold"
            self.score += 1
        elif rsi > 70:
            self.signals["RSI"] = "overbought"
            self.score -= 1
        else:
            self.signals["RSI"] = "neutral"
    
    def moving_avg_analysis(self, data):
        close = self._series_to_scalar(data["Close"])
        sma20 = self._series_to_scalar(data["SMA20"])
        ema20 = self._series_to_scalar(data["EMA20"])
        sma50 = self._series_to_scalar(data["SMA50"])
        sma200 = self._series_to_scalar(data["SMA200"])

        # SMA20 for short term trend
        if close > sma20:
            self.signals["SMA20"] = "bullish"
            self.score += 0.5
        else:
            self.signals["SMA20"] = "bearish"
            self.score -= 0.5
            
        # EMA20 for recent price changes
        if close > ema20:
            self.signals["EMA20"] = "bullish"
            self.score += 0.5
        else:
            self.signals["EMA20"] = "bearish"
            self.score -= 0.5
            
        # SMA50 for medium term trend
        if close > sma50:
            self.signals["SMA50"] = "bullish"
            self.score += 0.75
        else:
            self.signals["SMA50"] = "bearish"
            self.score -= 0.75
            
        # SMA200 for long term trend
        if close > sma200:
            self.signals["SMA200"] = "bullish"
            self.score += 1
        else:
            self.signals["SMA200"] = "bearish"
            self.score -= 1
            
        # golden cross
        if sma50 > sma200:
            self.signals["MA_Cross"] = "golden_cross"  # bullish long term
            self.score += 1.5
        else:
            self.signals["MA_Cross"] = "death_cross"  # bearish long term
            self.score -= 1.5
    
    def bollinger_bands_analysis(self, data):
        # less decisive signal
        close = self._series_to_scalar(data["Close"])
        upper = self._series_to_scalar(data["BB_Upper"])
        lower = self._series_to_scalar(data["BB_Lower"])
        middle = self._series_to_scalar(data["BB_Middle"])
        
        bandWidth = upper - lower
        if bandWidth == 0: # for divide by 0 error
            upperDist = 0
            lowerDist = 0
        else:
            upperDist = (upper - close) / bandWidth * 2
            lowerDist = (close - lower) / bandWidth * 2
        
        if upperDist < 0.1:  # close to upper
            self.signals["BB"] = "near_upper"
            self.score -= 0.5
        elif lowerDist < 0.1:  # close to lower
            self.signals["BB"] = "near_lower"
            self.score += 0.5
        elif close > middle:
            self.signals["BB"] = "above_middle"
            self.score += 0.25
        elif close < middle:
            self.signals["BB"] = "below_middle"
            self.score -= 0.25
        else:
            self.signals["BB"] = "at_middle"
    
    def stochastic_analysis(self, current_data):
        # less decisive signal
        k = self._series_to_scalar(current_data["Stoch_K"])
        d = self._series_to_scalar(current_data["Stoch_D"])
        
        if k < 20:
            self.signals["Stochastic"] = "oversold"
            self.score += 0.75
        elif k > 80:
            self.signals["Stochastic"] = "overbought"
            self.score -= 0.75
        else:
            self.signals["Stochastic"] = "neutral"
            
        # K crossing D
        # need to add rolling window analysis
        if k > d:
            self.signals["Stochastic_cross"] = "bullish"
            self.score += 0.5
        else:
            self.signals["Stochastic_cross"] = "bearish"
            self.score -= 0.5
    
    def calculate_overall_score(self):
        # -8 to 8
        
        if self.score > 3:
            self.signals["overall"] = "strongly_bullish"
        elif self.score > 1:
            self.signals["overall"] = "bullish"
        elif self.score < -3:
            self.signals["overall"] = "strongly_bearish"
        elif self.score < -1:
            self.signals["overall"] = "bearish"
        else:
            self.signals["overall"] = "neutral"
            
        
    def analyse_trend(self, historical_data, period=5): # last 5 days by default
        recent_closes = historical_data["Close"].iloc[-period:].squeeze() # turns df to series
        if recent_closes.is_monotonic_increasing:
            self.signals["recent_trend"] = "uptrend"
            self.score += 1
        elif recent_closes.is_monotonic_decreasing:
            self.signals["recent_trend"] = "downtrend"
            self.score -= 1
        else:
            self.signals["recent_trend"] = "sideways"

    def run_all_analyses(self, current_data, historical_data):
        self.macd_analysis(current_data)
        self.rsi_analysis(current_data)
        self.moving_avg_analysis(current_data)
        self.bollinger_bands_analysis(current_data)
        self.stochastic_analysis(current_data)
        self.analyse_trend(historical_data)
        self.calculate_overall_score()
        return self.signals, self.score
    
if __name__ == "__main__":
    from historical_data_retriever import DataRetriever
    from indicators import TechnicalIndicators

    fetcher = DataRetriever(period="1mo", interval="15m")
    historicalData = fetcher.get_data("XHLD")
    
    calculator = TechnicalIndicators()
    indicatorData = calculator.get_indicators(historicalData) 
    print(indicatorData)

    currentData = indicatorData.iloc[-1]
    print(currentData["MACD"])

    analyser = TechnicalAnalyser()
    signals, score = analyser.run_all_analyses(currentData, indicatorData)

    print("Technical Analysis Signals:")
    for key, value in signals.items():
        print(f"{key}: {value}")
    print(f"Overall Score: {score}")