# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 20:56:12 2021

@author: adamlo
"""
import ccxt 

# bitmex   = ccxt.bitmex()

currentUSDT = 0
currentETH = 0
current_ETH_USDT = 0
testMode = False # True or False

f = open("D:\\Users\\adamlo\\Documents\\Binance\\adamlo60771916\\123.txt","r")
apiKey = f.readlines()[0]
f = open("D:\\Users\\adamlo\\Documents\\Binance\\adamlo60771916\\sabc.txt","r")
skey = f.readlines()[0]

exchange = ccxt.binance({
    'apiKey': apiKey,
    'secret': skey,
    'enableRateLimit': True,
})

binance_current_balance = exchange.fetch_balance()

binance_current_balance_ETH = binance_current_balance.get('ETH').get('free')
binance_current_balance_USDT = binance_current_balance.get('USDT').get('free')

current_ETH_USDT = exchange.fetch_ticker('ETH/USDT').get('close')
print(current_ETH_USDT)

volume_can_buy = binance_current_balance_USDT/current_ETH_USDT*0.999
volume_can_buy_round = round(volume_can_buy,5)
print(volume_can_buy)
print(volume_can_buy_round)

symbol = 'ETH/USDT'  
type = 'market'  # 'limit' or 'market'
side = 'sell'  # 'sell' or 'buy'
amount = binance_current_balance_ETH # 1.0 or volume_can_buy_round
price = None  # 0.060154 or None

# extra params and overrides if needed
params = {
    'test': testMode,  # test if it's valid, but don't actually place it
}

order = exchange.create_order(symbol, type, side, amount, price, params)

print(order)