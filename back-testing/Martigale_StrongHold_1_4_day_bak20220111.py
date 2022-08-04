# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 15:40:40 2022

@author: adaml
"""
from __future__ import(absolute_import, division, print_function, unicode_literals)

import datetime
import backtrader as bt
import pandas as pd

tradeStatNumber = -1
startPrice = 0.0

maxPriceReadyToSell = 0.0
lowPriceReadyToBuy = 0.0

purchasedPriceLV0 = 0.0
purchasedPriceLV1 = 0.0
purchasedPriceLV2 = 0.0
purchasedPriceLV3 = 0.0
purchasedPriceLV4 = 0.0

averagePriceLV0 = 0.0
averagePriceLV1 = 0.0
averagePriceLV2 = 0.0
averagePriceLV3 = 0.0
averagePriceLV4 = 0.0

dropLV1 = 1 - (4 / 100)
dropLV2 = 1 - (12 / 100)
dropLV3 = 1 - (28 / 100)
dropLV4 = 1 - (60 / 100)

upLV0 = (1 / 100) +1
upLV1 = (5 / 100) +1
upLV2 = (10 / 100) +1
upLV3 = (20 / 100) +1
upLV4 = (40 / 100) +1

shareLV0 = 1
shareLV1 = 4
shareLV2 = 16
shareLV3 = 64
shareLV4 = 256
totalShare = shareLV0 + shareLV1 + shareLV2 + shareLV3 + shareLV4

readyForBuyorSell = "" #text "buy" or "sell" only
                
class Martingale(bt.Strategy):
    def __init__(self):
        global tradeStatNumber
        tradeStatNumber = -1

    def next(self):
            global tradeStatNumber
            global startPrice
            global purchasedPriceLV0
            global purchasedPriceLV1
            global purchasedPriceLV2
            global purchasedPriceLV3
            global purchasedPriceLV4
            global startPrice
            global dropLV1
            global dropLV2
            global dropLV3
            global dropLV4
            global upLV0
            global upLV1
            global upLV2
            global upLV3
            global upLV4
            global shareLV0
            global shareLV1
            global shareLV2
            global shareLV3
            global shareLV4
            global totalShare
            global averagePriceLV0
            global averagePriceLV1
            global averagePriceLV2
            global averagePriceLV3
            global averagePriceLV4
            print("Testing f_tradeStatNumber: "+str(tradeStatNumber))
            
            #First time buy level 0
            if tradeStatNumber == -1:
                self.order = self.buy(size=1)
                tradeStatNumber = tradeStatNumber + 1
                startPrice = self.data.close[0]
                purchasedPriceLV0 = self.data.close[0]
                purchasedPriceLV1 = self.data.close[0] * dropLV1
                purchasedPriceLV2 = self.data.close[0] * dropLV2
                purchasedPriceLV3 = self.data.close[0] * dropLV3
                purchasedPriceLV4 = self.data.close[0] * dropLV4
                
                averagePriceLV0 = self.data.close[0]
                averagePriceLV1 = (purchasedPriceLV0 + shareLV1 * purchasedPriceLV1)/(shareLV0+shareLV1)
                averagePriceLV2 = (purchasedPriceLV0 + shareLV1 * purchasedPriceLV1 + shareLV2 * purchasedPriceLV2)/(shareLV0+shareLV1+shareLV2)
                averagePriceLV3 = (purchasedPriceLV0 + shareLV1 * purchasedPriceLV1 + shareLV2 * purchasedPriceLV2 + shareLV3 * purchasedPriceLV3)/(shareLV0+shareLV1+shareLV2+shareLV3)
                averagePriceLV4 = (purchasedPriceLV0 + shareLV1 * purchasedPriceLV1 + shareLV2 * purchasedPriceLV2 + shareLV3 * purchasedPriceLV3 + shareLV4 * purchasedPriceLV4)/totalShare
                
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            #Sell all on level 0    
            if tradeStatNumber == 0 and self.data.close[0] / startPrice > upLV0:
                self.order = self.close()
                tradeStatNumber = -1
                print("Sell date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
            
            #Seond time buy 
            if tradeStatNumber == 0 and self.data.close[0] / startPrice < dropLV1:
                self.order = self.buy(size=4)
                purchasedPriceLV1 = self.data.close[0]
                tradeStatNumber = tradeStatNumber + 1
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                print("averagePriceLV1: "+str(averagePriceLV1))
                
            #Sell all
            if tradeStatNumber == 1 and self.data.close[0] / averagePriceLV1 > upLV1:
                self.order = self.close()
                tradeStatNumber = -1
                print("Sell date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
            
            #3 time buy
            if tradeStatNumber == 1 and self.data.close[0] / startPrice < dropLV2:
                self.order = self.buy(size=16)
                purchasedPriceLV2 = self.data.close[0]
                tradeStatNumber = tradeStatNumber + 1
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                print("averagePriceLV1: "+str(averagePriceLV1))
                print("averagePriceLV2: "+str(averagePriceLV2))
                
            #Sell all 
            if tradeStatNumber == 2 and self.data.close[0] / averagePriceLV2 > upLV2:
                self.order = self.close()
                tradeStatNumber = -1
                print("Sell date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            #4 time buy 
            if tradeStatNumber == 2 and self.data.close[0] / startPrice < dropLV3:
                self.order = self.buy(size=64)
                purchasedPriceLV3 = self.data.close[0]
                tradeStatNumber = tradeStatNumber + 1
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                print("averagePriceLV1: "+str(averagePriceLV1))
                print("averagePriceLV2: "+str(averagePriceLV2))
                print("averagePriceLV3: "+str(averagePriceLV3))
                
            #Sell all
            if tradeStatNumber == 3 and self.data.close[0] / averagePriceLV3 > upLV3:
                self.order = self.close()
                tradeStatNumber = -1
                print("Sell date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
             #5 time buy 
            if tradeStatNumber == 3 and self.data.close[0] / startPrice < dropLV4:
                self.order = self.buy(size=256)
                purchasedPriceLV4 = self.data.close[0]
                tradeStatNumber = tradeStatNumber + 1
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                print("averagePriceLV1: "+str(averagePriceLV1))
                print("averagePriceLV2: "+str(averagePriceLV2))
                print("averagePriceLV3: "+str(averagePriceLV3))
                print("averagePriceLV4: "+str(averagePriceLV4))
                
            #Sell all 
            if tradeStatNumber == 4 and self.data.close[0] / averagePriceLV4 > upLV4:
                self.order = self.close()
                tradeStatNumber = -1
                print("Sell date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])


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

dataframe=pd.read_csv('BTCUSD_day_k_2018_2022.csv')
dataframe['datetime'] = pd.to_datetime(dataframe['time'])
dataframe.set_index('datetime', inplace=True)
dataframe['openinterest']=0
brf_daily = bt.feeds.PandasData(dataname=dataframe, fromdate=datetime.datetime(2018,1,1,0,0),todate=datetime.datetime(2022,12,30,0,0))

cerebro = bt.Cerebro()

cerebro.adddata(brf_daily)

#Input the name of the Strategy
cerebro.addstrategy(Martingale)

startcash = 70000 * totalShare
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
print("Net profit: "+str(portvalue - startcash))
print("Net profit %: "+str(round(((portvalue - startcash)/startcash)*100,2)))
#print("Net profit %: "+str((portvalue - startcash)/startcash))

cerebro.plot()  
#cerebro.plot(style='candlestick')


