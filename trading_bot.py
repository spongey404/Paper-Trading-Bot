from dotenv import load_dotenv
import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from trading_strategy import TradingStrategy

class TradingBot:
    def __init__(self, ticker):
        load_dotenv()
        self.API_KEY = os.getenv("ALPACA_API_KEY")
        self.API_SECRET = os.getenv("ALPACA_SECRET_KEY")

        self.ticker = ticker

        self.tradingClient = TradingClient(api_key=self.API_KEY, secret_key=self.API_SECRET, paper=True)

        self.strategy = TradingStrategy(ticker=self.ticker)

    def get_account_info(self):
        account = self.tradingClient.get_account()
        return dict(account)
    
    def get_position(self):
        try:
            position = self.tradingClient.get_open_position(self.ticker)
            return position
        except Exception as e:
            return None
        
    def get_trade_signal(self):
        analysisResult = self.strategy.run_analysis()
        finalSignal = analysisResult["final_signal"]
        return analysisResult, finalSignal
    
    def place_order(self, signal, qty=10):
        if signal == 1: # buy
            order = OrderSide.BUY
        elif signal == -1: # sell
            order = OrderSide.SELL
        else:
            print("Trade signal indicates to hold. No order was placed")
            return None

        marketOrder = MarketOrderRequest(symbol=self.ticker, qty=qty, side=order, time_in_force=TimeInForce.DAY)
        return marketOrder

    def run_bot(self):
        analysisResult, tradeSignalInt = self.get_trade_signal()
        order = self.place_order(tradeSignalInt)
        self.tradingClient.submit_order(order_data=order)
        position = self.get_position()

        return {
            'analysis': analysisResult,
            'position': position,
            'order': order
        }


if __name__ == "__main__":
    x = TradingBot("CRSP")
    # analysisResult, tradeSignalInt = x.get_trade_signal()
    # print(analysisResult, tradeSignalInt)
    # print(f"current {x.ticker} position: {x.get_position()}")
    # order = x.place_order(1)
    # x.tradingClient.submit_order(order_data=order)
    # print(f"current {x.ticker} position: {x.get_position()}")

    # analysisResult, tradeSignalInt = x.get_trade_signal()
    # print(analysisResult, tradeSignalInt)

    print(f"current {x.ticker} position: {x.get_position()}\n")
    x.run_bot()
    print(f"current {x.ticker} position: {x.get_position()}")

