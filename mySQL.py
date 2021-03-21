##########################################
# Name: Jeremy Marks                     #
# Purpose: gets stock data from database #
##########################################
import datetime, pandas as pd
from sqlalchemy import create_engine

#connect to database
db_connection = create_engine('mysql+pymysql://MY_USERNAME:MY_PASSWORD@localhost/stocks')

#This was never used for actual backtesting, I found csv files were much faster to retrieve from so I used them for the testing
startTime = datetime.datetime.now()
#creates pandas dataframe with all the given stock symbol
df = pd.read_sql("SELECT * FROM stocks.stockdata USE INDEX (symbol) where symbol = 'STOCK_SYMBOL'", con=db_connection)
print("Query Took:", datetime.datetime.now()-startTime)