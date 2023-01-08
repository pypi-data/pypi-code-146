import itertools
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from statsmodels.stats.proportion import proportion_confint
from datetime import datetime
from itertools import product
from math import log
import numpy as np
import pandas as pd
import seaborn as sns
import holoviews as hv
from matplotlib import pyplot as plt

# Настройки графиков

from functools import wraps


def _set_options(func):
    """Обертка для применения визуальных настроек"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        diagramm = func(*args, **kwargs)
        for bnd, opts in [('matplotlib', matplotlib_opts),
                          ('bokeh', bokeh_opts)]:
            if (bnd in hv.Store._options
                    and bnd == hv.Store.current_backend):
                return diagramm.opts(opts)
        return diagramm
    return wrapper


colors = hv.Cycle(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                   '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])

matplotlib_opts = {
    'Scatter.Weight_of_Evidence': {
        'plot': dict(show_grid=True, legend_position='right', width=450),
        'style': dict(color='r', size=5),
    },
    'NdOverlay.Objects_rate': {
        'plot': dict(xrotation=45, legend_cols=1, legend_position='right'),
    },
    'Spread.Objects_rate': {
        'plot': dict(show_legend=True, show_grid=True),
        'style': dict(facecolor=colors),
    },
    'Overlay.Woe_Stab': {
        'plot': dict(legend_position='right'),
    },
    'Curve.Weight_of_Evidence': {
        'style': dict(color=colors),
    },
    'Spread.Confident_Intervals': {
        'plot': dict(show_grid=True, xrotation=45),
        'style': dict(facecolor=colors, alpha=0.3),
    },
}

bokeh_opts = {
    'Scatter.Weight_of_Evidence': {
        'plot': dict(show_grid=True, tools=['hover'], legend_position='right', width=450),
        'style': dict(color='r', size=5),
    },
    'NdOverlay.Objects_rate': {
        'plot': dict(xrotation=45, legend_position='right', width=450),
    },
    'Spread.Objects_rate': {
        'plot': dict(show_legend=True, show_grid=True, tools=['hover']),
        'style': dict(color=colors),
    },
    'Overlay.Woe_Stab': {
        'plot': dict(legend_position='right', width=450),
    },
    'Curve.Weight_of_Evidence': {
        'plot': dict(tools=['hover']),
        'style': dict(color=colors),
    },
    'Spread.Confident_Intervals': {
        'plot': dict(show_grid=True, xrotation=45),
        'style': dict(color=colors, alpha=0.3),
    },
}

# Гистограммы


def beauty_hist(df, feature, target, n):
    """
    Строит приятную гистограмму распределения признака от целевой переменной

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Признак, распределение которого, требуется посмотреть
    target: Целевая переменная для разбиения признака
    n: Кол-во bin-ов
    """
    df2 = pd.melt(df[[feature, target]], id_vars=target,
                  value_vars=[feature], value_name='value')
    bins = np.linspace(df2.value.min(), df2.value.max(), n)
    g = sns.FacetGrid(
        df2,
        col="variable",
        hue=target,
        palette='rainbow',
        col_wrap=2,
        size=10)
    g.map(plt.hist, 'value', alpha=0.5, density=True, bins=bins, ec="k")
    g.axes[-1].legend()
    plt.show()


def stacked_hist(df, feature, target):
    """
    Возвращает стобец распределения признака в рамках каждого из значений целевой переменной

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Признак, распределение которго, требуется посмотреть
    target: Целевая переменная, будет на оси x графика
    """
    overview = pd.crosstab(
        df[target],
        df[feature]).sort_values(
        target,
        ascending=True)
    sum_series = overview.sum(axis=1)
    for col in list(overview.columns):
        overview[col] = overview[col] / sum_series
    overview.plot(kind='bar', stacked=True)


def print_corr_matrix(df, features):
    """
    Строит матрицу корреляций признаков

    Parameters
    ----------
    df: Объект pandas.DataFrame
    features: Список признаков, взаимную корреляцию которых требуется посчитать
    """
    corr = df[features].corr(method='spearman')
    plt.figure(figsize=(10, 10))
    sns.heatmap(corr, vmax=1, square=True, annot=True, cmap='cubehelix')
    plt.title('Correlation between different features')
    bottom, top = plt.ylim()
    plt.ylim([bottom + 0.5, top - 0.5])
    plt.show()

# Для задачи линейной регресии


def make_bucket(df, feature, num_buck=10):
    """
    Производит разбиение на бакеты

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака числового или категориального
    num_buck: Количество бакетов для группирровки
    """
    bucket = np.ceil(
        df[feature].rank(
            pct=True) *
        num_buck).fillna(
            num_buck +
        1)
    agg = df[feature].groupby(bucket).agg(['min', 'max'])

    def _format_buck(row):
        if row['bucket'] == num_buck + 1:
            return 'missing'
        elif row['min'] == row['max']:
            return _format_(row['min'])
        else:
            return _format_(row['min']) + ' - ' + _format_(row['max'])

    bucket = df[[feature]].assign(bucket=bucket)\
        .join(agg, on='bucket')\
        .apply(_format_buck, axis=1)

    return df.assign(bucket=bucket)


def _format_(x, decimal=3):
    """
    Форматируем названия бакетов

    Parameters
    ----------
    x: Вход - строка или число
    decimal: Желаемое кол-во знаков после запятой
    """
    if not isinstance(x, str):
        div, mod = x // 1, x % 1
        if mod == 0:
            if div == 0:
                return '%d' % x
            elif int(np.floor(np.log10(abs(div)))) < 3:
                return '%d' % x
        if div == 0:
            power = int(np.floor(np.log10(abs(mod))))
            digits = decimal - power - 1
            return '%s' % np.around(x, digits)
        else:
            power = int(np.floor(np.log10(abs(div))))
            digits = decimal
            if power < 3:
                return '%s' % np.around(x, digits)
            elif power < 10:
                return '%se+0%s' % (np.around(x /
                                    np.power(10, power), digits), power)
            else:
                return '%se+%s' % (np.around(x /
                                   np.power(10, power), digits), power)
    return '%s' % x


def check_linearity(df, feature, target, num_buck=10):
    """
    Позволяет оценивать линейность зависимости целевой переменной от признака.
    Строит график зависимости и лучшую регрессионную прямую (с наименьшим r_2)

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового!)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """
    return df.pipe(make_bucket, feature, num_buck) \
             .groupby('bucket').mean() \
             .pipe(lambda x: hv.Scatter(zip(np.array(x[feature]), np.array(x[target])),
                                        kdims=f'{feature}', vdims=f'{target}',
                                        label=f"Проверка линейности зависимости {target} от {feature}")
                   * simple_reg(np.array(x[feature]),
                                np.array(x[target])))


def check_homoscedacity(df, feature, target):
    """
    Позволяет оценивать гомоскедастичность зависимости целевой переменной от признака.

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового!)
    target: Название целевой переменной
    """
    simple_model = LinearRegression()
    simple_model.fit(
        np.array(df[feature]).reshape(-1, 1), np.array(df[target]))
    predicts = simple_model.predict(np.array(df[feature]).reshape(-1, 1))

    def get_residuals(y, pred):
        return np.array(y) - np.array(pred)

    return hv.Scatter(zip(predicts, get_residuals(df[target], predicts)),
                      kdims=['Estimated target'], vdims=['Residual'],
                      label=f"Проверка гомоскедастичности признака {feature}")


# Для задачи логистической регресии


def _logit(p):
    """
    Возвращает логит от вероятности

    Parameters
    ----------
    p: вероятность просрочки
    """
    return np.log(p / (1 - p))


def _woe(p, q):
    """
    Считает WoE для бакета

    Parameters
    ----------
    p: вероятность просрочки в бакете
    q: вероятность просрочки на всем корпусе
    """
    p, q = np.clip([p, q], 0.001, 0.999)
    return _logit(p) - _logit(q)


def _woe_confint(n, cnt, q):
    """
    Считает 95%% доверительный интервал для WoE

    Parameters
    ----------
    n: кол-во просрочек в бакете
    cnt: кол-во элементов в бакете
    q: вероятность просрочки на всем корпусе
    """
    p_low, p_high = proportion_confint(n, cnt, method='normal')
    return _woe(p_low, q), _woe(p_high, q)


def bad_rate(df, feature, target, num_buck=10):
    """
    Считает bad_rate для каждого бакета признака в модели классификации.
    Возвращает датафрейм с аггрегациями (сумма таргета в бакете, среднее значение предсказания,
    количество эл-ов в бакете, среднее значение признака в бакете)
    Во избежание исключений наложено ограничение: 0.001 <= bad_rate <= 0.999

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового или категориального)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """
    if df[feature].dtype == 'O':
        return df.pipe(make_bucket, feature, num_buck)\
            .assign(obj_cnt=1)\
            .groupby('bucket')\
            .agg({target: 'sum', 'obj_cnt': 'sum'})\
            .rename(columns={target: 'target_sum'})\
            .assign(bad_rate=lambda x: x.target_sum / x.obj_cnt)
    else:
        return df.pipe(make_bucket, feature, num_buck)\
            .assign(obj_cnt=1)\
            .groupby('bucket')\
            .agg({target: 'sum', 'obj_cnt': 'sum', feature: 'mean'})\
            .rename(columns={target: 'target_sum', feature: 'feature_avg'})\
            .assign(bad_rate=lambda x: x.target_sum / x.obj_cnt)


def woe(df, feature, target, num_buck=10):
    """
    Считает WOE для признака в модели классификации.
    Доля объектов каждого класса ограничивается 0.001 - снизу и 0.999 - сверху.

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового или категориального)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """
    agg = bad_rate(df, feature, target, num_buck).reset_index()
    agg = agg[agg.target_sum != 0]
    return agg.assign(nums=agg['obj_cnt'].sum(), bad_nums=agg['target_sum'].sum())\
              .assign(woe=lambda x: _woe(x.bad_rate, x.bad_nums / x.nums))\
              .drop(['bad_nums', 'nums'], axis=1)\
              .sort_values(by='woe', ascending=False)\
              .set_index('bucket')


def IV(df, feature, target, num_buck=10):
    """
    Считает Information Value для признака в модели бинарной классификации.

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового или категориального)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """
    return woe(df, feature, target, num_buck)\
        .assign(iv=lambda x: (x.target_sum / x.target_sum.sum() -
                              (x.obj_cnt - x.target_sum) / (x.obj_cnt.sum() - x.target_sum.sum())) * x.woe)\
        .iv.sum()


def iv_report(df, features, target, num_buck=10):
    """
    Считает IV для указанных признаков в модели классификации.
    Возвращает в порядке убывания кортежи из трех элементов:(признак, IV, интерпретация)

    Parameters
    ----------
    df: Объект pandas.DataFrame
    features: Список названий признаков (числовых или категориальных)
    target: Название целевой переменной
    num_buck: Количество бакетов для разбиения
    """
    def desc(x):
        if x > 0.5:
            power = 'Suspicious'
        elif x > 0.3:
            power = 'Strong'
        elif x > 0.1:
            power = 'Medium'
        elif x > 0.02:
            power = 'Weak'
        else:
            power = 'Useless'
        return (x, power)

    ivs = {}
    for column in list(features):
        ivs[column] = desc(IV(df, column, target, num_buck))

    ivs = list(ivs.items())
    ivs.sort(key=lambda i: i[1], reverse=True)
    print('         Name         ||  Value  || Interpretation')
    print('--------------------------------------------------')
    for feature in ivs:
        print(f'{feature[0]:21} ||  {feature[1][0]:.3f}  || {feature[1][1]}')


def iv_agg(df, features, target, num_bucks=[10, 10]):
    """
    Считает совокупный IV для указанных признаков в модели бинарной классификации.

    Parameters
    ----------
    df: Объект pandas.DataFrame
    features: Список названий признаков (числовых или категориальных)
    target: Название целевой переменной
    num_bucks: Список количества бакетов для каждой из переменных
    """
    index = make_bucket(df[[features[-1]]], features[-1],
                        num_buck=num_bucks[-1])['bucket'].values
    columns = []

    for i, feature in enumerate(features[:-1]):
        columns.append(make_bucket(
            df[[feature]], feature, num_buck=num_bucks[i])['bucket'].values)

    obj_cnt = (pd.crosstab(index=index,
                           columns=columns,
                           margins=True))
    target_sum = (pd.crosstab(index=index,
                              columns=columns,
                              values=df[target].values,
                              aggfunc=np.sum,
                              margins=True))
    bad_rate = (pd.crosstab(index=index,
                            columns=columns,
                            values=df[target].values,
                            aggfunc=np.mean,
                            margins=True))
    agg = pd.DataFrame({'obj_cnt': obj_cnt.iloc[:-1, :-1].unstack().values,
                        'target_sum': target_sum.iloc[:-1, :-1].unstack().values,
                        'bad_rate': bad_rate.iloc[:-1, :-1].unstack().values})
    agg = agg[agg.target_sum != 0]
    return agg.assign(nums=agg['obj_cnt'].sum(), bad_nums=agg['target_sum'].sum())\
              .assign(woe=lambda x: _woe(x.bad_rate, x.bad_nums / x.nums))\
              .assign(iv=lambda x: (x.target_sum / x.target_sum.sum() -
                                    (x.obj_cnt - x.target_sum) / (x.obj_cnt.sum() - x.target_sum.sum())) * x.woe)\
              .iv.sum()


def simple_reg(predictor, target):
    """
    Строит простую линейную регрессию
    Использует для отрисовки прямой и подсчета r^2

    Parameters
    ----------
    predictor: Массив значений признака
    target: Массив значений целевой переменной
    """
    check = LinearRegression()
    check.fit(predictor.reshape(-1, 1), target)
    return hv.Curve((np.array([min(predictor) - 1, max(predictor) + 1]),
                     check.coef_ * np.array([min(predictor) - 1, max(predictor) + 1]) + check.intercept_))


def r_2check(df, feature, target, num_buck=10):
    """
    Для заданного признака строт простую линейную регрессию для бакетов получаемых из функции woe
    Возвращает r2_score полученного результата

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового!)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """
    model = LinearRegression()
    data = woe(df, feature, target, num_buck)
    data = data[data.feature_avg.notnull()]
    X = np.array(data.feature_avg)
    y = np.array(data.woe)
    model.fit(X.reshape(-1, 1), y)
    return round(r2_score(y, model.predict(X.reshape(-1, 1))), 3)


@_set_options
def print_woe_curve(df, feature, target, num_buck=10):
    """
    Считает WOE, и по полученным точкам строит лучшую прямую (с наибольшим r_2)
    Можно задавать размер изображения, например так:
        %%output size = 150

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового!)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """

    agg = bad_rate(df, feature, target, num_buck).reset_index()
    agg = agg[(agg.target_sum != 0) & (agg.feature_avg.notnull())]
    agg = agg.assign(nums=agg['obj_cnt'].sum(), bad_nums=agg['target_sum'].sum())\
        .assign(woe=lambda x: _woe(x.bad_rate, x.bad_nums / x.nums),
                woe_low=lambda x: _woe_confint(x.target_sum,
                                               x.obj_cnt,
                                               x.bad_nums / x.nums)[0],
                woe_high=lambda x: _woe_confint(x.target_sum,
                                                x.obj_cnt,
                                                x.bad_nums / x.nums)[1])\
        .assign(woe_u=lambda x: x.woe_high - x.woe,
                woe_b=lambda x: x.woe - x.woe_low)

    r2_woe = r_2check(df, feature, target, num_buck)
    scatter = hv.Scatter(data=agg,
                         kdims=['feature_avg'],
                         vdims=['woe'],
                         group='Weight of Evidence',
                         label=f'r2_score = {r2_woe}')
    errors = hv.ErrorBars(data=agg,
                          kdims=['feature_avg'],
                          vdims=['woe', 'woe_u', 'woe_b'],
                          group='Confident Intervals')
    reg = simple_reg(np.array(agg.feature_avg), np.array(agg.woe))
    return hv.Overlay(items=[scatter, errors, reg],
                      group='Woe Curve',
                      label=feature).redim.range(feature_avg=(agg.feature_avg.min() * 1.15,
                                                              agg.feature_avg.max() * 1.15),
                                                 woe=(agg.woe.min() * 1.15,
                                                      agg.woe.max() * 1.15))


# Динамика переменных и WoE


@_set_options
def distribution(df, feature, date, num_buck=10, date_freq='Q'):
    """
    Строит график распределения признака во времени

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака числового или категориального
    date: Наименование временной переменной
    num_buck: Количество бакетов, если признак числовой
    date_freq: Частота агрегации времени
    """
    agg = df.pipe(make_bucket, feature, num_buck)\
            .assign(obj_cnt=1)\
            .groupby([pd.Grouper(key=date, freq=date_freq), 'bucket'])\
            .agg({'obj_cnt': sum})\
            .reset_index()\
            .assign(obj_total=lambda x: (x.groupby([pd.Grouper(key=date,
                                                               freq=date_freq)])['obj_cnt'].transform('sum')))\
            .assign(obj_rate=lambda x: x.obj_cnt / x.obj_total)\
            .reset_index()\
            .assign(objects_rate=lambda x:
                    x.groupby(date).apply(
                        lambda y: y.obj_rate.cumsum().to_frame())
                    .reset_index(drop=True))\
        .assign(obj_rate_u=0, obj_rate_b=lambda x: x['obj_rate'])

    data = hv.Dataset(
        agg, kdims=[
            'bucket', date], vdims=[
            'objects_rate', 'obj_rate_b', 'obj_rate_u'])

    return data.to.spread(kdims=[date],
                          vdims=['objects_rate', 'obj_rate_b', 'obj_rate_u'],
                          group='Objects rate',
                          label=feature).overlay('bucket')


@_set_options
def woe_stab(df, feature, target, date, num_buck=3, date_freq='Q'):
    """
    Строит WoE признака во времени, позволяет оценить его устойчивость

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака числового или категориального
    target: Название целевой переменной
    date: Наименование временной переменной
    num_buck: Количество бакетов, если признак числовой
    date_freq: Частота агрегации времени
    """
    agg = df.pipe(make_bucket, feature, num_buck)\
            .assign(obj_cnt=1)\
            .groupby([pd.Grouper(key=date, freq=date_freq), 'bucket'])\
            .agg({target: 'sum', 'obj_cnt': sum})\
            .rename(columns={target: 'target_sum'})\
            .assign(bad_rate=lambda x: x.target_sum / x.obj_cnt)

    agg = agg.assign(nums=agg.groupby([date])['obj_cnt'].transform('sum'),
                     bad_nums=agg.groupby([date])['target_sum'].transform('sum'))\
        .assign(woe=lambda x: _woe(x.bad_rate, x.bad_nums / x.nums),
                woe_low=lambda x: _woe_confint(x.target_sum,
                                               x.obj_cnt,
                                               x.bad_nums / x.nums)[0],
                woe_high=lambda x: _woe_confint(x.target_sum,
                                                x.obj_cnt,
                                                x.bad_nums / x.nums)[1])\
        .assign(woe_u=lambda x: x.woe_high - x.woe,
                woe_b=lambda x: x.woe - x.woe_low)\
        .reset_index()

    agg = agg[agg.target_sum != 0]

    data = hv.Dataset(
        agg, kdims=[
            'bucket', date], vdims=[
            'woe', 'woe_b', 'woe_u'])

    confident_intervals = (data.to.spread(kdims=[date],
                                          vdims=['woe', 'woe_b', 'woe_u'],
                                          group='Confident Intervals')
                           .overlay('bucket'))
    woe_curves = (data.to.curve(kdims=[date],
                                vdims=['woe'],
                                group='Weight of Evidence')
                  .overlay('bucket'))
    return hv.Overlay(items=[confident_intervals * woe_curves],
                      group='Woe Stab',
                      label=f'{feature}')


def HL(target, predict, num_buck=10):
    """
    Считает статистику Хосмера-Лемешева

    Parameters
    ----------
    target - истинные значения целевой переменной
    predict - предсказания вероятности
    num_buck - количество бакетов
    """
    data = pd.DataFrame({'target': target, 'predict': predict})

    data = (
        data.pipe(make_bucket, 'predict', num_buck)
            .assign(obj_cnt=1)
            .groupby('bucket')
            .agg({'target': 'sum', 'predict': 'mean', 'obj_cnt': 'sum'})
            .assign(bad_rate=lambda x: x.target / x.obj_cnt)
            .reset_index()
    )
    return int(sum((data.predict - data.bad_rate) ** 2 /
               (data.predict * (1 - data.predict)) * data.obj_cnt))


def plot_gain_chart(target, predict, num_buck=10):
    """
    Строит gain_chart по истиным и предсказанным меткам
    На первом шаге бьет наблюдения на бакеты, затем считает средний bad_rate.
    На втором шаге строится график, где кривая обозначает предсказанное значение целевой переменной, столбцы - истинные.

    Parameters
    ----------
    target - истинные значения целевой переменной
    predict - предсказания вероятности
    num_buck - количество бакетов
    """
    data = pd.DataFrame({'target': target, 'predict': predict})
    H = HL(target, predict, num_buck)
    data = (
        data.assign(bucket=np.ceil(data['predict'].rank(pct=True) * num_buck))
            .assign(obj_cnt=1)
            .groupby('bucket')
            .agg({'target': 'sum', 'predict': 'mean', 'obj_cnt': 'sum'})
            .assign(bad_rate=lambda x: x.target / x.obj_cnt)
            .reset_index()
    )

    bars_gain = hv.Bars(data, kdims=['bucket'], vdims=['bad_rate'], label='observed') \
                  .opts(plot={'xrotation': 90, 'show_legend': True}, style={'color': 'yellow'})

    curve_gain = hv.Curve(data, kdims=['bucket'], vdims=['predict'], label='predicted') \
        .opts(plot={'xrotation': 90, 'show_legend': True}, style={'color': 'black'})

    return hv.Overlay([bars_gain, curve_gain]).redim.label(**{'target': 'Bad Rate'})\
             .relabel(f'HL_score = {H}').opts(plot={'legend_position': 'top_left'})


# Для визуализации коэффициентов линейных и не только моделей


def feature_importance(names, values, verbose=False, thr=0.05):
    """
    Возвращает словарь и печатает в порядке убывания коэффициенты для признаков

    Parameters
    ----------
    names: Список наименований признаков
    values: Список коэффициентов для этих признаков
    verbose: Стоит ли печатать результат
    thr: Не выводить признаки с меньшим вкладом
    """
    names = names.tolist()
    val_dict = {}
    for name, value in zip(names, values):
        val_dict[name] = round(value, 3)
    if verbose:
        coef_list = list(val_dict.items())
        coef_list.sort(key=lambda i: i[1], reverse=True)
        for i in coef_list:
            if i[1] >= thr:
                print(i[0], ':', round(i[1], 5))
    return val_dict


# Методы для перестановочных статистических критериев


def permutation_t_stat_ind(sample1, sample2):
    return np.mean(sample1) - np.mean(sample2)


def get_random_combinations(n1, n2, max_combinations):
    index = list(range(n1 + n2))
    indices = set([tuple(index)])
    for i in range(max_combinations - 1):
        np.random.shuffle(index)
        indices.add(tuple(index))
    return [(index[:n1], index[n1:]) for index in indices]


def permutation_zero_dist_ind(sample1, sample2, max_combinations=None):
    joined_sample = np.hstack((sample1, sample2))
    n1 = len(sample1)
    n = len(joined_sample)

    if max_combinations:
        indices = get_random_combinations(n1, len(sample2), max_combinations)
    else:
        indices = [(list(index), filter(lambda i: i not in index, range(n)))
                   for index in itertools.combinations(range(n), n1)]

    distr = [joined_sample[list(i[0])].mean() - joined_sample[list(i[1])].mean()
             for i in indices]
    return distr


def permutation_test(sample, mean, max_permutations=None,
                     alternative='two-sided'):
    if alternative not in ('two-sided', 'less', 'greater'):
        raise ValueError("alternative not recognized\n"
                         "should be 'two-sided', 'less' or 'greater'")

    t_stat = permutation_t_stat_ind(sample, mean)

    zero_distr = permutation_zero_dist_ind(sample, mean, max_permutations)

    if alternative == 'two-sided':
        return sum([1. if abs(x) >= abs(t_stat)
                   else 0. for x in zero_distr]) / len(zero_distr)

    if alternative == 'less':
        return sum([1. if x <= t_stat else 0. for x in zero_distr]
                   ) / len(zero_distr)

    if alternative == 'greater':
        return sum([1. if x >= t_stat else 0. for x in zero_distr]
                   ) / len(zero_distr)

# Модели временных рядов


class HoltLinearTrend:

    """
    Модель Хольта двойного экспоненциального сглаживания
    Про алгоритм подробнее здесь:
    https://habr.com/ru/company/ods/blog/327242/

    Parameters
    ----------
    series: исходный временной ряд
    alpha, beta: коэффициенты модели линйного тренда Хольта
    n_preds: горизонт предсказаний

    Attributes
    ----------
    result: массив значений алгоритма двойного сглаживаня применненного к series
    Level: массив значений уровня в модели сглаживаня
    Trend: массив значений тренда в модели сглаживаня

    """

    def __init__(self, series, alpha, beta, n_preds):
        self.series = series
        self.alpha = alpha
        self.beta = beta
        self.n_preds = n_preds

    def double_exponential_smoothing(self):
        self.result = []
        self.Level = []
        self.Trend = []

        for i in range(len(self.series) + self.n_preds):
            if i == 0:  # инициализируем значения компонент
                self.result.append(self.series[0])
                level, trend = self.series[0], self.series[1] - self.series[0]
                self.Level.append(level)
                self.Trend.append(trend)
                continue
            if i >= len(self.series):  # прогнозируем
                m = i - len(self.series) + 1
                self.result.append(level + m * trend)
            else:
                self.result.append(level + trend)
                val = self.series[i]
                prev_level, level = level, self.alpha * \
                    val + (1 - self.alpha) * (level + trend)
                trend = self.beta * (level - prev_level) + \
                    (1 - self.beta) * trend

            self.Level.append(level)
            self.Trend.append(trend)


class HoltWinters:

    """
    Модель Хольта-Винтерса тройного экспоненциального сглаживания с методом Брутлага для детектирования аномалий
    Про алгоритм подробнее здесь:
    https://habr.com/ru/company/ods/blog/327242/
    Про метод Брутлага подробнее здесь:
    https://fedcsis.org/proceedings/2012/pliks/118.pdf

    Parameters
    ----------
    series: исходный временной ряд
    slen: длина сезона
    alpha, beta, gamma: коэффициенты модели Хольта-Винтерса
    n_preds: горизонт предсказаний
    scaling_factor: задаёт ширину доверительного интервала по Брутлагу (обычно принимает значения от 2 до 3)

    Attributes
    ----------
    result: массив значений алгоритма тройного сглаживаня применненного к series
    Smooth: массив уровней (level) в модели сглаживаня
    Season: массив сезонных компонент в модели сглаживаня
    Trend: массив значений тренда в модели сглаживаня
    UpperBond: массив верхних границ дов.интервалов Брутлага
    LowerBond: массив нижних значений дов.интерваллов Брутлага

    """

    def __init__(self, series, slen, alpha, beta,
                 gamma, n_preds, scaling_factor=1.96):
        self.series = series
        self.slen = slen
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.n_preds = n_preds
        self.scaling_factor = scaling_factor

    def initial_trend(self):
        sum = 0.0
        for i in range(self.slen):
            sum += float(self.series[i + self.slen] -
                         self.series[i]) / self.slen
        return sum / self.slen

    def initial_seasonal_components(self):
        seasonals = {}
        season_averages = []
        n_seasons = int(len(self.series) / self.slen)
        # вычисляем сезонные средние
        for j in range(n_seasons):
            season_averages.append(
                sum(self.series[self.slen * j: self.slen * j + self.slen]) / float(self.slen))
        # вычисляем начальные значения
        for i in range(self.slen):
            sum_of_vals_over_avg = 0.0
            for j in range(n_seasons):
                sum_of_vals_over_avg += self.series[self.slen *
                                                    j + i] - season_averages[j]
            seasonals[i] = sum_of_vals_over_avg / n_seasons
        return seasonals

    def triple_exponential_smoothing(self):
        self.result = []
        self.Smooth = []
        self.Season = []
        self.Trend = []
        self.PredictedDeviation = []
        self.UpperBond = []
        self.LowerBond = []

        for i in range(len(self.series) + self.n_preds):
            if i == 0:  # инициализируем значения компонент
                smooth = self.series[0]
                trend = self.initial_trend()
                seasonals = self.initial_seasonal_components()
                deviations = np.array([0.0] * self.slen)
                self.result.append(self.series[0])
                self.Smooth.append(smooth)
                self.Trend.append(trend)

                self.Season.append(seasonals[i % self.slen])

                self.PredictedDeviation.append(deviations[i % self.slen])

                self.UpperBond.append(self.result[0] +
                                      self.scaling_factor *
                                      self.PredictedDeviation[0])

                self.LowerBond.append(self.result[0] -
                                      self.scaling_factor *
                                      self.PredictedDeviation[0])
                continue
            if i >= len(self.series):  # прогнозируем
                m = i - len(self.series) + 1
                self.result.append(smooth + m * trend +
                                   seasonals[i % self.slen])

                # во время прогноза с каждым шагом увеличиваем неопределенность
                prev_deviation = deviations[i % self.slen]
                deviations[i % self.slen] = deviations[i % self.slen] * 1.01

            else:
                self.result.append(smooth + trend + seasonals[i % self.slen])
                val = self.series[i]
                prev_smooth, smooth = smooth, self.alpha * \
                    (val - seasonals[i % self.slen]) + \
                    (1 - self.alpha) * (smooth + trend)
                trend = self.beta * (smooth - prev_smooth) + \
                    (1 - self.beta) * trend
                seasonals[i % self.slen] = self.gamma * \
                    (val - smooth) + (1 - self.gamma) * \
                    seasonals[i % self.slen]

                # Отклонение рассчитывается в соответствии с алгоритмом
                # Брутлага
                prev_deviation = deviations[i % self.slen]
                deviations[i % self.slen] = self.gamma * np.abs(
                    self.series[i] - self.result[i]) + (1 - self.gamma) * prev_deviation

            self.UpperBond.append(self.result[-1] +
                                  self.scaling_factor *
                                  prev_deviation)

            self.LowerBond.append(self.result[-1] -
                                  self.scaling_factor *
                                  prev_deviation)

            self.Smooth.append(smooth)
            self.Trend.append(trend)
            self.Season.append(seasonals[i % self.slen])
            self.PredictedDeviation.append(deviations[i % self.slen])


def timeseriesCVscore(x, data, r=0, method='HoltWinters', slen=7):
    """
    Производит кросс-валидацию на временных рядах для модели линейного тренда Хольта или модели Хольта-Винтерса
    Максимальное значение n_splits, таково, что (n_splits + 1) * 2 * slen <= len(data) (для линейной модели Хольта slen=1)
    Возвращает функцию, которую надо передать на вход оптимизатору, например:
    opt = scipy.optimize.minimize(timeseriesCVscore, x0=[0, 0, 0], args=(data, ), method="TNC", bounds = ((0, 1), (0, 1), (0, 1)))
    Из оптимизатора можно взять  оптимальные значение параметров:
    alpha, beta, gamma = opt.x

    Parameters
    ----------
    x: переменная, содержащая параметры модели (для Хольта: [alpha, beta], для Хольта-Винтерса: [alpha, beta, gamma])
    data: pd.Series - тренировочные данные для кросс-валидации
    r: коэффициент дисконтирования для взвешенной MSE, должен быть больше нуля
        По умолчанию = 0 - это эквивалентно обыкновенной MSE, а чем он больше, тем меньший вклад в ошибку дают более ранние значения
    method: Какую модель требуется валидировать двойного ('Holt') или тройного ('HoltWinters') экспоненциального сглаживания
    slen: Длина сезона для method = 'HoltWinters'
    """
    # Метрика
    def weighted_mse(actual, predictions, r):
        weights = [1 / np.power(1 + r, i) for i in range(len(actual), 0, -1)]
        return np.mean(
            ((np.array(actual) - np.array(predictions)) ** 2) * np.array(weights))

    # Вектор ошибок
    errors = []

    # Данные в numpy массив
    values = data.values

    # Задаём число фолдов для кросс-валидации
    tscv = TimeSeriesSplit(n_splits=3)

    # Идем по фолдам, на каждом обучаем модель, строим прогноз на отложенной
    # выборке и считаем ошибку
    for train, test in tscv.split(values):

        if method == 'HoltWinters':
            model = HoltWinters(
                series=values[train],
                slen=slen,
                alpha=x[0],
                beta=x[1],
                gamma=x[2],
                n_preds=len(test))
            model.triple_exponential_smoothing()

        if method == 'Holt':
            model = HoltLinearTrend(
                series=values[train],
                alpha=x[0],
                beta=x[1],
                n_preds=len(test))
            model.double_exponential_smoothing()

        predictions = model.result[-len(test):]
        actual = values[test]

    # Можно считать обыычный MSE или взвесить и дать больший вес свежим
    # значением
        error = weighted_mse(actual, predictions, r=r)
        errors.append(error)

    # Возвращаем средний квадрат ошибки по вектору ошибок
    return np.mean(np.array(errors))


def plotHolt(model, dataset, target, predict_interval, xlim=None):
    """
    Отрисовавает график временного ряда с наложением результата модели

    Parameters
    ----------
    model: обучення модель Хольта
    dataset: Объект pandas.DataFrame
    target: Пригнозирумая переменная
    predict_interval: Временной интервал для прогнозирования
    xlim: Сколько последних точек надо отобразить на графике, по умолчанию - все
    """
    if len(model.result) > len(dataset):
        dataset = pd.concat([dataset, pd.DataFrame(
            np.array([np.NaN] * predict_interval), columns=[target])])
    plt.figure(figsize=(25, 10))
    plt.plot(model.result, "b", label="Model")
    plt.plot(dataset[target].values, "g", label="Actual")
    plt.axvspan(
        len(dataset) -
        predict_interval -
        1,
        len(dataset),
        alpha=0.5,
        color='lightgrey')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc="best", fontsize=13)
    if xlim:
        plt.xlim(len(dataset) - xlim, len(dataset))
    plt.show()


def plotHoltWinters(model, dataset, target, predict_interval, xlim=None):
    """
    Отрисовавает график временного ряда с наложением прогнозируемого ряда
    Отражает доверительный интревал Брутлага и аномальные относительно него значения

    Parameters
    ----------
    model: обучення модель Хольта-Винтреса
    dataset: Объект pandas.DataFrame
    target: Пригнозирумая переменная
    predict_interval: Временной интервал для прогнозирования
    xlim: Сколько последних точек надо отобразить на графике, по умолчанию - все
    """
    if len(model.result) > len(dataset):
        dataset = pd.concat([dataset, pd.DataFrame(
            np.array([np.NaN] * predict_interval), columns=[target])])
    Anomalies = np.array([np.NaN] * len(dataset[target]))
    Anomalies[dataset[target].values <
              model.LowerBond] = dataset[target].values[dataset[target].values < model.LowerBond]
    Anomalies[dataset[target].values >
              model.UpperBond] = dataset[target].values[dataset[target].values > model.UpperBond]
    plt.figure(figsize=(25, 10))
    plt.plot(model.result, "b", label="Model")
    plt.plot(model.UpperBond, "k--", alpha=0.5, label="Up/Low confidence")
    plt.plot(model.LowerBond, "k--", alpha=0.5)
    plt.fill_between(x=range(0,
                             len(model.result)),
                     y1=model.UpperBond,
                     y2=model.LowerBond,
                     alpha=0.5,
                     color="grey")
    plt.plot(dataset[target].values, "g", label="Actual")
    plt.plot(Anomalies, "ro", markersize=7, label="Anomalies")
    plt.axvspan(
        len(dataset) -
        predict_interval -
        1,
        len(dataset),
        alpha=0.5,
        color='lightgrey')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc="best", fontsize=13)
    if xlim:
        plt.xlim(len(dataset) - xlim, len(dataset))
    plt.show()


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    Печатает и отрисовывает матрицу ошибок для задачи классификации
    Для нормализации небходимо передать аргумент normalize=True

    Parameters
    ----------
    cm: Матрица ошибок вида metrics.confusion_matrix(.., ..)
    classes: Наименование для значений целевой переменной
    normalize: Булева переменная, для нормализации матрицы
    title: Название для графика
    cmap: Цветовая палитра, по умолчанию: plt.cm.Blues
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    bottom, top = plt.ylim()
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes, rotation=45)
    plt.ylim([bottom, top])

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 verticalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('Истинный класс')
    plt.xlabel('Предсказанный класс')
    plt.show()


def stat_difference_by_flg(df, feature, target, name, flg, num_buck=10):
    """
    Считает разность в значениях целевой переменной между подмножествами исходного df, разбитого по флагу
    Подсчет происходит по бакетам признака feature если он числовой и просто по его значениям, если категориальный

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового или категориального)
    target: Название целевой переменной
    name: Как обозвать целевой признак
    flg: флаг по которому исходный фрейм разбивается на две части. Вычитание из flg=0. Как будто из прошлого
    num_buck: Количество бакетов, если признак числовой
    """
    if df[feature].dtype == 'O':
        agg = df.assign(obj_cnt=1)\
            .rename(columns={feature: 'bucket'})\
            .groupby([flg, 'bucket'], as_index=False)\
            .agg({target: 'mean', 'obj_cnt': 'sum'})\
            .rename(columns={target: 'AR', 'obj_cnt': 'feature_cnt'})\

        after = agg[agg[flg] == 1].copy()
        before = agg[agg[flg] == 0].copy()

        return before.join(after.set_index('bucket'), on='bucket', rsuffix='_after') \
            .assign(AR_decrease_mean=lambda x: x.AR - x.AR_after,
                    AR_decrease_std=lambda x: np.sqrt((x.AR * (1 - x.AR) / x.feature_cnt) + (x.AR_after * (1 - x.AR_after) / x.feature_cnt_after))) \
            .assign(AR_decrease_min=lambda x: x.AR_decrease_mean - 1.96 * x.AR_decrease_std,
                    AR_decrease_max=lambda x: x.AR_decrease_mean + 1.96 * x.AR_decrease_std) \
            .assign(AR_decrease_overall=lambda x: x.AR_decrease_mean * x.feature_cnt_after / after.feature_cnt.sum())[['bucket', 'AR_decrease_overall', 'AR_decrease_mean', 'AR_decrease_min', 'AR_decrease_max']] \
            .sort_values(by='AR_decrease_overall', ascending=False) \
            .rename(columns={'AR_decrease_overall': name + '_decrease_overall',
                             'AR_decrease_mean': name + '_decrease_mean',
                             'AR_decrease_min': name + '_decrease_min',
                             'AR_decrease_max': name + '_decrease_max'})\
            .set_index('bucket')

    else:
        # Бьем на бакеты, считаем AR до и после
        agg = df[df[feature].notnull()]\
            .assign(bucket=np.ceil(df[feature].rank(pct=True) * num_buck), obj_cnt=1)\
            .groupby([flg, 'bucket'], as_index=False)\
            .agg({target: 'mean', 'obj_cnt': 'sum', feature: 'mean'})\
            .rename(columns={target: 'AR', 'obj_cnt': 'feature_cnt', feature: 'feature_avg'})
# Разделяем фрейм на до и после
        after = agg[agg[flg] == 1].copy()
        before = agg[agg[flg] == 0].copy()
# Считаем среднюю разницу и доверительный интервал для этой средней
        return before.join(after.set_index('bucket'), on='bucket', rsuffix='_after')\
            .assign(AR_decrease_mean=lambda x: x.AR - x.AR_after,
                    AR_decrease_std=lambda x: np.sqrt((x.AR * (1 - x.AR) / x.feature_cnt) + (x.AR_after * (1 - x.AR_after) / x.feature_cnt_after)))\
            .assign(AR_decrease_min=lambda x: x.AR_decrease_mean - 1.96 * x.AR_decrease_std,
                    AR_decrease_max=lambda x: x.AR_decrease_mean + 1.96 * x.AR_decrease_std)\
            .assign(AR_decrease_overall=lambda x: x.AR_decrease_mean * x.feature_cnt_after / after.feature_cnt.sum())[['bucket', 'feature_avg', 'feature_avg_after', 'AR_decrease_overall', 'AR_decrease_mean', 'AR_decrease_min', 'AR_decrease_max']]\
            .rename(columns={'feature_avg': 'feature_avg_before'})\
            .rename(columns={'AR_decrease_overall': name + '_decrease_overall',
                             'AR_decrease_mean': name + '_decrease_mean',
                             'AR_decrease_min': name + '_decrease_min',
                             'AR_decrease_max': name + '_decrease_max'})\
            .set_index('bucket')


# Остальное


def plot_dual_axis(data, col1, col2, title=None):
    """
    Построение графика с двумя осями ординат

    Parameters
    ----------
    data: Объект pandas.DataFrame
    col1: Название основоного признака (левая ось)
    col2: Название дополнительного признака (правая ось)
    title: Заголовок графика
    """
    fig, ax1 = plt.subplots(
        figsize=(12, 6)
    )
    ax2 = ax1.twinx()

    ax2.bar(
        data.index,
        data[col2],
        width=20,
        alpha=0.15,
        fill=True,
        edgecolor='b'
    )
    ax1.plot(
        data.index,
        data[col1],
        'go--',
        linewidth=2
    )

    def naming(name):
        return ' '.join(
            [x[0].upper() + x[1:]
             for x in name.split('_')
            ]
        )

    ax1.set_xlabel(
        naming(data.index.name)
    )
    ax1.set_ylabel(
        naming(col1),
        color='g'
    )
    ax2.set_ylabel(
        naming(col2),
        color='b'
    )
    plt.title(title)
    plt.show()


# Пишем приветственное сообщение
print('Привет! Ты импортировал собственный модуль')
print('В нем собраны часто востребованные в работе методы, посмотреть их cписок можно с помощью dir(pm)')
print('Приятного использования!')
