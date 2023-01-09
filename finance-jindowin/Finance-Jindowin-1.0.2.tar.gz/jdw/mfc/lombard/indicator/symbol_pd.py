# -*- encoding:utf-8 -*-
from jdw.mfc.lombard.indicator.date import week_of_date


def _benchmark(df, benchmark_pd):
    """
    在内部使用kline_pd获取金融时间序列pd.DataFrame后，如果参数中
    基准benchmark（pd.DataFrame对象）存在，使用基准benchmark的
    时间范围切割kline_pd返回的金融时间序列
    :param df: 金融时间序列pd.DataFrame对象
    :param benchmark: 资金回测时间标尺，AbuBenchmark实例对象
    :return: 使用基准的时间范围切割返回的金融时间序列
    """
    if len(df.index & benchmark_pd.index) <= 0:
        # 如果基准benchmark时间范围和输入的df没有交集，直接返回None
        return None

    df = df.reindex(benchmark_pd.index)
    kl_pd = df.loc[benchmark_pd.index]

    # 两个金融时间序列通过loc寻找交集
    kl_pd = df.loc[benchmark_pd.index]
    # nan的date个数即为不相交的个数
    nan_cnt = kl_pd['date'].isnull().value_counts()
    # 两个金融序列是否相同的结束日期
    same_end = df.index[-1] == benchmark_pd.index[-1]
    # 两个金融序列是否相同的开始日期
    same_head = df.index[0] == benchmark_pd.index[0]

    # 如果nan_cnt即不相交个数大于benchmark基准个数的1/3，放弃
    base_keep_div = 3
    if same_end or same_head:
        # 如果两个序列有相同的开始或者结束改为1/2，也就是如果数据头尾日起的标尺有一个对的上的话，放宽na数量
        base_keep_div = 2
    if same_end and same_head:
        # 如果两个序列同时有相同的开始和结束改为1，也就是如果数据头尾日起的标尺都对的上的话，na数量忽略不计
        base_keep_div = 1

    #if symbol.is_a_stock():
    #    # 如果是A股市场的目标，由于停盘频率和周期都会长与其它市场所以再放宽一些
    #    base_keep_div *= 0.7

    if nan_cnt.index.shape[0] > 0 and nan_cnt.index.tolist().count(True) > 0 \
            and nan_cnt.loc[True] > benchmark_pd.shape[0] / base_keep_div:
        # nan 个数 > 基准base_keep_div分之一放弃
        return None

    # 来到这里说明没有放弃，那么就填充nan
    # 首先nan的交易量是0
    kl_pd.volume.fillna(value=0, inplace=True)
    # nan的p_change是0
    kl_pd.p_change.fillna(value=0, inplace=True)
    # 先把close填充了，然后用close填充其它的
    kl_pd.close.fillna(method='pad', inplace=True)
    kl_pd.close.fillna(method='bfill', inplace=True)
    # 用close填充open
    kl_pd.open.fillna(value=kl_pd.close, inplace=True)
    # 用close填充high
    kl_pd.high.fillna(value=kl_pd.close, inplace=True)
    # 用close填充low
    kl_pd.low.fillna(value=kl_pd.close, inplace=True)
    # 用close填充pre_close
    kl_pd.pre_close.fillna(value=kl_pd.close, inplace=True)

    # 细节nan处理完成后，把剩下的nan都填充了
    kl_pd = kl_pd.fillna(method='pad')
    # bfill再来一遍只是为了填充最前面的nan
    kl_pd.fillna(method='bfill', inplace=True)

    # pad了数据所以，交易日期date的值需要根据time index重新来一遍
    kl_pd['date'] = [int(ts.date().strftime("%Y%m%d")) for ts in kl_pd.index]
    kl_pd['date_week'] = kl_pd['date'].apply(
        lambda x: week_of_date(str(x), '%Y%m%d'))

    return kl_pd