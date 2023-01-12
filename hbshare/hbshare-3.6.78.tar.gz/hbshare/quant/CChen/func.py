import pymysql
import numpy as np
import pandas as pd
from scipy import optimize as sco


def generate_table(database, table, generate_sql, sql_ip, sql_user, sql_pass, table_comment=''):
    db = pymysql.connect(host=sql_ip, user=sql_user, password=sql_pass, database=database)

    cursor = db.cursor()

    sql = 'create table if not exists `' + table + '` ' + generate_sql + ' comment=\'' + table_comment + '\''
    cursor.execute(sql)
    db.close()


def portfolio_var(weights, cov_matrix):
    return np.dot(weights.T, np.dot(cov_matrix, weights))


def risk_contribute(weights, cov_matrix):
    std = np.sqrt(portfolio_var(weights, cov_matrix))
    mrc = np.matrix(cov_matrix) * np.matrix(weights).T
    return np.multiply(mrc, np.matrix(weights).T) / std


def portfolio_annualised_performance(weights, mean_returns, cov_matrix, freq=252):
    returns = np.sum(mean_returns * weights) * freq
    std = np.sqrt(portfolio_var(weights, cov_matrix)) * np.sqrt(freq)
    return std, returns


def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate, freq=252):
    p_var, p_ret = portfolio_annualised_performance(weights, mean_returns, cov_matrix, freq=freq)
    return -(p_ret - risk_free_rate) / p_var


def max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate=0.015, freq=252, single_max=0.3):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate, freq)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    # bound = (0.0, 1.0)
    # bounds = tuple(bound for asset in range(num_assets))
    bounds = sco.Bounds([0] * num_assets, [single_max] * num_assets)
    result = sco.minimize(
        negative_sharpe_ratio,
        np.array(num_assets * [1 / num_assets]),
        args=args,
        bounds=bounds,
        constraints=constraints
    )
    return pd.DataFrame(
        result.x,
        index=mean_returns.index,
        columns=['allocation']
    )


def risk_error_sum(weights, cov_matrix):
    # print(weights)
    p_vol = np.sqrt(portfolio_var(weights=weights, cov_matrix=cov_matrix))
    asset_rc = risk_contribute(weights=weights, cov_matrix=cov_matrix)
    return sum(np.abs(asset_rc - p_vol / len(weights)))[0, 0]


def total_weight_constraint(x):
    return np.sum(x) - 1.0


def long_only_constraint(x):
    return x


def risk_parity(cov_matrix, single_max=1, max_i=5000):
    w0 = [0.5] * len(cov_matrix)
    cons = (
        {'type': 'eq', 'fun': total_weight_constraint}
        # {'type': 'ineq', 'fun': long_only_constraint}
    )
    res = sco.minimize(
        risk_error_sum,
        np.array(w0),
        args=cov_matrix,
        constraints=cons,
        bounds=sco.Bounds([0] * len(cov_matrix), [single_max] * len(cov_matrix)),
        options={
            'disp': True,
            'maxiter': max_i
        },
        method='SLSQP',
    )
    return res


if __name__ == '__main__':
    from hbshare.quant.CChen.db_const import sql_write_path_work

    codes = [
        '000001.XSHE',
        '000507.XSHE',
        # '000517.XSHE',
        # '600566.XSHG',
        # '600555.XSHG',
        # '600556.XSHG',
        # '600565.XSHG',
        # '600563.XSHG'
    ]

    data_raw = pd.read_sql_query(
        'select t_date, code, close from a_shares_jq  '
        'where t_date<=20210601 and t_date>=20200101 '
        'and code in ' + str(tuple(codes)),
        sql_write_path_work['daily']
    )
    data = data_raw.pivot(index='t_date', columns='code', values='close')
    returns = data.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    rp_w = risk_parity(cov_matrix=cov_matrix).x
    rc = risk_contribute(weights=rp_w, cov_matrix=cov_matrix)
    p_vol = np.sqrt(portfolio_var(weights=rp_w, cov_matrix=cov_matrix))
    rb = risk_error_sum(weights=rp_w, cov_matrix=cov_matrix)
    print(mean_returns)
    print(cov_matrix)

    max_sharpe = max_sharpe_ratio(mean_returns=mean_returns, cov_matrix=cov_matrix, single_max=1)
    print(max_sharpe)

    max_sharpe.allocation = [round(i*100, 2)for i in max_sharpe.allocation]
    # max_sharpe = max_sharpe.T

    print(max_sharpe)

