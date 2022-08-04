import pandas as pd
import numpy
import datetime as DT
from Historic_Crypto import HistoricalData

coin = 'ETH-USD'
timeSecond = 3600  # 1 hour
x = []
startGrid = 2500
endGrid = 99999
gridSize = 0
numberOfGrid = 200  # 150 or 200
numberOfDayChecking = 90  # 30, 60 or 90 days
today = DT.date.today()
week_ago = today - DT.timedelta(days=numberOfDayChecking)
dateFormat = '%Y-%m-%d'
week_ago = week_ago.strftime(dateFormat)

coinHourly = HistoricalData(coin, timeSecond,
                            f"{week_ago}-00-00").retrieve_data()

#coinHourly.to_csv (r'hourlyETH.csv', index = True, header=True)

onlyHighLow = pd.DataFrame(coinHourly, columns=['high', 'low'])

onlyHighLow = onlyHighLow.reset_index()

for index, row in onlyHighLow.iterrows():
    if row['high'] > row['low']:
        x.append(round(row['high'] - row['low']))
    else:
        x.append(round(row['low'] - row['high']))

mean = round(numpy.mean(x))
stdDev = round(numpy.std(x))
print(f"The mean is {mean}")
print(f"The standard deviation is {stdDev}")

startStdDev = mean - stdDev
endStdDev = mean + stdDev

print('Mean - standard deviation is  ' + str(round(startStdDev, 2)))

gridSize = round(mean - stdDev)

endGrid = round(numberOfGrid * gridSize + startGrid)

print(f"The start grid is {startGrid}.")
print(f"The number of grid is {numberOfGrid}.")
print(f"The grid size is {gridSize}.")
print(f"The end grid is {endGrid}.")

# currentHigh = onlyHighLow['high'].iloc[-1]
currentPrice = coinHourly['close'].iloc[-1]
print(f"The current price is {currentPrice}")

print(f"The recommended start and end grid will be:")

gridRange = endGrid - startGrid
meangridRange = gridRange / 2
recommendedStartGrid = currentPrice - meangridRange
recommendedEndGrid = currentPrice + meangridRange

print(f"The recommended start grid is {round(recommendedStartGrid)}.")
print(f"The recommended end grid is {round(recommendedEndGrid)}.")
