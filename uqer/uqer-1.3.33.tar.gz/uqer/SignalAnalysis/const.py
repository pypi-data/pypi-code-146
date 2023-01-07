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
RM_STYLE_MAPPING = {"SIZENL": u"非线性市值",
                    "MOMENTUM": u"动量",
                    "SIZE": u"市值",
                    "EARNYILD": u"盈利能力",
                    "LIQUIDTY": u"流动性",
                    "GROWTH": u"成长性",
                    "LEVERAGE": u"杠杆率",
                    "RESVOL": u"波动率",
                    "BTOP": u"价值",
                    "specific_return": u"特殊性成分",
                    "specific_risk": u"特殊性成分",
                    "BETA": u"beta",
                    "INDUSTRY": u"行业",
                    "COUNTRY": u"国家", }

RISK_INDUSTRY_MAP = {
    'dy_cne5_old': 'sw14',
    'dy_cne5_new': 'sw21'
}
INDUSTRY_VERSION_MAP = {
    'sw14':['AERODEF', 'AgriForest', 'Auto', 'BETA', 'BTOP', 'Bank',
            'BuildDeco', 'CHEM', 'CONMAT', 'COUNTRY', 'CommeTrade',
            'Computer', 'Conglomerates', 'EARNYILD', 'ELECEQP',
            'Electronics', 'FoodBever', 'GROWTH', 'Health', 'HouseApp',
            'IronSteel', 'LEVERAGE', 'LIQUIDTY', 'LeiService', 'LightIndus',
            'MOMENTUM', 'MachiEquip', 'Media', 'Mining', 'NonBankFinan',
            'NonFerMetal', 'RESVOL', 'RealEstate', 'SIZE', 'SIZENL',
            'Telecom', 'Textile', 'Transportation', 'Utilities'],
    'sw21':['Agriculture', 'Automobiles', 'BETA', 'BTOP', 'Banks', 'BasicChemicals', 'BeautyCare',
            'BuildMater', 'Chemicals', 'Coal', 'COUNTRY', 'Commerce',
            'Computers', 'Conglomerates', 'ConstrDecor', 'Defense', 'EARNYILD',
            'ElectricalEquip', 'Electronics', 'EnvironProtect', 'FoodBeverages', 'GROWTH', 'HealthCare', 'HomeAppliances',
            'LEVERAGE', 'LIQUIDTY', 'Leisure', 'LightIndustry',
            'MOMENTUM', 'MachineEquip', 'Media', 'Mining', 'NonbankFinan',
            'NonferrousMetals', 'Petroleum', 'PowerEquip', 'RESVOL', 'RealEstate', 'RetailTrade', 'SIZE', 'SIZENL',
            'SocialServices', 'Steel', 'Telecoms', 'TextileGarment', 'TextileApparel', 'Transportation', 'Utilities']
}

INDUSTRY_SW14_TO_21 = {
    'AgriForest': 'Agriculture',
    'Auto': 'Automobiles',
    'Bank': 'Banks',
    'BuildDeco': 'ConstrDecor',
    'CHEM': 'Chemicals',
    'CommeTrade': 'Commerce',
    'Computer': 'Computers',
    'CONMAT': 'BuildMater',
    'AERODEF': 'Defense',
    'ELECEQP': 'ElectricalEquip',
    'FoodBever': 'FoodBeverages',
    'Health': 'HealthCare',
    'HouseApp': 'HomeAppliances',
    'LeiService': 'Leisure',
    'LightIndus': 'LightIndustry',
    'MachiEquip': 'MachineEquip',
    'NonFerMetal': 'NonferrousMetals',
    'NonBankFinan': 'NonbankFinan',
    'IronSteel': 'Steel',
    'Telecom': 'Telecoms',
    'Textile': 'TextileGarment'
}