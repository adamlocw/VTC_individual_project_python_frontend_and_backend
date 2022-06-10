from flask import Flask, render_template
# https://faun.pub/integrating-mongodb-with-flask-8f6568863c2a
from flask_pymongo import pymongo
import requests
import json
import pandas as pd
import datetime as dt
import numpy
app = Flask('app')

BTCUSDT = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
ETHUSDT = 'https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT'
mongoDB_URI = 'mongodb+srv://sysadmin:Nerv-19830228@cluster0.9wtze.mongodb.net/?retryWrites=true&w=majority'
url = 'https://api.binance.com/api/v3/klines'
symbol = 'BTCUSDT'
interval = '1h'


@app.route('/')
def hello_world():
  return '<h1>Hello, World!</h1>'

@app.route('/login')
def login():
     return render_template('login.html', Name='Adam LO')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
  cryptoBalanceList = []
  CONNECTION_STRING = mongoDB_URI
  client = pymongo.MongoClient(CONNECTION_STRING)
  db = client.get_database('VTC_individual_project')
  cryptoBalance = pymongo.collection.Collection(db, 'cryptoBalance')
  date = cryptoBalance.find()
  # ethBalance = mongo.VTC_individual_project.cryptoBalance.find()
  BTCUSDTjson = requests.get(BTCUSDT).text
  ETHUSDTjson = requests.get(ETHUSDT).text
  BTCUSDTdata = json.loads(BTCUSDTjson)
  ETHUSDTdata = json.loads(ETHUSDTjson)
  BTCUSDTprice = round(float(BTCUSDTdata['price']),2)
  ETHUSDTprice = round(float(ETHUSDTdata['price']),2)
  print(BTCUSDTprice)
  print(ETHUSDTprice)
  for doc in date:
    # print(doc)
    cryptoBalanceList.append(doc['balance'])
    
  print(cryptoBalanceList)
  cryptoBalanceLatest = cryptoBalanceList[-1]
  return render_template('dashboard.html', Name='Adam LO', BTCUSDTprice=BTCUSDTprice, ETHUSDTprice=ETHUSDTprice, cryptoBalanceLatest=cryptoBalanceLatest)
  
@app.route('/totalcryptobalance')
def cryptoBalanceChart():
  data = [
    ("2022-01-13",100036.7),
    ("2022-01-16",100036.7),
    ("2022-01-21",95151.21),
    ("2022-02-05",95275.93),
    ("2022-02-08",95277.4),
    ("2022-02-10",95278.87),
    ("2022-02-16",95280.35),
    ("2022-02-20",98088.83),
    ("2022-03-07",92025.83),
    ("2022-03-24",92056.72),
    ("2022-03-28",92087.63),
    ("2022-03-30",92118.56),
    ("2022-04-02",92149.52),
    ("2022-04-04",92149.52),
    ("2022-04-07",92149.52)
  ]
  labels = [row[0] for row in data]
  values = [row[1] for row in data]
  return render_template("totalCryptoBalance.html", labels=labels, values=values)

@app.route('/macdbalance')
def maceBalanceChart():
  data = [
    ("2022-01-21",45114.55),
    ("2022-02-20",47923.03),
    ("2022-03-07",41860.03),
    ("2022-04-07",47816.84)
  ]
  labels = [row[0] for row in data]
  values = [row[1] for row in data]
  print(type(data))
  print(type(labels))
  return render_template("maceBalance.html", labels=labels, values=values)

@app.route('/martingalebalance')
def martingaleBalanceChart():
  data = [
    ("2022-01-13",50036.66),
    ("2022-02-05",50161.38),
    ("2022-02-08",50164.32),
    ("2022-02-10",50164.32),
    ("2022-02-16",50165.8),
    ("2022-03-24",50196.69),
    ("2022-03-28",50227.6),
    ("2022-03-30",50258.53),
    ("2022-04-02",50289.49),
    ("2022-04-04",50320.46)
  ]
  labels = [row[0] for row in data]
  values = [row[1] for row in data]
  return render_template("martingaleBalance.html", labels=labels, values=values)

@app.route('/btc1day')
def btc1day():
  labels=[]
  url = 'https://api.binance.com/api/v3/klines'
  symbol = 'BTCUSDT'
  interval = '1d'
  par = {'symbol': symbol, 'interval': interval, 'limit':1000}
  data = pd.DataFrame(json.loads(requests.get(url, params= par).text))
  data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
  data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.datetime]
  data=data.astype(float)
  onlyClose = pd.DataFrame(data, columns= ['close'])
  onlyDate = pd.DataFrame(data, columns= ['datetime'])
  onlyCloseList = list(onlyClose['close']) 
  onlyDateList = list(onlyDate['datetime']) 
  # Change the timestamp to be date
  for x in onlyDateList:
    labels.append(dt.datetime.fromtimestamp(x/1000.0).strftime('%Y-%m-%d'))
  values = onlyCloseList
  return render_template("btc1day.html", labels=labels, values=values)

@app.route('/eth1day')
def eth1day():
  labels=[]
  url = 'https://api.binance.com/api/v3/klines'
  symbol = 'ETHUSDT'
  interval = '1d'
  par = {'symbol': symbol, 'interval': interval, 'limit':1000}
  data = pd.DataFrame(json.loads(requests.get(url, params= par).text))
  data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
  data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.datetime]
  data=data.astype(float)
  onlyClose = pd.DataFrame(data, columns= ['close'])
  onlyDate = pd.DataFrame(data, columns= ['datetime'])
  onlyCloseList = list(onlyClose['close']) 
  onlyDateList = list(onlyDate['datetime']) 
  # Change the timestamp to be date
  for x in onlyDateList:
    labels.append(dt.datetime.fromtimestamp(x/1000.0).strftime('%Y-%m-%d'))
  values = onlyCloseList
  return render_template("eth1day.html", labels=labels, values=values)

@app.route('/btc1hour')
def btc1hour():
  labels=[]
  url = 'https://api.binance.com/api/v3/klines'
  symbol = 'BTCUSDT'
  interval = '1h'
  par = {'symbol': symbol, 'interval': interval, 'limit':1000}
  data = pd.DataFrame(json.loads(requests.get(url, params= par).text))
  data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
  data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.datetime]
  data=data.astype(float)
  onlyClose = pd.DataFrame(data, columns= ['close'])
  onlyDate = pd.DataFrame(data, columns= ['datetime'])
  onlyCloseList = list(onlyClose['close']) 
  onlyDateList = list(onlyDate['datetime']) 
  # Change the timestamp to be date
  for x in onlyDateList:
    labels.append(dt.datetime.fromtimestamp(x/1000.0).strftime('%Y-%m-%d %H:%M'))
  values = onlyCloseList
  return render_template("btc1hour.html", labels=labels, values=values)

@app.route('/eth1hour')
def eth1hour():
  labels=[]
  url = 'https://api.binance.com/api/v3/klines'
  symbol = 'ETHUSDT'
  interval = '1h'
  par = {'symbol': symbol, 'interval': interval, 'limit':1000}
  data = pd.DataFrame(json.loads(requests.get(url, params= par).text))
  data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
  data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.datetime]
  data=data.astype(float)
  onlyClose = pd.DataFrame(data, columns= ['close'])
  onlyDate = pd.DataFrame(data, columns= ['datetime'])
  onlyCloseList = list(onlyClose['close']) 
  onlyDateList = list(onlyDate['datetime']) 
  # Change the timestamp to be date
  for x in onlyDateList:
    labels.append(dt.datetime.fromtimestamp(x/1000.0).strftime('%Y-%m-%d %H:%M'))
  values = onlyCloseList
  return render_template("eth1hour.html", labels=labels, values=values)

app.run(host='0.0.0.0', port=8080)