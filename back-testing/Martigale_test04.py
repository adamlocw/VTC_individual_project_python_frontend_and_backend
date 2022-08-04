# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 16:12:27 2022

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
dropLV1 = 2 / 100
dropLV2 = 4 / 100
dropLV3 = 16 / 100
dropLV4 = 32 / 100
upLV1 = 1 / 100
upLV2 = 2 / 100
upLV3 = 3 / 100
upLV4 = 4 / 100
shareLV0 = 1
shareLV1 = 2
shareLV2 = 4
shareLV3 = 8
shareLV4 = 16
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
            print("Testing f_tradeStatNumber: "+str(tradeStatNumber))
            
            #First time buy level 0
            if tradeStatNumber == -1:
                self.order = self.buy(size=1)
                purchasedPriceLV0 = self.data.close[0]
                tradeStatNumber = tradeStatNumber + 1
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            #Sell all on level 0    
            if tradeStatNumber == 0 and self.data.close[0] / purchasedPriceLV0 > 1.01:
                self.order = self.close()
                tradeStatNumber = -1
            
            #Seond time buy when level 0 dropped more 1%
            if tradeStatNumber == 0 and self.data.close[0] / purchasedPriceLV0 < 0.99:
                self.order = self.buy(size=2)
                purchasedPriceLV1 = self.data.close[0]
                tradeStatNumber = tradeStatNumber + 1
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            #Sell all on leve 1
            if tradeStatNumber == 1 and self.data.close[0] / purchasedPriceLV1 > 1.02:
                self.order = self.close()
                tradeStatNumber = -1
                
            if tradeStatNumber == 1 and self.data.close[0] / purchasedPriceLV1 < 0.96:
                self.order = self.buy(size=4)
                purchasedPriceLV2 = self.data.close[0]
                tradeStatNumber = tradeStatNumber + 1
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            if tradeStatNumber == 2 and self.data.close[0] / purchasedPriceLV2 > 1.04:
                self.order = self.close()
                tradeStatNumber = -1
                
            if tradeStatNumber == 2 and self.data.close[0] / purchasedPriceLV2 < 0.92:
                self.order = self.buy(size=8)
                purchasedPriceLV3 = self.data.close[0]
                tradeStatNumber = tradeStatNumber + 1
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            if tradeStatNumber == 3 and self.data.close[0] / purchasedPriceLV3 > 1.04:
                self.order = self.close()
                tradeStatNumber = -1
                
            if tradeStatNumber == 3 and self.data.close[0] / purchasedPriceLV3 < 0.84:
                self.order = self.buy(size=16)
                purchasedPriceLV4 = self.data.close[0]
                tradeStatNumber = tradeStatNumber + 1
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
                
            if tradeStatNumber == 4 and self.data.close[0] / purchasedPriceLV4 > 1.04:
                self.order = self.close()
                tradeStatNumber = -1


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

dataframe=pd.read_csv('BTCUSD_day_k_2018.csv')
dataframe['datetime'] = pd.to_datetime(dataframe['time'])
dataframe.set_index('datetime', inplace=True)
dataframe['openinterest']=0
brf_daily = bt.feeds.PandasData(dataname=dataframe, fromdate=datetime.datetime(2018,1,1,0,0),todate=datetime.datetime(2018,12,31,23,59))

cerebro = bt.Cerebro()

cerebro.adddata(brf_daily)

cerebro.addstrategy(Martingale)

startcash = 70000 * 50
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


