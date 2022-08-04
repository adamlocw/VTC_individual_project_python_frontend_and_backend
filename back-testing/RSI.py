# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 23:26:24 2022

@author: adaml
"""
from __future__ import(absolute_import, division, print_function, unicode_literals)

import datetime
import backtrader as bt
import pandas as pd

class CommInfoFractional(bt.CommissionInfo):
    def getsize(self, price, cash):
        '''Returns fractional size for cash operation @price'''
        return self.p.leverage * (cash / price)

class firstRSI_Strategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy(size= self.broker.get_cash() / self.data.close[0])
                # print("Cash in broker: " + str(self.broker.get_cash()))
                # print("Current price: " + str(self.data.close[0]))
                # print("Buy size : " + str(self.broker.get_cash() / self.data.close[0]))
                # self.order = self.buy()
                # print("Buy date:")
                # print(self.data.datetime.datetime())
                # print(self.data.close[0])
        else:
            if self.rsi > 70:
                #self.sell(size=100)
                self.order = self.close()
                # print("Sell date:")
                # print(self.data.datetime.datetime())
                # print(self.data.close[0])

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

dataframe=pd.read_csv('ETHUSD_day_k_2018_2022.csv')
dataframe['datetime'] = pd.to_datetime(dataframe['time'])
dataframe.set_index('datetime', inplace=True)
dataframe['openinterest']=0
brf_daily = bt.feeds.PandasData(dataname=dataframe, fromdate=datetime.datetime(2018,1,1,0,0),todate=datetime.datetime(2021,12,31,0,0))

cerebro = bt.Cerebro()

cerebro.adddata(brf_daily)

#Input the name of the Strategy
cerebro.addstrategy(firstRSI_Strategy)

startcash = 4000
cerebro.broker.setcash(startcash)
cerebro.broker.setcommission(commission=0.0001)
cerebro.broker.addcommissioninfo(CommInfoFractional())

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
# print('Final Portfolio Value: ${}'.format(portvalue))
# print('P/L: ${}'.format(pnl))
print('Final Startcash Value: ${}'.format(startcash))
print('Final Portfolio Value: ${}'.format(portvalue))
print('P/L: ${}'.format(pnl))
print("Net profit: "+str(round(portvalue - startcash,2)))
print("Net profit %: "+str(round(((portvalue - startcash)/startcash)*100,2)))
#print("Net profit %: "+str((portvalue - startcash)/startcash))

cerebro.plot()  
#cerebro.plot(style='candlestick')

