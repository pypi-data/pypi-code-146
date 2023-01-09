import matplotlib.pyplot as plt
import seaborn as sns
from .statistical_tests import *
import pandas as pd
import scipy.stats
from scipy.stats import norm
import math
import numpy as np
from scipy.optimize import minimize

def cc_plot(params):
    '''
    Accepts dictionaries, pd.Series, np.array() as inputs
    Example 1:
    >>>cc_plot({'SMA': [30, 30.5, 40], 'EMA': [40, 67, 87]})

    Example 2:
    >>>cc_plot(np.array([30, 30.5, 40]))

    '''
    try:
        if str(type(params)) == "<class 'dict'>":
            arr = ['b', 'g', 'y', 'r', 'm', 'k', 'w', 'c']

            plt.figure(figsize=(15, 6))
            i = 0

            try:
                for key in params.keys():
                    params[f'{key}'].plot(color=arr[i])
                    i += 1
            except:
                for key in params.keys():
                    plt.plot(params[f'{key}'], color=arr[i])
                    i += 1

            plt.ylabel('Values', fontsize=14)
            plt.xlabel('Time/Days', fontsize=14)
            plt.xticks(rotation=60)
            plt.legend(params.keys())

        elif str(type(params)) == "<class 'pandas.core.series.Series'>":
            arr = ['b', 'g', 'y', 'r', 'm', 'k', 'w', 'c']

            plt.figure(figsize=(15, 6))

            params.plot()

            plt.xticks(rotation=60)
            plt.ylabel('Values', fontsize=14)
            plt.xlabel('Time/Days', fontsize=14)

        elif str(type(params)) == "<class 'numpy.ndarray'>" or str(type(params)) == "<class 'list'>":
            plt.figure(figsize=(15, 6))

            plt.plot(params)

            plt.xticks(rotation=60)
            plt.ylabel('Values', fontsize=14)
            plt.xlabel('Time/Days', fontsize=14)

    except Exception as e:
        print(e)


def plot_ef(n_points, er, cov, style='.-', legend=False, show_cml=False, riskfree_rate=0, show_ew=False, show_gmv=False):
    """
    Plots the multi-asset efficient frontier
    """
    weights = optimal_weights(n_points, er, cov)
    rets = [portfolio_return(w, er) for w in weights]
    vols = [portfolio_vol(w, cov) for w in weights]
    ef = pd.DataFrame({
        "Returns": rets,
        "Volatility": vols
    })
    ax = ef.plot.line(x="Volatility", y="Returns", style=style, legend=legend)
    if show_cml:
        ax.set_xlim(left = 0)
        # get MSR
        w_msr = msr(riskfree_rate, er, cov)
        r_msr = portfolio_return(w_msr, er)
        vol_msr = portfolio_vol(w_msr, cov)
        # add CML
        cml_x = [0, vol_msr]
        cml_y = [riskfree_rate, r_msr]
        ax.plot(cml_x, cml_y, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=10)
    if show_ew:
        n = er.shape[0]
        w_ew = np.repeat(1/n, n)
        r_ew = portfolio_return(w_ew, er)
        vol_ew = portfolio_vol(w_ew, cov)
        # add EW
        ax.plot([vol_ew], [r_ew], color='goldenrod', marker='o', markersize=10)
    if show_gmv:
        w_gmv = gmv(cov)
        r_gmv = portfolio_return(w_gmv, er)
        vol_gmv = portfolio_vol(w_gmv, cov)
        # add EW
        ax.plot([vol_gmv], [r_gmv], color='midnightblue', marker='o', markersize=10)

        return ax

def plot_ef2(n_points, er, cov):
    """
    Plots the 2-asset efficient frontier
    """
    if er.shape[0] != 2 or er.shape[0] != 2:
        raise ValueError("plot_ef2 can only plot 2-asset frontiers")
    weights = [np.array([w, 1-w]) for w in np.linspace(0, 1, n_points)]
    rets = [portfolio_return(w, er) for w in weights]
    vols = [portfolio_vol(w, cov) for w in weights]
    ef = pd.DataFrame({
        "Returns": rets,
        "Volatility": vols
    })
    return ef.plot.line(x="Volatility", y="Returns", style=".-")
