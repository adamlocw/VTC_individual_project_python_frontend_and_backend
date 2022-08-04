import talib
import requests
import json
import pandas as pd
import datetime as dt
# import numpy
import pymongo
from sendEmail import sendEmail
from addRecordMACDBalance import addRecordMACDBalance
from datetime import datetime

url = 'https://api.binance.com/api/v3/klines'
symbol = 'ETHUSDT'
interval = '1d'
macdTradeLogUnitArray=[]

par = {'symbol': symbol, 'interval': interval, 'limit': 1000}
data = pd.DataFrame(json.loads(requests.get(url, params=par).text))
data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore']
data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.datetime]
data = data.astype(float)

macd, signal, hist = talib.MACD(data['close'], 12, 26, 9)

print(hist[-1])  # don't use
print(hist[-2])  # need
print(hist[-3])  # need

# Get the current MACD balance
# Mongodb connection
myclient = pymongo.MongoClient(
    "mongodb+srv://sysadmin:Nerv-19830228@cluster0.9wtze.mongodb.net/test")
# Select the database
mydb = myclient["VTC_individual_project"]
# Set up the collection
macdBalanceCol = mydb["macdBalance"]
macdTradeLogCol = mydb["macdTradeLog"]
# Init array
macdBalanceArray = []
# Get all Balance
for x in macdBalanceCol.find():
    macdBalanceArray.append(x['balance'])
# Get the latest Balance
latestMACDBalance = macdBalanceArray[-1]
currectCrypto = data['close'][-1]
cryptoUnit = latestMACDBalance/currectCrypto
cryptoUnit = round(cryptoUnit, 4)

for x in macdTradeLogCol.find():
    macdTradeLogUnitArray.append(x['unit'])
latestMacdTradeLogUnit = macdTradeLogUnitArray[-1]

print(latestMACDBalance)
print(currectCrypto)

if(hist[-2] > 0 and hist[-3] <= 0):
# if(True):
    # MACD golden cross and call buy crypto
    print('BUY')
    mydict = {"trade": "buy", "cryptoPrice": currectCrypto, "usdt": latestMACDBalance, "unit": cryptoUnit}
    x=macdTradeLogCol.insert_one(mydict)
    print (x.inserted_id)
    # Add record of MACD balance
    addRecordMACDBalance(latestMACDBalance)
    emailTo = "adamlocw@gmail.com"
    emailSubject = "ETH buy on Binace using MACD trigger (Mock)"
    emailBody = f"ETH (MACD 12 26 9) BUY on Binance right now by VTC individual project. {datetime.now()}"
    sendEmail(emailTo, emailSubject, emailBody)

if(hist[-2] < 0 and hist[-3] >= 0):
# if(True):
    # MACD die cross and call sell crypto
    print('SELL')
    latestMACDBalance = latestMacdTradeLogUnit * currectCrypto
    mydict = {"trade": "sell", "cryptoPrice": currectCrypto, "usdt": latestMACDBalance, "unit": cryptoUnit}
    x=macdTradeLogCol.insert_one(mydict)
    print (x.inserted_id)
    # Add record of MACD balance
    addRecordMACDBalance(latestMACDBalance)
    emailTo = "adamlocw@gmail.com"
    emailSubject = "ETH sell on Binace using MACD trigger (Mock)"
    emailBody = f"ETH (MACD 12 26 9) SELL on Binance right now by VTC individual project. {datetime.now()}"
    sendEmail(emailTo, emailSubject, emailBody)

# print(data)
