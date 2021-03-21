########################################
# Name: Jeremy Marks                   #
# Purpose: download and input stock    #
#   prices to local mySQL database     #
########################################
import alpaca_trade_api as tradeapi
from sqlalchemy import create_engine

#connects to my local mySQL database
engine = create_engine('mysql+pymysql://MY_USERNAME:MY_PASSWORD@localhost/stocks')

api_key = 'MY_API_KEY_FOR_ALPACA'
api_secret = 'MY_API_SECRET_KEY_FOR_ALPAC'
base_url = 'https://paper-api.alpaca.markets'

#connects to alpaca api
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

def toDatabase(stock):
    #list of dates to get, adds up to every day in the year
    dates = [
        ['-01-01','-05-30'],
        ['-06-01','-10-31'],
        ['-11-01','-12-31']
    ]
    #gets just headers to write to csv and clears file if had previous info
    historicalData = api.polygon.historic_agg_v2(stock, multiplier = 1, timespan ='minute', _from='2004-01-01', to='2004-01-01').df
    historicalData.to_csv(path_or_buf=r'Stock_CSV/'+stock+'.csv', header=True, mode='w')

    #loops through year
    for year in range(2004,2021+1):
        for i in range(3):
            #gets historical prices from api in dateframe format
            df = api.polygon.historic_agg_v2(stock, multiplier = 1, timespan ='minute', _from=str(year)+dates[i][0], to=str(year)+dates[i][1], limit=300000).df
            df = df.drop(columns = ["vwap"])
            df['symbol'] = stock
            #saves to csv with append to file mode
            df.to_csv(path_or_buf=r'Stock_CSV/'+stock+'.csv', header=False, mode='a')
            #df.to_sql('stockdata', con = engine, if_exists='append')   #adds to database, but I started using csv instead of database for majority of things
    print("Input", stock, "to database\n")

#list of all stocks to add
stockList = [
    'AAL',
    'AAPL',
    'ACST',
    'ADMP',
    'AEZS',
    'AGTC',
    'AIKI',
    'ALRN',
    'AMD',
    'APA',
    'APHA',
    'AREC',
    'ARTL',
    'ATHX',
    'ATOS',
    'AVGR',
    'AZN',
    'AZRX',
    'BBBY',
    'BCRX',
    'BIOL',
    'BLNK',
    'BNGO',
    'BRQS',
    'CDEV',
    'CGNT',
    'CIDM',
    'CLOV',
    'CMCSA',
    'CRBP',
    'CRON',
    'CSCO',
    'CTRM',
    'DISCA',
    'DKNG',
    'DRRX',
    'DVAX',
    'FB',
    'FCEL',
    'GEVO',
    'GHSI',
    'GNUS',
    'GSM',
    'HBAN',
    'HOL',
    'IDEX',
    'IMVT',
    'INO',
    'INTC',
    'IQ',
    'JAGX',
    'JD',
    'KOPN',
    'LI',
    'LIZI',
    'LLNW',
    'MARA',
    'MBRX',
    'MRNA',
    'MSFT',
    'MU',
    'MVIS',
    'NAKD',
    'NMTR',
    'NNDM',
    'OCGN',
    'OGI',
    'ONTX',
    'OPK',
    'PHUN',
    'PLUG',
    'RIOT',
    'SAVA',
    'SHIP',
    'SHLS',
    'SIRI',
    'SLM',
    'SLS',
    'SNDL',
    'SOLO',
    'SPWR',
    'SRNE',
    'TELL',
    'TIGR',
    'TLRY',
    'TNXP',
    'TRCH',
    'TSLA',
    'TTOO',
    'TXMD',
    'UAL',
    'VBIV',
    'VIAC',
    'VTRS',
    'VTVT',
    'VXRT',
    'VYNE',
    'WKHS',
    'XSPA',
    'ZNGA']    

#main function
for stocks in stockList:
    toDatabase(stocks)