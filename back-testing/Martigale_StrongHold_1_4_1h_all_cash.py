# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 15:40:40 2022

@author: adaml
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import backtrader as bt
import pandas as pd

tradeStatNumber = -1
startPrice = 0.0

maxPriceReadyToSell = 0.0
lowPriceReadyToBuy = 0.0

# purchasedPriceLV0 = 0.0
# purchasedPriceLV1 = 0.0
# purchasedPriceLV2 = 0.0
# purchasedPriceLV3 = 0.0
# purchasedPriceLV4 = 0.0
purchasedPriceLV = [0.0, 0.0, 0.0, 0.0, 0.0]

# averagePriceLV0 = 0.0
# averagePriceLV1 = 0.0
# averagePriceLV2 = 0.0
# averagePriceLV3 = 0.0
# averagePriceLV4 = 0.0
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

# orderVolumeLV0 = 0.0
# orderVolumeLV1 = 0.0
# orderVolumeLV2 = 0.0
# orderVolumeLV3 = 0.0
# orderVolumeLV4 = 0.0
orderVolumeLV = [0.0, 0.0, 0.0, 0.0, 0.0]

readyForBuyorSell = ""  #text "buy" or "sell" only


class Martingale(bt.Strategy):
    def __init__(self):
        global tradeStatNumber
        tradeStatNumber = -1

    def next(self):
        # global purchasedPriceLV0
        # global purchasedPriceLV1
        # global purchasedPriceLV2
        # global purchasedPriceLV3
        # global purchasedPriceLV4
        # global dropLV1
        # global dropLV2
        # global dropLV3
        # global dropLV4
        # global upLV0
        # global upLV1
        # global upLV2
        # global upLV3
        # global upLV4
        # global shareLV0
        # global shareLV1
        # global shareLV2
        # global shareLV3
        # global shareLV4
        # global averagePriceLV0
        # global averagePriceLV1
        # global averagePriceLV2
        # global averagePriceLV3
        # global averagePriceLV4
        # global orderVolumeLV0
        # global orderVolumeLV1
        # global orderVolumeLV2
        # global orderVolumeLV3
        # global orderVolumeLV4
        global tradeStatNumber
        global startPrice
        global totalShare
        global purchasedPriceLV
        global averagePriceLV
        global dropLV
        global upLV
        global shareLV
        global orderVolumeLV

        # print("Testing f_tradeStatNumber: "+str(tradeStatNumber))

        #First time buy level 0
        if tradeStatNumber == -1:
            startPrice = self.data.close[0]
            purchasedPriceLV[0] = self.data.close[0]
            purchasedPriceLV[1] = self.data.close[0] * dropLV[1]
            purchasedPriceLV[2] = self.data.close[0] * dropLV[2]
            purchasedPriceLV[3] = self.data.close[0] * dropLV[3]
            purchasedPriceLV[4] = self.data.close[0] * dropLV[4]

            averagePriceLV[0] = self.data.close[0]
            averagePriceLV[1] = (purchasedPriceLV[0] +
                                 shareLV[1] * purchasedPriceLV[1]) / (
                                     shareLV[0] + shareLV[1])
            averagePriceLV[2] = (
                purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] +
                shareLV[2] * purchasedPriceLV[2]) / (shareLV[0] + shareLV[1] +
                                                     shareLV[2])
            averagePriceLV[3] = (
                purchasedPriceLV[0] + shareLV[1] * purchasedPriceLV[1] +
                shareLV[2] * purchasedPriceLV[2] +
                shareLV[3] * purchasedPriceLV[3]) / (shareLV[0] + shareLV[1] +
                                                     shareLV[2] + shareLV[3])
            averagePriceLV[4] = (purchasedPriceLV[0] +
                                 shareLV[1] * purchasedPriceLV[1] +
                                 shareLV[2] * purchasedPriceLV[2] +
                                 shareLV[3] * purchasedPriceLV[3] +
                                 shareLV[4] * purchasedPriceLV[4]) / totalShare

            minUSD = self.broker.get_cash() / totalShare

            orderVolumeLV[0] = shareLV[0] * minUSD / averagePriceLV[0]
            orderVolumeLV[1] = shareLV[1] * minUSD / averagePriceLV[1]
            orderVolumeLV[2] = shareLV[2] * minUSD / averagePriceLV[2]
            orderVolumeLV[3] = shareLV[3] * minUSD / averagePriceLV[3]
            orderVolumeLV[4] = shareLV[4] * minUSD / averagePriceLV[4]

            self.order = self.buy(size=orderVolumeLV[0])
            tradeStatNumber = tradeStatNumber + 1

            # print("Buy date:")
            # print(self.data.datetime.datetime())
            # print(self.data.close[0])

        #Sell all on level 0
        if tradeStatNumber == 0 and self.data.close[0] / startPrice > upLV[0]:
            self.order = self.close()
            tradeStatNumber = -1
            # print("Sell date:")
            # print(self.data.datetime.datetime())
            # print(self.data.close[0])

        #Seond time buy
        if tradeStatNumber == 0 and self.data.close[0] / startPrice < dropLV[1]:
            self.order = self.buy(size=orderVolumeLV[1])
            purchasedPriceLV[1] = self.data.close[0]
            tradeStatNumber = tradeStatNumber + 1
            # print("Buy date:")
            # print(self.data.datetime.datetime())
            # print(self.data.close[0])
            # print("averagePriceLV1: " + str(averagePriceLV[1]))
            # print("shareLV1: " + str(shareLV[1]))

        #Sell all
        if tradeStatNumber == 1 and self.data.close[0] / averagePriceLV[
                1] > upLV[1]:
            self.order = self.close()
            tradeStatNumber = -1
            # print("Sell date:")
            # print(self.data.datetime.datetime())
            # print(self.data.close[0])

        #3 time buy
        if tradeStatNumber == 1 and self.data.close[0] / startPrice < dropLV[2]:
            self.order = self.buy(size=orderVolumeLV[2])
            purchasedPriceLV[2] = self.data.close[0]
            tradeStatNumber = tradeStatNumber + 1
            # print("Buy date:")
            # print(self.data.datetime.datetime())
            # print(self.data.close[0])
            # print("averagePriceLV1: " + str(averagePriceLV[1]))
            # print("averagePriceLV2: " + str(averagePriceLV[2]))
            # print("shareLV1: " + str(shareLV[1]))
            # print("shareLV2: " + str(shareLV[2]))

        #Sell all
        if tradeStatNumber == 2 and self.data.close[0] / averagePriceLV[
                2] > upLV[2]:
            self.order = self.close()
            tradeStatNumber = -1
            # print("Sell date:")
            # print(self.data.datetime.datetime())
            # print(self.data.close[0])

        #4 time buy
        if tradeStatNumber == 2 and self.data.close[0] / startPrice < dropLV[3]:
            self.order = self.buy(size=orderVolumeLV[3])
            purchasedPriceLV[3] = self.data.close[0]
            tradeStatNumber = tradeStatNumber + 1
            # print("Buy date:")
            # print(self.data.datetime.datetime())
            # print(self.data.close[0])
            # print("averagePriceLV1: " + str(averagePriceLV[1]))
            # print("averagePriceLV2: " + str(averagePriceLV[2]))
            # print("averagePriceLV3: " + str(averagePriceLV[3]))
            # print("shareLV1: " + str(shareLV[1]))
            # print("shareLV2: " + str(shareLV[2]))
            # print("shareLV3: " + str(shareLV[3]))

        #Sell all
        if tradeStatNumber == 3 and self.data.close[0] / averagePriceLV[
                3] > upLV[3]:
            self.order = self.close()
            tradeStatNumber = -1
            # print("Sell date:")
            # print(self.data.datetime.datetime())
            # print(self.data.close[0])

        #5 time buy
        if tradeStatNumber == 3 and self.data.close[0] / startPrice < dropLV[4]:
            self.order = self.buy(size=orderVolumeLV[4])
            purchasedPriceLV[4] = self.data.close[0]
            tradeStatNumber = tradeStatNumber + 1
            # print("Buy date:")
            # print(self.data.datetime.datetime())
            # print(self.data.close[0])
            # print("averagePriceLV1: " + str(averagePriceLV[1]))
            # print("averagePriceLV2: " + str(averagePriceLV[2]))
            # print("averagePriceLV3: " + str(averagePriceLV[3]))
            # print("averagePriceLV4: " + str(averagePriceLV[4]))
            # print("shareLV1: " + str(shareLV[1]))
            # print("shareLV2: " + str(shareLV[2]))
            # print("shareLV3: " + str(shareLV[3]))
            # print("shareLV4: " + str(shareLV[4]))

        #Sell all
        if tradeStatNumber == 4 and self.data.close[0] / averagePriceLV[
                4] > upLV[4]:
            self.order = self.close()
            tradeStatNumber = -1
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


dataframe = pd.read_csv('ETHUSD_day_k_2018_2022.csv')
dataframe['datetime'] = pd.to_datetime(dataframe['time'])
dataframe.set_index('datetime', inplace=True)
dataframe['openinterest'] = 0
brf_daily = bt.feeds.PandasData(dataname=dataframe,
                                fromdate=datetime.datetime(2018, 1, 1, 0, 0),
                                todate=datetime.datetime(2021, 12, 31, 0, 0))

cerebro = bt.Cerebro()

cerebro.adddata(brf_daily)

#Input the name of the Strategy
cerebro.addstrategy(Martingale)

startcash = 4000
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
print("Net profit: "+str(round(portvalue - startcash,2)))
print("Net profit %: " +
      str(round(((portvalue - startcash) / startcash) * 100, 2)))
#print("Net profit %: "+str((portvalue - startcash)/startcash))

cerebro.plot()
#cerebro.plot(style='candlestick')
