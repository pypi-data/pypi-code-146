#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import requests
import hashlib
import copy
import time
"""
对于公众号：
    返回参数列表：
        名称	类型	必须	描述
        code	int	是	请求结果200表示成功，其他则为失败
        message	string	是	请求结果描述
        data	T	否	请求返回结果集，可空
    
    错误码及说明：
        错误码	说明
        200	成功
        1001	consumerkey非法
        1002	签名校验错误
        1003	请求参数缺失
        1004	timestamp 值非法
        1005	timestamp 过期
        1006	请求参数有重复
        500	系统错误
        404	记录不存在
        405	访问过于频繁，可减少并发调用频次

对于快应用：
    请求响应格式：
        每次请求均返回下列参数，data字段格式详见各个接口，响应格式为json，后续每个接口的返回字段说明只列出data内字段定义
        
        名称	类型	必须	描述
        code	int	是	响应code，200表示成功，其它错误码详见第3节
        message	string	是	响应描述，成功返回success，其它错误码返回相应错误信息
        data	Object	否	具体响应结果，详见各自接口描述
    错误码及说明：
        错误码	说明
        200	成功
        1001	appkey非法
        1002	签名校验错误
        1003	请求参数缺失
        1004	timestamp 值格式非法
        1005	timestamp 不在有效范围内
        1006	请求参数存在重复
        1007	指定时间范围无效
        1008	指定时间范围超出限制
        500	系统错误
"""


def make_sign(
        consumer_key: str = None,  # 从服务商处获取
        secret_key: str = None,  # 从服务商处获取
        data: dict = None,  # 要传的数据
        timestamp: int = None
):
    """
    生成签名
    """
    if timestamp is None:
        timestamp: int = int(time.time() * 1000)
    if data is None:
        data = {}
    data['timestamp'] = timestamp  # 增加必填字段
    data['consumerkey'] = consumer_key  # 增加必填字段
    local_secret_key = secret_key

    local_data = copy.deepcopy(data)
    local_data['secretkey'] = local_secret_key
    sorted_keys = sorted(local_data.keys())
    key_values = ''
    for key in sorted_keys:
        key_value = '%s=%s' % (key, local_data[key])
        key_values += key_value
    d5 = hashlib.md5()
    d5.update(key_values.encode(encoding='UTF-8'))  # update添加时会进行计算
    sign = d5.hexdigest()

    data['sign'] = sign  # 增加sign

    if 'secretkey' in data:
        data.pop('secretkey')  # 防止多传此值

    return data


def make_sign_quickapp(
        app_key: str = None,  # 从服务商处获取
        app_secret: str = None,  # 从服务商处获取
        data: dict = None,  # 要传的数据
        timestamp: int = None
):
    """
    生成签名，适用于快应用
    :param app_key: 接口调用身份标识，由平台提供
    :param app_secret:
    :param data:
    :param timestamp: 当前13位毫秒时间戳
    """
    if timestamp is None:
        timestamp: int = int(time.time() * 1000)
    if data is None:
        data = {}
    data['timestamp'] = timestamp  # 增加必填字段
    data['appkey'] = app_key  # 增加必填字段
    local_data = copy.deepcopy(data)
    local_data['appsecret'] = app_secret
    sorted_keys = sorted(local_data.keys())
    key_values = ''
    for key in sorted_keys:
        key_value = '%s=%s' % (key, local_data[key])
        key_values += key_value
    d5 = hashlib.md5()
    d5.update(key_values.encode(encoding='UTF-8'))  # update添加时会进行计算
    sign = d5.hexdigest()

    data['sign'] = sign  # 增加sign

    if 'appsecret' in data:
        data.pop('appsecret')  # 防止多传此值

    return data


def site_list(
        consumer_key: str,
        secret_key: str
):
    """
    2.1分销站点列表

    入参：
        名称	类型	必须	描述
        consumerkey	long	是	分销商唯一标识
        timestamp	long	是	当前时间戳，取13位毫秒时间戳
        sign	string	是	API输入参数签名结果，使用md5加密,见MD5签名规则

    返回：
        名称	类型	必须	描述
        code	int	是	返回值
        message	string	是	信息描述
        mpId	long	是	站点所属公众号id
        mpName	string	是	站点所属公众号名称
        appID	string	是	公众号开发者的appid
        id	long	是	站点id
        domain	string	是	站点域名
        name	string	是	站点名称
    """
    data = make_sign(
        consumer_key=consumer_key,
        secret_key=secret_key
    )
    url = 'https://bi.reading.163.com/dist-api/siteList'
    response = requests.request(
        method='GET',
        url=url,
        params=data
    )
    return response.json()


def site_list_quickapp(
        app_key: str,
        app_secret: str
):
    """
    2.1. 子账号列表查询
    适用于快应用

    入参：
        名称	类型	必须	描述
        app_key
        app_secret

    返回：
        名称	类型	必须	描述
        code	int	是	响应code，200表示成功，其它错误码详见第3节
        message	string	是	响应描述，成功返回success，其它错误码返回相应错误信息
        data	long	是	具体响应结果，详见各自接口描述

    data详情：
        名称	类型	必须	描述
        subProviderId	long	是	子账号id
        subProviderEmail	string	是	子账号邮箱
        subProviderName	string	是	子账号姓名/昵称
        subProviderPhone	string	是	子账号联系方式
        createTime	long	是	子账号创建时间，13位毫秒时间戳

    返回demo:
        {
            "code": 200,
            "data": {
                "subProviderList": [
                    {
                        "subProviderId": 132,
                        "subProviderEmail": "test123@163.com",
                        "subProviderName": "子账号1",
                        "subProviderPhone": "18818881911",
                        "createTime": 1625220710221
                    }
                ]
            },
            "message": "success"
        }

    """
    data = make_sign_quickapp(
        app_key=app_key,
        app_secret=app_secret
    )
    url = 'https://quickbi.yunydbook163.com/dist-api/sub-provider/list'
    response = requests.request(
        method='GET',
        url=url,
        params=data
    )
    return response.json()


def recharge_list(
        consumer_key: str,
        secret_key: str,
        site_id: int,
        start_time: int = None,
        end_time: int = None,
        page: int = 1,
        page_size: int = 20,
        pay_status: int = None,
):
    """
    2.2分销站点充值信息列表

    入参：
        名称	类型	必须	描述
        consumerkey	long	是	分销商唯一标识
        timestamp	long	是	当前时间戳，取13位毫秒时间戳
        sign	string	是	API输入参数签名结果，使用md5加密,见MD5签名规则
        siteid	long	是	站点id
        starttime	long	否	开始时间，格式yyyyMMddHHmm 包含
        endtime	long	否	结束时间，格式yyyyMMddHHmm 不包含
        pageSize	int	否	默认一页显示20条记录,可以根据自身需求设置，限制10000条
        page	int	否	默认第一页
        paystatus	int	否	订单状态：0-未付款，1-已付款，2-交易关闭，不传默认获取所有记录

    返回：
        名称	类型	必须	描述
        code	int	是	返回值
        message	string	是	信息描述
        totalPage	int	是	总页数
        userId	long	是	用户id
        nickName	string	是	用户昵称
        ip	string	是	充值ip
        userAgent	string	是	充值ua
        userFollowTime	long	是	用户关注时间
        userRegisterTime	long	是	用户注册时间
        wx_originalId	string	是	公众号原始id
        wx_mpName	string	是	公众号名称
        wx_user_openId	string	是	微信用户openid
        rechargeUuid	string	是	订单号
        ewTradeId	string	否	交易号,payStatus=1有值
        payTime	long	否	订单支付时间，payStatus=1有值
        rechargeMethod	int	是	充值渠道：1-微信，2-支付宝
        money	int	是	到账阅点，单位：分
        createTime	long	是	订单生成时间
        updateTime	long	是	订单更新时间
        payStatus	int	是	订单状态：0-未付款，1-已付款， 2-交易关闭
        sourceUuid	string	否	订单关联书籍id
        bookTitle	string	否	订单关联书籍名称
    """
    local_data = {
        'siteid': site_id
    }
    if start_time is not None:
        local_data['starttime'] = start_time
    if end_time is not None:
        local_data['endtime'] = end_time
    if page_size is not None:
        local_data['pageSize'] = page_size
    if page is not None:
        local_data['page'] = page
    if pay_status is not None:
        local_data['paystatus'] = pay_status

    data = make_sign(
        consumer_key=consumer_key,
        secret_key=secret_key,
        data=local_data
    )
    url = 'https://bi.reading.163.com/dist-api/rechargeList'
    response = requests.request(
        method='GET',
        url=url,
        params=data
    )
    return response.json()


def recharge_list_quickapp(
        app_key: str,
        app_secret: str,
        site_id: int,
        start_time: int = None,
        end_time: int = None,
        page: int = 1,
        page_size: int = 20,
        pay_status: int = None
):
    """
    2.2. 充值订单查询
    适用于快应用
    :param app_key: 分销商唯一标识
    :param app_secret:
    :param start_time: 开始时间，13位毫秒时间戳，包含
    :param end_time: 结束时间，13位毫秒时间戳，不包含
    :param pay_status: 订单状态，0-未支付，1-已支付；不传默认获取所有
    :param site_id: 子账号id，筛选该子账号下的数据；从“子账号列表查询”接口获取
    :param page: 页码，默认第1页
    :param page_size: 每页记录数，默认20，上限1000条
    :param app_key: 分销商唯一标识

    返回：
        名称	类型	必须	描述
        code	int	是	响应code，200表示成功，其它错误码详见第3节
        message	string	是	响应描述，成功返回success，其它错误码返回相应错误信息
        data	long	是	具体响应结果，详见各自接口描述

    data详情：
        名称	类型	必须	描述
        totalPage	int	是	当前查询条件对应结果集列表总页数
        rechargeSid	string	是	充值流水号，唯一
        money	int	是	充值金额，单位分
        payStatus	int	是	充值状态 0：未付款；1：已付款
        payTime	long	否	支付时间，13位毫秒时间戳，payStatus=1时有值
        ewTradeId	string	否	支付订单的订单号，payStatus=1时有值
        createTime	long	是	下单时间，13位毫秒时间戳
        updateTime	long	是	订单状态更新时间，13位毫秒时间戳
        userId	long	是	用户id
        userRegisterTime	long	是	用户注册时间，13位毫秒时间戳
        userLinkId	long	否	用户注册时的推广链接id
        bookId	string	否	订单关联书籍id
        bookTitle	string	否	订单关联书籍名称
        subProviderEmail	string	否	用户关联的子账号邮箱，可能为null，表示不关联任何子账号
        subProviderName	string	否	用户关联的子账号姓名/昵称，可能为null，表示不关联任何子账号
        aid	string	否	广告计划id，字符串格式，可能为null
        cid	string	否	广告创意id，字符串格式，可能为null

    返回demo:
        {
            "code": 200,
            "data": {
                "totalPage": 1,
                "rechargeList": [
                    {
                        "userId": 763,
                        "createTime": 1625220710221,
                        "updateTime": 1625220710221,
                        "payTime": null,
                        "ewTradeId": null,
                        "money": 666,
                        "payStatus": 0,
                        "bookId": "e4b6d2f142e74e9491c5d52d667c445a_4",
                        "bookTitle": "王者归来",
                        "userRegisterTime": 1625214739686,
                        "userLinkId": 1,
                        "subProviderEmail": "test123@163.com",
                        "subProviderName": "子账号1",
                        "aid": "1730984822949911",
                        "cid": "1730984839846999",
                        "rechargeSid": "qa_Lis2060fc99"
                    },
                    {
                        "userId": 759,
                        "createTime": 1625538561398,
                        "updateTime": 1625538568134,
                        "payTime": 1625538567000,
                        "ewTradeId": "4200001149202107064836488960",
                        "money": 1200,
                        "payStatus": 1,
                        "bookId": null,
                        "bookTitle": null,
                        "userRegisterTime": 1625214739776,
                        "userLinkId": null,
                        "subProviderEmail": null,
                        "subProviderName": null,
                        "aid": null,
                        "cid": null,
                        "rechargeSid": "qa_Liodf0f9dff"
                    }
                ]
            },
            "message": "success"
        }
    """
    local_data = {
        'subProviderId': site_id
    }
    if start_time is not None:
        local_data['startTime'] = start_time
    if end_time is not None:
        local_data['endTime'] = end_time
    if page_size is not None:
        local_data['pageSize'] = page_size
    if page is not None:
        local_data['page'] = page
    if pay_status is not None:
        local_data['payStatus'] = pay_status

    data = make_sign_quickapp(
        app_key=app_key,
        app_secret=app_secret,
        data=local_data
    )
    url = 'https://quickbi.yunydbook163.com/dist-api/recharge/list'
    response = requests.request(
        method='GET',
        url=url,
        params=data
    )
    return response.json()
