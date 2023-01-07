# -*- coding: utf-8 -*-
# 通联数据机密
# --------------------------------------------------------------------
# 通联数据股份公司版权所有 © 2013-2022
#
# 注意：本文所载所有信息均属于通联数据股份公司资产。本文所包含的知识和技术概念均属于
# 通联数据产权，并可能由中国、美国和其他国家专利或申请中的专利所覆盖，并受商业秘密或
# 版权法保护。
# 除非事先获得通联数据股份公司书面许可，严禁传播文中信息或复制本材料。
#
# DataYes CONFIDENTIAL
# --------------------------------------------------------------------
# Copyright © 2013-2022 DataYes, All Rights Reserved.
#
# NOTICE: All information contained herein is the property of DataYes
# Incorporated. The intellectual and technical concepts contained herein are
# proprietary to DataYes Incorporated, and may be covered by China, U.S. and
# Other Countries Patents, patents in process, and are protected by trade
# secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from DataYes.
from . import api_base

try:
    from StringIO import StringIO
except:
    from io import StringIO
import pandas as pd
import sys
from datetime import datetime
from .api_base import get_cache_key, get_data_from_cache, put_data_in_cache, pretty_traceback
import inspect

try:
    unicode
except:
    unicode = str

__doc__ = "知识图谱"


def ProThemeGet(theProID="", theProName="", productID="", field="", pandas="1"):
    """
    存储主题产业链各节点的位置及产品代码。

    :param theProID: 节点代码 可以是列表 可空
    :param theProName: 节点名称 可以是列表 可空
    :param productID: 产品代码 可以是列表 可空
    :param field: 所需字段 可以是列表 可空
    :param pandas: 1表示返回 pandas data frame，0表示返回csv 可空
    :return: :raise e: API查询的结果，是CSV或者被转成pandas data frame；若查询API失败，返回空data frame； 若解析失败，则抛出异常
    """

    pretty_traceback()
    frame = inspect.currentframe()
    func_name, cache_key = get_cache_key(frame)
    cache_result = get_data_from_cache(func_name, cache_key)
    if cache_result is not None:
        return cache_result
    split_index = None
    split_param = None
    httpClient = api_base.__getConn__()
    requestString = []
    requestString.append('/api/kGraph/getProTheme.csv?ispandas=1&')
    requestString.append("theProID=")
    if hasattr(theProID, '__iter__') and not isinstance(theProID, str):
        if len(theProID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = theProID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in theProID]))
    else:
        requestString.append(str(theProID) if not isinstance(theProID, unicode) else theProID)
    requestString.append("&theProName=")
    if hasattr(theProName, '__iter__') and not isinstance(theProName, str):
        if len(theProName) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = theProName
            requestString.append(None)
        else:
            requestString.append(
                ','.join([str(item) if not isinstance(item, unicode) else item for item in theProName]))
    else:
        requestString.append(str(theProName) if not isinstance(theProName, unicode) else theProName)
    requestString.append("&productID=")
    if hasattr(productID, '__iter__') and not isinstance(productID, str):
        if len(productID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = productID
            requestString.append(None)
        else:
            requestString.append(
                ','.join([str(item) if not isinstance(item, unicode) else item for item in productID]))
    else:
        requestString.append(str(productID) if not isinstance(productID, unicode) else productID)
    requestString.append("&field=")
    if hasattr(field, '__iter__') and not isinstance(field, str):
        if len(field) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = field
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in field]))
    else:
        requestString.append(str(field) if not isinstance(field, unicode) else field)
    if split_param is None:
        csvString = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
        if csvString is None or len(csvString) == 0 or (
                csvString[0] == '-' and not api_base.is_no_data_warn(csvString, False)) or csvString[0] == '{':
            api_base.handle_error(csvString, 'ProThemeGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (
                    temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, 'ProThemeGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n') + 1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'theProID', u'productID', u'theProName', u'parentID', u'type', u'class', u'position', u'version',
                     u'isNew', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO,
                              dtype={'theProID': 'str', 'productID': 'str', 'theProName': 'str', 'parentID': 'str',
                                     'type': 'str', 'position': 'str'}, )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()


def ProThemeChainGet(productID="", relProductID="", field="", pandas="1"):
    """
    存储主题产业链中涉及的产业链上下游关系。

    :param productID: 主产品代码，可通过getProTheme获取productID 可以是列表,productID、relProductID至少选择一个
    :param relProductID: 关联产品代码，可通过getProTheme获取productID 可以是列表,productID、relProductID至少选择一个
    :param field: 所需字段 可以是列表 可空
    :param pandas: 1表示返回 pandas data frame，0表示返回csv 可空
    :return: :raise e: API查询的结果，是CSV或者被转成pandas data frame；若查询API失败，返回空data frame； 若解析失败，则抛出异常
    """

    pretty_traceback()
    frame = inspect.currentframe()
    func_name, cache_key = get_cache_key(frame)
    cache_result = get_data_from_cache(func_name, cache_key)
    if cache_result is not None:
        return cache_result
    split_index = None
    split_param = None
    httpClient = api_base.__getConn__()
    requestString = []
    requestString.append('/api/kGraph/getProThemeChain.csv?ispandas=1&')
    requestString.append("productID=")
    if hasattr(productID, '__iter__') and not isinstance(productID, str):
        if len(productID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = productID
            requestString.append(None)
        else:
            requestString.append(
                ','.join([str(item) if not isinstance(item, unicode) else item for item in productID]))
    else:
        requestString.append(str(productID) if not isinstance(productID, unicode) else productID)
    requestString.append("&relProductID=")
    if hasattr(relProductID, '__iter__') and not isinstance(relProductID, str):
        if len(relProductID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = relProductID
            requestString.append(None)
        else:
            requestString.append(
                ','.join([str(item) if not isinstance(item, unicode) else item for item in relProductID]))
    else:
        requestString.append(str(relProductID) if not isinstance(relProductID, unicode) else relProductID)
    requestString.append("&field=")
    if hasattr(field, '__iter__') and not isinstance(field, str):
        if len(field) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = field
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in field]))
    else:
        requestString.append(str(field) if not isinstance(field, unicode) else field)
    if split_param is None:
        csvString = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
        if csvString is None or len(csvString) == 0 or (
                csvString[0] == '-' and not api_base.is_no_data_warn(csvString, False)) or csvString[0] == '{':
            api_base.handle_error(csvString, 'ProThemeChainGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (
                    temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, 'ProThemeChainGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n') + 1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'productID', u'relProductID', u'priRelation', u'relativePosition', u'version', u'isNew',
                     u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype={'productID': 'str', 'relProductID': 'str', 'priRelation': 'str',
                                           'relativePosition': 'str'}, )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()


def ProThemeComGet(partyID="", partyShortName="", partyFullName="", productID="", field="", pandas="1"):
    """
    存储主题产业链中涉及的公司产品关系。

    :param partyID: 公司ID，可通过DataAPI.PartyIDGet获取 可以是列表,partyID、partyShortName、partyFullName、productID至少选择一个
    :param partyShortName: 公司简称,partyID、partyShortName、partyFullName、productID至少选择一个
    :param partyFullName: 公司全称，支持模糊查询,partyID、partyShortName、partyFullName、productID至少选择一个
    :param productID: 标准产品代码，可通过getProTheme获取productID 可以是列表,partyID、partyShortName、partyFullName、productID至少选择一个
    :param field: 所需字段 可以是列表 可空
    :param pandas: 1表示返回 pandas data frame，0表示返回csv 可空
    :return: :raise e: API查询的结果，是CSV或者被转成pandas data frame；若查询API失败，返回空data frame； 若解析失败，则抛出异常
    """

    pretty_traceback()
    frame = inspect.currentframe()
    func_name, cache_key = get_cache_key(frame)
    cache_result = get_data_from_cache(func_name, cache_key)
    if cache_result is not None:
        return cache_result
    split_index = None
    split_param = None
    httpClient = api_base.__getConn__()
    requestString = []
    requestString.append('/api/kGraph/getProThemeCom.csv?ispandas=1&')
    requestString.append("partyID=")
    if hasattr(partyID, '__iter__') and not isinstance(partyID, str):
        if len(partyID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = partyID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in partyID]))
    else:
        requestString.append(str(partyID) if not isinstance(partyID, unicode) else partyID)
    if not isinstance(partyShortName, str) and not isinstance(partyShortName, unicode):
        partyShortName = str(partyShortName)

    requestString.append("&partyShortName=%s" % (partyShortName))
    if not isinstance(partyFullName, str) and not isinstance(partyFullName, unicode):
        partyFullName = str(partyFullName)

    requestString.append("&partyFullName=%s" % (partyFullName))
    requestString.append("&productID=")
    if hasattr(productID, '__iter__') and not isinstance(productID, str):
        if len(productID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = productID
            requestString.append(None)
        else:
            requestString.append(
                ','.join([str(item) if not isinstance(item, unicode) else item for item in productID]))
    else:
        requestString.append(str(productID) if not isinstance(productID, unicode) else productID)
    requestString.append("&field=")
    if hasattr(field, '__iter__') and not isinstance(field, str):
        if len(field) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = field
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in field]))
    else:
        requestString.append(str(field) if not isinstance(field, unicode) else field)
    if split_param is None:
        csvString = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
        if csvString is None or len(csvString) == 0 or (
                csvString[0] == '-' and not api_base.is_no_data_warn(csvString, False)) or csvString[0] == '{':
            api_base.handle_error(csvString, 'ProThemeComGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (
                    temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, 'ProThemeComGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n') + 1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'partyID', u'partyShortName', u'partyFullName', u'relationPro', u'productID', u'version',
                     u'isNew', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype={'partyShortName': 'str', 'partyFullName': 'str', 'relationPro': 'str',
                                           'productID': 'str'}, )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()


def ProThemeIndexDataGet(indicID="", periodDate="", beginDate="", endDate="", field="", pandas="1"):
    """
    存储主题产业链中涉及的指标数据。

    :param indicID: 指标代码，可通过getProThemeIndexInfo获取 可以是列表,indicID、periodDate至少选择一个
    :param periodDate: 数据日期 可以是列表,indicID、periodDate至少选择一个
    :param beginDate: 数据查询起始日期，输入格式"YYYYMMDD" 可空
    :param endDate: 数据查询截至日期，输入格式"YYYYMMDD" 可空
    :param field: 所需字段 可以是列表 可空
    :param pandas: 1表示返回 pandas data frame，0表示返回csv 可空
    :return: :raise e: API查询的结果，是CSV或者被转成pandas data frame；若查询API失败，返回空data frame； 若解析失败，则抛出异常
    """

    pretty_traceback()
    frame = inspect.currentframe()
    func_name, cache_key = get_cache_key(frame)
    cache_result = get_data_from_cache(func_name, cache_key)
    if cache_result is not None:
        return cache_result
    split_index = None
    split_param = None
    httpClient = api_base.__getConn__()
    requestString = []
    requestString.append('/api/kGraph/getProThemeIndexData.csv?ispandas=1&')
    requestString.append("indicID=")
    if hasattr(indicID, '__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    try:
        if isinstance(periodDate, datetime):
            periodDate = periodDate.strftime('%Y%m%d')
        elif isinstance(periodDate, list):
            tds = []
            for td in periodDate:
                td = td.strftime('%Y%m%d')
                tds.append(td)
            periodDate = tds
        else:
            raise Exception
    except:
        if isinstance(periodDate, (str, unicode)):
            tradeDates = periodDate.split(',')
            tds = []
            for td in tradeDates:
                td = td.replace('-', '')
                tds.append(td)
            periodDate = tds
        elif isinstance(periodDate, list):
            tds = []
            for td in periodDate:
                td = td.replace('-', '')
                tds.append(td)
            periodDate = tds

    requestString.append("&periodDate=")
    if hasattr(periodDate, '__iter__') and not isinstance(periodDate, str):
        if len(periodDate) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = periodDate
            requestString.append(None)
        else:
            requestString.append(
                ','.join([str(item) if not isinstance(item, unicode) else item for item in periodDate]))
    else:
        requestString.append(str(periodDate) if not isinstance(periodDate, unicode) else periodDate)
    try:
        beginDate = beginDate.strftime('%Y%m%d')
    except:
        beginDate = beginDate.replace('-', '')
    requestString.append("&beginDate=%s" % (beginDate))
    try:
        endDate = endDate.strftime('%Y%m%d')
    except:
        endDate = endDate.replace('-', '')
    requestString.append("&endDate=%s" % (endDate))
    requestString.append("&field=")
    if hasattr(field, '__iter__') and not isinstance(field, str):
        if len(field) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = field
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in field]))
    else:
        requestString.append(str(field) if not isinstance(field, unicode) else field)
    if split_param is None:
        csvString = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
        if csvString is None or len(csvString) == 0 or (
                csvString[0] == '-' and not api_base.is_no_data_warn(csvString, False)) or csvString[0] == '{':
            api_base.handle_error(csvString, 'ProThemeIndexDataGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (
                    temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, 'ProThemeIndexDataGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n') + 1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'indicID', u'nameCN', u'publishDate', u'periodDate', u'dataValue', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype={'indicID': 'str', 'nameCN': 'str'}, )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()


def ProThemeIndexInfoGet(productID="", indicID="", nameCN="", field="", pandas="1"):
    """
    存储主题产业链中涉及的指标信息。

    :param productID: 产品代码，可通过getProTheme获取productID 可以是列表,productID、indicID、nameCN至少选择一个
    :param indicID: 指标代码 可以是列表,productID、indicID、nameCN至少选择一个
    :param nameCN: 指标名称，支持模糊查询,productID、indicID、nameCN至少选择一个
    :param field: 所需字段 可以是列表 可空
    :param pandas: 1表示返回 pandas data frame，0表示返回csv 可空
    :return: :raise e: API查询的结果，是CSV或者被转成pandas data frame；若查询API失败，返回空data frame； 若解析失败，则抛出异常
    """

    pretty_traceback()
    frame = inspect.currentframe()
    func_name, cache_key = get_cache_key(frame)
    cache_result = get_data_from_cache(func_name, cache_key)
    if cache_result is not None:
        return cache_result
    split_index = None
    split_param = None
    httpClient = api_base.__getConn__()
    requestString = []
    requestString.append('/api/kGraph/getProThemeIndexInfo.csv?ispandas=1&')
    requestString.append("productID=")
    if hasattr(productID, '__iter__') and not isinstance(productID, str):
        if len(productID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = productID
            requestString.append(None)
        else:
            requestString.append(
                ','.join([str(item) if not isinstance(item, unicode) else item for item in productID]))
    else:
        requestString.append(str(productID) if not isinstance(productID, unicode) else productID)
    requestString.append("&indicID=")
    if hasattr(indicID, '__iter__') and not isinstance(indicID, str):
        if len(indicID) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = indicID
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in indicID]))
    else:
        requestString.append(str(indicID) if not isinstance(indicID, unicode) else indicID)
    if not isinstance(nameCN, str) and not isinstance(nameCN, unicode):
        nameCN = str(nameCN)

    requestString.append("&nameCN=%s" % (nameCN))
    requestString.append("&field=")
    if hasattr(field, '__iter__') and not isinstance(field, str):
        if len(field) > 100 and split_param is None:
            split_index = len(requestString)
            split_param = field
            requestString.append(None)
        else:
            requestString.append(','.join([str(item) if not isinstance(item, unicode) else item for item in field]))
    else:
        requestString.append(str(field) if not isinstance(field, unicode) else field)
    if split_param is None:
        csvString = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
        if csvString is None or len(csvString) == 0 or (
                csvString[0] == '-' and not api_base.is_no_data_warn(csvString, False)) or csvString[0] == '{':
            api_base.handle_error(csvString, 'ProThemeIndexInfoGet')
        elif csvString[:2] == '-1':
            csvString = ''
    else:
        p_list = api_base.splist(split_param, 100)
        csvString = []
        for index, item in enumerate(p_list):
            requestString[split_index] = ','.join([str(it) if not isinstance(it, unicode) else it for it in item])
            temp_result = api_base.__getCSV__(''.join(requestString), httpClient, gw=True)
            if temp_result is None or len(temp_result) == 0 or temp_result[0] == '{' or (
                    temp_result[0] == '-' and not api_base.is_no_data_warn(temp_result, False)):
                api_base.handle_error(temp_result, 'ProThemeIndexInfoGet')
            if temp_result[:2] != '-1':
                csvString.append(temp_result if len(csvString) == 0 else temp_result[temp_result.find('\n') + 1:])
        csvString = ''.join(csvString)

    if len(csvString) == 0:
        if 'field' not in locals() or len(field) == 0:
            field = [u'productID', u'indicID', u'nameCN', u'unit', u'freq', u'stat', u'source', u'updateTime']
        if hasattr(field, '__iter__') and not isinstance(field, str):
            csvString = ','.join(field) + '\n'
        else:
            csvString = field + '\n'
    if pandas != "1":
        put_data_in_cache(func_name, cache_key, csvString)
        return csvString
    try:
        myIO = StringIO(csvString)
        pdFrame = pd.read_csv(myIO, dtype={'productID': 'str', 'indicID': 'str', 'nameCN': 'str', 'unit': 'str',
                                           'freq': 'str', 'stat': 'str', 'source': 'str'}, )
        put_data_in_cache(func_name, cache_key, pdFrame)
        return pdFrame
    except Exception as e:
        raise e
    finally:
        myIO.close()
