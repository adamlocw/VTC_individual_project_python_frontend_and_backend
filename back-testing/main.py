# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 19:57:48 2022

@author: adaml
"""

from __future__ import(absolute_import, division, print_function, unicode_literals)

import datetime
import backtrader as bt
import pandas as pd

class MyStrategy(bt.Strategy):
    def next(self):
        print(self.data.datetime.datetime())
        print(self.data.close[0])

cerebro = bt.Cerebro()

dataframe=pd.read_csv('ETHUSD_1h_k_2021.csv')
#print(str(dataframe))
dataframe['datetime'] = pd.to_datetime(dataframe['time'])
dataframe.set_index('datetime', inplace=True)
dataframe['openinterest']=0
brf_daily = bt.feeds.PandasData(dataname=dataframe, fromdate=datetime.datetime(2021,1,1,0,0),todate=datetime.datetime(2021,12,31,23,59))

cerebro.adddata(brf_daily)

cerebro.addstrategy(MyStrategy)

cerebro.run() 

#cerebro.plot()  
#cerebro.plot(style='candlestick')


