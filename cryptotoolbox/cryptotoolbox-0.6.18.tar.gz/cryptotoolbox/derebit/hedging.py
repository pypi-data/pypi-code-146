import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, minimize
from cryptotoolbox.realtime import realtime_plotting_utility

def final_value_pool_assets(final_price=None, initial_lp_value = None, initial_asset_price=None, initial_asset_a_amt=None, initial_asset_b_amt=None, lp_lower_bound=None, lp_upper_bound=None):
    notional = None
    if initial_asset_price < lp_lower_bound:
        notional = initial_asset_a_amt
    elif (
            initial_asset_price > lp_lower_bound
            and initial_asset_price < lp_upper_bound
    ):
        notional = (
                initial_asset_a_amt
                * (initial_asset_price / lp_lower_bound) ** 0.5
                * (
                        (lp_upper_bound) ** 0.5
                        - (lp_lower_bound) ** 0.5
                )
                / (
                        (lp_upper_bound) ** 0.5
                        - (initial_asset_price) ** 0.5
                )
        )
    else:
        notional = initial_asset_b_amt / (
                (lp_lower_bound * lp_upper_bound) ** 0.5
        )
    final_amount_a = None
    final_amount_b = None
    if final_price <= lp_lower_bound:
        final_amount_a = notional
        final_amount_b = 0
    elif (
            final_price > lp_lower_bound
            and final_price < lp_upper_bound
    ):
        final_amount_a = (
                notional
                * (lp_lower_bound / final_price) ** 0.5
                * ((lp_upper_bound) ** 0.5 - (final_price) ** 0.5)
                / (
                        (lp_upper_bound) ** 0.5
                        - (lp_lower_bound) ** 0.5
                )
        )
        final_amount_b = (
                notional
                * ((lp_lower_bound * lp_upper_bound) ** 0.5)
                * (((final_price) ** 0.5) - ((lp_lower_bound) ** 0.5))
                / (
                        (lp_upper_bound) ** 0.5
                        - (lp_lower_bound) ** 0.5
                )
        )
    else:
        final_amount_a = 0
        final_amount_b = (
                notional * (lp_lower_bound * lp_upper_bound) ** 0.5
        )
    return (final_amount_a * final_price + final_amount_b)-initial_lp_value


def compute_optional_profile(x,y, longs_val=None, shorts_val=None, lp_lower_bound=None, lp_upper_bound=None, get_lp_value_gain=None):
    results=[]
    for final_price in [lp_lower_bound + (i / 100.) * (lp_upper_bound - lp_lower_bound) for i in range(0, 100, 10)]:
        lp_value = get_lp_value_gain(final_price)
        print(f'final price {final_price}')
        print(f'final lp_value {lp_value}')

        mid_size = int(len(x))
        total_deriv_payoff = 0.
        for i in range(mid_size):
            pay_of_long_i = x[i] * longs_val[i](final_price)
            pay_of_short_i = y[i] * shorts_val[i](final_price)
            total_deriv_payoff = total_deriv_payoff + pay_of_long_i + pay_of_short_i

        tmp = {
            'price': final_price,
            'lp_value': lp_value,
            'deriv_payoff':total_deriv_payoff
        }
        results.append(tmp)

    value_df = pd.DataFrame().from_dict(results)
    value_df = value_df.set_index('price')
    return value_df

def compute_derivatives_profile(longs_val=None, shorts_val=None, lp_lower_bound=None, lp_upper_bound=None, get_lp_value_gain=None):
    results=[]
    for final_price in [lp_lower_bound + (i / 100.) * (lp_upper_bound - lp_lower_bound) for i in range(0, 100, 10)]:
        lp_value = get_lp_value_gain(final_price)
        print(f'final price {final_price}')
        print(f'final lp_value {lp_value}')
        mid_size = len(longs_val)
        tmp = {
            'price': final_price,
            'lp_value': lp_value,
        }
        for i in range(mid_size):
            pay_of_long_i = 1. * longs_val[i](final_price)
            pay_of_short_i = 1. * shorts_val[i](final_price)
            tmp[f'pay_of_long_{i}']=pay_of_long_i
            tmp[f'pay_of_short_{i}']=pay_of_short_i

        results.append(tmp)

    value_df = pd.DataFrame().from_dict(results)
    value_df = value_df.set_index('price')
    return value_df


def hedge_global_lp_position(maturity_df, get_lp_value_gain=None, lp_lower_bound=None, lp_upper_bound=None, plot_html=True):
    try:
        longs_val =  maturity_df['long_payoff_fun'].values
        shorts_val = maturity_df['short_payoff_fun'].values
        x_init = np.zeros(2 * len(longs_val))
        def to_optimize_l1_distance(x, longs_val=None, shorts_val=None,lp_lower_bound=None, lp_upper_bound=None, get_lp_value_gain=None):
            l1_norm = 0
            for final_price in [lp_lower_bound + (i / 100.) * (lp_upper_bound - lp_lower_bound) for i in range(0, 100, 10)]:
                lp_value = get_lp_value_gain(final_price)
                print(f'final price {final_price}')
                print(f'final lp_value {lp_value}')

                mid_size = int(len(x) / 2)
                total_deriv_payoff = 0.
                for i in range(mid_size):
                    pay_of_long_i = x[i] * longs_val[i](final_price)
                    pay_of_short_i = x[mid_size + i] * shorts_val[i](final_price)
                    print(pay_of_long_i)
                    print(pay_of_short_i)
                    total_deriv_payoff = total_deriv_payoff + pay_of_long_i + pay_of_short_i

                l1_norm = l1_norm +abs(lp_value-total_deriv_payoff)
            return l1_norm

        gogo = lambda x: to_optimize_l1_distance(x, longs_val=longs_val, shorts_val=shorts_val, lp_lower_bound=lp_lower_bound, lp_upper_bound=lp_upper_bound, get_lp_value_gain=get_lp_value_gain)
        low_bound = 0.
        up_bound = +np.infty
        const_ind = Bounds(low_bound, up_bound)
        result_final = minimize(
            gogo,
            x_init,
            bounds=const_ind,
            method='SLSQP'
        )
        optimal_size_to_swap = np.nan
        if result_final.success:
            optimal_size_to_swap = result_final.x


        mid_size = int(len(optimal_size_to_swap)/2)
        longs_i = np.zeros(mid_size)
        shorts_i = np.zeros(mid_size)
        for i in range(mid_size):
            long_i = optimal_size_to_swap[i]
            short_i = optimal_size_to_swap[mid_size + i]
            longs_i[i]=long_i - min(long_i,short_i)
            shorts_i[i]=short_i - min(long_i,short_i)

        maturity_df['longs_i'] = longs_i
        maturity_df['shorts_i'] = shorts_i


        if plot_html:
            value_df = compute_derivatives_profile(longs_val=longs_val, shorts_val=shorts_val,
                                                   lp_lower_bound=lp_lower_bound, lp_upper_bound=lp_upper_bound,
                                                   get_lp_value_gain=get_lp_value_gain)
            fig = realtime_plotting_utility.plot_dollar_multiple_time_series(data_df=value_df,
                                                                             logy=False, split=False,
                                                                             put_on_same_scale=False,
                                                                             title=f'LP value')
            fig.show()

            value_df = compute_optional_profile(longs_i, shorts_i, longs_val=longs_val, shorts_val=shorts_val,lp_lower_bound=lp_lower_bound, lp_upper_bound=lp_upper_bound, get_lp_value_gain=get_lp_value_gain)
            fig = realtime_plotting_utility.plot_dollar_multiple_time_series(data_df=value_df,
                                                                             logy=False, split=False,
                                                                             put_on_same_scale=False,
                                                                             title=f'LP value')
            fig.show()
        maturity_df['instrument_cost'] = maturity_df['longs_i']*maturity_df['long_immediate_cost'] +maturity_df['shorts_i']*maturity_df['short_immediate_gain']
        total_cost = -maturity_df['instrument_cost'].sum()
        maturity_df['total_cost']=total_cost
        return maturity_df
    except Exception as e:
        return None