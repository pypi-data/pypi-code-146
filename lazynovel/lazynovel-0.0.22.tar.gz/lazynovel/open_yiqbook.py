#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests
from lazysdk import lazytime
from lazysdk import lazymd5
"""
万丈书城（中文在线 快应用）开放接口SDK

所有接口的响应结构均为 json，格式及说明如下：
JSON
    {
         "code": 0,
         "msg": null,
         "data": {},
         "exception": null,
         "sysTime": 1651218161000
    }
    
返回码
    code message 处理建议
    0 ok 正确返回，无需处理
    8004 sign 错误 签名计算错误（排查代码）或者密钥失效（联系商务）
    9060 timestamp 不合法 见文档 1.2 节关于 ts 字段的说明
    500 内部错误 稍后重试，大面积持续失败请联系研发团队
"""


def make_sign(
        params: dict
):
    """
    生成签名
    :param params: 参数字典
    :return:
    """
    use_keys = ['distributorId', 'appKey', 'timeStamp']  # 只使用这些字段签名
    params_keys = list(params.keys())
    params_keys.sort(reverse=False)
    params_str = ''
    for each_key in params_keys:
        if each_key in use_keys:
            if params.get(each_key) is not None:
                if len(str(params.get(each_key))) > 0:
                    params_str += f'{each_key}={params[each_key]}&'
    params_str = params_str[:-1]
    sign = lazymd5.md5_str(params_str)
    params['sign'] = sign  # 一定要包含的字段
    params.pop('appKey')  # 一定要删除的字段
    return params


def get_user_recharge(
        distributor_id,
        sign_key,
        page_no: int = 1,
        page_size: int = 20
):
    """
    充值信息（获取充值列表）
    :param distributor_id: 分销商标识
    :param sign_key:
    :param page_no: 页号,参数示例：100
    :param page_size: 每页条数,参数示例：100
    :return:
    """
    # ---------------- 相对固定设置 ----------------
    time_stamp = lazytime.get_timestamp()
    params = dict()
    params['distributorId'] = distributor_id  # 渠道id【签名必须】
    params['appKey'] = sign_key  # 渠道id【签名必须】
    params['timeStamp'] = time_stamp * 1000  # 时间戳【签名必须】
    params = make_sign(
        params=params
    )
    params['offset'] = (page_no - 1) * page_size
    params['limit'] = page_size
    # ---------------- 相对固定设置 ----------------

    url = 'http://openapi.yiqbook.com/out/openapi/data/user/recharge'
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        params=params,
        return_json=True
    )
