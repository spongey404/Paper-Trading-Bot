from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
# parameters = API-key, Secret-key
tradingClient = TradingClient("", "", paper=True) 

account = tradingClient.get_account()

print(account.account_number)