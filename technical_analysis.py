
class TechnicalAnalyser:
    def __init__(self):
        self.signals = {}

    def macd_analysis(self, data):
        macd = data["MACD"]
        macdSignal = data["MACD_Signal"]
        if macd > macdSignal:
            self.signals["MACD"] = "bullish"
        elif macd < macdSignal:
            self.signals["MACD"] = "bearish"
        else:
            self.signals["MACD"] = "neutral"

        if data["MACD_Hist"] > 0:
            self.signals["MACD_momentum"] = "up"
        else:
            self.signals["MACD_momentum"] = "down"
    

    def rsi_analysis(self, data):
        rsi = data["RSI"]
        if rsi < 30:
            self.signals["RSI"] = "oversold"
        elif rsi > 70:
            self.signals["RSI"] = "overbought"
        else:
            self.signals["RSI"] = "neutral"
    
    def moving_avg_analysis(self, data):
        close 

