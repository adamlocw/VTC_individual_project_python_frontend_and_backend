# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 19:49:35 2022

@author: adamlo
"""
from Historic_Crypto import HistoricalData

# crypto_data = HistoricalData('BTC-USD',60,'2017-12-31-23-58','2019-01-01-00-01').retrieve_data()

# crypto_data.to_csv('BTCUSB_1m_k_2018.csv')

# crypto_data = HistoricalData('BTC-USD',60,'2020-12-31-23-58','2022-01-01-00-01').retrieve_data()

# crypto_data.to_csv('BTCUSB_1m_k_2021.csv')

# crypto_data = HistoricalData('ETH-USD',60,'2017-12-31-23-58','2019-01-01-00-01').retrieve_data()

# crypto_data.to_csv('ETHUSB_1m_k_2018.csv')

# crypto_data = HistoricalData('ETH-USD',60,'2020-12-31-23-58','2022-01-01-00-01').retrieve_data()

# crypto_data.to_csv('ETHUSB_1m_k_2021.csv')

crypto_data = HistoricalData('ETH-USD',86400,'2021-06-01-00-00').retrieve_data()

crypto_data.to_csv('ETHUSD_1d_k_2022only.csv')

crypto_data = HistoricalData('BTC-USD',86400,'2021-06-01-00-00').retrieve_data()

crypto_data.to_csv('BTCUSD_1d_k_2022only.csv')