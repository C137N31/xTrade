from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import requests
import time
import pandas as pd
#pd.set_option('expand_frame_repor', False)

BASE_URL = 'https://api.binance.com'
limit = 1000

kline = '/api/v1/klines'

kline_url = BASE_URL + kline + '?' + 'symbol=BTCUSDT&interval=1m&limit=' + str(limit)

end_time   = int(time.time() // 60 * 60 * 1000)

resp = requests.get(kline_url)
#print(resp.json())
df = pd.DataFrame(resp.json(),
                  columns={'open_time':0, 'Open':1, 'High':2, 'Low':3, 'Close':4, 'Volume':5, 'close_time':6, 'quote_volume':7,
                                      'trades':8, 'taker_base_volume':9, 'taker_quote_volume':10, 'ignore':11})
# 0-open time, 1-open, 2-high, 3-low, 4-close, 5-volume, 6-close time, 7-quote asset volume, 8-number of traders, 
# 9-taker buy base asset volume, 10-taker buy quote asset volume, 11-ignore
df['Date'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)
df['Adj Close'] = df['Close']
df5 = df.loc[:,['Date','Open','High','Low','Close','Adj Close','Volume']]
df5.set_index('Date', inplace=True)
#print(df5)
df5.to_csv('DataFeed/BTC' + str(end_time) + '.csv')

exit()

start_time = int(end_time  - limit * 60 * 1000)

while True:
    url = BASE_URL + kline + '?' + 'symbol=BTCUSDT&interval=1M&limit=' + str(limit) + '&startTime=' + str(start_time) + '&endTime=' + str(end_time)
    resp = requests.get(url)
    data = resp.json()
    df = pd.DataFrame(data, columns={'open_time':0, 'Open':1, 'High':2, 'Low':3, 'Close':4, 'Volume':5, 'close_time':6, 'quote_volume':7,
                                      'trades':8, 'taker_base_volume':9, 'taker_quote_volume':10, 'ignore':11})
    
    df['open_time'] = df['open_time'].apply(lambda x: (x // 60) * 60 * 1000)
    df['Adj Close'] = df['Close']
    df['Date'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)
    df['Date'] = df['Date'].apply(lambda x: str(x)[0:19]) # 2020-10-16 12:34:56
    df.drop_duplicates(subset=['open_time','close_time','quote_volume','trades','taker_base_volume','taker_quote_volume','ignore'], inplace=True)
    
    for index, item in df.iterrows():
        try:
            dt = pd.to_datetime(item['open_time'], unit='ms')
            dt = datetime.datetime.strptime(str(dt), '%Y-%m-%d %H:%M:%S')
        except:
            dt = pd.to_datetime(item['open_time'], unit='ms')
    
    df.set_index('Date', inplace=True)
    df.to_csv('DataFeed/BTC' + str(end_time) + '.csv')

    if len(df) < 1000:
        break

    end_time = start_time
    start_time = int(end_time  - limit * 60 * 1000)
exit()
