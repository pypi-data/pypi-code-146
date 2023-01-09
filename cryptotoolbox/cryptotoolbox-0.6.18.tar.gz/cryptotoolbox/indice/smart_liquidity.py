from datetime import datetime

from cryptotoolbox.connector import crypto_connector
from cryptotoolbox.realtime import realtime_plotting_utility
from scipy.interpolate import interp1d

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import numpy as np

import pandas as pd


import datetime as datetime


from cryptotoolbox.connector import crypto_connector
from scipy import stats
import pandas as pd
import numpy as np
from numpy.lib.stride_tricks import as_strided as stride
from cryptotoolbox.realtime import realtime_plotting_utility
from scipy.optimize import Bounds, LinearConstraint, minimize



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



def annualize_percent(first_value=np.nan, last_value=np.nan, nb_years=np.nan):
    return (last_value / first_value) ** (1. / nb_years) - 1.


def compute_impermanent_loss_v2(p_0=np.nan, p_out=np.nan):
    tau = p_out / p_0
    return 2 * np.sqrt(tau) / (1. + tau) - 1, tau


def compute_impermanent_loss_v3(p_0=np.nan, p_a=np.nan, p_b=np.nan, p_out=np.nan):
    ILv2, tau = compute_impermanent_loss_v2(p_0=p_0, p_out=p_out)
    square_one = np.sqrt(p_a / p_0)
    square_two = np.sqrt(p_0 / p_b)
    num_one = square_one + tau * square_two
    factor = 1. / (1. - num_one / (1. + tau))
    ILv3 = ILv2 * factor
    return ILv3, ILv2

### formule venant d'ici (à redémontrer)
#https://lambert-guillaume.medium.com/understanding-the-value-of-uniswap-v3-liquidity-positions-cdaaee127fe7
### formule venant d'ici (à redémontrer)
#https://lambert-guillaume.medium.com/pricing-uniswap-v3-lp-positions-towards-a-new-options-paradigm-dce3e3b50125
#https://lambert-guillaume.medium.com/how-to-create-a-perpetual-options-in-uniswap-v3-3c40007ccf1

def compute_total_LP_portfolio_value_first_methodo(p_a=np.nan, p_b=np.nan, p_out=np.nan):
    first_size = np.sqrt(p_a * p_b) * (np.sqrt(p_out) - np.sqrt(p_a))/(np.sqrt(p_b) - np.sqrt(p_a))
    second_size = np.sqrt(p_a * p_out) * (np.sqrt(p_b) - np.sqrt(p_out))/(np.sqrt(p_b) - np.sqrt(p_a))
    return first_size + second_size

def compute_total_LP_portfolio_value_second_methodo(p_a=np.nan, p_b=np.nan, p_out=np.nan):
    K = np.sqrt(p_a * p_b)
    r = np.sqrt(p_b/p_a)
    return (2.*np.sqrt(p_out * K * r) - p_out - K)/(r-1)

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


def get_sma(prices, rate):
    return prices.rolling(rate).mean()


def get_bollinger_bands(prices, rate=20):
    sma = get_sma(prices, rate)
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * 2  # Calculate top band
    bollinger_down = sma - std * 2  # Calculate bottom band
    return bollinger_up, bollinger_down

def get_price_data(me_pair=None, initial_date=None, local_root_directory='none'):
    ssj = me_pair[0]
    ssj_against = me_pair[1]

    pair = ssj + ssj_against
    daily_crypto_starting_day = initial_date

    daily_crypto_starting_date = datetime.datetime.strptime(daily_crypto_starting_day, '%Y-%m-%d')
    starting_date = daily_crypto_starting_date
    running_date = datetime.datetime.now()

    nb_days_total = (running_date - daily_crypto_starting_date).days
    print(nb_days_total)
    refetch_all = True
    data_df = crypto_connector.fetch_crypto_daily_data(ssj=ssj, ssj_against=ssj_against,
                                                       local_root_directory=local_root_directory,
                                                       daily_return_pkl_filename_suffix='_daily_returns.pkl',
                                                       refetch_all=refetch_all,
                                                       daily_crypto_starting_day=daily_crypto_starting_date,
                                                       daily_crypto_ending_day=running_date)

    data_df = data_df[['open', 'high', 'low', 'close', 'volume']]
    data_df.columns = ['Open', 'High', 'Low', 'Close', 'volume']
    data_df['Date'] = data_df.index
    data_df['DateStr'] = data_df.index.astype(str)
    print('done')
    data_df['Date'] = pd.to_datetime(data_df['Date'])
    data_df['weekday'] = data_df.apply(lambda x: datetime.datetime.date(x['Date']).weekday(), axis=1)
    data_df = data_df.set_index('Date')

    return data_df

def get_apr(date, pct_change, volume_df = None, current_apr=None):
    x = np.array(list(current_apr.keys()))
    y = list(current_apr.values())
    f2 = interp1d(x, y, kind='linear')
    try:
        pct_change = max(1.,pct_change)
        apr = f2(pct_change)
    except Exception as e:
        print(f'trouble {pct_change}')
        print(e)
    current_apr_ethbtc = apr/100.
    daily_current_apr_ethbtc= (1.+current_apr_ethbtc)**(1./365.)-1.

    ratio = volume_df.loc[date].volumeToken0 / volume_df.iloc[-1].volumeToken0
    prorata_daily_current_apr_ethbtc = daily_current_apr_ethbtc * ratio
    return prorata_daily_current_apr_ethbtc

def get_swapping_cost(swapping_size_proportion =None, swapping_cost_map=None):
    if np.isnan(swapping_size_proportion):
        return np.nan
    assert swapping_size_proportion <= 1.
    assert swapping_size_proportion >= 0.
    percentage_swapping_size_proportion = 100. * swapping_size_proportion
    x = np.array(list(swapping_cost_map.keys()))
    y = list(swapping_cost_map.values())
    f2 = interp1d(x, y, kind='linear')
    cost = np.nan
    try:
        cost = f2(percentage_swapping_size_proportion).item()
    except Exception as e:
        print(f'trouble computing swapping cost{percentage_swapping_size_proportion}')
        print(e)
    return cost



def LS_IL_boundaries_with_signal(data_df = None, plotHtml = False, me_pair = ('ETH', 'BTC'), bb_periods=[5, 15, 30, 55], stdNbrs=[2., 3., 5.], distance_to_bound_percs = [0,5,10,15,20,30,40], current_apr=None, bypass_signal=True, bypass_stoploss=True, swapping_cost_map = {1:1e-4, 10:0.01, 50:0.05, 75:0.075, 100:0.1},starting_number_of_numeraire = 1000):
    ssj = me_pair[0]
    ssj_against = me_pair[1]
    objectives = []

    for bb_period in bb_periods:
        for stdNbr in stdNbrs:
            for distance_to_bound_perc in distance_to_bound_percs:
                df = data_df.copy()
                df['Date']=df.index
                print(f'params_{bb_period}_{stdNbr}')
                df = getBBands(df.copy(), period=bb_period, stdNbr=stdNbr)
                df = df.dropna()

                stage_nb = 0

                pct_change = np.nan
                real_upper_bound = np.nan
                real_lower_bound = np.nan
                buffer_upper_bound = np.nan
                buffer_lower_bound = np.nan

                initial_real_upper_bound = np.nan
                initial_real_lower_bound = np.nan


                df['pct_change'] = (stdNbr * df['std']) / df['Close'] * 100
                avg_pct_change = df['pct_change'].mean()
                ### to compute a proper metric
                if bypass_stoploss:
                    df['stoploss_condition'] = False
                if bypass_signal:
                    df['signal'] = 1.

                if plotHtml:
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=df[['Close', 'upper', 'lower']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'Bollinger {ssj}{ssj_against}')
                    fig.show()

                initial_price = df['Close'].iloc[0]
                begining_initial_price = df['Close'].iloc[0]

                initial_lp_value = np.nan
                preceding_vault_signal = df['signal'].iloc[0]

                stages = []
                counter = 0
                the_end = False
                for i, row in df.iterrows():
                    if i == df.index[-1]:
                        the_end = True
                    if counter == 0:
                        counter = counter + 1
                        continue
                    ILv3, ILv2 = np.nan, np.nan
                    lp_value_first, lp_value_second = np.nan, np.nan
                    lp_position_profit = np.nan
                    flipped_lp_position_profit = np.nan


                    apr = get_apr(row['DateStr'],  row['pct_change'], volume_df=data_df.copy(), current_apr=current_apr)

                    # if currently providing and we enter in a risk off mode we need to compute IL
                    we_are_out = np.isnan(real_upper_bound)

                    stoploss_condition = row['stoploss_condition']
                    vault_signal = row['signal']

                    print(f'real_upper_bound {real_upper_bound}')
                    high = row['High']
                    print(f'high {high}')
                    print(f'real_lower_bound {real_lower_bound}')
                    low = row['Low']
                    print(f'low {low}')
                    print(f'stoploss_condition {stoploss_condition}')
                    print(f'distance to bounds {distance_to_bound_perc}')
                    curILv3 = np.nan
                    curILv2 = np.nan
                    curlp_value_first = np.nan
                    curlp_value_second = np.nan
                    curlp_position_profit = np.nan
                    curflipped_lp_position_profit = np.nan

                    # defining_new_state = (bounds_broken and providing) or (providing and slope_too_sloppy)
                    broken_bounds = np.nan
                    if not we_are_out:
                        distance_to_bound = distance_to_bound_perc/100. * real_upper_bound
                        buffer_upper_bound = real_upper_bound - distance_to_bound
                        buffer_lower_bound = real_lower_bound + distance_to_bound

                        broken_bounds= (row['High'] > buffer_upper_bound or row['Low'] < buffer_lower_bound)
                        assert (not np.isnan(initial_price)) and (not np.isnan(real_lower_bound)) and (
                            not np.isnan(real_upper_bound))
                        p_out = row['Close']
                        curILv3, curILv2 = compute_impermanent_loss_v3(p_0=initial_price, p_a=real_lower_bound,
                                                                 p_b=real_upper_bound,
                                                                 p_out=p_out)
                        curlp_value_first = compute_total_LP_portfolio_value_first_methodo(p_a=real_lower_bound,
                                                                 p_b=real_upper_bound,
                                                                 p_out=p_out)
                        curlp_value_second = compute_total_LP_portfolio_value_second_methodo(p_a=real_lower_bound,
                                                                 p_b=real_upper_bound,
                                                                 p_out=p_out)
                        curlp_position_profit = (curlp_value_first - initial_lp_value) / initial_lp_value
                        curflipped_lp_position_profit = preceding_vault_signal * curlp_position_profit



                    signal_change = False
                    if vault_signal != preceding_vault_signal:
                        signal_change = True

                    we_enter = False
                    we_out = False
                    we_rebalance_signal = False
                    we_rebalance_bounds = False
                    #############
                    if stoploss_condition:
                        if we_are_out: ### we do nothing
                            print('we do nothing, already out')
                        if not we_are_out: ### we out
                            print('we out the position because of the stop loss condition')
                            we_out = True
                            assert (not np.isnan(initial_price)) and (not np.isnan(real_lower_bound)) and (
                                not np.isnan(real_upper_bound))
                            p_out = row['Close']
                            ILv3, ILv2 = compute_impermanent_loss_v3(p_0=initial_price, p_a=real_lower_bound,
                                                                     p_b=real_upper_bound,
                                                                     p_out=p_out)
                            lp_value_first = compute_total_LP_portfolio_value_first_methodo(p_a=real_lower_bound,
                                                                                            p_b=real_upper_bound,
                                                                                            p_out=p_out)
                            lp_value_second = compute_total_LP_portfolio_value_second_methodo(p_a=real_lower_bound,
                                                                                             p_b=real_upper_bound,
                                                                                             p_out=p_out)
                            lp_position_profit = (lp_value_first-initial_lp_value)/initial_lp_value
                            flipped_lp_position_profit = preceding_vault_signal * lp_position_profit

                            real_upper_bound = np.nan
                            real_lower_bound = np.nan
                            stage_nb = stage_nb + 1

                    if not stoploss_condition:
                        if we_are_out: ### we enter a position  cause no stop loss signal
                            we_enter = True
                            print('we enter')
                            initial_price = row['Close']
                            real_upper_bound = row['High'] + stdNbr * row['std']

                            pct_change = (real_upper_bound - row['High']) / row['High']
                            real_lower_bound = row['Low'] - stdNbr * row['std']

                            if np.isnan(initial_real_upper_bound):
                                initial_real_upper_bound = real_upper_bound
                                initial_real_lower_bound = real_lower_bound

                            stage_nb = stage_nb + 1
                            if np.isnan(initial_lp_value):
                                initial_lp_value = compute_total_LP_portfolio_value_first_methodo(p_a=real_lower_bound,
                                                                                                  p_b=real_upper_bound,
                                                                                                  p_out=initial_price)

                        if not we_are_out:
                            if broken_bounds or signal_change or the_end:## we rebalance
                                if broken_bounds:
                                    we_rebalance_bounds = True
                                    print('we rebalance because of buffer bounds being touched')
                                if signal_change:
                                    we_rebalance_signal=True
                                    print('we rebalance because of long/short signal change')
                                up = row['High'] > buffer_upper_bound
                                down = row['Low'] < buffer_lower_bound
                                ## one bound must be broken
                                assert up or down or signal_change or the_end
                                # p_out = np.nan
                                # if up:
                                #     p_out = real_upper_bound
                                # elif down:
                                #     p_out = real_lower_bound
                                # else:
                                p_out = row['Close']

                                ##### all in LP loss
                                ILv3, ILv2 = compute_impermanent_loss_v3(p_0=initial_price, p_a=real_lower_bound,
                                                                         p_b=real_upper_bound,
                                                                         p_out=p_out)
                                lp_value_first = compute_total_LP_portfolio_value_first_methodo(p_a=real_lower_bound,
                                                                                                p_b=real_upper_bound,
                                                                                                p_out=p_out)
                                lp_value_second = compute_total_LP_portfolio_value_second_methodo(p_a=real_lower_bound,
                                                                                                  p_b=real_upper_bound,
                                                                                                  p_out=p_out)

                                lp_position_profit = (lp_value_first - initial_lp_value) / initial_lp_value
                                flipped_lp_position_profit = preceding_vault_signal * lp_position_profit


                                # if up:
                                #     initial_price = row['High']
                                # else:
                                #     initial_price = row['Low']
                                initial_price = row['Close']

                                # here compute the previous impermanent loss

                                stage_nb = stage_nb + 1
                                real_upper_bound = row['High'] + stdNbr * row['std']

                                pct_change = (real_upper_bound - row['High']) / row['High']
                                real_lower_bound = row['Low'] - stdNbr * row['std']

                                initial_lp_value = compute_total_LP_portfolio_value_first_methodo(p_a=real_lower_bound,
                                                                                                  p_b=real_upper_bound,
                                                                                                  p_out=p_out)

                    stages.append({
                        'date': row['Date'],
                        'Close':row['Close'],
                        'incurred_v3': ILv3,
                        'incurred_v2': ILv2,
                        'pct_change' : pct_change,
                        'lp_position_profit':lp_position_profit,
                        'flipped_lp_position_profit':flipped_lp_position_profit,
                        'lp_value_first': lp_value_first,
                        'lp_value_second': lp_value_second,
                        'initial_lp_value':initial_lp_value,
                        'initial_price': initial_price,
                        'signal_change':signal_change,
                        'preceding_vault_signal':preceding_vault_signal,
                        'broken_bounds':broken_bounds,
                        'stoploss_condition':stoploss_condition,
                        'the_end': the_end,
                        'we_enter': we_enter,
                        'we_out' : we_out,
                        'curILv3' :curILv3,
                        'curILv2' :curILv2,
                        'curflipped_lp_position_profit': curflipped_lp_position_profit,
                        'curlp_position_profit': curlp_position_profit,
                        'curlp_value_first' : curlp_value_first,
                        'curlp_value_second' : curlp_value_second,
                        'we_rebalance_signal' : we_rebalance_signal,
                        'we_rebalance_bounds' : we_rebalance_bounds,
                        'real_upper_bound': real_upper_bound,
                        'real_lower_bound': real_lower_bound,
                        'buffer_upper_bound': buffer_upper_bound,
                        'buffer_lower_bound': buffer_lower_bound,
                        'distance_to_bound_perc':distance_to_bound_perc,
                        'stage_nb': stage_nb,
                        'apr': apr,
                    })
                    preceding_vault_signal = vault_signal

                stages_df = pd.DataFrame(stages)

                ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                ####### ####### ####### ####### swapping cost analysis
                ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                def rebalancing_signal(row):
                    we_rebalance_signal = row['we_rebalance_signal']
                    we_rebalance_bound = row['we_rebalance_bounds']
                    return we_rebalance_bound or we_rebalance_signal

                stages_df['rebalancing'] = stages_df.apply(rebalancing_signal, axis=1)

                rebalancing_df = stages_df[stages_df['rebalancing']].copy()

                if len(rebalancing_df)>0:
                    rebalancing_df['leaving_initial_price'] = rebalancing_df['initial_price'].shift(+1)
                    rebalancing_df['leaving_initial_price'].iloc[0] = begining_initial_price
                    rebalancing_df['leaving_real_upper_bound'] = rebalancing_df['real_upper_bound'].shift(+1)
                    rebalancing_df['leaving_real_lower_bound'] = rebalancing_df['real_lower_bound'].shift(+1)
                    rebalancing_df['leaving_real_upper_bound'].iloc[0] = initial_real_upper_bound
                    rebalancing_df['leaving_real_lower_bound'].iloc[0] = initial_real_lower_bound

                    rebal_data_df = rebalancing_df[['date','leaving_initial_price', 'initial_price', 'real_upper_bound', 'real_lower_bound', 'leaving_real_upper_bound', 'leaving_real_lower_bound']]

                    def compute_percentage_spread(row):
                        pct_chagne = (row['leaving_real_upper_bound']-row['leaving_initial_price'])/row['leaving_initial_price']
                        return pct_chagne

                    rebal_data_df['pct_change_upper'] = rebal_data_df.apply(compute_percentage_spread, axis=1)

                    ### ether = X (risqué)
                    ### BTC = Y (numéraire)
                    ### P = P ether in BTC
                    def get_liquidity_from_BTC(nb_amount_BTC, current_price, lower_bound ):
                        return nb_amount_BTC/(np.sqrt(current_price) - np.sqrt(lower_bound) )

                    def get_liquidity_from_ETH(nb_amount_ETH, current_price, upper_bound ):
                        return nb_amount_ETH/(1./np.sqrt(current_price) - 1./np.sqrt(upper_bound))

                    def get_ether_from_liquidity(liquidity, current_price, upper_bound):
                        return liquidity*(1./np.sqrt(current_price) -1./np.sqrt(upper_bound))

                    def get_btc_from_liquidity(liquidity, current_price, lower_bound):
                        return liquidity*(np.sqrt(current_price) - np.sqrt(lower_bound) )




                    previous_liquidities = np.zeros(len(rebal_data_df))
                    previous_ethers = np.zeros(len(rebal_data_df))
                    previous_btcs = np.zeros(len(rebal_data_df))
                    new_liquidities = np.zeros(len(rebal_data_df))
                    new_ethers = np.zeros(len(rebal_data_df))
                    new_btcs = np.zeros(len(rebal_data_df))
                    swapping_sizes = np.zeros(len(rebal_data_df))
                    swap_costs = np.zeros(len(rebal_data_df))
                    count = 0

                    previous_btc = np.nan
                    previous_liquidity = np.nan
                    previous_eth = np.nan

                    new_btc = np.nan
                    new_liquidity = np.nan
                    new_eth = np.nan

                    rebal_data_df.index = range(len(rebal_data_df))
                    to_keep_init_liq = np.nan
                    to_keep_init_eth = np.nan
                    to_keep_init_btc = np.nan
                    to_keep_init_price = np.nan
                    for ii, row in rebal_data_df.iterrows():
                        if ii == 0 :
                            ### btc at initial date
                            previous_btc = starting_number_of_numeraire
                            ## initial position configuration: leaving_initial_price inbetween leaving_real_upper_bound and leaving_real_lower_bound
                            leaving_initial_price = row['leaving_initial_price']
                            leaving_real_upper_bound = row['leaving_real_upper_bound']
                            leaving_real_lower_bound = row['leaving_real_lower_bound']
                            ## liquidity at initial date
                            previous_liquidity = get_liquidity_from_BTC(previous_btc,leaving_initial_price,leaving_real_lower_bound )
                            ## ether at initial date
                            previous_eth = get_ether_from_liquidity(previous_liquidity, leaving_initial_price,leaving_real_upper_bound)
                            previous_liquidity_bis = get_liquidity_from_ETH(previous_eth, leaving_initial_price,leaving_real_upper_bound)
                            to_keep_init_liq=previous_liquidity
                            to_keep_init_eth=previous_eth
                            to_keep_init_btc = previous_btc
                            to_keep_init_price = leaving_initial_price

                            assert abs(previous_liquidity_bis - previous_liquidity) < 1e-3
                        else :
                            previous_btc = new_btc
                            previous_eth = new_eth
                            previous_liquidity = new_liquidity

                        swapping_size = np.nan
                        # we leave the 'leaving position' at a new price which will become the new initial price
                        newly_initial_price = row['initial_price']
                        ### we limit the price move to the upper and lower bounds of the position we are in (quantities do not move after in univ3)
                        truncated_newly_initial_price = min(newly_initial_price,leaving_real_upper_bound )
                        truncated_newly_initial_price = max(truncated_newly_initial_price,leaving_real_lower_bound )

                        def get_new_btc_quantity_from_price_change(liquidity, new_price, old_price):
                            return liquidity * (np.sqrt(new_price)-np.sqrt(old_price))

                        def get_new_ether_quantity_from_price_change(liquidity, new_price, old_price):
                            return liquidity * (1./np.sqrt(new_price)-1./np.sqrt(old_price))

                        deltaBTC = get_new_btc_quantity_from_price_change(previous_liquidity, truncated_newly_initial_price, leaving_initial_price)
                        deltaETH = get_new_ether_quantity_from_price_change(previous_liquidity, truncated_newly_initial_price, leaving_initial_price)

                        previous_ethers[count] = previous_eth
                        previous_btcs[count] = previous_btc
                        previous_liquidities[count] = previous_liquidity

                        after_withdrawal_btc = previous_btc + deltaBTC
                        after_withdrawal_eth = previous_eth + deltaETH

                        print(f'after_withdrawal_eth {after_withdrawal_eth}')
                        print(f'after_withdrawal_btc {after_withdrawal_btc}')

                        ####### rebalancing quantities for the new position
                        new_real_lower_bound = row['real_lower_bound']
                        new_real_upper_bound = row['real_upper_bound']
                        # rebalancing the bounds

                        def get_btc_matching_proportion(eth_amount=None, current_price=None, lower_bound=None,
                                                        upper_bound=None):
                            new_liquidity = get_liquidity_from_ETH(eth_amount, current_price, upper_bound)
                            new_btc = get_btc_from_liquidity(new_liquidity, current_price, lower_bound)
                            return new_btc, new_liquidity

                        def get_eth_matching_proportion(btc_amount=None, current_price=None, lower_bound=None,
                                                        upper_bound=None):
                            new_liquidity = get_liquidity_from_BTC(btc_amount, current_price, lower_bound)
                            new_eth = get_ether_from_liquidity(new_liquidity, current_price, upper_bound)
                            return new_eth, new_liquidity

                        new_btc, _ = get_btc_matching_proportion(eth_amount=after_withdrawal_eth,
                                                                 current_price=newly_initial_price,
                                                                 lower_bound=new_real_lower_bound,
                                                                 upper_bound=new_real_upper_bound)
                        ##### we end up with eth equivalent to more btc than we have : we must swap eth
                        has_to_swap_eth =  new_btc >= after_withdrawal_btc

                        new_eth, _ = get_eth_matching_proportion(btc_amount=after_withdrawal_btc,
                                                                 current_price=newly_initial_price,
                                                                 lower_bound=new_real_lower_bound,
                                                                 upper_bound=new_real_upper_bound)
                        ##### we end up with btc equivalent to more eth than we have : we must swap btc
                        has_to_swap_btc = new_eth >= after_withdrawal_eth
                        print(has_to_swap_btc)
                        print(has_to_swap_eth)
                        if after_withdrawal_btc>0. and after_withdrawal_eth>0.:
                            assert has_to_swap_btc == ~has_to_swap_eth

                        if has_to_swap_btc: #### we have more btcs than eth
                            new_btc = after_withdrawal_btc
                            print(f'new btc {new_btc}')
                            print(f'new price {newly_initial_price}')
                            print(f'new lower bound {new_real_lower_bound}')
                            print(f'new upper bound {new_real_upper_bound}')


                            pool_ratio_price = new_btc/new_eth
                            print(f'new ratio {pool_ratio_price}')

                            def get_eth_amount_to_swap(x= None, slippage = 20e-4, initial_btc=None,initial_ether=None,lower_bound=None, upper_bound=None, current_price=None):
                                btc_left = (1.-x)*initial_btc
                                #### if we swap too big quantities we incur price slippage
                                #### if we swap BTCs to ETH, the price of ETH in BTC Y/X will drop
                                slippage_price = current_price * (1. - slippage)
                                ##### the left btc and swapped ether will make the position
                                eth_in_lp, liquidity = get_eth_matching_proportion(btc_amount=btc_left,
                                                                           current_price=slippage_price,
                                                                           lower_bound=lower_bound,
                                                                           upper_bound=upper_bound)
                                return eth_in_lp ,slippage_price,liquidity

                            def get_eth_amount_to_swap_functional(x= None, slippage = 20e-4, initial_btc=None,initial_ether=None,lower_bound=None, upper_bound=None, current_price=None):
                                btc_left = (1.-x)*initial_btc

                                btc_to_swap = x*initial_btc
                                #### if we swap too big quantities we incur price slippage
                                #### if we swap BTCs to ETH, the price of ETH in BTC Y/X will drop
                                slippage_price = current_price * (1. - slippage)
                                ##### the left btc and swapped ether will make the position
                                eth_in_lp, _ = get_eth_matching_proportion(btc_amount=btc_left,
                                                                           current_price=slippage_price,
                                                                           lower_bound=lower_bound,
                                                                           upper_bound=upper_bound)
                                differential = (eth_in_lp -initial_ether)*slippage_price - btc_to_swap
                                return abs(differential)

                            to_optimize = lambda x: get_eth_amount_to_swap_functional(x=x,initial_btc = after_withdrawal_btc, initial_ether = after_withdrawal_eth,current_price= newly_initial_price, lower_bound=new_real_lower_bound, upper_bound = new_real_upper_bound)
                            test_opti = to_optimize(0.5)
                            low_bound = 0.
                            up_bound = 1.
                            const_ind = Bounds(low_bound , up_bound )


                            result_final = minimize(
                                to_optimize,
                                0.5,
                                bounds=const_ind,
                                method='Nelder-Mead'
                            )
                            optimal_size_to_swap = np.nan
                            if result_final.success:
                                optimal_size_to_swap = result_final.x[0]

                            print(f'optimal_size_to_swap {optimal_size_to_swap}')
                            swapping_size = optimal_size_to_swap
                            new_btc = (1.-optimal_size_to_swap)*after_withdrawal_btc
                            new_eth,slippage_price,liquidity = get_eth_amount_to_swap(x=optimal_size_to_swap,initial_btc = after_withdrawal_btc,  initial_ether = after_withdrawal_eth,current_price= newly_initial_price, lower_bound=new_real_lower_bound, upper_bound = new_real_upper_bound)

                            new_liquidity = get_liquidity_from_ETH(new_eth, slippage_price,new_real_upper_bound)
                            new_liquidity_bis = get_liquidity_from_BTC(new_btc, slippage_price,new_real_lower_bound)

                            if not np.isnan(new_liquidity) and not abs(new_liquidity) < 1e-6:
                                condition_to_check = abs(new_liquidity-new_liquidity_bis)/abs(new_liquidity)<1e-3
                                if not condition_to_check:
                                    print('trouble')
                                assert abs(new_liquidity-new_liquidity_bis)/abs(new_liquidity)<1e-3
                            else :
                                print('trouble')

                        elif has_to_swap_eth :
                            new_eth = after_withdrawal_eth
                            print(f'new eth {new_eth}')
                            print(f'new price {newly_initial_price}')
                            print(f'new lower bound {new_real_lower_bound}')
                            print(f'new upper bound {new_real_upper_bound}')


                            def get_btc_amount_to_swap(x= None, slippage = 20e-4, initial_eth=None, initial_btc=None,lower_bound=None, upper_bound=None, current_price=None):
                                eth_left = (1.-x)*initial_eth
                                eth_to_swap = x*initial_eth
                                #### if we swap too big quantities we incur price slippage
                                #### if we swap BTCs to ETH, the price of ETH in BTC Y/X will drop
                                slippage_price = current_price * (1. + slippage)
                                ##### the left btc and swapped ether will make the position
                                btc_in_lp, liquidity = get_btc_matching_proportion(eth_amount=eth_left,
                                                                           current_price=slippage_price,
                                                                           lower_bound=lower_bound,
                                                                           upper_bound=upper_bound)
                                return btc_in_lp, slippage_price, liquidity

                            def get_btc_amount_to_swap_functional(x= None, slippage = 20e-4, initial_eth=None,initial_btc=None,lower_bound=None, upper_bound=None, current_price=None):
                                eth_left = (1.-x)*initial_eth
                                eth_to_swap = x*initial_eth
                                #### if we swap too big quantities we incur price slippage
                                #### if we swap BTCs to ETH, the price of ETH in BTC Y/X will drop
                                slippage_price = current_price * (1. + slippage)
                                ##### the left btc and swapped ether will make the position
                                btc_in_lp, _ = get_btc_matching_proportion(eth_amount=eth_left,
                                                                           current_price=slippage_price,
                                                                           lower_bound=lower_bound,
                                                                           upper_bound=upper_bound)
                                differential = eth_to_swap*slippage_price - (btc_in_lp-initial_btc)
                                return abs(differential)

                            to_optimize = lambda x: get_btc_amount_to_swap_functional(x=x,initial_eth = after_withdrawal_eth,initial_btc= after_withdrawal_btc, current_price=newly_initial_price, lower_bound=new_real_lower_bound, upper_bound = new_real_upper_bound)
                            test_opti = to_optimize(0.5)
                            low_bound = 0.
                            up_bound = 1.
                            const_ind = Bounds(low_bound , up_bound )


                            result_final = minimize(
                                to_optimize,
                                0.5,
                                bounds=const_ind,
                                method='Nelder-Mead'
                            )
                            optimal_size_to_swap = np.nan
                            if result_final.success:
                                optimal_size_to_swap = result_final.x[0]

                            print(f'optimal_size_to_swap {optimal_size_to_swap}')
                            swapping_size = optimal_size_to_swap
                            new_eth = (1.-optimal_size_to_swap)*after_withdrawal_eth
                            new_btc, slippage_price, liquidity = get_btc_amount_to_swap(x=optimal_size_to_swap,initial_eth = after_withdrawal_eth,initial_btc= after_withdrawal_btc, current_price=newly_initial_price, lower_bound=new_real_lower_bound, upper_bound = new_real_upper_bound)

                            new_liquidity = get_liquidity_from_ETH(new_eth, slippage_price,new_real_upper_bound)
                            new_liquidity_bis = get_liquidity_from_BTC(new_btc, slippage_price,new_real_lower_bound)
                            if not np.isnan(new_liquidity) and not abs(new_liquidity) < 1e-6:
                                condition_to_check = abs(new_liquidity-new_liquidity_bis)/abs(new_liquidity)<1e-3
                                if not condition_to_check:
                                    print('trouble')
                                assert abs(new_liquidity-new_liquidity_bis)/abs(new_liquidity)<1e-3
                            else :
                                print('trouble')
                        else :
                            new_eth = after_withdrawal_eth
                            new_btc = after_withdrawal_btc

                        new_ethers[count] = new_eth
                        new_btcs[count] = new_btc
                        new_liquidities[count] = new_liquidity
                        swapping_sizes[count] = swapping_size
                        swap_cost = get_swapping_cost(swapping_size_proportion=swapping_size, swapping_cost_map=swapping_cost_map)
                        swap_costs[count] = swap_cost

                        previous_liquidity=new_liquidity
                        previous_btc=new_btc
                        previous_eth=new_eth

                        count = count + 1
                        print('done')

                    rebal_data_df['previous_btcs'] = previous_btcs
                    rebal_data_df['previous_ethers'] = previous_ethers
                    rebal_data_df['previous_liquidities'] = previous_liquidities

                    rebal_data_df['new_btcs'] = new_btcs
                    rebal_data_df['new_ethers'] = new_ethers
                    rebal_data_df['new_liquidities'] = new_liquidities

                    rebal_data_df['swapping_sizes'] = swapping_sizes
                    rebal_data_df['swapping_cost'] = swap_costs

                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                # ####### ####### ####### ####### end of swapping cost analysis
                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                #
                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                # ####### ####### ####### ####### incorporation into the backtest
                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######

                stages_df['date'] = pd.to_datetime(stages_df['date'])
                stages_df.set_index('date', inplace=True)
                stages_rebal_df = None
                insert_rebalancing_costs = True
                if insert_rebalancing_costs:
                    stages_rebal_df = pd.merge(stages_df.copy(), rebal_data_df.copy(), suffixes = ['','_rebal'],  how = 'left', right_on='date', left_on='date')
                    stages_rebal_df = stages_rebal_df.set_index('date')
                else :
                    stages_rebal_df = stages_df.copy()

                print('computing the mark to market value')

                def compute_mark_to_market_numeraire_assets(previous_numeraire_size, previous_liquidity_size,previous_price,data_df = None):
                    counter = 0
                    numeraire_sizes = np.zeros(len(data_df))
                    for i, row in data_df.iterrows():
                        rebal = row['rebalancing']
                        if rebal :
                            previous_numeraire_size = row['new_btcs']
                            previous_liquidity_size = row['new_liquidities']
                            previous_price =  row['Close']
                            numeraire_sizes[counter] = previous_numeraire_size
                        else :
                            # we mark to market the asset valo
                            current_price = row['Close']
                            deltanumeraire = get_new_btc_quantity_from_price_change(previous_liquidity_size, current_price, previous_price)
                            numeraire_size = previous_numeraire_size + deltanumeraire
                            numeraire_sizes[counter] = numeraire_size
                        counter = counter + 1
                    return numeraire_sizes
                stages_rebal_df['numeraire_size_mark_to_market'] = compute_mark_to_market_numeraire_assets(to_keep_init_btc, to_keep_init_liq,to_keep_init_price,data_df=stages_rebal_df.copy())

                def compute_mark_to_market_risky_assets(previous_risky_size,previous_liquidity_size,previous_price,data_df = None):
                    counter = 0
                    risky_sizes = np.zeros(len(data_df))
                    for i, row in data_df.iterrows():
                        rebal = row['rebalancing']
                        if rebal :
                            previous_risky_size = row['new_ethers']
                            previous_liquidity_size = row['new_liquidities']
                            previous_price =  row['Close']
                            risky_sizes[counter] = previous_risky_size
                        else :
                            # we mark to market the asset valo
                            current_price = row['Close']
                            delta_risky = get_new_ether_quantity_from_price_change(previous_liquidity_size, current_price, previous_price)
                            risky_size = previous_risky_size + delta_risky
                            risky_sizes[counter] = risky_size
                        counter = counter + 1
                    return risky_sizes

                stages_rebal_df['risky_size_mark_to_market'] = compute_mark_to_market_risky_assets(to_keep_init_eth,to_keep_init_liq,to_keep_init_price,data_df=stages_rebal_df.copy())

                stages_rebal_df['new_btcs'].iloc[0]=to_keep_init_btc
                stages_rebal_df['new_ethers'].iloc[0]=to_keep_init_eth

                stages_rebal_df['new_btcs'] = stages_rebal_df['new_btcs'].ffill()
                stages_rebal_df['new_ethers'] = stages_rebal_df['new_ethers'].ffill()
                stages_rebal_df['new_liquidities'] = stages_rebal_df['new_liquidities'].ffill()

                stages_rebal_df['swapping_sizes'] = stages_rebal_df['swapping_sizes'].fillna(0.)


                stages_rebal_df['new_liquidities'] = stages_rebal_df['new_liquidities'].bfill()
                stages_rebal_df['swapping_sizes'] = stages_rebal_df['swapping_sizes'].bfill()



                stages_rebal_df = stages_rebal_df.rename(columns = {'new_btcs':'numeraire_size',
                                                 'new_ethers':'risky_size',
                                                 'new_liquidities':'liquidity_size'})

                print('investigating the rebalancing datas')


                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                # ####### ####### ####### ####### computing the incurred loss
                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######



                all_df = pd.merge(df.copy(),  stages_rebal_df.copy(),suffixes= ['','_rebal'], how = 'left', left_index=True, right_index=True)
                all_df['swapping_cost'] = all_df['swapping_cost'].fillna(0.)




                all_df['apr'] = all_df['apr'].fillna(0.)
                all_df['incurred_v3'] = all_df['incurred_v3'].fillna(0.)
                all_df['incurred_v2'] = all_df['incurred_v2'].fillna(0.)

                all_df['flipped_lp_position_profit'] = all_df['flipped_lp_position_profit'].fillna(0.)
                all_df['lp_position_profit'] = all_df['lp_position_profit'].fillna(0.)
                #all_df[['incurred_v3', 'lp_position_profit', 'we_rebalance_signal', 'preceding_vault_signal','flipped_lp_position_profit']]

                print('computing the gain and losses from all in liguidity')

                all_df['mark_to_market_loss_v2'] = 100. * (1.+all_df['curILv2'].values)



                all_df['loss_v3'] = 100. * np.cumprod(1 + all_df['incurred_v3'].values)
                all_df['loss_v2'] = 100. * np.cumprod(1 + all_df['incurred_v2'].values)

                all_df['curILv3'] = all_df['curILv3'].fillna(0.)
                all_df['rebalancing'] = all_df['rebalancing'].fillna(False)

                def compute_loss_v3_mark_to_market(data_df = None):
                    previous_valo = 100.
                    valos = np.zeros(len(data_df))
                    counter = 0
                    for i, row in data_df.iterrows():
                        rebal = row['rebalancing']
                        current_valo_since_rebal = row['curILv3']
                        valos[counter]= previous_valo * (1. + current_valo_since_rebal)
                        if rebal :
                            previous_valo = valos[counter]
                        counter = counter + 1
                    return valos

                all_df['mark_to_market_loss_v3'] = compute_loss_v3_mark_to_market(data_df=all_df[['incurred_v3', 'curILv3', 'rebalancing']].copy())
                all_df['mark_to_market_loss_v3_returns'] = all_df['mark_to_market_loss_v3'].pct_change()
                all_df['mark_to_market_loss_v3_returns'] = all_df['mark_to_market_loss_v3_returns'].fillna(0.)

                all_df['mark_to_market_loss_v3_without_reset'] = 100. * (1. + all_df['curILv3'].values)


                all_df['cumulated_apr'] =  100. * np.cumprod(1 + all_df['apr'].values)
                all_df['cumulated_swapping_costs'] =  100. * np.cumprod(1  - all_df['swapping_cost'].values)

                all_df['value_LP_LS'] = 100. * np.cumprod(1 + all_df['flipped_lp_position_profit'].values)
                all_df['value_LP_LO'] = 100. * np.cumprod(1 + all_df['lp_position_profit'].values)

                ### computing the mark to market value
                #### curlp_position_profit is the return since the last rebalancing position : the vintage point is reseted each time we rebalance
                ###all_df[['lp_position_profit', 'curlp_position_profit', 'rebalancing','mark_to_market_lp_value', 'value_LP_LO' ]]
                ## this would not work weneed reset
                all_df['mark_to_market_lp_value_without_reset'] = 100. * (1. + all_df['curlp_position_profit'].values)

                def compute_lp_mark_to_market(data_df = None):
                    previous_valo = 100.
                    valos = np.zeros(len(data_df))
                    counter = 0
                    for i, row in data_df.iterrows():
                        rebal = row['rebalancing']
                        current_valo_since_rebal = row['curlp_position_profit']
                        valos[counter]= previous_valo * (1. + current_valo_since_rebal)
                        if rebal :
                            previous_valo = valos[counter]
                        counter = counter + 1
                    return valos

                all_df['curlp_position_profit'] = all_df['curlp_position_profit'].fillna(0.)
                all_df['rebalancing'] = all_df['rebalancing'].fillna(False)

                all_df['mark_to_market_lp_value'] = compute_lp_mark_to_market(data_df = all_df[['lp_position_profit', 'curlp_position_profit', 'rebalancing','value_LP_LO']].copy())
                ###all_df[['lp_position_profit', 'curlp_position_profit', 'rebalancing','mark_to_market_lp_value', 'mark_to_market_lp_value_without_reset', 'value_LP_LO' ]]

                all_df['mark_to_market_lp_value_returns'] = all_df['mark_to_market_lp_value'].pct_change()
                all_df['mark_to_market_lp_value_returns'] = all_df['mark_to_market_lp_value_returns'].fillna(0.)

                all_df['performance_LP_LS'] = 100. * np.cumprod(
                    1 + all_df['flipped_lp_position_profit'].values + all_df['apr'].values - all_df['swapping_cost'].values)
                all_df['performance_LP_LO'] = 100. * np.cumprod(
                    1 + all_df['lp_position_profit'].values + all_df['apr'].values - all_df['swapping_cost'].values)

                all_df['performance_LP_LO_mark_to_market'] = 100. * np.cumprod(1 + all_df['mark_to_market_lp_value_returns'].values + all_df['apr'].values - all_df['swapping_cost'].values)

                all_df['performance_LP_LO'] = 100. * np.cumprod(
                    1 + all_df['lp_position_profit'].values + all_df['apr'].values - all_df['swapping_cost'].values)

                all_df['performance_ILV3_mark_to_market'] = 100. * np.cumprod(1 + all_df['mark_to_market_loss_v3_returns'].values + all_df['apr'].values - all_df['swapping_cost'].values)
                all_df['performance_ILV3'] = 100. * np.cumprod(1 + all_df['incurred_v3'].values + all_df['apr'].values - all_df['swapping_cost'].values)

                #all_df['gain_and_loss_v3'] = 100. * np.cumprod(1 + all_df['incurred_v3'].values + all_df['apr'].values)
                #all_df['gain_and_loss_v2'] = 100. * np.cumprod(1 + all_df['incurred_v2'].values + all_df['apr'].values )

                all_df['performance_against_risky_mark_to_market'] = all_df['performance_LP_LO_mark_to_market']/all_df['Close']
                all_df['performance_against_risky'] = all_df['performance_LP_LO']/all_df['Close']


                if plotHtml:
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['performance_against_risky_mark_to_market','performance_against_risky']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'Performance against a full risky HODL basket {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['performance_ILV3_mark_to_market']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'Performance against a 50/50 HODL basket {ssj} {ssj_against}')
                    fig.show()

                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['performance_ILV3_mark_to_market','performance_ILV3']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'Performance against a 50/50 HODL basket {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['performance_ILV3_mark_to_market']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'Performance against a 50/50 HODL basket {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['cumulated_swapping_costs']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'swapping costs {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['swapping_cost']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'swapping costs {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['swapping_sizes']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'swapping sizes {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['numeraire_size_mark_to_market','numeraire_size', 'risky_size_mark_to_market', 'risky_size']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'assets {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['numeraire_size_mark_to_market','numeraire_size']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'numeraire size {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['risky_size_mark_to_market','risky_size']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'risky {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['liquidity_size']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'liquidity size {ssj} {ssj_against}')
                    fig.show()

                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['loss_v3', 'mark_to_market_loss_v3']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'impermanent loss V3 {ssj} {ssj_against}')
                    fig.show()

                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['loss_v3', 'mark_to_market_loss_v3']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'loss v3 {ssj} {ssj_against}')
                    fig.show()


                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['loss_v2', 'mark_to_market_loss_v2']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'v3 bounds {ssj} {ssj_against}')
                    fig.show()

                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['value_LP_LO', 'mark_to_market_lp_value']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'mark-to-market/book LP position value {ssj} {ssj_against}')
                    fig.show()

                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['real_lower_bound', 'real_upper_bound', 'Close']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'v3 bounds {ssj} {ssj_against}')
                    fig.show()

                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['signal']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'v3 bounds {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['curILv3']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'v3 IL {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['curlp_value_first']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'LP position value {ssj} {ssj_against}')
                    fig.show()
                    fig = realtime_plotting_utility.plot_multiple_time_series(
                        data_df=all_df[['flipped_lp_position_profit']].copy(), logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'LP position value {ssj} {ssj_against}')
                    fig.show()

                    fig1 = realtime_plotting_utility.plot_multiple_time_series(
                        #                    data_df=all_df[['loss_v2', 'loss_v3', 'gain_and_loss_v3','gain_and_loss_LS']].copy(),
                        data_df=all_df[['performance_LP_LS', 'performance_LP_LO']].copy(),
                        logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'Absolute performance LO/LS {ssj} {ssj_against}')
                    fig1.show()

                    fig1 = realtime_plotting_utility.plot_multiple_time_series(
                        #                    data_df=all_df[['loss_v2', 'loss_v3', 'gain_and_loss_v3','gain_and_loss_LS']].copy(),
                        data_df=all_df[['performance_LP_LO_mark_to_market', 'performance_LP_LO']].copy(),
                        logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'Absolute performance v3 liquidity providing {ssj} {ssj_against}')
                    fig1.show()

                    fig1 = realtime_plotting_utility.plot_multiple_time_series(
                        #                    data_df=all_df[['loss_v2', 'loss_v3', 'gain_and_loss_v3','gain_and_loss_LS']].copy(),
                        data_df=all_df[['performance_LP_LO']].copy(),
                        logy=False, split=False,
                        put_on_same_scale=False,
                        title=f'Absolute performance v3 liquidity providing {ssj} {ssj_against}')
                    fig1.show()


                stages_df = all_df.copy()
                # computing the annulized loss
                delta = stages_df.index[len(stages_df) - 1] - stages_df.index[0]
                nb_years = delta.days / 365

                print(f'nb years {nb_years}')
                first_v3_value = stages_df['loss_v3'].iloc[0]
                first_v2_value = stages_df['loss_v2'].iloc[0]

                last_v3_value = stages_df['loss_v3'].iloc[len(stages_df) - 1]
                last_v2_value = stages_df['loss_v2'].iloc[len(stages_df) - 1]

                v2_loss_apy = annualize_percent(first_value=first_v2_value, last_value=last_v2_value,
                                                nb_years=nb_years)
                v3_loss_apy = annualize_percent(first_value=first_v3_value, last_value=last_v3_value,
                                                nb_years=nb_years)

                sum_rebalance = all_df['stage_nb'].max()

                # objective 1 : minimiser le nombre de rebalancements
                obj_rebalance = sum_rebalance
                # objective 2 : minimiser l'impermanent loss
                all_df['providingLiquidity'] = ~np.isnan(all_df['real_upper_bound'])
                on_mode = (all_df['providingLiquidity'] == 1).sum()/len(all_df)
                from cryptotoolbox.risk_metrics import riskmetrics

                kpi_df = riskmetrics.get_kpi(all_df[[f'performance_LP_LO_mark_to_market']])
                obf_data= {
                    'bb_period': bb_period,
                    'stdNbr': stdNbr,
                    'distance_to_bound_perc': distance_to_bound_perc,
                    'mean_pct_change': avg_pct_change,
                    'nb_rebalancing_days': obj_rebalance,
                    'on_mode':on_mode,
                    'v2_loss_apy': v2_loss_apy,
                    'v3_loss_apy': v3_loss_apy,
                }
                obf_data.update(kpi_df.to_dict()['performance_LP_LO_mark_to_market'])

                objectives.append(obf_data)

    print('done')
    objectives_df = pd.DataFrame(objectives)
    return objectives_df, all_df


def LS_IL_boundaries_with_signal_and_stoploss(data_df = None, plotHtml = False, me_pair = ('ETH', 'BTC'), bb_periods=[5, 15, 30, 55], stdNbrs=[2., 3., 5.], distance_to_bound_percs = [0,5,10,15,20,30,40], current_apr=None, bypass_signals=True, bypass_stoploss=True, swapping_cost_map = {1:1e-4, 10:0.01, 50:0.05, 75:0.075, 100:0.1},starting_number_of_numeraire = 1000, local_image_directory=None):
    weekly_hedging_cost = 0.01
    ssj = me_pair[0]
    ssj_against = me_pair[1]
    objectives = []
    for bypass_signal in bypass_signals:
        for bb_period in bb_periods:
            for stdNbr in stdNbrs:
                for distance_to_bound_perc in distance_to_bound_percs:
                    df = data_df.copy()
                    df['Date']=df.index
                    params_str = f'params_{bb_period}_{stdNbr}_{distance_to_bound_perc}'
                    print(params_str)
                    df = getBBands(df.copy(), period=bb_period, stdNbr=stdNbr)
                    df = df.dropna()

                    stage_nb = 0

                    pct_change = np.nan
                    real_upper_bound = np.nan
                    real_lower_bound = np.nan
                    buffer_upper_bound = np.nan
                    buffer_lower_bound = np.nan

                    initial_real_upper_bound = np.nan
                    initial_real_lower_bound = np.nan


                    df['pct_change'] = (stdNbr * df['std']) / df['Close'] * 100
                    avg_pct_change = df['pct_change'].mean()
                    ### to compute a proper metric
                    if bypass_stoploss:
                        df['stoploss_condition'] = False
                    if bypass_signal:
                        df['signal'] = 1.

                    if plotHtml:
                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=df[['Close', 'upper', 'lower']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'Bollinger {ssj}{ssj_against}')
                        fig.show()

                    initial_price = df['Close'].iloc[0]
                    begining_initial_price = df['Close'].iloc[0]

                    initial_lp_value = np.nan
                    preceding_vault_signal = df['signal'].iloc[0]

                    stages = []
                    counter = 0
                    the_end = False
                    for i, row in df.iterrows():
                        if i == df.index[-1]:
                            the_end = True
                        if counter == 0:
                            counter = counter + 1
                            continue
                        ILv3, ILv2 = np.nan, np.nan
                        lp_value_first, lp_value_second = np.nan, np.nan
                        lp_position_profit = np.nan
                        flipped_lp_position_profit = np.nan


                        apr = get_apr(row['DateStr'],  row['pct_change'], volume_df=data_df.copy(), current_apr=current_apr)

                        # if currently providing and we enter in a risk off mode we need to compute IL
                        we_are_out = np.isnan(real_upper_bound)

                        stoploss_condition = row['stoploss_condition']
                        vault_signal = row['signal']

                        print(f'real_upper_bound {real_upper_bound}')
                        high = row['High']
                        print(f'high {high}')
                        print(f'real_lower_bound {real_lower_bound}')
                        low = row['Low']
                        print(f'low {low}')
                        print(f'stoploss_condition {stoploss_condition}')
                        print(f'distance to bounds {distance_to_bound_perc}')
                        curILv3 = np.nan
                        curILv2 = np.nan
                        curlp_value_first = np.nan
                        curlp_value_second = np.nan
                        curlp_position_profit = np.nan
                        curflipped_lp_position_profit = np.nan

                        # defining_new_state = (bounds_broken and providing) or (providing and slope_too_sloppy)
                        broken_bounds = np.nan
                        if not we_are_out:
                            distance_to_bound = distance_to_bound_perc/100. * real_upper_bound
                            buffer_upper_bound = real_upper_bound - distance_to_bound
                            buffer_lower_bound = real_lower_bound + distance_to_bound

                            broken_bounds= (row['High'] > buffer_upper_bound or row['Low'] < buffer_lower_bound)
                            assert (not np.isnan(initial_price)) and (not np.isnan(real_lower_bound)) and (
                                not np.isnan(real_upper_bound))
                            p_out = row['Close']
                            curILv3, curILv2 = compute_impermanent_loss_v3(p_0=initial_price, p_a=real_lower_bound,
                                                                     p_b=real_upper_bound,
                                                                     p_out=p_out)
                            curlp_value_first = compute_total_LP_portfolio_value_first_methodo(p_a=real_lower_bound,
                                                                     p_b=real_upper_bound,
                                                                     p_out=p_out)
                            curlp_value_second = compute_total_LP_portfolio_value_second_methodo(p_a=real_lower_bound,
                                                                     p_b=real_upper_bound,
                                                                     p_out=p_out)
                            curlp_position_profit = (curlp_value_first - initial_lp_value) / initial_lp_value
                            curflipped_lp_position_profit = preceding_vault_signal * curlp_position_profit



                        signal_change = False
                        if vault_signal != preceding_vault_signal:
                            signal_change = True

                        we_enter = False
                        we_out = False
                        we_rebalance_signal = False
                        we_rebalance_bounds = False
                        #############
                        if stoploss_condition:
                            if we_are_out: ### we do nothing
                                print('we do nothing, already out')
                            if not we_are_out: ### we out
                                print('we out the position because of the stop loss condition')
                                we_out = True
                                assert (not np.isnan(initial_price)) and (not np.isnan(real_lower_bound)) and (
                                    not np.isnan(real_upper_bound))
                                p_out = row['Close']
                                ILv3, ILv2 = compute_impermanent_loss_v3(p_0=initial_price, p_a=real_lower_bound,
                                                                         p_b=real_upper_bound,
                                                                         p_out=p_out)
                                lp_value_first = compute_total_LP_portfolio_value_first_methodo(p_a=real_lower_bound,
                                                                                                p_b=real_upper_bound,
                                                                                                p_out=p_out)
                                lp_value_second = compute_total_LP_portfolio_value_second_methodo(p_a=real_lower_bound,
                                                                                                 p_b=real_upper_bound,
                                                                                                 p_out=p_out)
                                lp_position_profit = (lp_value_first-initial_lp_value)/initial_lp_value
                                flipped_lp_position_profit = preceding_vault_signal * lp_position_profit

                                real_upper_bound = np.nan
                                real_lower_bound = np.nan
                                stage_nb = stage_nb + 1

                        if not stoploss_condition:
                            if we_are_out: ### we enter a position  cause no stop loss signal
                                we_enter = True
                                print('we enter')
                                initial_price = row['Close']
                                real_upper_bound = row['High'] + stdNbr * row['std']

                                pct_change = (real_upper_bound - row['High']) / row['High']
                                real_lower_bound = row['Low'] - stdNbr * row['std']

                                if np.isnan(initial_real_upper_bound):
                                    initial_real_upper_bound = real_upper_bound
                                    initial_real_lower_bound = real_lower_bound

                                stage_nb = stage_nb + 1
                                if np.isnan(initial_lp_value):
                                    initial_lp_value = compute_total_LP_portfolio_value_first_methodo(p_a=real_lower_bound,
                                                                                                      p_b=real_upper_bound,
                                                                                                      p_out=initial_price)

                            if not we_are_out:
                                if broken_bounds or signal_change or the_end:## we rebalance
                                    if broken_bounds:
                                        we_rebalance_bounds = True
                                        print('we rebalance because of buffer bounds being touched')
                                    if signal_change:
                                        we_rebalance_signal=True
                                        print('we rebalance because of long/short signal change')
                                    up = row['High'] > buffer_upper_bound
                                    down = row['Low'] < buffer_lower_bound
                                    ## one bound must be broken
                                    assert up or down or signal_change or the_end
                                    # p_out = np.nan
                                    # if up:
                                    #     p_out = real_upper_bound
                                    # elif down:
                                    #     p_out = real_lower_bound
                                    # else:
                                    p_out = row['Close']

                                    ##### all in LP loss
                                    ILv3, ILv2 = compute_impermanent_loss_v3(p_0=initial_price, p_a=real_lower_bound,
                                                                             p_b=real_upper_bound,
                                                                             p_out=p_out)
                                    lp_value_first = compute_total_LP_portfolio_value_first_methodo(p_a=real_lower_bound,
                                                                                                    p_b=real_upper_bound,
                                                                                                    p_out=p_out)
                                    lp_value_second = compute_total_LP_portfolio_value_second_methodo(p_a=real_lower_bound,
                                                                                                      p_b=real_upper_bound,
                                                                                                      p_out=p_out)

                                    lp_position_profit = (lp_value_first - initial_lp_value) / initial_lp_value
                                    flipped_lp_position_profit = preceding_vault_signal * lp_position_profit


                                    # if up:
                                    #     initial_price = row['High']
                                    # else:
                                    #     initial_price = row['Low']
                                    initial_price = row['Close']

                                    # here compute the previous impermanent loss

                                    stage_nb = stage_nb + 1
                                    real_upper_bound = row['High'] + stdNbr * row['std']

                                    pct_change = (real_upper_bound - row['High']) / row['High']
                                    real_lower_bound = row['Low'] - stdNbr * row['std']

                                    initial_lp_value = compute_total_LP_portfolio_value_first_methodo(p_a=real_lower_bound,
                                                                                                      p_b=real_upper_bound,
                                                                                                      p_out=p_out)

                        stages.append({
                            'date': row['Date'],
                            'Close':row['Close'],
                            'incurred_v3': ILv3,
                            'incurred_v2': ILv2,
                            'pct_change' : pct_change,
                            'lp_position_profit':lp_position_profit,
                            'flipped_lp_position_profit':flipped_lp_position_profit,
                            'lp_value_first': lp_value_first,
                            'lp_value_second': lp_value_second,
                            'initial_lp_value':initial_lp_value,
                            'initial_price': initial_price,
                            'signal_change':signal_change,
                            'preceding_vault_signal':preceding_vault_signal,
                            'vault_signal':vault_signal,
                            'broken_bounds':broken_bounds,
                            'stoploss_condition':stoploss_condition,
                            'the_end': the_end,
                            'we_enter': we_enter,
                            'we_out' : we_out,
                            'curILv3' :curILv3,
                            'curILv2' :curILv2,
                            'curflipped_lp_position_profit': curflipped_lp_position_profit,
                            'curlp_position_profit': curlp_position_profit,
                            'curlp_value_first' : curlp_value_first,
                            'curlp_value_second' : curlp_value_second,
                            'we_rebalance_signal' : we_rebalance_signal,
                            'we_rebalance_bounds' : we_rebalance_bounds,
                            'real_upper_bound': real_upper_bound,
                            'real_lower_bound': real_lower_bound,
                            'buffer_upper_bound': buffer_upper_bound,
                            'buffer_lower_bound': buffer_lower_bound,
                            'distance_to_bound_perc':distance_to_bound_perc,
                            'stage_nb': stage_nb,
                            'apr': apr,
                        })
                        preceding_vault_signal = vault_signal

                    stages_df = pd.DataFrame(stages)

                    stages_df['vault_no_hedge'] = stages_df['preceding_vault_signal']>0.
                    hedging = False
                    hedging_cost_time =np.zeros(len(stages_df))
                    counter = 0
                    hedging_counter = 1
                    for ii, row in stages_df.iterrows():
                        vault_no_hedge = row['vault_no_hedge']
                        if not hedging and not vault_no_hedge:
                            hedging = True
                            hedging_counter = 1
                        if hedging and vault_no_hedge:
                            hedging = False
                        if hedging and not vault_no_hedge:
                            hedging_counter = hedging_counter + 1
                        if hedging_counter % 7 ==0:
                            hedging_cost_time[counter] = -weekly_hedging_cost
                        counter = counter + 1
                    stages_df['hedging_cost']=hedging_cost_time
                    print('hedging_cost done')

                    stages_df['vault_no_hedge'] = stages_df['vault_no_hedge'].astype(float)
                    stages_df['lp_position_profit'] = stages_df['lp_position_profit'].fillna(0.)
                    if not bypass_signal:
                        stages_df['lp_position_profit'] = stages_df['lp_position_profit']*stages_df['vault_no_hedge'] + stages_df['hedging_cost']

                    print('investigate')
                    ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    ####### ####### ####### ####### swapping cost analysis
                    ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    def rebalancing_signal(row):
                        we_rebalance_signal = row['we_rebalance_signal']
                        we_rebalance_bound = row['we_rebalance_bounds']
                        return we_rebalance_bound or we_rebalance_signal

                    stages_df['rebalancing'] = stages_df.apply(rebalancing_signal, axis=1)

                    rebalancing_df = stages_df[stages_df['rebalancing']].copy()
                    insert_rebalancing_costs = None
                    if len(rebalancing_df)>0:
                        rebalancing_df['leaving_initial_price'] = rebalancing_df['initial_price'].shift(+1)
                        rebalancing_df['leaving_initial_price'].iloc[0] = begining_initial_price
                        rebalancing_df['leaving_real_upper_bound'] = rebalancing_df['real_upper_bound'].shift(+1)
                        rebalancing_df['leaving_real_lower_bound'] = rebalancing_df['real_lower_bound'].shift(+1)
                        rebalancing_df['leaving_real_upper_bound'].iloc[0] = initial_real_upper_bound
                        rebalancing_df['leaving_real_lower_bound'].iloc[0] = initial_real_lower_bound

                        rebal_data_df = rebalancing_df[['date','leaving_initial_price', 'initial_price', 'real_upper_bound', 'real_lower_bound', 'leaving_real_upper_bound', 'leaving_real_lower_bound']]

                        def compute_percentage_spread(row):
                            pct_chagne = (row['leaving_real_upper_bound']-row['leaving_initial_price'])/row['leaving_initial_price']
                            return pct_chagne

                        rebal_data_df['pct_change_upper'] = rebal_data_df.apply(compute_percentage_spread, axis=1)

                        ### ether = X (risqué)
                        ### BTC = Y (numéraire)
                        ### P = P ether in BTC
                        def get_liquidity_from_BTC(nb_amount_BTC, current_price, lower_bound ):
                            return nb_amount_BTC/(np.sqrt(current_price) - np.sqrt(lower_bound) )

                        def get_liquidity_from_ETH(nb_amount_ETH, current_price, upper_bound ):
                            return nb_amount_ETH/(1./np.sqrt(current_price) - 1./np.sqrt(upper_bound))

                        def get_ether_from_liquidity(liquidity, current_price, upper_bound):
                            return liquidity*(1./np.sqrt(current_price) -1./np.sqrt(upper_bound))

                        def get_btc_from_liquidity(liquidity, current_price, lower_bound):
                            return liquidity*(np.sqrt(current_price) - np.sqrt(lower_bound) )




                        previous_liquidities = np.zeros(len(rebal_data_df))
                        previous_ethers = np.zeros(len(rebal_data_df))
                        previous_btcs = np.zeros(len(rebal_data_df))
                        new_liquidities = np.zeros(len(rebal_data_df))
                        new_ethers = np.zeros(len(rebal_data_df))
                        new_btcs = np.zeros(len(rebal_data_df))
                        swapping_sizes = np.zeros(len(rebal_data_df))
                        swap_costs = np.zeros(len(rebal_data_df))
                        count = 0

                        previous_btc = np.nan
                        previous_liquidity = np.nan
                        previous_eth = np.nan

                        new_btc = np.nan
                        new_liquidity = np.nan
                        new_eth = np.nan

                        rebal_data_df.index = range(len(rebal_data_df))
                        to_keep_init_liq = np.nan
                        to_keep_init_eth = np.nan
                        to_keep_init_btc = np.nan
                        to_keep_init_price = np.nan
                        for ii, row in rebal_data_df.iterrows():
                            if ii == 0 :
                                ### btc at initial date
                                previous_btc = starting_number_of_numeraire
                                ## initial position configuration: leaving_initial_price inbetween leaving_real_upper_bound and leaving_real_lower_bound
                                leaving_initial_price = row['leaving_initial_price']
                                leaving_real_upper_bound = row['leaving_real_upper_bound']
                                leaving_real_lower_bound = row['leaving_real_lower_bound']
                                ## liquidity at initial date
                                previous_liquidity = get_liquidity_from_BTC(previous_btc,leaving_initial_price,leaving_real_lower_bound )
                                ## ether at initial date
                                previous_eth = get_ether_from_liquidity(previous_liquidity, leaving_initial_price,leaving_real_upper_bound)
                                previous_liquidity_bis = get_liquidity_from_ETH(previous_eth, leaving_initial_price,leaving_real_upper_bound)
                                to_keep_init_liq=previous_liquidity
                                to_keep_init_eth=previous_eth
                                to_keep_init_btc = previous_btc
                                to_keep_init_price = leaving_initial_price

                                assert abs(previous_liquidity_bis - previous_liquidity) < 1e-3
                            else :
                                previous_btc = new_btc
                                previous_eth = new_eth
                                previous_liquidity = new_liquidity

                            swapping_size = np.nan
                            # we leave the 'leaving position' at a new price which will become the new initial price
                            newly_initial_price = row['initial_price']
                            ### we limit the price move to the upper and lower bounds of the position we are in (quantities do not move after in univ3)
                            truncated_newly_initial_price = min(newly_initial_price,leaving_real_upper_bound )
                            truncated_newly_initial_price = max(truncated_newly_initial_price,leaving_real_lower_bound )

                            def get_new_btc_quantity_from_price_change(liquidity, new_price, old_price):
                                return liquidity * (np.sqrt(new_price)-np.sqrt(old_price))

                            def get_new_ether_quantity_from_price_change(liquidity, new_price, old_price):
                                return liquidity * (1./np.sqrt(new_price)-1./np.sqrt(old_price))

                            deltaBTC = get_new_btc_quantity_from_price_change(previous_liquidity, truncated_newly_initial_price, leaving_initial_price)
                            deltaETH = get_new_ether_quantity_from_price_change(previous_liquidity, truncated_newly_initial_price, leaving_initial_price)

                            previous_ethers[count] = previous_eth
                            previous_btcs[count] = previous_btc
                            previous_liquidities[count] = previous_liquidity

                            after_withdrawal_btc = previous_btc + deltaBTC
                            after_withdrawal_eth = previous_eth + deltaETH

                            print(f'after_withdrawal_eth {after_withdrawal_eth}')
                            print(f'after_withdrawal_btc {after_withdrawal_btc}')

                            ####### rebalancing quantities for the new position
                            new_real_lower_bound = row['real_lower_bound']
                            new_real_upper_bound = row['real_upper_bound']
                            # rebalancing the bounds

                            def get_btc_matching_proportion(eth_amount=None, current_price=None, lower_bound=None,
                                                            upper_bound=None):
                                new_liquidity = get_liquidity_from_ETH(eth_amount, current_price, upper_bound)
                                new_btc = get_btc_from_liquidity(new_liquidity, current_price, lower_bound)
                                return new_btc, new_liquidity

                            def get_eth_matching_proportion(btc_amount=None, current_price=None, lower_bound=None,
                                                            upper_bound=None):
                                new_liquidity = get_liquidity_from_BTC(btc_amount, current_price, lower_bound)
                                new_eth = get_ether_from_liquidity(new_liquidity, current_price, upper_bound)
                                return new_eth, new_liquidity

                            new_btc, _ = get_btc_matching_proportion(eth_amount=after_withdrawal_eth,
                                                                     current_price=newly_initial_price,
                                                                     lower_bound=new_real_lower_bound,
                                                                     upper_bound=new_real_upper_bound)
                            ##### we end up with eth equivalent to more btc than we have : we must swap eth
                            has_to_swap_eth =  new_btc >= after_withdrawal_btc

                            new_eth, _ = get_eth_matching_proportion(btc_amount=after_withdrawal_btc,
                                                                     current_price=newly_initial_price,
                                                                     lower_bound=new_real_lower_bound,
                                                                     upper_bound=new_real_upper_bound)
                            ##### we end up with btc equivalent to more eth than we have : we must swap btc
                            has_to_swap_btc = new_eth >= after_withdrawal_eth
                            print(has_to_swap_btc)
                            print(has_to_swap_eth)
#                            if after_withdrawal_btc>0. and after_withdrawal_eth>0.:
#                                assert has_to_swap_btc == ~has_to_swap_eth

                            if has_to_swap_btc: #### we have more btcs than eth
                                new_btc = after_withdrawal_btc
                                print(f'new btc {new_btc}')
                                print(f'new price {newly_initial_price}')
                                print(f'new lower bound {new_real_lower_bound}')
                                print(f'new upper bound {new_real_upper_bound}')


                                pool_ratio_price = new_btc/new_eth
                                print(f'new ratio {pool_ratio_price}')

                                def get_eth_amount_to_swap(x= None, slippage = 20e-4, initial_btc=None,initial_ether=None,lower_bound=None, upper_bound=None, current_price=None):
                                    btc_left = (1.-x)*initial_btc
                                    #### if we swap too big quantities we incur price slippage
                                    #### if we swap BTCs to ETH, the price of ETH in BTC Y/X will drop
                                    slippage_price = current_price * (1. - slippage)
                                    ##### the left btc and swapped ether will make the position
                                    eth_in_lp, liquidity = get_eth_matching_proportion(btc_amount=btc_left,
                                                                               current_price=slippage_price,
                                                                               lower_bound=lower_bound,
                                                                               upper_bound=upper_bound)
                                    return eth_in_lp ,slippage_price,liquidity

                                def get_eth_amount_to_swap_functional(x= None, slippage = 20e-4, initial_btc=None,initial_ether=None,lower_bound=None, upper_bound=None, current_price=None):
                                    btc_left = (1.-x)*initial_btc

                                    btc_to_swap = x*initial_btc
                                    #### if we swap too big quantities we incur price slippage
                                    #### if we swap BTCs to ETH, the price of ETH in BTC Y/X will drop
                                    slippage_price = current_price * (1. - slippage)
                                    ##### the left btc and swapped ether will make the position
                                    eth_in_lp, _ = get_eth_matching_proportion(btc_amount=btc_left,
                                                                               current_price=slippage_price,
                                                                               lower_bound=lower_bound,
                                                                               upper_bound=upper_bound)
                                    differential = (eth_in_lp -initial_ether)*slippage_price - btc_to_swap
                                    return abs(differential)

                                to_optimize = lambda x: get_eth_amount_to_swap_functional(x=x,initial_btc = after_withdrawal_btc, initial_ether = after_withdrawal_eth,current_price= newly_initial_price, lower_bound=new_real_lower_bound, upper_bound = new_real_upper_bound)
                                test_opti = to_optimize(0.5)
                                low_bound = 0.
                                up_bound = 1.
                                const_ind = Bounds(low_bound , up_bound )


                                result_final = minimize(
                                    to_optimize,
                                    0.5,
                                    bounds=const_ind,
                                    method='Nelder-Mead'
                                )
                                optimal_size_to_swap = np.nan
                                if result_final.success:
                                    optimal_size_to_swap = result_final.x[0]

                                print(f'optimal_size_to_swap {optimal_size_to_swap}')
                                swapping_size = optimal_size_to_swap
                                new_btc = (1.-optimal_size_to_swap)*after_withdrawal_btc
                                new_eth,slippage_price,liquidity = get_eth_amount_to_swap(x=optimal_size_to_swap,initial_btc = after_withdrawal_btc,  initial_ether = after_withdrawal_eth,current_price= newly_initial_price, lower_bound=new_real_lower_bound, upper_bound = new_real_upper_bound)

                                new_liquidity = get_liquidity_from_ETH(new_eth, slippage_price,new_real_upper_bound)
                                new_liquidity_bis = get_liquidity_from_BTC(new_btc, slippage_price,new_real_lower_bound)

                                if not np.isnan(new_liquidity) and not abs(new_liquidity) < 1e-6:
                                    condition_to_check = abs(new_liquidity-new_liquidity_bis)/abs(new_liquidity)<1e-3
                                    if not condition_to_check:
                                        print('trouble')
                                    assert abs(new_liquidity-new_liquidity_bis)/abs(new_liquidity)<1e-3
                                else :
                                    print('trouble')

                            elif has_to_swap_eth :
                                new_eth = after_withdrawal_eth
                                print(f'new eth {new_eth}')
                                print(f'new price {newly_initial_price}')
                                print(f'new lower bound {new_real_lower_bound}')
                                print(f'new upper bound {new_real_upper_bound}')


                                def get_btc_amount_to_swap(x= None, slippage = 20e-4, initial_eth=None, initial_btc=None,lower_bound=None, upper_bound=None, current_price=None):
                                    eth_left = (1.-x)*initial_eth
                                    eth_to_swap = x*initial_eth
                                    #### if we swap too big quantities we incur price slippage
                                    #### if we swap BTCs to ETH, the price of ETH in BTC Y/X will drop
                                    slippage_price = current_price * (1. + slippage)
                                    ##### the left btc and swapped ether will make the position
                                    btc_in_lp, liquidity = get_btc_matching_proportion(eth_amount=eth_left,
                                                                               current_price=slippage_price,
                                                                               lower_bound=lower_bound,
                                                                               upper_bound=upper_bound)
                                    return btc_in_lp, slippage_price, liquidity

                                def get_btc_amount_to_swap_functional(x= None, slippage = 20e-4, initial_eth=None,initial_btc=None,lower_bound=None, upper_bound=None, current_price=None):
                                    eth_left = (1.-x)*initial_eth
                                    eth_to_swap = x*initial_eth
                                    #### if we swap too big quantities we incur price slippage
                                    #### if we swap BTCs to ETH, the price of ETH in BTC Y/X will drop
                                    slippage_price = current_price * (1. + slippage)
                                    ##### the left btc and swapped ether will make the position
                                    btc_in_lp, _ = get_btc_matching_proportion(eth_amount=eth_left,
                                                                               current_price=slippage_price,
                                                                               lower_bound=lower_bound,
                                                                               upper_bound=upper_bound)
                                    differential = eth_to_swap*slippage_price - (btc_in_lp-initial_btc)
                                    return abs(differential)

                                to_optimize = lambda x: get_btc_amount_to_swap_functional(x=x,initial_eth = after_withdrawal_eth,initial_btc= after_withdrawal_btc, current_price=newly_initial_price, lower_bound=new_real_lower_bound, upper_bound = new_real_upper_bound)
                                test_opti = to_optimize(0.5)
                                low_bound = 0.
                                up_bound = 1.
                                const_ind = Bounds(low_bound , up_bound )


                                result_final = minimize(
                                    to_optimize,
                                    0.5,
                                    bounds=const_ind,
                                    method='Nelder-Mead'
                                )
                                optimal_size_to_swap = np.nan
                                if result_final.success:
                                    optimal_size_to_swap = result_final.x[0]

                                print(f'optimal_size_to_swap {optimal_size_to_swap}')
                                swapping_size = optimal_size_to_swap
                                new_eth = (1.-optimal_size_to_swap)*after_withdrawal_eth
                                new_btc, slippage_price, liquidity = get_btc_amount_to_swap(x=optimal_size_to_swap,initial_eth = after_withdrawal_eth,initial_btc= after_withdrawal_btc, current_price=newly_initial_price, lower_bound=new_real_lower_bound, upper_bound = new_real_upper_bound)

                                new_liquidity = get_liquidity_from_ETH(new_eth, slippage_price,new_real_upper_bound)
                                new_liquidity_bis = get_liquidity_from_BTC(new_btc, slippage_price,new_real_lower_bound)
                                if not np.isnan(new_liquidity) and not abs(new_liquidity) < 1e-6:
                                    condition_to_check = abs(new_liquidity-new_liquidity_bis)/abs(new_liquidity)<1e-3
                                    if not condition_to_check:
                                        print('trouble')
                                    assert abs(new_liquidity-new_liquidity_bis)/abs(new_liquidity)<1e-3
                                else :
                                    print('trouble')
                            else :
                                new_eth = after_withdrawal_eth
                                new_btc = after_withdrawal_btc

                            new_ethers[count] = new_eth
                            new_btcs[count] = new_btc
                            new_liquidities[count] = new_liquidity
                            swapping_sizes[count] = swapping_size
                            swap_cost = get_swapping_cost(swapping_size_proportion=swapping_size, swapping_cost_map=swapping_cost_map)
                            swap_costs[count] = swap_cost

                            previous_liquidity=new_liquidity
                            previous_btc=new_btc
                            previous_eth=new_eth

                            count = count + 1
                            print('done')

                        rebal_data_df['previous_btcs'] = previous_btcs
                        rebal_data_df['previous_ethers'] = previous_ethers
                        rebal_data_df['previous_liquidities'] = previous_liquidities

                        rebal_data_df['new_btcs'] = new_btcs
                        rebal_data_df['new_ethers'] = new_ethers
                        rebal_data_df['new_liquidities'] = new_liquidities

                        rebal_data_df['swapping_sizes'] = swapping_sizes
                        rebal_data_df['swapping_cost'] = swap_costs
                        insert_rebalancing_costs = True
                    else:
                        insert_rebalancing_costs = False

                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    # ####### ####### ####### ####### end of swapping cost analysis
                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    #
                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    # ####### ####### ####### ####### incorporation into the backtest
                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######

                    stages_df['date'] = pd.to_datetime(stages_df['date'])
                    stages_df.set_index('date', inplace=True)
                    stages_rebal_df = None

                    if insert_rebalancing_costs:
                        stages_rebal_df = pd.merge(stages_df.copy(), rebal_data_df.copy(), suffixes = ['','_rebal'],  how = 'left', right_on='date', left_on='date')
                        stages_rebal_df = stages_rebal_df.set_index('date')
                        print('computing the mark to market value')

                        def compute_mark_to_market_numeraire_assets(previous_numeraire_size, previous_liquidity_size,
                                                                    previous_price, data_df=None):
                            counter = 0
                            numeraire_sizes = np.zeros(len(data_df))
                            for i, row in data_df.iterrows():
                                rebal = row['rebalancing']
                                if rebal:
                                    previous_numeraire_size = row['new_btcs']
                                    previous_liquidity_size = row['new_liquidities']
                                    previous_price = row['Close']
                                    numeraire_sizes[counter] = previous_numeraire_size
                                else:
                                    # we mark to market the asset valo
                                    current_price = row['Close']
                                    deltanumeraire = get_new_btc_quantity_from_price_change(previous_liquidity_size,
                                                                                            current_price,
                                                                                            previous_price)
                                    numeraire_size = previous_numeraire_size + deltanumeraire
                                    numeraire_sizes[counter] = numeraire_size
                                counter = counter + 1
                            return numeraire_sizes

                        stages_rebal_df['numeraire_size_mark_to_market'] = compute_mark_to_market_numeraire_assets(
                            to_keep_init_btc, to_keep_init_liq, to_keep_init_price, data_df=stages_rebal_df.copy())

                        def compute_mark_to_market_risky_assets(previous_risky_size, previous_liquidity_size,
                                                                previous_price, data_df=None):
                            counter = 0
                            risky_sizes = np.zeros(len(data_df))
                            for i, row in data_df.iterrows():
                                rebal = row['rebalancing']
                                if rebal:
                                    previous_risky_size = row['new_ethers']
                                    previous_liquidity_size = row['new_liquidities']
                                    previous_price = row['Close']
                                    risky_sizes[counter] = previous_risky_size
                                else:
                                    # we mark to market the asset valo
                                    current_price = row['Close']
                                    delta_risky = get_new_ether_quantity_from_price_change(previous_liquidity_size,
                                                                                           current_price,
                                                                                           previous_price)
                                    risky_size = previous_risky_size + delta_risky
                                    risky_sizes[counter] = risky_size
                                counter = counter + 1
                            return risky_sizes

                        stages_rebal_df['risky_size_mark_to_market'] = compute_mark_to_market_risky_assets(
                            to_keep_init_eth, to_keep_init_liq, to_keep_init_price, data_df=stages_rebal_df.copy())

                        stages_rebal_df['new_btcs'].iloc[0] = to_keep_init_btc
                        stages_rebal_df['new_ethers'].iloc[0] = to_keep_init_eth

                        stages_rebal_df['new_btcs'] = stages_rebal_df['new_btcs'].ffill()
                        stages_rebal_df['new_ethers'] = stages_rebal_df['new_ethers'].ffill()
                        stages_rebal_df['new_liquidities'] = stages_rebal_df['new_liquidities'].ffill()

                        stages_rebal_df['swapping_sizes'] = stages_rebal_df['swapping_sizes'].fillna(0.)

                        stages_rebal_df['new_liquidities'] = stages_rebal_df['new_liquidities'].bfill()
                        stages_rebal_df['swapping_sizes'] = stages_rebal_df['swapping_sizes'].bfill()

                        stages_rebal_df = stages_rebal_df.rename(columns={'new_btcs': 'numeraire_size',
                                                                          'new_ethers': 'risky_size',
                                                                          'new_liquidities': 'liquidity_size'})

                        print('investigating the rebalancing datas')


                    else :
                        stages_rebal_df = stages_df.copy()
                        stages_rebal_df['swapping_cost'] = 0.
                        stages_rebal_df['swapping_sizes'] = 0.
                        stages_rebal_df['risky_size_mark_to_market'] = 0.
                        stages_rebal_df['numeraire_size_mark_to_market'] = 0.
                        stages_rebal_df['risky_size'] = 0.
                        stages_rebal_df['numeraire_size'] = 0.
                        stages_rebal_df['liquidity_size'] = 0.

                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    # ####### ####### ####### ####### computing the incurred loss
                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
                    # ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######



                    all_df = pd.merge(df.copy(),  stages_rebal_df.copy(),suffixes= ['','_rebal'], how = 'left', left_index=True, right_index=True)
                    all_df['swapping_cost'] = all_df['swapping_cost'].fillna(0.)




                    all_df['apr'] = all_df['apr'].fillna(0.)
                    all_df['incurred_v3'] = all_df['incurred_v3'].fillna(0.)
                    all_df['incurred_v2'] = all_df['incurred_v2'].fillna(0.)

                    all_df['flipped_lp_position_profit'] = all_df['flipped_lp_position_profit'].fillna(0.)
                    all_df['lp_position_profit'] = all_df['lp_position_profit'].fillna(0.)
                    #all_df[['incurred_v3', 'lp_position_profit', 'we_rebalance_signal', 'preceding_vault_signal','flipped_lp_position_profit']]

                    print('computing the gain and losses from all in liguidity')

                    all_df['mark_to_market_loss_v2'] = 100. * (1.+all_df['curILv2'].values)



                    all_df['loss_v3'] = 100. * np.cumprod(1 + all_df['incurred_v3'].values)
                    all_df['loss_v2'] = 100. * np.cumprod(1 + all_df['incurred_v2'].values)

                    all_df['curILv3'] = all_df['curILv3'].fillna(0.)
                    all_df['rebalancing'] = all_df['rebalancing'].fillna(False)

                    def compute_loss_v3_mark_to_market(data_df = None):
                        previous_valo = 100.
                        valos = np.zeros(len(data_df))
                        counter = 0
                        for i, row in data_df.iterrows():
                            rebal = row['rebalancing']
                            current_valo_since_rebal = row['curILv3']
                            valos[counter]= previous_valo * (1. + current_valo_since_rebal)
                            if rebal :
                                previous_valo = valos[counter]
                            counter = counter + 1
                        return valos

                    all_df['mark_to_market_loss_v3'] = compute_loss_v3_mark_to_market(data_df=all_df[['incurred_v3', 'curILv3', 'rebalancing']].copy())
                    all_df['mark_to_market_loss_v3_returns'] = all_df['mark_to_market_loss_v3'].pct_change()
                    all_df['mark_to_market_loss_v3_returns'] = all_df['mark_to_market_loss_v3_returns'].fillna(0.)

                    all_df['mark_to_market_loss_v3_without_reset'] = 100. * (1. + all_df['curILv3'].values)


                    all_df['cumulated_apr'] =  100. * np.cumprod(1 + all_df['apr'].values)
                    all_df['cumulated_swapping_costs'] =  100. * np.cumprod(1  - all_df['swapping_cost'].values)

                    all_df['value_LP_LS'] = 100. * np.cumprod(1 + all_df['flipped_lp_position_profit'].values)
                    all_df['value_LP_LO'] = 100. * np.cumprod(1 + all_df['lp_position_profit'].values)

                    ### computing the mark to market value
                    #### curlp_position_profit is the return since the last rebalancing position : the vintage point is reseted each time we rebalance
                    ###all_df[['lp_position_profit', 'curlp_position_profit', 'rebalancing','mark_to_market_lp_value', 'value_LP_LO' ]]
                    ## this would not work weneed reset
                    all_df['mark_to_market_lp_value_without_reset'] = 100. * (1. + all_df['curlp_position_profit'].values)

                    def compute_lp_mark_to_market(data_df = None):
                        previous_valo = 100.
                        valos = np.zeros(len(data_df))
                        counter = 0
                        for i, row in data_df.iterrows():
                            rebal = row['rebalancing']
                            current_valo_since_rebal = row['curlp_position_profit']
                            valos[counter]= previous_valo * (1. + current_valo_since_rebal)
                            if rebal :
                                previous_valo = valos[counter]
                            counter = counter + 1
                        return valos

                    all_df['curlp_position_profit'] = all_df['curlp_position_profit'].fillna(0.)
                    all_df['rebalancing'] = all_df['rebalancing'].fillna(False)

                    all_df['mark_to_market_lp_value'] = compute_lp_mark_to_market(data_df = all_df[['lp_position_profit', 'curlp_position_profit', 'rebalancing','value_LP_LO']].copy())
                    ###all_df[['lp_position_profit', 'curlp_position_profit', 'rebalancing','mark_to_market_lp_value', 'mark_to_market_lp_value_without_reset', 'value_LP_LO' ]]

                    all_df['mark_to_market_lp_value_returns'] = all_df['mark_to_market_lp_value'].pct_change()
                    all_df['mark_to_market_lp_value_returns'] = all_df['mark_to_market_lp_value_returns'].fillna(0.)

                    all_df['performance_LP_LS'] = 100. * np.cumprod(
                        1 + all_df['flipped_lp_position_profit'].values + all_df['apr'].values - all_df['swapping_cost'].values)
                    all_df['performance_LP_LO'] = 100. * np.cumprod(
                        1 + all_df['lp_position_profit'].values + all_df['apr'].values - all_df['swapping_cost'].values)

                    all_df['performance_LP_LO_mark_to_market'] = 100. * np.cumprod(1 + all_df['mark_to_market_lp_value_returns'].values + all_df['apr'].values - all_df['swapping_cost'].values)

                    all_df['performance_LP_LO'] = 100. * np.cumprod(
                        1 + all_df['lp_position_profit'].values + all_df['apr'].values - all_df['swapping_cost'].values)

                    all_df['performance_ILV3_mark_to_market'] = 100. * np.cumprod(1 + all_df['mark_to_market_loss_v3_returns'].values + all_df['apr'].values - all_df['swapping_cost'].values)
                    all_df['performance_ILV3'] = 100. * np.cumprod(1 + all_df['incurred_v3'].values + all_df['apr'].values - all_df['swapping_cost'].values)

                    #all_df['gain_and_loss_v3'] = 100. * np.cumprod(1 + all_df['incurred_v3'].values + all_df['apr'].values)
                    #all_df['gain_and_loss_v2'] = 100. * np.cumprod(1 + all_df['incurred_v2'].values + all_df['apr'].values )

                    all_df['performance_against_risky_mark_to_market'] = all_df['performance_LP_LO_mark_to_market']/all_df['Close']
                    all_df['performance_against_risky'] = all_df['performance_LP_LO']/all_df['Close']

                    params_str = params_str.replace('.', 'comma')
                    if plotHtml:
                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['performance_against_risky_mark_to_market','performance_against_risky']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'Performance_against_a_full_risky_HODL_basket_{ssj}{ssj_against}.png')
                        fig.show()
                        fig.write_image(local_image_directory+f'Performance_against_a_full risky_HODL_basket_{ssj}{ssj_against}{params_str}.png')
                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['performance_ILV3_mark_to_market']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'Performance against a 50/50 HODL basket {ssj} {ssj_against}')
                        fig.write_image(local_image_directory+f'Performance_against_a_5050_HODL_basket_{ssj}{ssj_against}{params_str}.png')
                        fig.show()

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['performance_ILV3_mark_to_market','performance_ILV3']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'Performance against a 50/50 HODL basket {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'Performance_against_a_5050_HODL_basket_{ssj}{ssj_against}{params_str}.png')

                        # fig = realtime_plotting_utility.plot_multiple_time_series(
                        #     data_df=all_df[['performance_ILV3_mark_to_market']].copy(), logy=False, split=False,
                        #     put_on_same_scale=False,
                        #     title=f'Performance against a 50/50 HODL basket {ssj} {ssj_against}')
                        # fig.show()
                        # fig.write_image(local_image_directory+f'Performance_against_a_5050_HODL_basket_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['cumulated_swapping_costs']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'cumulated swapping costs {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'cumulated_swapping_costs_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['swapping_cost']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'swapping costs {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'swapping_costs_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['swapping_sizes']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'swapping sizes {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'swapping_sizes_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['numeraire_size_mark_to_market','numeraire_size', 'risky_size_mark_to_market', 'risky_size']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'assets {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'assets_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['numeraire_size_mark_to_market','numeraire_size']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'numeraire size {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'numeraire_size_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['risky_size_mark_to_market','risky_size']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'risky {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'risky_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['liquidity_size']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'liquidity size {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'liquidity_size_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['loss_v3', 'mark_to_market_loss_v3']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'impermanent loss V3 {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'impermanent_loss_V3_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['loss_v3', 'mark_to_market_loss_v3']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'loss v3 {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'loss_v3_{ssj}{ssj_against}{params_str}.png')


                        # fig = realtime_plotting_utility.plot_multiple_time_series(
                        #     data_df=all_df[['loss_v2', 'mark_to_market_loss_v2']].copy(), logy=False, split=False,
                        #     put_on_same_scale=False,
                        #     title=f'v3 bounds {ssj} {ssj_against}')
                        # fig.show()
                        # fig.write_image(local_image_directory+f'v2_bounds_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['value_LP_LO', 'mark_to_market_lp_value']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'mark-to-market_book LP position value {ssj} {ssj_against}.png')
                        fig.show()
                        fig.write_image(local_image_directory+f'mark-to-market_book_LP_position_value_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['real_lower_bound', 'real_upper_bound', 'Close']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'v3 bounds {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'v3_bounds_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['signal']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'v3 bounds {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'v3_bounds_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['curILv3']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'v3 IL {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'v3_IL_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['curlp_value_first']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'LP position value {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'LP_position_value_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            data_df=all_df[['flipped_lp_position_profit']].copy(), logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'LP position value {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'LP_position_value_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            #                    data_df=all_df[['loss_v2', 'loss_v3', 'gain_and_loss_v3','gain_and_loss_LS']].copy(),
                            data_df=all_df[['performance_LP_LS', 'performance_LP_LO']].copy(),
                            logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'Absolute performance LO/LS {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'Absolute_performance_LO_LS_{ssj}{ssj_against}{params_str}.png')

                        fig = realtime_plotting_utility.plot_multiple_time_series(
                            #                    data_df=all_df[['loss_v2', 'loss_v3', 'gain_and_loss_v3','gain_and_loss_LS']].copy(),
                            data_df=all_df[['performance_LP_LO_mark_to_market', 'performance_LP_LO']].copy(),
                            logy=False, split=False,
                            put_on_same_scale=False,
                            title=f'Absolute performance v3 liquidity providing {ssj} {ssj_against}')
                        fig.show()
                        fig.write_image(local_image_directory+f'Absolute_performance_v3_liquidity_providing_{ssj}{ssj_against}{params_str}.png')

                        # fig = realtime_plotting_utility.plot_multiple_time_series(
                        #     #                    data_df=all_df[['loss_v2', 'loss_v3', 'gain_and_loss_v3','gain_and_loss_LS']].copy(),
                        #     data_df=all_df[['performance_LP_LO']].copy(),
                        #     logy=False, split=False,
                        #     put_on_same_scale=False,
                        #     title=f'Absolute performance v3 liquidity providing {ssj} {ssj_against}')
                        # fig.show()
                        # fig.write_image(local_image_directory+f'Absolute_performance_v3_liquidity_providing_{ssj}{ssj_against}{params_str}.png')


                    stages_df = all_df.copy()
                    # computing the annulized loss
                    delta = stages_df.index[len(stages_df) - 1] - stages_df.index[0]
                    nb_years = delta.days / 365

                    print(f'nb years {nb_years}')
                    first_v3_value = stages_df['loss_v3'].iloc[0]
                    first_v2_value = stages_df['loss_v2'].iloc[0]

                    last_v3_value = stages_df['loss_v3'].iloc[len(stages_df) - 1]
                    last_v2_value = stages_df['loss_v2'].iloc[len(stages_df) - 1]

                    v2_loss_apy = annualize_percent(first_value=first_v2_value, last_value=last_v2_value,
                                                    nb_years=nb_years)
                    v3_loss_apy = annualize_percent(first_value=first_v3_value, last_value=last_v3_value,
                                                    nb_years=nb_years)

                    sum_rebalance = all_df['stage_nb'].max()

                    # objective 1 : minimiser le nombre de rebalancements
                    obj_rebalance = sum_rebalance
                    # objective 2 : minimiser l'impermanent loss
                    all_df['providingLiquidity'] = ~np.isnan(all_df['real_upper_bound'])
                    on_mode = (all_df['providingLiquidity'] == 1).sum()/len(all_df)
                    from cryptotoolbox.risk_metrics import riskmetrics

                    kpi_df = riskmetrics.get_kpi(all_df[[f'performance_LP_LO_mark_to_market']])
                    obf_data= {
                        'bypass_signal':bypass_signal,
                        'bb_period': bb_period,
                        'stdNbr': stdNbr,
                        'distance_to_bound_perc': distance_to_bound_perc,
                        'mean_pct_change': avg_pct_change,
                        'nb_rebalancing_days': obj_rebalance,
                        'on_mode':on_mode,
                        'v2_loss_apy': v2_loss_apy,
                        'v3_loss_apy': v3_loss_apy,
                    }
                    obf_data.update(kpi_df.to_dict()['performance_LP_LO_mark_to_market'])

                    objectives.append(obf_data)

    print('done')
    objectives_df = pd.DataFrame(objectives)
    return objectives_df, all_df
