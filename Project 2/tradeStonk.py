####################################
# Name: Jeremy Marks               #
# Purpose: trades stocks real time #
####################################
import ta
import alpaca_trade_api as tradeapi
from text import send_text
from datetime import date

#authentication variables
api_key = 'MY_API_KEY_FOR_ALPACA'
api_secret = 'MY_API_SECRET_KEY_FOR_ALPAC'
base_url = 'https://paper-api.alpaca.markets'

#connects to api
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

#buys stock through api
def orderMarket(stock, shares=5):
    api.submit_order(
        symbol=stock,
        qty=shares,
        side='buy',
        type='market',
        time_in_force='gtc'
    )

#sells stock through api
def sellMarket(stock, shares = 5):
    api.submit_order(
        symbol=stock,
        qty=shares,
        side='sell',
        type='market',
        time_in_force='gtc',
    )

#variables
run = True
bought = False
currentRSI = 0
oversold = 30
overbought = 70
shares = 50

#gets current day and 2 days ago, since 2 days is needed for accurate rsi calculation
currentDay = str(date.today())
day = int(currentDay[-2:])
twoDaysAgo = currentDay[:-2]
twoDaysAgo = twoDaysAgo + str(day-2)

#Note this strategy does not actually work very well, made this mostly to just test if I could get buying and selling working with a strategy
while run:
    response = api.polygon.historic_agg_v2('AMD', 1, 'minute', _from=twoDaysAgo, to=currentDay, limit=None).df
    response.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'VWAP']
    rsiArr = (ta.momentum.RSIIndicator(response["Close"],14)).rsi()
    #checks if rsi has changed
    if rsiArr[-1] != currentRSI:
        currentRSI = rsiArr[-1]
        print("Rsi: ", round(currentRSI,2))
    #buys if rsi is under the oversold value and not already bought
    if currentRSI < oversold and not bought:
        bought = True
        orderMarket('AMD', shares)
        #texts me everytime it buys, uses text.py
        send_text('jeremy', 'Bought')
    #sells if rsi is over the oversold value and has shares to sell
    elif currentRSI > overbought and bought:
        bought = False
        sellMarket('AMD', shares)
        #texts me everytime it sells, uses text.py
        send_text('jeremy', 'Sold')