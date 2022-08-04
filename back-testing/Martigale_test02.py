# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 14:46:33 2022

@author: adaml
"""
from __future__ import(absolute_import, division, print_function, unicode_literals)

import datetime
import backtrader as bt
import pandas as pd

class firstRSI_Strategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                #self.buy(size=100)
                size = int(self.broker.get_cash() / self.data.close[0])
                self.order = self.buy(size=size)
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                print("Size of buy:")
                print(size)
        else:
            if self.rsi > 70:
                #self.sell(size=100)
                self.order = self.close()
                print("Sell date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
class Martingale(bt.Strategy):
    def __init__(self):
        f = open("tradeStatNumber.txt", "w")
        f.write(str(-1))
        f.close()

    def next(self):
            f_tradeStatNumber = open("tradeStatNumber.txt", "r")
            f_startPrice = open("startPrice.txt", "r")
            f_maxPriceReadyToSell = open("maxPriceReadyToSell.txt", "r")
            f_lowPriceReadyToBuy = open("lowPriceReadyToBuy.txt", "r")
            f_purchasedPriceLV0 = open("purchasedPriceLV0.txt", "r")
            f_purchasedPriceLV1 = open("purchasedPriceLV1.txt", "r")
            f_purchasedPriceLV2 = open("purchasedPriceLV2.txt", "r")
            f_purchasedPriceLV3 = open("purchasedPriceLV3.txt", "r")
            f_purchasedPriceLV4 = open("purchasedPriceLV4.txt", "r")
            f_readyForBuyorSell = open("readyForBuyorSell.txt", "r")
            tradeStatNumber = int(f_tradeStatNumber.readline())
            purchasedPriceLV0 = float(f_purchasedPriceLV0.readline())
            purchasedPriceLV1 = float(f_purchasedPriceLV1.readline())
            purchasedPriceLV2 = float(f_purchasedPriceLV2.readline())
            purchasedPriceLV3 = float(f_purchasedPriceLV3.readline())
            purchasedPriceLV4 = float(f_purchasedPriceLV4.readline())
            readyForBuyorSell = f_readyForBuyorSell.readline()
            print("Testing f_tradeStatNumber: "+str(tradeStatNumber))
            f_tradeStatNumber.close()
            f_startPrice.close()
            f_maxPriceReadyToSell.close()
            f_lowPriceReadyToBuy.close()
            f_purchasedPriceLV0.close()
            f_purchasedPriceLV1.close()
            f_purchasedPriceLV2.close()
            f_purchasedPriceLV3.close()
            f_purchasedPriceLV4.close()
            f_readyForBuyorSell.close()
            
            if tradeStatNumber == -1:
                self.order = self.buy(size=1)
                f = open("purchasedPriceLV0.txt", "w")
                f.write(str(self.data.close[0]))
                f.close()
                tradeStatNumber = tradeStatNumber + 1
                f = open("tradeStatNumber.txt", "w")
                f.write(str(tradeStatNumber))
                f.close()
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            if tradeStatNumber == 0 and self.data.close[0] / purchasedPriceLV0 > 1.01:
                self.order = self.close()
                f = open("tradeStatNumber.txt", "w")
                f.write(str(-1))
                f.close()
                
            if tradeStatNumber == 0 and self.data.close[0] / purchasedPriceLV0 < 0.99:
                self.order = self.buy(size=2)
                f = open("purchasedPriceLV1.txt", "w")
                f.write(str(self.data.close[0]))
                f.close()
                tradeStatNumber = tradeStatNumber + 1
                f = open("tradeStatNumber.txt", "w")
                f.write(str(tradeStatNumber))
                f.close()
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            if tradeStatNumber == 1 and self.data.close[0] / ((1*purchasedPriceLV0+2*purchasedPriceLV1)/3) > 1.02:
                self.order = self.close()
                f = open("tradeStatNumber.txt", "w")
                f.write(str(-1))
                f.close()
                
            if tradeStatNumber == 1 and self.data.close[0] / purchasedPriceLV1 < 0.96:
                self.order = self.buy(size=4)
                f = open("purchasedPriceLV2.txt", "w")
                f.write(str(self.data.close[0]))
                f.close()
                tradeStatNumber = tradeStatNumber + 1
                f = open("tradeStatNumber.txt", "w")
                f.write(str(tradeStatNumber))
                f.close()
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            if tradeStatNumber == 2 and self.data.close[0] / ((1*purchasedPriceLV0+2*purchasedPriceLV1+4*purchasedPriceLV2)/8) > 1.04:
                self.order = self.close()
                f = open("tradeStatNumber.txt", "w")
                f.write(str(-1))
                f.close()
                
            if tradeStatNumber == 2 and self.data.close[0] / purchasedPriceLV2 < 0.92:
                self.order = self.buy(size=8)
                f = open("purchasedPriceLV3.txt", "w")
                f.write(str(self.data.close[0]))
                f.close()
                tradeStatNumber = tradeStatNumber + 1
                f = open("tradeStatNumber.txt", "w")
                f.write(str(tradeStatNumber))
                f.close()
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            if tradeStatNumber == 3 and self.data.close[0] / ((1*purchasedPriceLV0+2*purchasedPriceLV1+4*purchasedPriceLV2+8*purchasedPriceLV3)/15) > 1.08:
                self.order = self.close()
                f = open("tradeStatNumber.txt", "w")
                f.write(str(-1))
                f.close()
                
            if tradeStatNumber == 3 and self.data.close[0] / purchasedPriceLV3 < 0.84:
                self.order = self.buy(size=16)
                f = open("purchasedPriceLV4.txt", "w")
                f.write(str(self.data.close[0]))
                f.close()
                tradeStatNumber = tradeStatNumber + 1
                f = open("tradeStatNumber.txt", "w")
                f.write(str(tradeStatNumber))
                f.close()
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            if tradeStatNumber == 4 and self.data.close[0] / ((1*purchasedPriceLV0+2*purchasedPriceLV1+4*purchasedPriceLV2+8*purchasedPriceLV3+16*purchasedPriceLV4)/31) > 1.16:
                self.order = self.close()
                f = open("tradeStatNumber.txt", "w")
                f.write(str(-1))
                f.close()


def printTradeAnalysis(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    #Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total,2)
    strike_rate = (total_won / total_closed) * 100
    strike_rate = round(strike_rate, 2)
    #Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate','Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed,total_won,total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    #Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    #Print the rows
    print_list = [h1,r1,h2,r2]
    row_format ="{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('',*row))

def printSQN(analyzer):
    sqn = round(analyzer.sqn,2)
    print('SQN: {}'.format(sqn))

dataframe=pd.read_csv('BTCUSD_1h_k_2018.csv')
dataframe['datetime'] = pd.to_datetime(dataframe['time'])
dataframe.set_index('datetime', inplace=True)
dataframe['openinterest']=0
brf_daily = bt.feeds.PandasData(dataname=dataframe, fromdate=datetime.datetime(2018,1,1,0,0),todate=datetime.datetime(2018,12,31,23,59))

cerebro = bt.Cerebro()

cerebro.adddata(brf_daily)

cerebro.addstrategy(Martingale)

startcash = 70000 * 31
cerebro.broker.setcash(startcash)
cerebro.broker.setcommission(commission=0.0001)

# Add the analyzers we are interested in
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

strategies = cerebro.run()
firstStrat = strategies[0]

# print the analyzers
printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())
printSQN(firstStrat.analyzers.sqn.get_analysis())

#Get final portfolio Value
portvalue = cerebro.broker.getvalue()
pnl = portvalue - startcash

#Print out the final result
print('Final Startcash Value: ${}'.format(startcash))
print('Final Portfolio Value: ${}'.format(portvalue))
print('P/L: ${}'.format(pnl))

cerebro.plot()  
#cerebro.plot(style='candlestick')

