
BASE_SHIPPING_API_CODE = 20104000


class ShippingPartnerCodes(object):
    '''ExpressPartner里面要用到的code'''
    # 顺丰
    SF = "sf"
    # 顺丰同城急送
    SFTCJS = "sftcjs"
    # 圆通
    YTO = "yto"
    # 中通
    ZTO = "zto"
    # 申通
    STO = "sto"
    # EMS
    EMS = "ems"
    # 邮政
    YZPY = "yzpy"
    # 韵达
    YD = "yd"
    # 宅急送
    ZJS = "zjs"
    # 京东
    JD = "jd"
    # 德邦
    DBL = "dbl"
    # 百世快递
    HTKY = "htky"
    # 天天
    HHTT = "hhtt"
    # 其它
    OTHERS = "others"
    # 专柜代发
    SHOP = "shop"
    # 闪送
    SS = "ss"


# 快递公司代号与中文对照
ShippingPartnerCodes_DICT = {
    ShippingPartnerCodes.SF: "顺丰",
    ShippingPartnerCodes.SFTCJS: "顺丰同城急送",
    ShippingPartnerCodes.YTO: "圆通",
    ShippingPartnerCodes.ZTO: "中通",
    ShippingPartnerCodes.STO: "申通",
    ShippingPartnerCodes.EMS: "EMS",
    ShippingPartnerCodes.YZPY: "邮政",
    ShippingPartnerCodes.YD: "韵达",
    ShippingPartnerCodes.ZJS: "宅急送",
    ShippingPartnerCodes.JD: "京东",
    ShippingPartnerCodes.DBL: "德邦",
    ShippingPartnerCodes.HTKY: "百世快递",
    ShippingPartnerCodes.HHTT: "天天",
    ShippingPartnerCodes.OTHERS: "其它",
    ShippingPartnerCodes.SHOP: "专柜代发",
    ShippingPartnerCodes.SS: "闪送",
}


class PrintStatus(object):

    NEW = "new"
    PRINTING = "printing"
    PRINTED = "printed"


class SFShippingType(object):

    SF_NEXT_DAY = "sf_next_day"
    SF_THIRD_DAY = "sf_third_day"


class ZTOExpressImportFields(object):
    '''导入中通excel中用的column name'''

    SHIPPING_NUMBER = "shipping_number"
    NOTE = "note"
    POSTAGE = "postage"

    fields = {
        # SHIPPING_NUMBER: '单号',
        SHIPPING_NUMBER: '运单编号',
        POSTAGE: '运费',
        # NOTE: '备注'
        NOTE: '商品信息'
    }


class SFExpressImportFields(object):
    '''导入顺丰excel中用的column name'''

    SHIPPING_NUMBER = "shipping_number"
    NOTE = "note"
    ASSIGNMENT_ID = "assignment_id"
    POSTAGE = "postage"

    fields = {
        SHIPPING_NUMBER: '运单号',
        ASSIGNMENT_ID: '订单号',
        NOTE: '操作备注',
        POSTAGE: "参考运费/元",
    }


# 邮费映射表
EXPRESS_PRICE_MAP = {
    "zto": {
        "北京": 6,
        "天津": 7,
        "河北": 7,
        "甘肃": 15,
        "宁夏": 15,
        "青海": 15,
        "海南": 20,
        "新疆": 20,
        "西藏": 20,
        "default": 8
    }
}


class express_pay_method(object):
    # 寄付
    SENDER_PAY = "sender_pay"
    # 到付
    RECEIVER_PAY = "receiver_pay"

    EXPRESS_PAY_METHOD_CHOISE = (
        (SENDER_PAY, "寄付"),
        (RECEIVER_PAY, "到付"),
    )
