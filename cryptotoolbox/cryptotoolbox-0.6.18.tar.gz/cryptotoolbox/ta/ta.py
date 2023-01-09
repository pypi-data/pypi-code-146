from scipy import stats
import pandas as pd
import numpy as np


def RORO_weekly_signal(y, btc='SOL', p1=1.05, p2=1.1, long_expo=1., short_expo=0.):  # On rentre le dataframe
    weekday = y.weekday.values
    cours = y[btc].values
    T = np.size(weekday)
    S = np.zeros(T)
    for t in range(22, T):
        if weekday[t] == 5 and cours[t - 22] > 0:
            if cours[t] > cours[t - 14] * p1 and cours[t] > cours[t - 21] * p2:
                S[t] = long_expo
            else:
                S[t] = short_expo
        else:
            S[t] = S[t - 1]
    return S


def compute_LO_indicator(data_df=None, token='Close'):
    addw = pd.DataFrame(index=data_df.index, data={'S{}'.format(token): RORO_weekly_signal(data_df, token)})
    data_df = data_df.join(addw, how='left')
    return data_df


def roll(df, w):
    v = df.values
    d0, d1 = v.shape
    s0, s1 = v.strides
    restricted_length = d0 - (w - 1)
    a = stride(v, (restricted_length, w, d1), (s0, s0, s1))
    rolled_df = pd.concat({
        row: pd.DataFrame(values, columns=df.columns)
        for row, values in zip(df.index[-restricted_length:], a)
    })
    return rolled_df.groupby(level=0)


def compute_monthly_LS_indicator(data_df=None, token='Close', pente_window=14, lookback_window=18, center=0.5,
                                 short=True):
    print('computing weekly signals')
    data_df['rebalance'] = data_df.index.day == 1

    monthly_df = data_df.copy()
    monthly_df = monthly_df[monthly_df['rebalance']]

    def compute_ranked_slope(short, center, lagging_df):
        lagging_df['rolling_slope_rank'] = lagging_df['rolling_slope'].rank(pct=True)
        if short:
            lagging_df['rolling_slope_rank_ls'] = 2 * lagging_df['rolling_slope_rank'] - center
            lagging_df['rolling_slope_rank_ls'] = lagging_df['rolling_slope_rank_ls'].clip(-1, 1)
        else:
            lagging_df['rolling_slope_rank_ls'] = lagging_df['rolling_slope_rank']

        gen_sig = lagging_df['rolling_slope_rank_ls'].iloc[-1]
        if gen_sig >= 0.:
            return 1.
        else:
            return -1.

    print('computing signals')

    def compute_slope(slope_df):
        y = slope_df.values
        slope = stats.linregress(np.arange(len(y)), y).slope
        return slope

    print('slope')
    monthly_df['rolling_slope'] = monthly_df[token].rolling(window=pente_window).apply(compute_slope)
    print('slope done')

    import functools
    go = functools.partial(compute_ranked_slope, short, center)
    signal_df = roll(monthly_df, lookback_window).apply(go)

    signal_df = signal_df.to_frame()
    signal_df.columns = ['signal_gen']

    data_df = pd.merge(data_df.copy(), signal_df.copy(), how='left', right_index=True, left_index=True)
    data_df['signal_gen'] = data_df['signal_gen'].ffill()

    def curate_signals(row, token):
        if abs(row[token]) <= 1e-3:
            return np.nan
        else:
            return row['signal_gen']

    go_sig = lambda x: curate_signals(x, token)
    data_df['signal_gen'] = data_df.apply(go_sig, axis=1)

    def curate_close(row, token):
        if abs(row[token]) <= 1e-3:
            return np.nan
        else:
            return row[token]

    go_close = lambda x: curate_close(x, token)
    data_df['close'] = data_df.apply(go_close, axis=1)
    data_df['signal'] = data_df['signal_gen'].shift()
    data_df['epoch_number'] = data_df['rebalance'].cumsum()
    return data_df


def getBBands(df, period=10, stdNbr=2):
    df['middle'] = get_sma(df['Close'], period)
    df['std'] = df['Close'].rolling(period).std()
    df['upper'] = df['middle'] + df['std'] * stdNbr
    df['lower'] = df['middle'] - df['std'] * stdNbr
    return df


def get_sma(prices, rate):
    return prices.rolling(rate).mean()


def get_bollinger_bands(prices, rate=20):
    sma = get_sma(prices, rate)
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * 2  # Calculate top band
    bollinger_down = sma - std * 2  # Calculate bottom band
    return bollinger_up, bollinger_down


def getBBands(df, period=10, stdNbr=2):
    df['middle'] = get_sma(df['Close'], period)
    df['std'] = df['Close'].rolling(period).std()
    df['upper'] = df['middle'] + df['std'] * stdNbr
    df['lower'] = df['middle'] - df['std'] * stdNbr
    return df


def compute_slope(series):
    m, b = np.polyfit(range(len(series)), series / max(series), 1)

    return m


def get_rsi(series):
    delta = series.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    down = np.abs(down)
    roll_up1 = up.ewm(span=14).mean()
    roll_down1 = down.ewm(span=14).mean()
    rs = roll_up1 / roll_down1
    return 100 - (100 / (1 + rs))


def get_rsi_signal(df):
    df['RSI'] = get_rsi(df['Close'])
    RSIsignal = []
    for i, row in df.iterrows():
        last_signal = 0
        if row['RSI'] > 70:
            last_signal = 0
        if row['RSI'] < 30:
            last_signal = 1
        RSIsignal.append(last_signal)

    return RSIsignal


def get_sma(prices, rate):
    return prices.rolling(rate).mean()


def get_macd(df, short_ema=12, long_ema=26, signal_line=9):
    macd_line = df[f'Close'].ewm(span=int(short_ema)).mean() - df[f'Close'].ewm(span=int(long_ema)).mean()
    df[f'macd_signal_diff'] = macd_line - macd_line.ewm(span=int(signal_line)).mean()

    return df.iloc[26:]


def get_macd_signal(btc_prices, short_ema=12, long_ema=26, signal_line=9):
    btc_prices = get_macd(btc_prices.copy(), short_ema, long_ema, signal_line)
    btc_prices['signalMACD'] = (btc_prices['macd_signal_diff'] > 0).astype(int)

    return btc_prices['signalMACD']


def get_bollinger_bands(prices, rate=20):
    sma = get_sma(prices, rate)
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * 2  # Calculate top band
    bollinger_down = sma - std * 2  # Calculate bottom band
    return bollinger_up, bollinger_down


def get_price_cross(btc_prices, small_ma=14, long_ma=21, p1=1, p2=1):
    btc_prices['maSmall'] = btc_prices['Close'].shift(small_ma)
    btc_prices['maLong'] = btc_prices['Close'].shift(long_ma)
    btc_prices['signal'] = (btc_prices['Close'] > btc_prices['maSmall'] * p1) & (
                btc_prices['Close'] > btc_prices['maLong'] * p2)

    return btc_prices['signal']


def get_ma_cross(btc_prices, small_ma, long_ma):
    btc_prices['maSmall'] = btc_prices['Close'].rolling(small_ma).mean()
    btc_prices['maLong'] = btc_prices['Close'].rolling(long_ma).mean()
    btc_prices['signal'] = btc_prices['maLong'] > btc_prices['maSmall']

    return btc_prices['signal']


def get_ema_cross(btc_prices, small_ma, long_ma):
    btc_prices['maSmall'] = btc_prices['Close'].ewm(small_ma).mean()
    btc_prices['maLong'] = btc_prices['Close'].ewm(long_ma).mean()
    btc_prices['signal'] = btc_prices['maLong'] > btc_prices['maSmall']

    return btc_prices['signal']


def compute_slop_indicator(btc_prices, number_ma=2, number_slope=2):
    btc_prices['maNb'] = btc_prices['Close'].rolling(number_ma).mean()
    btc_prices['slope'] = btc_prices['maNb'].rolling(number_slope).apply(compute_slope)
    btc_prices['slopeSign'] = np.sign(btc_prices['slope'])
    btc_prices['signalSlope'] = (btc_prices['slopeSign'] > 0).astype(int)

    return btc_prices['signalSlope']


def create_selected_indicators(btc_prices):
    btc_prices['signalSlope'] = compute_slop_indicator(btc_prices.copy())
    btc_prices['signalMACD'] = get_macd_signal(btc_prices.copy())
    btc_prices['signalRSI'] = get_rsi_signal(btc_prices.copy())

    return btc_prices


def create_all_indicators(btc_prices):
    for number_ma in [2, 5, 10, 15]:
        for number_slope in [2, 5, 10, 15]:
            btc_prices[f'signalSlope{str(number_ma) + "-" + str(number_slope)}'] = compute_slop_indicator(
                btc_prices.copy(), number_ma, number_slope)

    for maSmall in [2, 6, 12, 24]:
        for maLong in [26, 39, 52, 65]:
            btc_prices[f'signalMACD{str(maSmall) + "-" + str(maLong)}'] = get_macd_signal(btc_prices.copy(),
                                                                                          short_ema=maSmall,
                                                                                          long_ema=maLong)

    btc_prices['signalRSI'] = get_rsi_signal(btc_prices.copy())

    for maSmall in [2, 5, 10, 15]:
        for maLong in [20, 40, 60, 80, 100, 200]:
            btc_prices[f'signalMA{str(maSmall) + "-" + str(maLong)}'] = get_ma_cross(btc_prices.copy(), maSmall, maLong)

    for maSmall in [2, 5, 10, 15]:
        for maLong in [20, 40, 60, 80, 100, 200]:
            btc_prices[f'signalEMA{str(maSmall) + "-" + str(maLong)}'] = get_ema_cross(btc_prices.copy(), maSmall,
                                                                                       maLong)

    for maSmall in [5, 8, 10, 12, 14]:
        for maLong in [17, 19, 21, 26, 30]:
            btc_prices[f'signalPriceShift{str(maSmall) + "-" + str(maLong)}'] = get_price_cross(btc_prices.copy(),
                                                                                                maSmall, maLong)

    return btc_prices