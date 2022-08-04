# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 09:31:37 2022

@author: adaml
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import backtrader as bt
import pandas as pd

startcash = 1000000000


class MyStrategy(bt.Strategy):
    def next(self):
        print(self.data.datetime.datetime())
        print(self.data.close[0])


class Martingale(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=16,  # period for the slow moving average
        tradeStatNumber = -1,
        startPrice = 0,
        maxPriceReadyToSell = 0,
        lowPriceReadyToBuy = 0,
        purchasedPriceLV0 = 0,
        purchasedPriceLV1 = 0,
        purchasedPriceLV2 = 0,
        purchasedPriceLV3 = 0,
        purchasedPriceLV4 = 0,
        dropLV1 = 2 / 100,
        dropLV2 = 4 / 100,
        dropLV3 = 16 / 100,
        dropLV4 = 32 / 100,
        upLV1 = 1 / 100,
        upLV2 = 2 / 100,
        upLV3 = 3 / 100,
        upLV4 = 4 / 100,
        shareLV0 = 1,
        shareLV1 = 2,
        shareLV2 = 4,
        shareLV3 = 8,
        shareLV4 = 16,
        readyForBuyorSell = "" #text "buy" or "sell" only
    )
    

    def __init__(self):
        pass

    def next(self):
        if not self.position:  # not in the market
            if self.p.tradeStatNumber == -1:
                self.p.tradeStatNumber = 0
                self.buy(size=1)
                self.p.purchasedPriceLV0 = self.data.close[0]
                print("The Martigale trading is started. ")
            elif self.p.tradeStatNumber == 0:
                self.p.tradeStatNumber = 1
                self.buy(size=1)
                self.p.purchasedPriceLV0 = self.data.close[0]
                print("The Martigale trading is repeated. ")
            elif self.p.tradeStatNumber == 1:
                self.p.tradeStatNumber = 2
                self.buy(size=2)
                self.p.purchasedPriceLV1 = self.data.close[0]
                print("Dropped to ready to buy level 1. ") 
            elif self.p.tradeStatNumber == 2:
                self.p.tradeStatNumber = 3
                self.buy(size=4)
                self.p.purchasedPriceLV2 = self.data.close[0]
                print("Dropped to ready to buy level 2. ") 
            elif self.p.tradeStatNumber == 3:
                self.p.tradeStatNumber = 4
                self.buy(size=8)
                self.p.purchasedPriceLV3 = self.data.close[0]
                print("Dropped to ready to buy level 3. ")
            elif self.p.tradeStatNumber == 4:
                self.p.tradeStatNumber = 5
                self.buy(size=16)
                self.p.purchasedPriceLV4 = self.data.close[0]
                print("Dropped to ready to buy level 4. ") 
            elif self.p.tradeStatNumber == 5:
                print("All money is used. Waiting to close the trade. ") 
            else:
                # default handling
                print("Please check the tradeStatNumber. ")

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


class firstRSI_Strategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                #self.buy(size=100)
                self.order = self.buy()
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
        else:
            if self.rsi > 70:
                #self.sell(size=100)
                self.order = self.sell()
                print("Sell date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=16  # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


class firstRSI_Strategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                #self.buy(size=100)
                self.order = self.buy()
                print("Buy date:")
                print(self.data.datetime.datetime())
                print(self.data.close[0])
        else:
            if self.rsi > 70:
                #self.sell(size=100)
                self.order = self.sell()
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
    pnl_net = round(analyzer.pnl.net.total, 2)
    strike_rate = (total_won / total_closed) * 100
    strike_rate = round(strike_rate, 2)
    #Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed, total_won, total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    #Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    #Print the rows
    print_list = [h1, r1, h2, r2]
    row_format = "{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('', *row))


def printSQN(analyzer):
    sqn = round(analyzer.sqn, 2)
    print('SQN: {}'.format(sqn))


dataframe = pd.read_csv('ETHUSD_day_k_2021.csv')

dataframe['datetime'] = pd.to_datetime(dataframe['time'])
dataframe.set_index('datetime', inplace=True)
dataframe['openinterest'] = 0

brf_daily = bt.feeds.PandasData(dataname=dataframe,
                                fromdate=datetime.datetime(2021, 1, 1, 0, 0),
                                todate=datetime.datetime(2021, 12, 31, 23, 59))

cerebro = bt.Cerebro()

cerebro.adddata(brf_daily)

#Input the name of the Strategy
cerebro.addstrategy(SmaCross)


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
print('Final Portfolio Value: ${}'.format(portvalue))
print('P/L: ${}'.format(pnl))

#cerebro.plot()
#cerebro.plot(style='candlestick')
