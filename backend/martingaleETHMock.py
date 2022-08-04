import requests
import json
import pandas as pd
import datetime as dt
import pymongo
from sendEmail import sendEmail
from addRecordMartingaleBalance import addRecordMartingaleBalance
from datetime import datetime

url = 'https://api.binance.com/api/v3/klines'
symbol = 'ETHUSDT'
interval = '1h'

tradeStatNumber = -1
startPrice = 0.0
purchasedPriceLV = [0.0, 0.0, 0.0, 0.0, 0.0]
averagePriceLV = [0.0, 0.0, 0.0, 0.0, 0.0]
dropLV1 = 1 - (4 / 100)
dropLV2 = 1 - (12 / 100)
dropLV3 = 1 - (28 / 100)
dropLV4 = 1 - (60 / 100)
dropLV = [0.0, dropLV1, dropLV2, dropLV3, dropLV4]
upLV0 = 1 + (1 / 100)
upLV1 = 1 + (5 / 100)
upLV2 = 1 + (10 / 100)
upLV3 = 1 + (20 / 100)
upLV4 = 1 + (40 / 100)
upLV = [upLV0, upLV1, upLV2, upLV3, upLV4]
shareLV0 = 1
shareLV1 = 4
shareLV2 = 16
shareLV3 = 64
shareLV4 = 256
totalShare = shareLV0 + shareLV1 + shareLV2 + shareLV3 + shareLV4
shareLV = [shareLV0, shareLV1, shareLV2, shareLV3, shareLV4]
minUSD = 10
orderVolumeLV = [0.0, 0.0, 0.0, 0.0, 0.0]
historyPriceLV = [0.0, 0.0, 0.0, 0.0, 0.0]
historyOrderVolumeLV = [0.0, 0.0, 0.0, 0.0, 0.0]
readyForBuyorSell = ""  # text "buy" or "sell" only
martingaleTradeArray = []
martingaleBalanceArray = []
averagePriceLVArray = []
dropLVArray = []
orderVolumeLVArray = []
purchasedPriceLVArray = []
shareLVArray = []
upLVArray = []
historyOrderVolumeLVArray = []
historyPriceLVArray = []
startPriceArray=[]


par = {'symbol': symbol, 'interval': interval, 'limit': 1000}
data = pd.DataFrame(json.loads(requests.get(url, params=par).text))
data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore']
data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.datetime]
data = data.astype(float)

currentPrice = data['close'][-1]
print("martingale is started. ")
print(currentPrice)


myclient = pymongo.MongoClient(
    "mongodb+srv://sysadmin:Nerv-19830228@cluster0.9wtze.mongodb.net/test")
# Select the database
mydb = myclient["VTC_individual_project"]
# Set up the collection
martingaleTradeLogCol = mydb["martingaleTradeLog"]
martingaleBalanceCol = mydb["martingaleBalance"]
for x in martingaleTradeLogCol.find():
    martingaleTradeArray.append(x['tradeStatNumber'])
    averagePriceLVArray.append(x['averagePriceLV'])
    dropLVArray.append(x['dropLV'])
    orderVolumeLVArray.append(x['orderVolumeLV'])
    purchasedPriceLVArray.append(x['purchasedPriceLV'])
    shareLVArray.append(x['shareLV'])
    upLVArray.append(x['upLV'])
    historyOrderVolumeLVArray.append(x['historyOrderVolumeLV'])
    historyPriceLVArray.append(x['historyPriceLV'])
    startPriceArray.append(x['startPrice'])
# Get the latest Trade Stat Number
latestTradeStatNumber = martingaleTradeArray[-1]
# Get all Balance
for x in martingaleBalanceCol.find():
    martingaleBalanceArray.append(x['balance'])
# Get the latest Balance
latestMartingaleBalance = martingaleBalanceArray[-1]

print(latestTradeStatNumber)

if latestTradeStatNumber == -1:
    print("buy round 1")
    # Set the detailed level of purchasedPrice
    startPrice = currentPrice
    purchasedPriceLV[0] = currentPrice
    purchasedPriceLV[1] = currentPrice * dropLV[1]
    purchasedPriceLV[2] = currentPrice * dropLV[2]
    purchasedPriceLV[3] = currentPrice * dropLV[3]
    purchasedPriceLV[4] = currentPrice * dropLV[4]
    # Set the detailed level of averagePrice
    averagePriceLV[0] = currentPrice
    averagePriceLV[1] = (purchasedPriceLV[0] + shareLV[1]
                         * purchasedPriceLV[1]) / (shareLV[0] + shareLV[1])
    averagePriceLV[2] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2]) / (shareLV[0] + shareLV[1] + shareLV[2])
    averagePriceLV[3] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] + shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3]) / (shareLV[0] + shareLV[1] + shareLV[2] + shareLV[3])
    averagePriceLV[4] = (purchasedPriceLV[0] +
                         shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3] +
                         shareLV[4] * purchasedPriceLV[4]) / totalShare
    # Set USDT until
    minUSD = latestMartingaleBalance / totalShare
    minUSD = round(minUSD, 4)
    # Set the detailed level of Order Volume
    orderVolumeLV[0] = round(shareLV[0] * minUSD / averagePriceLV[0], 4)
    orderVolumeLV[1] = round(shareLV[1] * minUSD / averagePriceLV[1], 4)
    orderVolumeLV[2] = round(shareLV[2] * minUSD / averagePriceLV[2], 4)
    orderVolumeLV[3] = round(shareLV[3] * minUSD / averagePriceLV[3], 4)
    orderVolumeLV[4] = round(shareLV[4] * minUSD / averagePriceLV[4], 4)
    # Buy and add record level 0 of order volume in mock
    tradeStatNumber = latestTradeStatNumber + 1
    mydict = {"tradeStatNumber": tradeStatNumber,
              "averagePriceLV": averagePriceLV,
              "dropLV": dropLV,
              "orderVolumeLV": orderVolumeLV,
              "purchasedPriceLV": purchasedPriceLV,
              "shareLV": shareLV,
              "upLV": upLV,
              "startPrice": startPrice,
              "totalShare": totalShare,
              "historyPriceLV": [currentPrice, 0.0, 0.0, 0.0, 0.0],
              "historyOrderVolumeLV": [orderVolumeLVArray[-1][0], 0.0, 0.0, 0.0, 0.0]}
    x = martingaleTradeLogCol.insert_one(mydict)
    print(x.inserted_id)

# Sell all on level 0 (round 1) during the price is going up
if latestTradeStatNumber == 0 and currentPrice / purchasedPriceLVArray[-1][0] > upLVArray[-1][0]:
    # if True:
    # Calculate the USDT after sell all on level 0
    # ETH to USDT
    tradeResult = currentPrice*orderVolumeLVArray[-1][0]
    # Remaining USDT
    remainingUSDT = latestMartingaleBalance/totalShare*(totalShare-1)
    newBalance = tradeResult+remainingUSDT
    addRecordMartingaleBalance(newBalance)
    #Buy the level 0 after sell immediately
    # Set the detailed level of purchasedPrice
    startPrice = currentPrice
    purchasedPriceLV[0] = currentPrice
    purchasedPriceLV[1] = currentPrice * dropLV[1]
    purchasedPriceLV[2] = currentPrice * dropLV[2]
    purchasedPriceLV[3] = currentPrice * dropLV[3]
    purchasedPriceLV[4] = currentPrice * dropLV[4]
    # Set the detailed level of averagePrice
    averagePriceLV[0] = currentPrice
    averagePriceLV[1] = (purchasedPriceLV[0] + shareLV[1]
                         * purchasedPriceLV[1]) / (shareLV[0] + shareLV[1])
    averagePriceLV[2] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2]) / (shareLV[0] + shareLV[1] + shareLV[2])
    averagePriceLV[3] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] + shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3]) / (shareLV[0] + shareLV[1] + shareLV[2] + shareLV[3])
    averagePriceLV[4] = (purchasedPriceLV[0] +
                         shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3] +
                         shareLV[4] * purchasedPriceLV[4]) / totalShare
    # Set USDT until
    minUSD = latestMartingaleBalance / totalShare
    minUSD = round(minUSD, 4)
    # Set the detailed level of Order Volume
    orderVolumeLV[0] = round(shareLV[0] * minUSD / averagePriceLV[0], 4)
    orderVolumeLV[1] = round(shareLV[1] * minUSD / averagePriceLV[1], 4)
    orderVolumeLV[2] = round(shareLV[2] * minUSD / averagePriceLV[2], 4)
    orderVolumeLV[3] = round(shareLV[3] * minUSD / averagePriceLV[3], 4)
    orderVolumeLV[4] = round(shareLV[4] * minUSD / averagePriceLV[4], 4)
    tradeStatNumber = 0
    mydict = {"tradeStatNumber": tradeStatNumber,
              "averagePriceLV": averagePriceLV,
              "dropLV": dropLV,
              "orderVolumeLV": orderVolumeLV,
              "purchasedPriceLV": purchasedPriceLV,
              "shareLV": shareLV,
              "upLV": upLV,
              "startPrice": startPrice,
              "totalShare": totalShare,
              "historyPriceLV": [currentPrice, 0.0, 0.0, 0.0, 0.0],
              "historyOrderVolumeLV": [orderVolumeLVArray[-1][0], 0.0, 0.0, 0.0, 0.0]}
    x = martingaleTradeLogCol.insert_one(mydict)
    print(x.inserted_id)
    

# Buy the level 1 (round 2) when the current price dropped over dropLV[1]
print("buy round 2")
print(currentPrice)
print(purchasedPriceLVArray[-1][0])
print(currentPrice / purchasedPriceLVArray[-1][0])
print(dropLV[1])
if tradeStatNumber == 0 and currentPrice / purchasedPriceLVArray[-1][0] < dropLV[1]:
# if True:
    print("buy round 2")
    print(currentPrice)
    print(purchasedPriceLVArray[-1][0])
    print(currentPrice / purchasedPriceLVArray[-1][0])
    print(dropLV[1])
    # Make the JSON and add the record for mock trade
    tradeStatNumber = latestTradeStatNumber + 1
    mydict = {"tradeStatNumber": tradeStatNumber,
              "averagePriceLV": averagePriceLVArray[-1],
              "dropLV": dropLV,
              "orderVolumeLV": orderVolumeLVArray[-1],
              "purchasedPriceLV": purchasedPriceLVArray[-1],
              "shareLV": shareLV,
              "upLV": upLV,
              "startPrice": startPriceArray[-1],
              "totalShare": totalShare,
              "historyPriceLV": [purchasedPriceLVArray[-1][0], currentPrice, 0.0, 0.0, 0.0],
              "historyOrderVolumeLV": [orderVolumeLVArray[-1][0], orderVolumeLVArray[-1][1], 0.0, 0.0, 0.0]}
    x = martingaleTradeLogCol.insert_one(mydict)
    print(x.inserted_id)

# Sell all on level 1 (round 2) during the price is going up
if latestTradeStatNumber == 1 and currentPrice / purchasedPriceLVArray[-1][1] > upLVArray[-1][1]:
    # if True:
    # Calculate the USDT after sell all on level 0
    # ETH to USDT
    tradeResult = currentPrice*orderVolumeLVArray[-1][0]+currentPrice*orderVolumeLVArray[-1][1]
    # Remaining USDT
    remainingUSDT = latestMartingaleBalance/totalShare*(totalShare-1-4)
    newBalance = tradeResult+remainingUSDT
    addRecordMartingaleBalance(newBalance)
    #Buy the level 0 after sell immediately
    # Set the detailed level of purchasedPrice
    startPrice = currentPrice
    purchasedPriceLV[0] = currentPrice
    purchasedPriceLV[1] = currentPrice * dropLV[1]
    purchasedPriceLV[2] = currentPrice * dropLV[2]
    purchasedPriceLV[3] = currentPrice * dropLV[3]
    purchasedPriceLV[4] = currentPrice * dropLV[4]
    # Set the detailed level of averagePrice
    averagePriceLV[0] = currentPrice
    averagePriceLV[1] = (purchasedPriceLV[0] + shareLV[1]
                         * purchasedPriceLV[1]) / (shareLV[0] + shareLV[1])
    averagePriceLV[2] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2]) / (shareLV[0] + shareLV[1] + shareLV[2])
    averagePriceLV[3] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] + shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3]) / (shareLV[0] + shareLV[1] + shareLV[2] + shareLV[3])
    averagePriceLV[4] = (purchasedPriceLV[0] +
                         shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3] +
                         shareLV[4] * purchasedPriceLV[4]) / totalShare
    # Set USDT until
    minUSD = latestMartingaleBalance / totalShare
    minUSD = round(minUSD, 4)
    # Set the detailed level of Order Volume
    orderVolumeLV[0] = round(shareLV[0] * minUSD / averagePriceLV[0], 4)
    orderVolumeLV[1] = round(shareLV[1] * minUSD / averagePriceLV[1], 4)
    orderVolumeLV[2] = round(shareLV[2] * minUSD / averagePriceLV[2], 4)
    orderVolumeLV[3] = round(shareLV[3] * minUSD / averagePriceLV[3], 4)
    orderVolumeLV[4] = round(shareLV[4] * minUSD / averagePriceLV[4], 4)
    tradeStatNumber = 0
    mydict = {"tradeStatNumber": tradeStatNumber,
              "averagePriceLV": averagePriceLV,
              "dropLV": dropLV,
              "orderVolumeLV": orderVolumeLV,
              "purchasedPriceLV": purchasedPriceLV,
              "shareLV": shareLV,
              "upLV": upLV,
              "startPrice": startPrice,
              "totalShare": totalShare,
              "historyPriceLV": [currentPrice, 0.0, 0.0, 0.0, 0.0],
              "historyOrderVolumeLV": [orderVolumeLVArray[-1][0], 0.0, 0.0, 0.0, 0.0]}
    x = martingaleTradeLogCol.insert_one(mydict)
    print(x.inserted_id)

# Buy the on level 2 (round 3) when the current price dropped over dropLV[2]
if tradeStatNumber == 1 and currentPrice / purchasedPriceLVArray[-1][0] < dropLV[2]:
# if True:
    print("buy round 3")
    print(currentPrice)
    print(purchasedPriceLVArray[-1][1])
    print(currentPrice / purchasedPriceLVArray[-1][1])
    print(dropLV[2])
    # Make the JSON and add the record for mock trade
    tradeStatNumber = latestTradeStatNumber + 1
    mydict = {"tradeStatNumber": tradeStatNumber,
              "averagePriceLV": averagePriceLVArray[-1],
              "dropLV": dropLV,
              "orderVolumeLV": orderVolumeLVArray[-1],
              "purchasedPriceLV": purchasedPriceLVArray[-1],
              "shareLV": shareLV,
              "upLV": upLV,
              "startPrice": startPriceArray[-1],
              "totalShare": totalShare,
              "historyPriceLV": [purchasedPriceLVArray[-1][0], purchasedPriceLVArray[-1][1], currentPrice, 0.0, 0.0],
              "historyOrderVolumeLV": [orderVolumeLVArray[-1][0], orderVolumeLVArray[-1][1], orderVolumeLVArray[-1][2], 0.0, 0.0]}
    x = martingaleTradeLogCol.insert_one(mydict)
    print(x.inserted_id)

# Sell all on level 2 (round 3) during the price is going up
if latestTradeStatNumber == 2 and currentPrice / purchasedPriceLVArray[-1][2] > upLVArray[-1][2]:
    # if True:
    # Calculate the USDT after sell all on level 0
    # ETH to USDT
    tradeResult = currentPrice*orderVolumeLVArray[-1][0]+currentPrice*orderVolumeLVArray[-1][1]+currentPrice*orderVolumeLVArray[-1][2]
    # Remaining USDT
    remainingUSDT = latestMartingaleBalance/totalShare*(totalShare-1-4-16)
    newBalance = tradeResult+remainingUSDT
    addRecordMartingaleBalance(newBalance)
    #Buy the level 0 after sell immediately
    # Set the detailed level of purchasedPrice
    startPrice = currentPrice
    purchasedPriceLV[0] = currentPrice
    purchasedPriceLV[1] = currentPrice * dropLV[1]
    purchasedPriceLV[2] = currentPrice * dropLV[2]
    purchasedPriceLV[3] = currentPrice * dropLV[3]
    purchasedPriceLV[4] = currentPrice * dropLV[4]
    # Set the detailed level of averagePrice
    averagePriceLV[0] = currentPrice
    averagePriceLV[1] = (purchasedPriceLV[0] + shareLV[1]
                         * purchasedPriceLV[1]) / (shareLV[0] + shareLV[1])
    averagePriceLV[2] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2]) / (shareLV[0] + shareLV[1] + shareLV[2])
    averagePriceLV[3] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] + shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3]) / (shareLV[0] + shareLV[1] + shareLV[2] + shareLV[3])
    averagePriceLV[4] = (purchasedPriceLV[0] +
                         shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3] +
                         shareLV[4] * purchasedPriceLV[4]) / totalShare
    # Set USDT until
    minUSD = latestMartingaleBalance / totalShare
    minUSD = round(minUSD, 4)
    # Set the detailed level of Order Volume
    orderVolumeLV[0] = round(shareLV[0] * minUSD / averagePriceLV[0], 4)
    orderVolumeLV[1] = round(shareLV[1] * minUSD / averagePriceLV[1], 4)
    orderVolumeLV[2] = round(shareLV[2] * minUSD / averagePriceLV[2], 4)
    orderVolumeLV[3] = round(shareLV[3] * minUSD / averagePriceLV[3], 4)
    orderVolumeLV[4] = round(shareLV[4] * minUSD / averagePriceLV[4], 4)
    tradeStatNumber = 0
    mydict = {"tradeStatNumber": tradeStatNumber,
              "averagePriceLV": averagePriceLV,
              "dropLV": dropLV,
              "orderVolumeLV": orderVolumeLV,
              "purchasedPriceLV": purchasedPriceLV,
              "shareLV": shareLV,
              "upLV": upLV,
              "startPrice": startPrice,
              "totalShare": totalShare,
              "historyPriceLV": [currentPrice, 0.0, 0.0, 0.0, 0.0],
              "historyOrderVolumeLV": [orderVolumeLVArray[-1][0], 0.0, 0.0, 0.0, 0.0]}
    x = martingaleTradeLogCol.insert_one(mydict)
    print(x.inserted_id)

# Buy the on level 3 (round 4) when the current price dropped over dropLV[3]
if tradeStatNumber == 2 and currentPrice / purchasedPriceLVArray[-1][0] < dropLV[3]:
    # if True:
    print("buy round 4")
    print(currentPrice)
    print(purchasedPriceLVArray[-1][2])
    print(currentPrice / purchasedPriceLVArray[-1][2])
    print(dropLV[3])
    # Make the JSON and add the record for mock trade
    tradeStatNumber = latestTradeStatNumber + 1
    mydict = {"tradeStatNumber": tradeStatNumber,
              "averagePriceLV": averagePriceLVArray[-1],
              "dropLV": dropLV,
              "orderVolumeLV": orderVolumeLVArray[-1],
              "purchasedPriceLV": purchasedPriceLVArray[-1],
              "shareLV": shareLV,
              "upLV": upLV,
              "startPrice": startPriceArray[-1],
              "totalShare": totalShare,
              "historyPriceLV": [purchasedPriceLVArray[-1][0], purchasedPriceLVArray[-1][1], purchasedPriceLVArray[-1][2], currentPrice, 0.0],
              "historyOrderVolumeLV": [orderVolumeLVArray[-1][0], orderVolumeLVArray[-1][1], orderVolumeLVArray[-1][2], orderVolumeLVArray[-1][3], 0.0]}
    x = martingaleTradeLogCol.insert_one(mydict)
    print(x.inserted_id)

# Sell all on level 3 (round 4) during the price is going up
if latestTradeStatNumber == 3 and currentPrice / purchasedPriceLVArray[-1][3] > upLVArray[-1][3]:
    # if True:
    # Calculate the USDT after sell all on level 0
    # ETH to USDT
    tradeResult = currentPrice*orderVolumeLVArray[-1][0]+currentPrice*orderVolumeLVArray[-1][1]+currentPrice*orderVolumeLVArray[-1][2]+currentPrice*orderVolumeLVArray[-1][3]
    # Remaining USDT
    remainingUSDT = latestMartingaleBalance/totalShare*(totalShare-1-4-16-64)
    newBalance = tradeResult+remainingUSDT
    addRecordMartingaleBalance(newBalance)
    #Buy the level 0 after sell immediately
    # Set the detailed level of purchasedPrice
    startPrice = currentPrice
    purchasedPriceLV[0] = currentPrice
    purchasedPriceLV[1] = currentPrice * dropLV[1]
    purchasedPriceLV[2] = currentPrice * dropLV[2]
    purchasedPriceLV[3] = currentPrice * dropLV[3]
    purchasedPriceLV[4] = currentPrice * dropLV[4]
    # Set the detailed level of averagePrice
    averagePriceLV[0] = currentPrice
    averagePriceLV[1] = (purchasedPriceLV[0] + shareLV[1]
                         * purchasedPriceLV[1]) / (shareLV[0] + shareLV[1])
    averagePriceLV[2] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2]) / (shareLV[0] + shareLV[1] + shareLV[2])
    averagePriceLV[3] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] + shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3]) / (shareLV[0] + shareLV[1] + shareLV[2] + shareLV[3])
    averagePriceLV[4] = (purchasedPriceLV[0] +
                         shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3] +
                         shareLV[4] * purchasedPriceLV[4]) / totalShare
    # Set USDT until
    minUSD = latestMartingaleBalance / totalShare
    minUSD = round(minUSD, 4)
    # Set the detailed level of Order Volume
    orderVolumeLV[0] = round(shareLV[0] * minUSD / averagePriceLV[0], 4)
    orderVolumeLV[1] = round(shareLV[1] * minUSD / averagePriceLV[1], 4)
    orderVolumeLV[2] = round(shareLV[2] * minUSD / averagePriceLV[2], 4)
    orderVolumeLV[3] = round(shareLV[3] * minUSD / averagePriceLV[3], 4)
    orderVolumeLV[4] = round(shareLV[4] * minUSD / averagePriceLV[4], 4)
    tradeStatNumber = 0
    mydict = {"tradeStatNumber": tradeStatNumber,
              "averagePriceLV": averagePriceLV,
              "dropLV": dropLV,
              "orderVolumeLV": orderVolumeLV,
              "purchasedPriceLV": purchasedPriceLV,
              "shareLV": shareLV,
              "upLV": upLV,
              "startPrice": startPrice,
              "totalShare": totalShare,
              "historyPriceLV": [currentPrice, 0.0, 0.0, 0.0, 0.0],
              "historyOrderVolumeLV": [orderVolumeLVArray[-1][0], 0.0, 0.0, 0.0, 0.0]}
    x = martingaleTradeLogCol.insert_one(mydict)
    print(x.inserted_id)

# Buy the on level 4 (round 5 - the last round) when the current price dropped over dropLV[4]
if tradeStatNumber == 3 and currentPrice / purchasedPriceLVArray[-1][0] < dropLV[4]:
    # if True:
    print("buy round 5")
    print(currentPrice)
    print(purchasedPriceLVArray[-1][3])
    print(currentPrice / purchasedPriceLVArray[-1][3])
    print(dropLV[4])
    # Make the JSON and add the record for mock trade
    tradeStatNumber = latestTradeStatNumber + 1
    mydict = {"tradeStatNumber": tradeStatNumber,
              "averagePriceLV": averagePriceLVArray[-1],
              "dropLV": dropLV,
              "orderVolumeLV": orderVolumeLVArray[-1],
              "purchasedPriceLV": purchasedPriceLVArray[-1],
              "shareLV": shareLV,
              "upLV": upLV,
              "startPrice": startPriceArray[-1],
              "totalShare": totalShare,
              "historyPriceLV": [purchasedPriceLVArray[-1][0], purchasedPriceLVArray[-1][1], purchasedPriceLVArray[-1][2], purchasedPriceLVArray[-1][3], currentPrice],
              "historyOrderVolumeLV": [orderVolumeLVArray[-1][0], orderVolumeLVArray[-1][1], orderVolumeLVArray[-1][2], orderVolumeLVArray[-1][3], orderVolumeLVArray[-1][4]]}
    x = martingaleTradeLogCol.insert_one(mydict)
    print(x.inserted_id)

# Sell all on level 4 (round 5 - the last round) during the price is going up and repeat to buy level 0 (round 1) again
if latestTradeStatNumber == 4 and currentPrice / purchasedPriceLVArray[-1][4] > upLVArray[-1][4]:
    # if True:
    # Calculate the USDT after sell all on level 0
    # ETH to USDT
    tradeResult = currentPrice*orderVolumeLVArray[-1][0]+currentPrice*orderVolumeLVArray[-1][1]+currentPrice*orderVolumeLVArray[-1][2]+currentPrice*orderVolumeLVArray[-1][3]+currentPrice*orderVolumeLVArray[-1][4]
    # Remaining USDT
    remainingUSDT = latestMartingaleBalance/totalShare*(totalShare-1-4-16-64-256)
    newBalance = tradeResult+remainingUSDT
    addRecordMartingaleBalance(newBalance)
    # Repeat to buy level 0 (round 1) 
    # Set the detailed level of purchasedPrice
    startPrice = currentPrice
    purchasedPriceLV[0] = currentPrice
    purchasedPriceLV[1] = currentPrice * dropLV[1]
    purchasedPriceLV[2] = currentPrice * dropLV[2]
    purchasedPriceLV[3] = currentPrice * dropLV[3]
    purchasedPriceLV[4] = currentPrice * dropLV[4]
    # Set the detailed level of averagePrice
    averagePriceLV[0] = currentPrice
    averagePriceLV[1] = (purchasedPriceLV[0] + shareLV[1]
                         * purchasedPriceLV[1]) / (shareLV[0] + shareLV[1])
    averagePriceLV[2] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2]) / (shareLV[0] + shareLV[1] + shareLV[2])
    averagePriceLV[3] = (purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] + shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3]) / (shareLV[0] + shareLV[1] + shareLV[2] + shareLV[3])
    averagePriceLV[4] = (purchasedPriceLV[0] +
                         shareLV[1] * purchasedPriceLV[1] +
                         shareLV[2] * purchasedPriceLV[2] +
                         shareLV[3] * purchasedPriceLV[3] +
                         shareLV[4] * purchasedPriceLV[4]) / totalShare
    # Set USDT until
    minUSD = latestMartingaleBalance / totalShare
    minUSD = round(minUSD, 4)
    # Set the detailed level of Order Volume
    orderVolumeLV[0] = round(shareLV[0] * minUSD / averagePriceLV[0], 4)
    orderVolumeLV[1] = round(shareLV[1] * minUSD / averagePriceLV[1], 4)
    orderVolumeLV[2] = round(shareLV[2] * minUSD / averagePriceLV[2], 4)
    orderVolumeLV[3] = round(shareLV[3] * minUSD / averagePriceLV[3], 4)
    orderVolumeLV[4] = round(shareLV[4] * minUSD / averagePriceLV[4], 4)
    # Buy and add record level 0 of order volume in mock
    tradeStatNumber = 0
    mydict = {"tradeStatNumber": tradeStatNumber,
              "averagePriceLV": averagePriceLV,
              "dropLV": dropLV,
              "orderVolumeLV": orderVolumeLV,
              "purchasedPriceLV": purchasedPriceLV,
              "shareLV": shareLV,
              "upLV": upLV,
              "startPrice": startPrice,
              "totalShare": totalShare,
              "historyPriceLV": [currentPrice, 0.0, 0.0, 0.0, 0.0],
              "historyOrderVolumeLV": [orderVolumeLVArray[-1][0], 0.0, 0.0, 0.0, 0.0]}
    x = martingaleTradeLogCol.insert_one(mydict)
    print(x.inserted_id)
    print("buy round 1")