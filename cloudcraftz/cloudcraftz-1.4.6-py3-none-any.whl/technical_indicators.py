import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from pykalman import KalmanFilter

def simple_moving_average(arr, params={'periods': 2}):
    """
    Parameters
    -------------------------------------------------
    arr: np.array, list or pd.Series
    params: dict (with 'periods' as key and an integer as value)
            value is the window size , default value is 2.

    returns: np.array (SMA signal)
    """
    try:
        new_data = np.array(arr)
        data = pd.DataFrame(new_data, columns=['value'])
        data['Rolling Mean'] = data['value'].rolling(window=params['periods']).mean()
        mov_avg = np.array(data['Rolling Mean'])

        return mov_avg

    except Exception as e:
        print(e)


def relative_strength_index(arr, params={'periods': 14, 'kind': simple_moving_average}):
    """
    Parameters
    -------------------------------------------------
    arr: np.array, list or pd.Series
    params: dict (with 'periods' as key and an integer as value
            value is the window size , default value is 14. The second key 
            here is the 'kind', which is by default 'SMA')

    returns: rsi signal 
    """
    try:
        new_data = np.array(arr)
        data = pd.DataFrame(new_data, columns=['values'])
        data['diff'] = data['values'].diff()
        dUp, dDown = data['diff'].copy(), data['diff'].copy()

        dUp[dUp < 0] = 0
        dDown[dDown > 0] = 0

        dDown = dDown.abs()

        mUp = params['kind'](dUp, {'periods': params['periods']})
        mDown = params['kind'](dDown, {'periods': params['periods']})

        rs = mUp / mDown
        rsi = 100 - (100/(1 + rs))

        return rsi

    except Exception as e:
        print(e)


def exponential_moving_average(arr, params = {'periods': 9}):
    """
    Parameters
    -------------------------------------------------
    arr: np.array, list or pd.Series
    params: dict (with 'periods' as key and an integer as value)
            value is the window size , default value is 9.

    returns: np.array (EMA signal)
    """
    try:
        arr1 = np.array(arr)
        arr2 = pd.DataFrame(arr1, columns = ['value'])
        arr2['ewm'] = arr2['value'].ewm(span = params['periods'], adjust=False).mean()
        exp_avg = np.array(arr2['ewm'])

        return exp_avg

    except Exception as e:
        print(e)


def ROC(arr, params={'periods': 2}):
    """
    Parameters
    -------------------------------------------------
    arr: np.array, list or pd.Series
    params: dict (with 'periods' as key and an integer as value)
            value is the window size , default value is 2.

    returns: np.array (ROC signal)
    """
    try:
        arr = np.array(arr)
        data = pd.DataFrame(arr, columns=['values'])
        N = data['values'].diff(params['periods'])
        D = data['values'].shift(params['periods'])
        ROC = pd.Series(N/D, name='ROC')

        return np.array(ROC)
    except Exception as e:
        print(e)


def get_bollinger_bands(arr, params={'rate': 20}):
    """
    Parameters
    -------------------------------------------------
    arr: np.array, list or pd.Series
    params: dict (with 'rate' as key and an integer as value)
            value is the window size , default value is 20.

    returns: 3 bands of bollinger .
    """
    try:
        arr = np.array(arr)
        data = pd.DataFrame(arr, columns=['values'])
        sma = simple_moving_average(arr, {'periods': params['rate']})
        data['std'] = data['values'].rolling(params['rate']).std()
        bollinger_up = sma + (data['std'] * 2)
        bollinger_down = sma - (data['std'] * 2)

        return np.array(bollinger_up), np.array(bollinger_down), sma
    except Exception as e:
        print(e)


def get_macd(arr, params={'fast': 12, 'slow': 26, 'signal-span': 9, 'adjust': False}):
    """
    Parameters
    -------------------------------------------------
    arr: np.array, list or pd.Series
    params: dict [keys and defaults - 'fast': 12, 'slow': 26, 'signal-span': 9, 'adjust': False]

    returns: np.array (MACD, Signal) a tuple of two numpy arrays
    """
    try:
        arr = np.array(arr)
        data = pd.DataFrame(arr, columns=['values'])
        exp1 = data['values'].ewm(span=params['fast'], adjust=params['adjust']).mean()
        exp2 = data['values'].ewm(span=params['slow'], adjust=params['adjust']).mean()
        data['macd'] = exp1 - exp2
        data['signal'] = data['macd'].ewm(span=params['signal-span'], adjust=params['adjust']).mean()

        return np.array(data['macd']), np.array(data['signal'])
    except Exception as e:
        print(e)


def on_balance_volume(arr, params = {'volume': [4, 7, 9, 10]}):
    """
    Parameters
    -------------------------------------------------
    arr: np.array, list or pd.Series
    params: dict (with 'volume' as key and a list as value)
            by default a dummy list is passed make sure to pass a 
            valid list or array.

    returns: np.array (OBV signal)
    """
    try:
        arr1 = np.array(arr)
        arr3 = np.array(params['volume'])
        arr2 = pd.DataFrame(arr1, columns=['values'])
        arr4 = pd.DataFrame(arr3, columns=['volume'])
        data = pd.concat([arr2, arr4], axis=1)

        data['on_bal_val'] = (np.sign(data['values'].diff()) * data['volume']).fillna(0).cumsum()
        obv_avg = np.array(data['on_bal_val'])
        return obv_avg

    except Exception as e:
        print(e)


def aroon_indicator(arr, params = {'lb' : 25}):
    """
    Parameters
    -------------------------------------------------
    arr: np.array, list or pd.Series
    params: dict (with 'lb' as key and an integer as value)
            default value is 25.

    returns: np.array (Aroon signal)
    """
    try:
        data = np.array(arr)
        new_data = pd.DataFrame(data, columns=['values'])

        df = new_data.copy()
        df['up'] = 100 * df['values'].rolling(params['lb'] + 1).apply(lambda x: x.argmax()) / params['lb']
        df['down'] = 100 * df['values'].rolling(params['lb'] + 1).apply(lambda x: x.argmin()) / params['lb']

        return np.array(df['up']), np.array(df['down'])

    except Exception as e:
        print(e)


def stochastic(arr, high, low, params={'%K-type': 'slow'}):
    """
    Parameters
    -------------------------------------------------
    arr: np.array, list or pd.Series
    high: np.array, list or pd.Series
    low: np.array, list or pd.Series
    params: dict (with '%K-type' as key and a string as value)
            value is 'slow' by default , may use 'fast'.

    returns: np.array (tuple) , Stochastic Oscillator
    """
    if params['%K-type'] == 'slow':
        n = 3
    elif params['%K-type'] == 'fast':
        n = 1
    else:
        print("Enter only fast or slow .")

    try:
        arr, high, low = np.array(arr), np.array(high), np.array(low)
        df = {'values': arr, 'High': high, 'Low': low}
        data = pd.DataFrame(df, columns=['values', 'High', 'Low'])
        data['14-high'] = data['High'].rolling(14).max()
        data['14-low'] = data['Low'].rolling(14).min()
        data['%K'] = (data['values'] - data['14-low'])*100/(data['14-high'] - data['14-low'])
        data['%D'] = data['%K'].rolling(n).mean()

        return np.array(data['%K']), np.array(data['%D'])
    except Exception as e:
        print(e)


def kalmanFilter(arr):
    """
    Parameters
    -------------------------------------------------
    arr: np.array, list or pd.Series
    
    returns: np.array (tuple) (kf_mean and Covariance)
    """
    
    kf = KalmanFilter(transition_matrices = [1], observation_matrices = [1], initial_state_mean = 0,
                initial_state_covariance = 1, observation_covariance = 1, transition_covariance =.01)

    try:
        arr = np.array(arr)
        state_means_kf, covar = kf.filter(arr)

        return np.array(state_means_kf), np.array(covar)

    except Exception as e:
        print(e)


def agg_pl_max_dd(signal, price, plot=False, god=False):
    """
    Parameters
    ----------------------------------------------------
    signal: a list or array of position values 
    price: a list or array of price values
    plot: True or False, default:False
    god: False (default), True only if it's a god signal

    returns: tuple of (cumulative p/L, minimum of cum_p/L, a dataframe)
    """
    try:
        if god:
            signal, price = np.array(signal), np.array(price)
            data = pd.DataFrame({'Signal': signal, 'Price': price})
            data['Price_Change'] = data['Price'].diff()
            data['Cumulative_P/L'] = (data['Price_Change'] * data['Signal']).cumsum()

        else:
            signal, price = np.array(signal), np.array(price)
            data = pd.DataFrame({'Signal': signal, 'Price': price})
            data['Price_Change'] = data['Price'].diff()
            data['Cumulative_P/L'] = (data['Price_Change'] * data['Signal'].shift(1)).cumsum()

        if plot:
            plt.figure(figsize=(15, 8))
            plt.title("Maximum Drawdown and Aggregate P/L", fontsize=17)
            plt.plot(data['Price'], color='r', linewidth=2)
            plt.plot(data['Price_Change'], color='b', linewidth=2)
            plt.plot(data['Cumulative_P/L'], color='g', linewidth=2)
            plt.xlabel('Days', fontsize=15)
            plt.ylabel('Value', fontsize=15)
            plt.legend(('Price', 'Price_Change', 'Cumulative_P/L'))

        return data['Cumulative_P/L'][len(data)-1], data['Cumulative_P/L'].min(), data
    except Exception as e:
        print(e)
