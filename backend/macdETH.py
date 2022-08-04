# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 23:07:01 2021

@author: adamlo

Get hourly k lione history by Binance
"""
import talib
from sendEmail import sendEmail
#from buyAllETH import buyAllETH
#from sellAllETH import sellAllETH

from threading import Thread
import os
import numpy as np
from binance.client import Client
from datetime import datetime, timedelta
import pandas as pd
import talib

currentUSDT = 0
currentETH = 0
current_ETH_USDT = 0
testMode = True  # True or False

f = open("apiKey.txt", "r")
apiKey = f.readlines()[0]
f = open("sKey.txt", "r")
sKey = f.readlines()[0]

api_key = os.environ.get(apiKey)
api_secret = os.environ.get(sKey)
N = 300
logDateTime = datetime.now().strftime('%Y%m%d%H%M%S')
date_N_days_ago = datetime.now() - timedelta(days=N)
date_N_days_ago = date_N_days_ago.strftime('%d %b, %Y')
date_N_today = datetime.now().strftime('%Y-%m-%d-%H')+"-00"
client = Client(api_key, api_secret)
candles = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1DAY, date_N_days_ago)
candles_df = pd.DataFrame(candles)
dailyCloseArray = candles_df[4].to_numpy()
dailyCloseArray = np.array(dailyCloseArray, dtype='f8')

macd, signal, hist = talib.MACD(dailyCloseArray, 12, 26, 9)


logDateTime = datetime.now().strftime('%Y%m%d%H%M%S')

print('Current price is '+str(dailyCloseArray[-1])+'\n')
print(f"{datetime.now()}\n")

isMACD_buy = hist[-3] <= 0 and hist[-2] > 0
isMACD_sell = hist[-3] >= 0 and hist[-2] < 0

print("MACD sell signal is \t"+str(isMACD_sell))
print("MACD buy signal is \t\t"+str(isMACD_buy)+'\n')


def func_adamlocw_Sell():
    # Call function to sell all ETH
    #sellAllETH()
    logName = 'darilyMACDBuyAllETH_'+str(logDateTime)+'.log'
    os.system('python sellAllETH.py > '+logName)
    # Send email for the trade record
    emailTo = "adamlocw@gmail.com"
    emailSubject = "ETH sell on Binace using MACD trigger"
    emailBody = f"ETH (MACD 12 26 9) SELL on Binance right now by VTC individual project. {datetime.now()}"
    sendEmail(emailTo, emailSubject, emailBody)


def func_adamlocw_buy():
    # Call function to buy all ETH
    #buyAllETH()
    logName = 'darilyMACDBuyAllETH_'+str(logDateTime)+'.log'
    os.system('python buyAllETH.py > '+logName)
    # Send email for the trade record
    emailTo = "adamlocw@gmail.com"
    emailSubject = "ETH buy on Binace using MACD trigger"
    emailBody = f"ETH (MACD 12 26 9) BUY on Binance right now by VTC individual project. {datetime.now()}"
    sendEmail(emailTo, emailSubject, emailBody)


#if isMACD_sell:
if isMACD_sell:
    Thread(target=func_adamlocw_Sell).start()
#if isMACD_buy:
if isMACD_buy:
    Thread(target=func_adamlocw_buy).start()
