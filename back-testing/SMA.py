# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 08:39:31 2022

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
        
class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=16   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy(size=self.broker.get_cash()/self.data.close[0])  # enter long
                # self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

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
cerebro.addstrategy(SmaCross) 

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

