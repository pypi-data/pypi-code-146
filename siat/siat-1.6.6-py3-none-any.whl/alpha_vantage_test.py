# -*- coding: utf-8 -*-

"""
功能：测试新的插件，仅限测试使用
作者：王德宏，北京外国语大学国际商学院
版权：2022(C) 仅限教学使用，商业使用需要授权
联络：wdehong2000@163.com
"""

# 绝对引用指定目录中的模块
import sys
sys.path.insert(0,r'S:\siat\siat')


#========================================================================
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='J4L80CM3ATCKNONG', output_format='pandas', indexing_type='date')
data, meta_data = ts.get_daily('GOOGL', outputsize='full')
data, meta_data = ts.get_daily('FCHI', outputsize='full')



#========================================================================

