import numpy as np
import pandas as pd
import pandas_ta as ta
import warnings
warnings.filterwarnings('ignore')
from boto3 import client
import boto3
from datetime import datetime, date

class QuantPanda:

    def SimpleMovingAverageCrossover(df, simple_moving_avg, entry_price_condition):

        if type(simple_moving_avg) != int or type(entry_price_condition) !=str:
            print('Pass a integer not character')

        elif entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')
              
        else:    
            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])
 
            df['MovingAverage'] = df['Close'].rolling(window= simple_moving_avg).mean().round(2)

            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)

            
            df['MovingAverageSignal'] = np.where(df['Close'] > df['MovingAverage'], 1, -1)

            df['Signal'] = 0

            for j in range(len(df)):

                if df['MovingAverageSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == -3) :
                    df['Signal'].iloc[j] = 1

                elif df['MovingAverageSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == 3):
                    df['Signal'].iloc[j] = -1
                
                #short continue next day
                elif df['MovingAverageSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -2

                #continue short trade
                elif df['MovingAverageSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -2
                
                #exit short trade
                elif df['MovingAverageSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == -1 or df['Signal'].iloc[j-1] == -2):
                    df['Signal'].iloc[j] = -3

                #long continue next day
                elif df['MovingAverageSignal'].iloc[j] == 1  and df['Signal'].iloc[j-1] == 1:
                    df['Signal'].iloc[j] = 2

                #continue long trade
                elif df['MovingAverageSignal'].iloc[j] == 1 and df['Signal'].iloc[j-1] == 2:
                    df['Signal'].iloc[j] = 2
                
                #exit long trade
                elif df['MovingAverageSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 1 or df['Signal'].iloc[j-1] == 2):
                    df['Signal'].iloc[j] = 3


            df['Signal'] = df['Signal'].shift(1)

            """"Long trades"""
            long_entry_df = df.loc[ df['Signal'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['Signal'] == 3][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            """"Short Trades"""
            short_entry_df = df.loc[ df['Signal'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['Signal'] == -3][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)


    def ExponentialMovingAverageCrossover(df, exponential_moving_avg, entry_price_condition):

        if type(exponential_moving_avg) != int or type(entry_price_condition)!=str:
            print('Pass a integer not character')

        elif entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')

        else: 

            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])
            
            df['MovingAverage'] = df['Close'].ewm(span=exponential_moving_avg).mean().round(2)

            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)

            df['MovingAverageSignal'] = np.where(df['Close'] > df['MovingAverage'], 1, -1)

            df['Signal'] = 0

            for j in range(len(df)):

                if df['MovingAverageSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == -3) :
                    df['Signal'].iloc[j] = 1

                elif df['MovingAverageSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == 3):
                    df['Signal'].iloc[j] = -1
                
                #short continue next day
                elif df['MovingAverageSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -2

                #continue short trade
                elif df['MovingAverageSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -2
                
                #exit short trade
                elif df['MovingAverageSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == -1 or df['Signal'].iloc[j-1] == -2):
                    df['Signal'].iloc[j] = -3

                #long continue next day
                elif df['MovingAverageSignal'].iloc[j] == 1  and df['Signal'].iloc[j-1] == 1:
                    df['Signal'].iloc[j] = 2

                #continue long trade
                elif df['MovingAverageSignal'].iloc[j] == 1 and df['Signal'].iloc[j-1] == 2:
                    df['Signal'].iloc[j] = 2
                
                #exit long trade
                elif df['MovingAverageSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 1 or df['Signal'].iloc[j-1] == 2):
                    df['Signal'].iloc[j] = 3


            df['Signal'] = df['Signal'].shift(1)

            """"Long trades"""
            long_entry_df = df.loc[ df['Signal'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['Signal'] == 3][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            """"Short Trades"""
            short_entry_df = df.loc[ df['Signal'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['Signal'] == -3][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)


    def DoubleSimpleMovingAverageCrossover(df, fast_simple_moving_avg, slow_simple_moving_avg, entry_price_condition):

        if (type(fast_simple_moving_avg) != int) or type(slow_simple_moving_avg) != int or type(entry_price_condition)!=str:
            print('Pass a integer not character')

        elif entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')

        else:

            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])
            
            df['FastMovingAverage'] = df['Close'].rolling(window= fast_simple_moving_avg).mean().round(2)
            df['SlowMovingAverage'] = df['Close'].rolling(window= slow_simple_moving_avg).mean().round(2)

            df['MovingAverageSignal'] = np.where(df['FastMovingAverage'] > df['SlowMovingAverage'], 1, -1)

            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)

            df['Signal'] = 0

            for j in range(len(df)):

                if df['MovingAverageSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == -3) :
                    df['Signal'].iloc[j] = 1

                elif df['MovingAverageSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == 3):
                    df['Signal'].iloc[j] = -1
                
                #short continue next day
                elif df['MovingAverageSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -2

                #continue short trade
                elif df['MovingAverageSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -2
                
                #exit short trade
                elif df['MovingAverageSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == -1 or df['Signal'].iloc[j-1] == -2):
                    df['Signal'].iloc[j] = -3

                #long continue next day
                elif df['MovingAverageSignal'].iloc[j] == 1  and df['Signal'].iloc[j-1] == 1:
                    df['Signal'].iloc[j] = 2

                #continue long trade
                elif df['MovingAverageSignal'].iloc[j] == 1 and df['Signal'].iloc[j-1] == 2:
                    df['Signal'].iloc[j] = 2
                
                #exit long trade
                elif df['MovingAverageSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 1 or df['Signal'].iloc[j-1] == 2):
                    df['Signal'].iloc[j] = 3


            df['Signal'] = df['Signal'].shift(1)

            """"Long trades"""
            long_entry_df = df.loc[ df['Signal'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['Signal'] == 3][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            """"Short Trades"""
            short_entry_df = df.loc[ df['Signal'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['Signal'] == -3][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)

    def DoubleExponentialMovingAverageCrossover(df, fast_exponential_moving_avg, slow_exponential_moving_avg, entry_price_condition):

        if type(fast_exponential_moving_avg) != int or type(slow_exponential_moving_avg) != int or type(entry_price_condition)!=str:
            print('Pass a integer not character')

        elif entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')

        else:

            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])
            
            df['FastMovingAverage'] = df['Close'].ewm(span=fast_exponential_moving_avg).mean().round(2)
            df['SlowMovingAverage'] = df['Close'].ewm(span=slow_exponential_moving_avg).mean().round(2)

            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)

            df['MovingAverageSignal'] = np.where(df['FastMovingAverage'] > df['SlowMovingAverage'], 1, -1)

            df['Signal'] = 0

            for j in range(len(df)):

                if df['MovingAverageSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == -3) :
                    df['Signal'].iloc[j] = 1

                elif df['MovingAverageSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == 3):
                    df['Signal'].iloc[j] = -1
                
                #short continue next day
                elif df['MovingAverageSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -2

                #continue short trade
                elif df['MovingAverageSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -2
                
                #exit short trade
                elif df['MovingAverageSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == -1 or df['Signal'].iloc[j-1] == -2):
                    df['Signal'].iloc[j] = -3

                #long continue next day
                elif df['MovingAverageSignal'].iloc[j] == 1  and df['Signal'].iloc[j-1] == 1:
                    df['Signal'].iloc[j] = 2

                #continue long trade
                elif df['MovingAverageSignal'].iloc[j] == 1 and df['Signal'].iloc[j-1] == 2:
                    df['Signal'].iloc[j] = 2
                
                #exit long trade
                elif df['MovingAverageSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 1 or df['Signal'].iloc[j-1] == 2):
                    df['Signal'].iloc[j] = 3


            df['Signal'] = df['Signal'].shift(1)

            """"Long trades"""
            long_entry_df = df.loc[ df['Signal'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['Signal'] == 3][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            """"Short Trades"""
            short_entry_df = df.loc[ df['Signal'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['Signal'] == -3][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)



    def RelativeStrength(df, lookback_period, overbought_zone, oversold_zone, entry_price_condition):

        if (type(lookback_period) != int) or type(overbought_zone) != int or type(oversold_zone) != int or type(entry_price_condition)!=str:
            print('Pass a integer not character')

        elif entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')

        else:

            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])

            df['Rsi'] = ta.rsi(df['Close'], length = lookback_period)

            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)
            
            df['Signal'] = 0

            for j in range(len(df)):

                if df['Rsi'].iloc[j] > overbought_zone and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == -3) :
                    df['Signal'].iloc[j] = -1

                elif df['Rsi'].iloc[j] < oversold_zone and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == 3):
                    df['Signal'].iloc[j] = 1
                
                #short continue next day
                elif df['Rsi'].iloc[j] > oversold_zone and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -2

                #continue short trade
                elif df['Rsi'].iloc[j] > oversold_zone and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -2
                
                #exit short trade
                elif df['Rsi'].iloc[j] <= oversold_zone and (df['Signal'].iloc[j-1] == -1 or df['Signal'].iloc[j-1] == -2):
                    df['Signal'].iloc[j] = -3

                #long continue next day
                elif df['Rsi'].iloc[j] < overbought_zone  and df['Signal'].iloc[j-1] == 1:
                    df['Signal'].iloc[j] = 2

                #continue long trade
                elif df['Rsi'].iloc[j] < overbought_zone and df['Signal'].iloc[j-1] == 2:
                    df['Signal'].iloc[j] = 2
                
                #exit long trade
                elif df['Rsi'].iloc[j] >= overbought_zone and (df['Signal'].iloc[j-1] == 1 or df['Signal'].iloc[j-1] == 2):
                    df['Signal'].iloc[j] = 3


            df['Signal'] = df['Signal'].shift(1)

            """"Long trades"""
            long_entry_df = df.loc[ df['Signal'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['Signal'] == 3][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            """"Short Trades"""
            short_entry_df = df.loc[ df['Signal'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['Signal'] == -3][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)


    def ADX(df, smoothing_length, threshold, entry_price_condition):

        if (type(smoothing_length) != int) or type(threshold) != int or type(entry_price_condition)!=str:
            print('Pass a integer not character')

        elif entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')

        else:

            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])

            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)

            df[['Adx', 'Dmp', 'Dmn']] = ta.adx(df['High'], df['Low'], df['Close'], length =smoothing_length)

            df['threshold'] = threshold

            #long trading signals
            df['DmpSignal'] = np.where(df['Dmp'] > 25 , 1, 0)
            df['LongPosition'] = df['DmpSignal'].diff()

            df['DmpSignal'] = df['DmpSignal'].shift(1)

            long_entry_df = df.loc[ df['LongPosition'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['LongPosition'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            #short trading signals
            df['DmnSignal'] = np.where(df['Dmn'] < 25 , 1, 0)
            df['ShortPosition'] = df['DmnSignal'].diff()

            df['DmnSignal'] = df['DmnSignal'].shift(1)

            short_entry_df = df.loc[ df['ShortPosition'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['ShortPosition'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)


    def WilliamRIndicator(df, lookback_period, overbought_zone, oversold_zone, entry_price_condition):

        if (type(lookback_period) != int) or type(overbought_zone) != int or (type(oversold_zone) != int) or type(entry_price_condition)!=str:
            print('Pass a integer not character')

        elif entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')

        else:

            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])

            df['WillR'] = ta.willr(df['High'], df['Low'], df['Close'],  length = lookback_period)

            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)
 
            df['Signal'] = 0

            for j in range(len(df)):

                if df['WillR'].iloc[j] > overbought_zone and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == -3) :
                    df['Signal'].iloc[j] = -1

                elif df['WillR'].iloc[j] < oversold_zone and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == 3):
                    df['Signal'].iloc[j] = 1
                
                #short continue next day
                elif df['WillR'].iloc[j] > oversold_zone and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -2

                #continue short trade
                elif df['WillR'].iloc[j] > oversold_zone and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -2
                
                #exit short trade
                elif df['WillR'].iloc[j] <= oversold_zone and (df['Signal'].iloc[j-1] == -1 or df['Signal'].iloc[j-1] == -2):
                    df['Signal'].iloc[j] = -3

                #long continue next day
                elif df['WillR'].iloc[j] < overbought_zone  and df['Signal'].iloc[j-1] == 1:
                    df['Signal'].iloc[j] = 2

                #continue long trade
                elif df['WillR'].iloc[j] < overbought_zone and df['Signal'].iloc[j-1] == 2:
                    df['Signal'].iloc[j] = 2
                
                #exit long trade
                elif df['WillR'].iloc[j] >= overbought_zone and (df['Signal'].iloc[j-1] == 1 or df['Signal'].iloc[j-1] == 2):
                    df['Signal'].iloc[j] = 3


            df['Signal'] = df['Signal'].shift(1)

            """"Long trades"""
            long_entry_df = df.loc[ df['Signal'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['Signal'] == 3][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            """"Short Trades"""
            short_entry_df = df.loc[ df['Signal'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['Signal'] == -3][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)


    def ParabolicStopAndReverse(df, acceleration_factor, max_acceleration_factor, entry_price_condition):

        if (type(acceleration_factor) != float) or type(max_acceleration_factor) != float or type(entry_price_condition)!=str:
            print('Pass a integer not character')

        elif entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')

        else:

            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])

            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)

            df[['lower_band', 'upper_band', 'af', 'condition']] = ta.psar(df['High'], df['Low'], df['Close'], af= acceleration_factor, max_af= max_acceleration_factor)

            df['lower_band'] = df['lower_band'].replace(np.nan, -1)
            df['upper_band'] = df['upper_band'].replace(np.nan, 1)

            df.loc[ df['lower_band'] == -1, 'ParabolicSignal'] = -1
            df.loc[ df['upper_band'] == 1, 'ParabolicSignal'] = 1

            df['Signal'] = 0

            for j in range(len(df)):

                if df['ParabolicSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == -3) :
                    df['Signal'].iloc[j] = 1

                elif df['ParabolicSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == 3):
                    df['Signal'].iloc[j] = -1
                
                #short continue next day
                elif df['ParabolicSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -2

                #continue short trade
                elif df['ParabolicSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -2
                
                #exit short trade
                elif df['ParabolicSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == -1 or df['Signal'].iloc[j-1] == -2):
                    df['Signal'].iloc[j] = -3

                #long continue next day
                elif df['ParabolicSignal'].iloc[j] == 1 and df['Signal'].iloc[j-1] == 1:
                    df['Signal'].iloc[j] = 2

                #continue long trade
                elif df['ParabolicSignal'].iloc[j] == 1 and df['Signal'].iloc[j-1] == 2:
                    df['Signal'].iloc[j] = 2
                
                #exit long trade
                elif df['ParabolicSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 1 or df['Signal'].iloc[j-1] == 2):
                    df['Signal'].iloc[j] = 3
            
            df['Signal'] = df['Signal'].shift(1)

            """"Long trades"""
            long_entry_df = df.loc[ df['Signal'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['Signal'] == 3][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            """"Short Trades"""
            short_entry_df = df.loc[ df['Signal'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['Signal'] == -3][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)


    def MovingAvergeConvergenceDivergence(df, fast_length, slow_length, signal_length, entry_price_condition):

        if (type(fast_length) != int) or type(slow_length) != int or (type(signal_length) != int) or type(entry_price_condition)!=str:
            print('Pass a integer not character')

        elif entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')

        else:

            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])

            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)


            df[['fast_moving', 'histogram', 'slow_moving']] = ta.macd(df['Close'], fast=fast_length, slow=slow_length, signal=signal_length)

            df['MacdSignal'] = np.where(df['histogram'] >=0 , 1 , -1)

            df['Signal'] = 0

            for j in range(len(df)):

                if df['MacdSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == -3) :
                    df['Signal'].iloc[j] = 1

                elif df['MacdSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == 3):
                    df['Signal'].iloc[j] = -1
                
                #short continue next day
                elif df['MacdSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -2

                #continue short trade
                elif df['MacdSignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -2
                
                #exit short trade
                elif df['MacdSignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == -1 or df['Signal'].iloc[j-1] == -2):
                    df['Signal'].iloc[j] = -3

                #long continue next day
                elif df['MacdSignal'].iloc[j] == 1 and df['Signal'].iloc[j-1] == 1:
                    df['Signal'].iloc[j] = 2

                #continue long trade
                elif df['MacdSignal'].iloc[j] == 1 and df['Signal'].iloc[j-1] == 2:
                    df['Signal'].iloc[j] = 2
                
                #exit long trade
                elif df['MacdSignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 1 or df['Signal'].iloc[j-1] == 2):
                    df['Signal'].iloc[j] = 3
            
            df['Signal'] = df['Signal'].shift(1)

            """"Long trades"""
            long_entry_df = df.loc[ df['Signal'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['Signal'] == 3][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            """"Short Trades"""
            short_entry_df = df.loc[ df['Signal'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['Signal'] == -3][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)


    def BollingerBands(df, lookback_period, std_dev, entry_price_condition):

        if (type(lookback_period) != int) or type(std_dev) != int or type(entry_price_condition)!=str:
            print('Pass a integer not character')

        elif entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')

        else:

            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])

            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)

            df[['lower_bollinger', 'moving_average', 'upper_bollinger','std']] = ta.bbands(df['Close'], length= lookback_period, std= std_dev)

            df['Signal'] = 0

            for j in range(len(df)):

                #generate long signal
                if df['Close'].iloc[j] > df['upper_bollinger'].iloc[j] and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == -3):
                    df['Signal'].iloc[j] = 1

                #generate short signal
                elif df['Close'].iloc[j] < df['lower_bollinger'].iloc[j] and (df['Signal'].iloc[j-1]==0 or df['Signal'].iloc[j-1] == 3):
                    df['Signal'].iloc[j] = -1

                #convert buy signal to  long positional signal
                elif df['Close'].iloc[j] >= df['moving_average'].iloc[j] and df['Signal'].iloc[j-1] ==1:
                    df['Signal'].iloc[j] = 2

                #carry forward long positional signal
                elif df['Close'].iloc[j] >= df['moving_average'].iloc[j] and df['Signal'].iloc[j-1] ==2:
                    df['Signal'].iloc[j] = 2

                #exit long positional signal
                elif df['Close'].iloc[j] < df['moving_average'].iloc[j] and df['Signal'].iloc[j-1] ==2:
                    df['Signal'].iloc[j] = 3

                #exit long immediate signal
                elif df['Close'].iloc[j] < df['moving_average'].iloc[j] and df['Signal'].iloc[j-1] ==1:
                    df['Signal'].iloc[j] = 3

                #convert short signal to short positional signal
                elif df['Close'].iloc[j] <= df['moving_average'].iloc[j] and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -2

                #carry forward short positional signal
                elif df['Close'].iloc[j] <= df['moving_average'].iloc[j] and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -2

                #exit short positional signal
                elif df['Close'].iloc[j] > df['moving_average'].iloc[j] and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -3

                #exit short immediate signal
                elif df['Close'].iloc[j] > df['moving_average'].iloc[j] and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -3

            df['Signal'] = df['Signal'].shift(1)

            """"Long trades"""
            long_entry_df = df.loc[ df['Signal'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['Signal'] == 3][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            """"Short Trades"""
            short_entry_df = df.loc[ df['Signal'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['Signal'] == -3][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)


    def DonchianChannels(df, lookback_period, entry_price_condition):

        if (type(lookback_period) != int) or type(entry_price_condition)!=str:
            print('Pass a integer not character')

        elif entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')

        else:

            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])

            df['WillR'] = ta.willr(df['High'], df['Low'], df['Close'],  length = lookback_period)

            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)

            df[['lower_band', 'mid_band', 'upper_band']] = ta.donchian(df['High'], df['Low'], lower_length= lookback_period, upper_length= lookback_period)

            df[['lower_band', 'mid_band', 'upper_band']] = df[['lower_band', 'mid_band', 'upper_band']].shift(1)

            df['Signal'] = 0

            for j in range(len(df)):

                #generate long signal
                if df['Close'].iloc[j] > df['upper_band'].iloc[j] and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == -3):
                    df['Signal'].iloc[j] = 1

                #generate short signal
                elif df['Close'].iloc[j] < df['lower_band'].iloc[j] and (df['Signal'].iloc[j-1]==0 or df['Signal'].iloc[j-1] == 3):
                    df['Signal'].iloc[j] = -1

                #convert buy signal to  long positional signal
                elif df['Close'].iloc[j] >= df['mid_band'].iloc[j] and df['Signal'].iloc[j-1] ==1:
                    df['Signal'].iloc[j] = 2

                #carry forward long positional signal
                elif df['Close'].iloc[j] >= df['mid_band'].iloc[j] and df['Signal'].iloc[j-1] ==2:
                    df['Signal'].iloc[j] = 2

                #exit long positional signal
                elif df['Close'].iloc[j] < df['mid_band'].iloc[j] and df['Signal'].iloc[j-1] ==2:
                    df['Signal'].iloc[j] = 3

                #exit long immediate signal
                elif df['Close'].iloc[j] < df['mid_band'].iloc[j] and df['Signal'].iloc[j-1] ==1:
                    df['Signal'].iloc[j] = 3

                #convert short signal to short positional signal
                elif df['Close'].iloc[j] <= df['mid_band'].iloc[j] and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -2

                #carry forward short positional signal
                elif df['Close'].iloc[j] <= df['mid_band'].iloc[j] and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -2

                #exit short positional signal
                elif df['Close'].iloc[j] > df['mid_band'].iloc[j] and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -3

                #exit short immediate signal
                elif df['Close'].iloc[j] > df['mid_band'].iloc[j] and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -3

            df['Signal'] = df['Signal'].shift(1)

            """"Long trades"""
            long_entry_df = df.loc[ df['Signal'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['Signal'] == 3][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            """"Short Trades"""
            short_entry_df = df.loc[ df['Signal'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['Signal'] == -3][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)


    def HeikinAshi(df, entry_price_condition):

        if entry_price_condition !='open' and entry_price_condition !='high' and entry_price_condition !='low' and entry_price_condition !='close' and entry_price_condition !='ohlcavg':
            print('entry price condition can be either open/high/low/close/ohlcavg')
        
        else:
            
            df.columns =['Date', 'Open', 'High', 'Low', 'Close','Volume']

            df['Date'] = pd.to_datetime(df['Date'])

            df['HAHigh'] = df['High']

            df['HALow'] = df['Low']

            df['HAClose'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25)
            
            df['HAOpen'] = 0

            for j in range(len(df)):

                if j ==0:
                    df['HAOpen'].iloc[j] = 0

                else:
                    df['HAOpen'].iloc[j] = ((df['HAOpen'].iloc[j-1] + df['HAClose'].iloc[j -1]) * 0.5).round(2)
            
            """Entry Price Conidtions"""
            if entry_price_condition =='open':
                df['AveragePrice']  = df['Open']

            elif entry_price_condition =='close':
                df['AveragePrice']  = df['Close']

            elif entry_price_condition =='high':
                df['AveragePrice']  = df['High']

            elif entry_price_condition =='low':
                df['AveragePrice']  = df['Low']

            elif entry_price_condition =='ohlcavg':
                df['AveragePrice'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) * 0.25).round(2)

            df = df.drop(columns =['Open', 'High', 'Low', 'Close'])

            df['HASignal'] = np.where(df['HAClose'] > df['HAOpen'], 1, -1)

            df['Signal'] = 0

            for j in range(len(df)):

                if df['HASignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == -3) :
                    df['Signal'].iloc[j] = 1

                elif df['HASignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 0 or df['Signal'].iloc[j-1] == 3):
                    df['Signal'].iloc[j] = -1
                
                #short continue next day
                elif df['HASignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -1:
                    df['Signal'].iloc[j] = -2

                #continue short trade
                elif df['HASignal'].iloc[j] == -1 and df['Signal'].iloc[j-1] == -2:
                    df['Signal'].iloc[j] = -2
                
                #exit short trade
                elif df['HASignal'].iloc[j] == 1 and (df['Signal'].iloc[j-1] == -1 or df['Signal'].iloc[j-1] == -2):
                    df['Signal'].iloc[j] = -3

                #long continue next day
                elif df['HASignal'].iloc[j] == 1 and df['Signal'].iloc[j-1] == 1:
                    df['Signal'].iloc[j] = 2

                #continue long trade
                elif df['HASignal'].iloc[j] == 1 and df['Signal'].iloc[j-1] == 2:
                    df['Signal'].iloc[j] = 2
                
                #exit long trade
                elif df['HASignal'].iloc[j] == -1 and (df['Signal'].iloc[j-1] == 1 or df['Signal'].iloc[j-1] == 2):
                    df['Signal'].iloc[j] = 3
            
            df['Signal'] = df['Signal'].shift(1)

            """"Long trades"""
            long_entry_df = df.loc[ df['Signal'] == 1][['Date', 'AveragePrice']].reset_index(drop=True)
            long_entry_df.columns =['EntryDate', 'EntryPrice']
            long_entry_df['Position'] ='Long'

            long_exit_df = df.loc[ df['Signal'] == 3][['Date', 'AveragePrice']].reset_index(drop=True)
            long_exit_df.columns =['ExitDate', 'ExitPrice']

            long_df = pd.concat([long_entry_df, long_exit_df], axis= 1).reset_index(drop=True).dropna()

            """Short Trades"""
            short_entry_df = df.loc[ df['Signal'] == -1][['Date', 'AveragePrice']].reset_index(drop=True)
            short_entry_df.columns =['EntryDate', 'EntryPrice']
            short_entry_df['Position'] ='Short'

            short_exit_df = df.loc[ df['Signal'] == -3][['Date', 'AveragePrice']].reset_index(drop=True)
            short_exit_df.columns =['ExitDate', 'ExitPrice']

            short_df = pd.concat([short_entry_df, short_exit_df], axis= 1).reset_index(drop=True).dropna()

            tradelog_df = pd.concat([long_df, short_df], axis = 0).dropna().reset_index(drop = True)
            tradelog_df = tradelog_df.sort_values(by =['EntryDate'])

            return tradelog_df.reset_index(drop = True)


    def PerformanceMetrics(df):
        
        df.loc[ df['Position'] =='Long', 'GainLossPctChg'] = (df['ExitPrice'] /df['EntryPrice'] - 1).round(2)
        df.loc[ df['Position'] =='Short', 'GainLossPctChg'] = ((df['EntryPrice'] - df['ExitPrice']) /df['EntryPrice']).round(2)

        df.loc[ df['Position'] =='Long', 'Pnl'] = df['ExitPrice'] - df['EntryPrice']
        df.loc[ df['Position'] =='Short', 'Pnl'] = df['EntryPrice'] - df['ExitPrice']

        win_rate = round((len(df.loc[ df['GainLossPctChg'] >=0]) / len(df)) * 100, 2)
        loss_rate = 100 - win_rate 

        avg_win = round(df.loc[ df['GainLossPctChg'] >=0]['GainLossPctChg'].mean() * 100, 2)
        avg_loss = round(df.loc[ df['GainLossPctChg'] < 0 ]['GainLossPctChg'].mean() * 100, 2)

        excepted_value = round((win_rate * 0.01 * avg_win) + (loss_rate * 0.01 * avg_loss), 2)

        average_holding_period = ((df['ExitDate'] - df['EntryDate']).dt.days).mean()

        profit_factor = (df.loc[ df['Pnl'] > 0]['Pnl'].sum()) / (df.loc[ df['Pnl'] < 0]['Pnl'].sum())
        profit_factor = round(profit_factor, 2)

        profit_factor = abs(profit_factor)

        biggest_winner = df['GainLossPctChg'].max() * 100
        biggest_loser = df['GainLossPctChg'].min() * 100

        dict_var = {'Win Rate' : win_rate,
                    'Loss Rate' : loss_rate,
                    'Average Win' : avg_win,
                    'Average Loss' : avg_loss,
                    'Expected Value' : excepted_value,
                    'Average holding period (days)' : average_holding_period,
                    'Profit Factor' : profit_factor,
                    'Biggest Winner' : biggest_winner,
                    'Biggest Loser' : biggest_loser}

        backtest_stat_df = pd.DataFrame.from_dict(dict_var, orient ='index')
        backtest_stat_df.columns=['Performance Metrics']

        return backtest_stat_df.round(2)


    