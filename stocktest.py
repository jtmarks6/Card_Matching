####################################################
# Name: Jeremy Marks                               #
# Purpose: backtest a strategy with the historical #
#   csv file from stocksToDatebaseCSV.py           #
####################################################
import alpaca_trade_api as tradeapi
import pandas as pd
import datetime, time, threading, ta, csv, json

#authentication variables
api_key = 'MY_API_KEY_FOR_ALPACA'
api_secret = 'MY_API_SECRET_KEY_FOR_ALPAC'
base_url = 'https://paper-api.alpaca.markets'

#connects to api
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

#variables for dates
monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
monthName = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#calculates rsi from csv and makes a stockrsi.csv file
def calcRSIforCSV(stock):
    readFile = pd.read_csv(stock+'.csv', sep=",") #Reads CSV
    rsiA= ta.momentum.RSIIndicator(readFile["close"], 14)
    rsiArr = rsiA.rsi()
    readFile["RSI"] = rsiArr
    rsi = pd.DataFrame(columns = ['Date', 'Close', 'RSI'])
    rsi["RSI"] = rsiArr
    rsi["Close"] = readFile["close"]
    rsi['Date'] = readFile["timestamp"]
    rsi.index.names = [stock]
    rsi.to_csv(stock+"rsi.csv", index=True, header=True, mode='w')

#checks all rsi of CSV file to calculate when would have bought and sold
def checkCSVBuySell(stock):
    oversold = 49 #buy when under this
    overbought = 50 #sell when over this
    readFile = pd.read_csv(stock+'rsi.csv', engine='c') #Reads CSV    
    bought = False
    avgPosPrice = 0
    shares = 1
    capital = 5000 #starts with $5000 to trade
    totalProfit = 0 #keep track of profit made
    resultsLink = 'results.txt'
    resultFile = open(resultsLink, "w")
    #loops through every minute of the file and tests if would have bought or sold
    for minute in range(len(readFile)):
        close = readFile["Close"][minute]
        rsi = readFile["RSI"][minute]
        date = readFile["Date"][minute]
        if bought:
            profit = round(shares*(close - avgPosPrice) , 2)
        if rsi < oversold and not bought: #buy sell rsi
            resultFile.write(str(date) + " Bought " + str(close) + "\n")
            bought = True
            avgPosPrice = close
            shares = round(capital/close, 0)
        elif rsi > overbought and bought:
            resultFile.write(str(date) + " Sold " + str(close) + "\n")
            totalProfit += profit
            #capital += profit #uncomment for profits being reinvested
            totalProfit = round(totalProfit,2)
            resultFile.write("Profit: " + str(profit) + "\n")
            resultFile.write("Total: " + str(round(totalProfit,2)) + "\n\n")
            bought = False
    resultFile.close()
    return totalProfit

#created stockrsi.csv
calcRSIforCSV('AMD')
#reads stockrsi.csv and calculates what profit would have been with strategy
checkCSVBuySell('AMD')