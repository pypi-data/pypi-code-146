import datetime as dt
import pandas as pd
import requests
import json
import math
from dateutil import parser

import numpy as np
from datetime import timedelta
import os

from cryptotoolbox.file_saver import dropbox_file_saver
import time

from cryptotoolbox.bot import binance_bot
from datetime import timedelta

import datetime
# CryptoCompare

sleeping_time = 0.5

def to_unix(s):
    if isinstance(s, str):
        dt_object = parser.parse(s)
    else:
        dt_object = s
    return int(dt_object.replace(tzinfo=dt.timezone.utc).timestamp())


def to_iso(ts):
    if type(ts) == str:
        ts = parser.parse(ts)
        return ts.replace(tzinfo=dt.timezone.utc).isoformat()
    else:
        return dt.datetime.utcfromtimestamp(ts).replace(tzinfo=dt.timezone.utc).isoformat()


def assess_rsp(response):
    if response.status_code != 200:
        raise RuntimeError('Bad gateway:', response.status_code)
    elif isinstance(response.json(), list) and len(response.json()) == 0:
        raise ValueError('No data')
    # elif response.json()['Response'] != 'Success':
    # raise RuntimeError(response.json()['Message'])


def extract_df(optype, precision, r):
    if optype == 'OHLC':
        try:
            tmp = r.json()['Data']['Data']
            return pd.DataFrame(tmp)
        except KeyError:
            print(r.json()['Message'])
    else:
        return pd.DataFrame(r.json()['Data'])


class CryptoCompare:
    def __init__(self, api_key=None, exchange=None):
        self.api_key = api_key
        self.e = exchange

    def get(self, optype, currency, startdate, enddate, precision):
        timedelta = to_unix(enddate) - to_unix(startdate)
        ts = to_unix(enddate)
        precision_dct = {'1h': 3600, 'hour': 3600, 'minute': 60}
        endpoint_dct = {'OHLC': {'url': 'https://min-api.cryptocompare.com/data/v2/histo{}'.format(precision),
                                 'params': {'fsym': currency, 'tsym': 'USD', 'limit': '2000', 'aggreggate': '1',
                                            'toTs': ts}},
                        'OBL2': {'url': 'https://min-api.cryptocompare.com/data/ob/l2/snapshot',
                                 'params': {'api_key', self.api_key}},
                        'HVOL': {'url': 'https://min-api.cryptocompare.com/data/symbol/histohour',
                                 'params': {'fsym': currency, 'tsym': 'USD', 'limit': '500', 'toTs': ts}}}

        if optype == 'OHLC' and precision == 'minute':
            endpoint_dct[optype]['params']['api_key'] = '{' + self.api_key + '}'

        runs, rest = divmod(timedelta / precision_dct[precision], int(endpoint_dct[optype]['params']['limit']))
        runs, rest = int(runs), str(int(math.ceil(rest)))
        output = pd.DataFrame()
        for run in range(runs):
            r = requests.request("GET", endpoint_dct[optype]['url'], params=endpoint_dct[optype]['params'])
            assess_rsp(r)
            output = pd.concat([output, extract_df(optype, precision, r)])
            endpoint_dct[optype]['params'].update({'toTs': output.time.min()})

        if rest != '0':
            endpoint_dct[optype]['params'].update({'limit': rest})
            print(endpoint_dct[optype]['params'])
            r = requests.request("GET", endpoint_dct[optype]['url'], params=endpoint_dct[optype]['params'])
            assess_rsp(r)
            output = pd.concat([output, extract_df(optype, precision, r)])

        output['timestamp'] = output.time.apply(lambda x: to_iso(x))
        output = output.set_index('timestamp', drop=True).sort_index().drop_duplicates()
        return output


def binance_get_histo_future_balance_snapshot(api, p, request_date):
    bot = binance_bot.NaPoleonBinanceFutureBot(api, p)
    return bot.get_futures_balance_snapshot(request_date)

def binance_get_future_balance_history(api, p, start_time, end_time):
    bot = binance_bot.NaPoleonBinanceFutureBot(api, p)
    temp_time = start_time
    valos = None
    while temp_time < end_time:
        temp_time = min(end_time, start_time+timedelta(int(30)))
        print(f'requesting between {start_time} and {temp_time}')
        temp_valos = bot.get_futures_balance_history(start_time, temp_time)
        start_time = temp_time
        if valos is None:
            valos = temp_valos.copy()
        else:
            valos = pd.concat([temp_valos, valos])

    valos['date'] = pd.to_datetime(valos['date'])
    valos = valos.sort_values(by=['date'])
    return valos

    # deltadays = end_time - start_time
    # middletime = start_time+ timedelta(int(deltadays.days/2))
    # first_valos = bot.get_futures_balance_history(start_time, middletime)
    # second_valos = bot.get_futures_balance_history(middletime, end_time)
    # return pd.concat([first_valos,second_valos])


def binance_get_futures_transfer_histo(api, p, start_time, end_time):
    bot = binance_bot.NaPoleonBinanceFutureBot(api, p)
    return bot.get_futures_transfer_history(['USDT', 'BNB'], start_time, end_time)

def binance_get_position_risk(api, p, start_time, end_time):
    bot = binance_bot.NaPoleonBinanceFutureBot(api, p)
    positions_df = pd.DataFrame(bot.get_future_position_risk())
    positions_df = positions_df[abs(positions_df['positionAmt'].astype(float)) > 0].copy()
    return positions_df

def binance_get_position_margin_history(api, p, start_time, end_time):
    bot = binance_bot.NaPoleonBinanceFutureBot(api, p)
    return bot.get_futures_positions_margin_change_history(['BTCUSDT','ETHUSDT'], start_time, end_time)


def request_day_data_paquet(url, me_ts, ssj):
    r = requests.get(url.format(ssj, me_ts))
    dataframe = None
    try:
        dataframe = pd.DataFrame(json.loads(r.text)['Data'])
    except Exception as e:
        print('no data')
    return dataframe

def cryptocompare_get(ssj ='USDT',ssj_against='USD', daily_crypto_starting_day=None, daily_crypto_ending_day=None, aggreg ='1d'):
    assert aggreg == '1d'
    dates_stub = daily_crypto_starting_day.strftime('%d_%b_%Y') + '_' + daily_crypto_ending_day.strftime('%d_%b_%Y')

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    hour = datetime.datetime.utcnow().hour
    ts = datetime.datetime(year, month, day, tzinfo=datetime.timezone.utc).timestamp() + hour * 3600
    ts1 = ts - 2001 * 3600 * 24
    ts2 = ts1 - 2001 * 3600 * 24
    ts3 = ts2 - 2001 * 3600 * 24
    ts4 = ts3 - 2001 * 3600 * 24
    ts5 = ts4 - 2001 * 3600 * 24
    ts6 = ts5 - 2001 * 3600 * 24
    ts7 = ts6 - 2001 * 3600 * 24
    ts8 = ts7 - 2001 * 3600 * 24

    print('Loading data')
    day_url_request = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym=' + ssj_against + '&toTs={}&limit=2000'
    dataframe = None
    for me_timestamp in [ts8, ts7, ts6, ts5, ts4, ts3, ts2, ts1, ts]:
        print('waiting')
        df = request_day_data_paquet(day_url_request, me_timestamp, ssj)
        if df is not None:
            if dataframe is not None:
                dataframe = dataframe.append(df, ignore_index=True)
            else:
                dataframe = df.copy()

    dataframe['time'] = pd.to_datetime(dataframe['time'], unit='s')
    dataframe = dataframe.sort_values(by=['time'])
    dataframe = dataframe.rename(columns={"time": "date"}, errors="raise")
    dataframe = dataframe.set_index(dataframe['date'])
    dataframe = dataframe.drop(columns=['date'])
    print('size fetched')
    print(dataframe.shape)
    dataframe = dataframe[dataframe.index >= daily_crypto_starting_day]
    dataframe = dataframe[dataframe.index <= daily_crypto_ending_day]
    print('size filtered after ' + str(daily_crypto_starting_day))
    print(dataframe.shape)
    return dataframe


#https://binance-docs.github.io/apidocs/spot/en/#wallet-endpoints
def binance_get(api, p, type_, start_time, end_time = None, symbol = None, aggreg = None):
  '''
  Accepted types: futures_funding, all_futures_orders, futures_klines (aggreg = 1H), spot_klines (aggreg = '1m', '1h')
  Accepted start_time, end_time: datetime ns
  '''

  from binance.client import Client
  import json
  import time

  client = Client(api, p)
  assert type_ in ['trade_history', 'futures_funding', 'futures_klines', 'wallet_history', 'spot_klines'], 'Wrong type_: trade_history, futures_funding, futures_klines, wallet_history available'
  if aggreg is not None:
    assert aggreg in ['1h', '1m', '5m','30m', '1d','12h'], 'Wrong aggreg_: 1m, 1h available'
    dct_cvt = {'1m': Client.KLINE_INTERVAL_1MINUTE, '5m': Client.KLINE_INTERVAL_5MINUTE, '30m': Client.KLINE_INTERVAL_30MINUTE, '1h':Client.KLINE_INTERVAL_1HOUR, '1d':Client.KLINE_INTERVAL_1DAY, '12h':Client.KLINE_INTERVAL_12HOUR}
    aggreg = dct_cvt[aggreg]

  output = pd.DataFrame()
  if type_ == 'futures_funding' and symbol is not None:
    startTime = int(start_time.timestamp()*1000)
    endTime = int(end_time.timestamp()*1000)
    while startTime<endTime:
      time_col = 'fundingTime'
      try:
        print(f'requesting funding {time_col} between {startTime} and {endTime}')
        print(f'requesting {type(startTime)} {type(endTime)} {startTime} {endTime}')
        startTime =int(startTime)
        endTime=int(endTime)
        output = pd.concat([output, pd.DataFrame(client.futures_funding_rate(symbol = symbol, startTime = startTime, endTime = endTime, limit = 1000))])
        time.sleep(sleeping_time)
      except json.decoder.JSONDecodeError:
        print('Could not convert to Json. Passing @time:', startTime)
      endTime = output.loc[:,time_col].min()
  elif type_ == 'trade_history':
    print('Retrieving all orders in 3H slices. Stay put.')
    time_col = 'time'
    drange = list(pd.date_range(start_time, end_time, freq ='3H'))
    for _ in range(len(drange)-1):
      startTime = int(drange[_].timestamp()*1000)
      endTime = int(drange[_+1].timestamp()*1000)
      try:
        print(f'requesting trades {time_col} between {startTime} and {endTime}')
        time.sleep(sleeping_time)
        print(f'requesting {type(startTime)} {type(endTime)} {startTime} {endTime}')
        startTime =int(startTime)
        endTime=int(endTime)
        tmp = pd.DataFrame(client.futures_account_trades(limit = 1000, startTime = startTime, endTime = endTime))
        output = pd.concat([output, tmp])
        time.sleep(sleeping_time)
      except json.decoder.JSONDecodeError:
        print('Could not convert to Json. Passing @time:', startTime)
        continue
    time.sleep(1)
  elif (type_ == 'futures_klines') and (symbol is not None) and (aggreg is not None):
    startTime = int(start_time.timestamp()*1000)
    endTime = int(end_time.timestamp()*1000)
    previousStartTime = startTime

    while startTime<endTime:
      time_col = 'time'
      try:
        print(f'requesting futures_kline {time_col} between {startTime} and {endTime}')
        time.sleep(sleeping_time)
        print(f'requesting {type(startTime)} {type(endTime)} {startTime} {endTime}')
        startTime =int(startTime)
        endTime=int(endTime)
        output = pd.concat([output, pd.DataFrame(client.futures_klines(symbol = symbol, interval = aggreg, startTime = startTime, endTime = endTime, limit = 1000))])
        time.sleep(sleeping_time)
      except json.decoder.JSONDecodeError:
        print('Could not convert to Json. Passing @time:', startTime)
      #futures_kline
      previousStartTime = startTime
      if output.empty:
          break
      startTime = output.loc[:, 0].max()
      if previousStartTime == startTime :
          break

    output.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_vol', 'ntrades', 'takerbuy_base_asset_vol', 'takerbuy_quote_asset_vol', 'ignore']
  elif type_ == 'wallet_history':
    startTime = int(start_time.timestamp()*1000)
    endTime = int(end_time.timestamp()*1000)
    previousStartTime = startTime
    while startTime<endTime:
      time_col = 'time'
      try:
        print(f'requesting income history {time_col} between {startTime} and {endTime}')
        time.sleep(sleeping_time)
        print(f'requesting {type(startTime)} {type(endTime)} {startTime} {endTime}')
        startTime =int(startTime)
        endTime=int(endTime)
        output = pd.concat([output, pd.DataFrame(client.futures_income_history(startTime = startTime, endTime=endTime, limit = 1000))])
        time.sleep(sleeping_time)

      except json.decoder.JSONDecodeError:
        print('Could not convert to Json. Passing @time:', startTime)
      # fincome histo
      previousStartTime = startTime
      startTime = output.loc[:, 'time'].max()
      if previousStartTime == startTime :
          break
  elif (type_ == 'spot_klines')  and (symbol is not None) and (aggreg is not None):
    startTime = int(start_time.timestamp()*1000)
    endTime = int(end_time.timestamp()*1000)
    previousStartTime = startTime

    while startTime<endTime:
      time_col = 'time'
      try:
        print(f'requesting income historical kline {time_col} between {startTime} and {endTime}')
        time.sleep(sleeping_time)
        print(f'requesting {type(startTime)} {type(endTime)} {startTime} {endTime}')
        startTime =int(startTime)
        endTime=int(endTime)
        output = pd.concat([output, pd.DataFrame(client.get_historical_klines(symbol = symbol, interval = aggreg, start_str = startTime, end_str = endTime, limit = 500))])
      except json.decoder.JSONDecodeError:
        print('Could not convert to Json. Passing @time:', startTime)
      previousStartTime = startTime
      startTime = output.loc[:, 0].max()
      if previousStartTime == startTime :
          break

    output.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_vol', 'ntrades', 'takerbuy_base_asset_vol', 'takerbuy_quote_asset_vol', 'ignore']
  else:
    print('Wrong param combination.')
    return
  output['ts'] = (output[time_col] / 1000).apply(lambda x: dt.datetime.utcfromtimestamp(x))
  output = output.sort_values(by='ts', ascending = True).drop_duplicates()
  print(type_, 'done. Shape:', output.shape)
  return output



def fetch_binance_ohlc(symbol = 'BTCUSDT', frequence = '1d', public_key = None, private_key= None, start_time= None, end_time= None, me_month=None, save_to_dropbox = False, dropbox_token = None, local_root_directory = './', trade_only_granularity = False, recompute_all=False, save_to_disk = True):
    print('fetching daily tezos')
    if recompute_all:
        binance_df = binance_get(public_key, private_key, 'spot_klines', start_time, end_time=end_time,
                                           symbol=symbol, aggreg=frequence)

        binance_df.index = pd.to_datetime(binance_df['ts'])
        binance_df['open'] = binance_df['open'].astype(float)
        binance_df['close'] = binance_df['close'].astype(float)
        binance_df['high'] = binance_df['high'].astype(float)
        binance_df['low'] = binance_df['low'].astype(float)
        if save_to_disk:
            save_equity_daily_data(data_df = binance_df, ticker = symbol, frequence=frequence, starting_date=start_time, running_date = end_time, local_root_directory = local_root_directory)
    else :
        try :
            filename = symbol + '_' + frequence + '_' + start_time.strftime('%d_%b_%Y') + '_' + end_time.strftime(
                '%d_%b_%Y') + '_daily_returns.pkl'
            binance_df = pd.read_pickle(local_root_directory + filename)
        except Exception as e :
            print(f'cant fetch data {e}')
            binance_df = binance_get(public_key, private_key, 'spot_klines', start_time, end_time=end_time,
                                     symbol=symbol, aggreg=frequence)

            binance_df.index = pd.to_datetime(binance_df['ts'])
            binance_df['open'] = binance_df['open'].astype(float)
            binance_df['close'] = binance_df['close'].astype(float)
            binance_df['high'] = binance_df['high'].astype(float)
            binance_df['low'] = binance_df['low'].astype(float)
            if save_to_disk:
                save_equity_daily_data(data_df=binance_df, ticker=symbol, frequence=frequence, starting_date=start_time,
                                   running_date=end_time, local_root_directory=local_root_directory)

    return binance_df

def save_equity_daily_data(data_df = None, ticker=None, frequence=None, provider = 'napoleon', starting_date=None,running_date=None,local_root_directory=None):
    filename = ticker + '_' + frequence + '_' + starting_date.strftime('%d_%b_%Y') + '_' + running_date.strftime(
        '%d_%b_%Y') + '_daily_returns.pkl'
    data_df.to_pickle(local_root_directory + filename)




