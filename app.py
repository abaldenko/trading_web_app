from flask import Flask, render_template, request
import os
import requests
import pandas as pd
from json import dumps, loads
from StringIO import StringIO
from datetime import datetime, timedelta

app = Flask(__name__)





@app.route('/')
def index():
  return render_template('index.html')

@app.route('/get_symbols')
def get_symbols():
  # if the symbol file doesn't exist
  # then download it
  symbol_path = 'static/symbols.csv'
  if not os.path.isfile(symbol_path): 
    os.system('mkdir -p static')
    url = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
    df = pd.read_csv(url)
    df.to_csv(symbol_path)

  # load the csv and reformat 
  df = pd.read_csv(symbol_path)
  df['text'] = df['Symbol']
  df['id'] = df.index
  return df[['text','id']].to_json(orient='records')

@app.route('/parameter_estimates', methods=["POST"])
def parameter_estimates():
  # TODO: build a real forecasting methodology ;)
  # right now i'm doing this super naive thing:
  #   get mean, std for historical daily close diff
  #   and forecast that
  #   close(tomorrow) = close(today) + N(mean,std)


  # get the symbol from the dropdown
  symbol=request.data[1:-1] # they have quotes
  
  # parameters for the request
  # symbol="YHOO"
  today = datetime.today()
  yesterday = today - timedelta(days=1)
  day = today.day
  month = today.month
  year = today.year

  # get open, close, etc. for some past time perios
  url = """http://ichart.finance.yahoo.com/table.csv?\
s={symbol}\
&d={d}\
&e={e}\
&f={f}\
&g=d\
&a=1\
&b=12\
&c=2015\
&ignore=.csv""".format(symbol=symbol, d=str(month-1), e=today, f=year)
  response = requests.get(url)
  raw_csv = StringIO(response.content)
  df = pd.read_csv(raw_csv)
  # print df.head()

  # calculate mean, std of daily differences
  # NOTE: assumes yesterday has an entry
  #       so it won't work for sundays on mondays right now
  mean_diff = df.Close.diff().mean()
  today_close = df[df.Date==yesterday.strftime('%Y-%m-%d')].Close.values[0]
  mean = today_close + mean_diff 
  std = df.Close.diff().std()
  
  # result
  result = {'mean':mean, 'std':std}
  print result

  return dumps(result) 

if __name__ == "__main__":
  app.run(debug=True, host='localhost',port=1234)