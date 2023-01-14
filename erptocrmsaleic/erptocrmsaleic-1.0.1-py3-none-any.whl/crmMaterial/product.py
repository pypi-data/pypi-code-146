import datetime

import requests
from pyrda.dbms.rds import RdClient

url = 'http://123.207.201.140:88/crm/crmapi/api_crmoperation.php'


class Product():
    def __init__(self):
        # 明确继承自上一级
        # 也可以不写默认继承
        self.token_china = 'B405719A-772E-4DF9-A560-C24948A3A5D6'
        self.app3 = RdClient(token=self.token_china)
        self.token_erp = "4D181CAB-4CE3-47A3-8F2B-8AB11BB6A227"
        self.app2 = RdClient(token=self.token_erp)
    def get_material(self):
        sql = 'select * from RDS_CRM_SRC_MaterialDetail where FIsdo =0'
        res = self.app3.select(sql)
        return res

    def log_crm(self):
        log_url = 'http://123.207.201.140:88/crm/crmapi/apiKey.php'
        parm = {'authen_code': '3BBf3C56'}
        log_res = requests.post(log_url, data=parm)
        result = log_res.json()
        self.data_template(result['key'], result['token'])
        return result

    def inser_logging(self, FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                      FCompanyName='CP'):
        app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
        sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + str(
            FMessage) + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
            FIsdo) + ")"
        data = app3.insert(sql)
        return data

    def query_material(self, key, token):
        query_url = 'http://123.207.201.140:88/ldcrm/crmapi/crmoperation.php'
        model = {
            "module": "Products",
            "func": "getList",
            "apikey": key,
            "token": token,
            "username": "admin",
            "pagesize": "10",
            "pagenum": "1",
            "searchtext": []
        }
        res = requests.post(query_url, model)
        return res

    def data_template(self, key, token):
        datas = self.get_material()
        for d in datas:
            model = {
                "module": "Products",
                "func": "newApiSave",
                "apikey": key,
                "token": token,
                "username": "admin",
                "dataList": [
                    {
                        'product_no': d['FNumber'],  # 1 产品编号
                        'productname': d['FNAME'],  # 2 产品名称
                        'productcategory': self.get_name('fname', 'V_BAS_ASSISTANTDATAENTRY_L', 'fid',
                                                         d['F_SZSP_ASSISTANT']),  # 3 产品类别
                        'productsheet': d['FSPECIFICATION'],  # 4 规格型号
                        'cf_4394': d['FMNEMONICCODE'],  # 5 助记码
                        'cf_4395': d['FOldNumber'],  # 6 旧物料编码
                        'cf_4396': d['FDescription'],  # 7 描述
                        'cf_4397': d['FMATERIALGROUP'],  # 8 物料分组
                        # 'cf_4398': d['FERPCLSID'],  # 9 物料属性
                        'cf_4399': d['FCONFIGTYPE'],  # 10 配置生产
                        'cf_4400': d['FFEATUREITEM'],  # 11 特征件子项
                        'cf_4401': d['FSUITE'],  # 12 套件
                        'usageunit': self.get_name('FNAME','rds_vw_unit','FUNITID',d['FPURCHASEPRICEUNITID']),  # 13 计量单位   有问题
                        'discontinued': 0,  # 14 禁用,checkbox
                        'cf_4402': d['FFORBIDREASON'],  # 15 禁用原因
                        'cf_4403': d['FISPURCHASE'],  # 16 允许采购
                        'cf_4404': d['FISSALE'],  # 17 允许销售
                        # 'cf_4405': d['FISINVENTORY'],  # 18 允许库存
                        'cf_4406': d['FISPRODUCE'],  # 19 允许生产
                        'cf_4407': d['FISSUBCONTRACT'],  # 20 允许委外
                        'cf_4408': d['FISASSET'],  # 21 允许资产
                        'cf_4409': 0,  # 22 是否灭菌
                        'cf_4410': "13",  # 23 默认税率
                        'cf_4411': d['FCATEGORYID'],  # 24 存货类别
                        'cf_4412': d['FTAXTYPE'],  # 25 税分类
                        'cf_4413': d['FCOSTPRICERATE'],  # 26 结算成本价加减价比例(%)
                        'procostprice': '',  # 27 参考成本价(RMB)
                        'cf_4414': d['FGROSSWEIGHT'],  # 28 毛重
                        'cf_4415': d['FNETWEIGHT'],  # 29 净重
                        'cf_4416': d['FWEIGHTUNITID'],  # 30 重量单位
                        'cf_4417': d['FLENGTH'],  # 31 长
                        'cf_4418': d['FWIDTH'],  # 32 宽
                        'cf_4419': d['FHEIGHT'],  # 33 高
                        'cf_4420': d['FVOLUME'],  # 34 体积
                        'cf_4421': d['FVOLUMEUNITID'],  # 35 尺寸单位
                        'cf_4506': d['FDOCUMENTSTATUS'],  # 36 数据状态
                        'cf_4507': d['FFORBIDSTATUS'],  # 37 禁用状态
                        'cf_4508': d['FREFSTATUS'],  # 38 已使用
                        'cf_4509': d['FSTOREUNITID'],  # 39 库存单位
                        'cf_4510': d['FAUXUNITID'],  # 40 辅助单位
                        'cf_4511': d['FUNITCONVERTDIR'],  # 41 换算方向
                        'cf_4512': d['FSTOCKID'],  # 42 仓库
                        'cf_4513': d['FSTOCKPLACEID'],  # 43 仓位
                        'cf_4514': d['FBOXSTANDARDQTY'],  # 44 单箱标准数量
                        'cf_4515': d['FISLOCKSTOCK'],  # 45 可锁库
                        'cf_4516': d['FISCYCLECOUNTING'],  # 46 启用周期盘点
                        'cf_4517': d['FCOUNTDAY'],  # 47 盘点周期
                        'cf_4518': d['FISMUSTCOUNTING'],  # 48 必盘
                        'cf_4519': d['FSTOREURNUM'],  # 49 库存单位换算率分子
                        'cf_4520': d['FSTOREURNOM'],  # 50 库存单位换算率分母
                        'cf_4521': d['FISBATCHMANAGE'],  # 51 启用批号管理
                        'cf_4522': d['FBATCHRULEID'],  # 52 批号编码规则
                        'cf_4523': d['FISKFPERIOD'],  # 53 启用保质期管理
                        'cf_4524': d['FISEXPPARTOFLOT'],  # 54 批号附属信息
                        'cf_4525': d['FEXPUNIT'],  # 55 保质期单位,数字
                        'cf_4526': d['FEXPPERIOD'],  # 56 保质期,数字
                        # 'cf_4527': d['FONLINELIFE'],  # 57 在架保寿期
                        'cf_4528': d['FREFCOST'],  # 58 参考成本
                        'cf_4529': '',  # 59 成本单位
                        'cf_4530': d['FCURRENCYID'],  # 60 币别
                        'cf_4531': d['FISENABLEMINSTOCK'],  # 61 最小库存预警
                        'cf_4532': d['FISENABLESAFESTOCK'],  # 62 安全库存预警
                        'cf_4533': d['FISENABLEMAXSTOCK'],  # 63 最大库存预警
                        'cf_4534': d['FISENABLEREORDER'],  # 64 再订货点预警
                        'cf_4535': d['FMINSTOCK'],  # 65 最小库存
                        'qtyearly': d['FSafeStock'],  # 66 安全库存
                        'cf_4536': d['FREORDERGOOD'],  # 67 再订货点
                        'cf_4537': d['FECONREORDERQTY'],  # 68 经济订货批量
                        'cf_4538': d['FMAXSTOCK'],  # 69 最大库存
                        'cf_4539': d['FSALEUNITID'],  # 70 销售单位
                        'cf_4540': d['FSALEPRICEUNITID'],  # 71 销售计价单位
                        'cf_4541': d['FORDERQTY'],  # 72 起订量
                        'cf_4542': d['FOUTLMTUNIT'],  # 73 超发控制单位
                        'cf_4543': d['FOUTSTOCKLMTH'],  # 74 超发上限(%)
                        'cf_4544': d['FOUTSTOCKLMTL'],  # 75 超发下限(%)
                        'cf_4545': d['FAGENTSALREDUCERATE'],  # 76 代理销售减价比例(%)
                        'cf_4546': d['FTAXCATEGORYCODEID'],  # 77 税收分类编码
                        'cf_4547': d['FISTAXENJOY'],  # 78 享受税收优惠政策,checkbox
                        'cf_4548': d['FTAXDISCOUNTSTYPE'],  # 79 税收优惠政策类型
                        'cf_4549': d['FSALGROUP'],  # 80 销售分组
                        'cf_4550': d['FISATPCHECK'],  # 81 ATP检查
                        'cf_4551': d['FISRETURN'],  # 82 允许退货
                        'cf_4552': d['FISRETURNPART'],  # 83 部件可退
                        'cf_4553': d['FUNVALIDATEEXPQTY'],  # 84 不参与可发量统计
                        'cf_4554': d['F_SZSP_DECIMAL2'],  # 85 管理成本
                        'cf_4555': d['FALLOWPUBLISH'],  # 86 允许发布到订货平台
                        'cf_4556': d['FISAFTERSALE'],  # 87 启用售后服务
                        'cf_4557': d['FISPRODUCTFILES'],  # 88 生成产品档案
                        'cf_4558': d['FISWARRANTED'],  # 89 是否保修
                        'cf_4559': d['FWARRANTY'],  # 90 保修期
                        'cf_4560': d['FWARRANTYUNITID'],  # 91 保修期单位
                        'cf_4561': d['FCHECKINCOMING'],  # 92 来料检验
                        'cf_4562': d['FCHECKPRODUCT'],  # 93 产品检验
                        'cf_4563': d['FISFIRSTINSPECT'],  # 94 产品首检
                        'cf_4564': d['FCHECKSTOCK'],  # 95 库存检验
                        'cf_4565': d['FCHECKRETURN'],  # 96 退货检验
                        'cf_4566': d['FCHECKDELIVERY'],  # 97 发货检验
                        'cf_4567': d['FCHECKOTHER'],  # 98 其他检验
                        'cf_4568': d['FCHECKENTRUSTED'],  # 99 受托材料检验
                        'cf_4569': d['FCHECKRETURNMTRL'],  # 100 生产退料检验
                        'cf_4570': d['FENABLECYCLISTQCSTK'],  # 101 启用库存周期复检
                        'cf_4571': d['FSTOCKCYCLE'],  # 102 复检周期(天)
                        'cf_4572': d['FENABLECYCLISTQCSTKEW'],  # 103 启用库存周期复检提醒
                        'cf_4573': d['FEWLEADDAY'],  # 104 提醒提前期(天)
                        'cf_4574': d['FINCSAMPSCHEMEID'],  # 105 抽样方案
                        'cf_4575': d['FINCQCSCHEMEID'],  # 106 质检方案
                        'cf_4576': d['FINSPECTGROUPID'],  # 107 质检组
                        'cf_4577': d['FINSPECTORID'],  # 108 质检员
                        'cf_4578': d['FPURCHASEUNITID'],  # 109 采购单位
                        'cf_4579': d['FPURCHASEPRICEUNITID'],  # 110 采购计价单位
                        'cf_4580': d['FPURCHASEORGID'],  # 111 采购组织
                        'cf_4581': d['FPURCHASERID'],  # 112 采购员
                        'cf_4582': d['FDEFAULTVENDORID'],  # 113 默认供应商
                        'cf_4583': d['FCHARGEID'],  # 114 费用项目
                        'cf_4584': d['FPOBILLTYPEID'],  # 115 采购类型
                        'cf_4585': d['FISQUOTA'],  # 116 配额管理
                        'cf_4586': d['FQUOTATYPE'],  # 117 配额方式
                        'cf_4587': d['FMINSPLITQTY'],  # 118 最小拆分数量
                        'cf_4588': d['FISVMIBUSINESS'],  # 119 是否VMI业务
                        'cf_4589': d['FISPR'],  # 120 需要请购
                        'cf_4590': d['FISSOURCECONTROL'],  # 121 货源控制
                        'cf_4591': d['FRECEIVEADVANCEDAYS'],  # 122 收货提前天数
                        'cf_4592': d['FRECEIVEMAXSCALE'],  # 123 收货上限比例%
                        'cf_4593': d['FRECEIVEMINSCALE'],  # 124 收货下限比例%
                        'cf_4594': d['FRECEIVEDELAYDAYS'],  # 125 收货延迟天数
                        'cf_4595': d['FDEFBARCODERULEID'],  # 126 默认条码规则
                        'cf_4596': d['FMinPackCount'],  # 127 最小包装数
                        'cf_4597': d['FPRINTCOUNT'],  # 128 重复打印数
                        # 'cf_4598': d['F_SZSP_CheckBox'],  # 129 启用条码管理，checkbox
                        'cf_4599': d['FSUBCONUNITID'],  # 130 委外单位
                        'cf_4600': d['FSUBCONPRICEUNITID'],  # 131 委外计价单位
                        'cf_4601': d['FSUBBILLTYPE'],  # 132 委外类型
                        'cf_4602': d['FAGENTPURPLUSRATE'],  # 133 代理采购加成比例%
                        'cf_4603': d['FWORKSHOPID'],  # 134 生产车间
                        'cf_4604': d['FPRODUCEUNITID'],  # 135 生产单位
                        'cf_4605': d['FFinishReceiptOverRate'],  # 136 入库超收比例%
                        'cf_4606': d['FFinishReceiptShortRate'],  # 137 入库欠收比例%
                        'cf_4607': d['FPRODUCEBILLTYPE'],  # 138 生产类型
                        'cf_4608': d['FORGTRUSTBILLTYPE'],  # 139 组织间受托类型
                        'cf_4609': d['FISPRODUCTLINE'],  # 140 生产线生产,logical
                        'cf_4610': d['FISSNCARRYTOPARENT'],  # 141 序列号携带到父项,logical
                        'cf_4611': d['FBACKFLUSHTYPE'],  # 142 倒冲数量
                        'cf_4612': d['FBOMUNITID'],  # 143 子项单位
                        'cf_4613': d['FCONSUMVOLATITITY'],  # 144 消耗波动%
                        'cf_4614': d['FLOSSPERCENT'],  # 145 变动损耗率%
                        'cf_4615': d['FFIXLOSS'],  # 146 固定损耗%
                        'cf_4616': d['FISMAINPRD'],  # 147 可为主产品，logical
                        'cf_4617': d['FISCOBY'],  # 148 可为联副产品,logical
                        'cf_4618': d['FISECN'],  # 149 启用ECN,logical
                        'cf_4619': d['FISSUETYPE'],  # 150 发料方式
                        'cf_4620': d['FBKFLTIME'],  # 151 倒冲时机
                        'cf_4621': d['FPICKSTOCKID'],  # 152 发料仓库
                        'cf_4622': d['FPICKBINID'],  # 153 发料仓位
                        'cf_4623': d['FOVERCONTROLMODE'],  # 154 超发控制方式
                        'cf_4624': d['FMINISSUEQTY'],  # 155 最小发料批量
                        'cf_4625': d['FISMINISSUEQTY'],  # 156 领料考虑最小发料批量,logical
                        'cf_4626': d['FISKITTING'],  # 157 是否关键件
                        'cf_4627': d['FISCOMPLETESET'],  # 158 是否齐套件
                        'cf_4628': d['FDEFAULTROUTING'],  # 159 默认工艺路线
                        'cf_4629': d['FPERUNITSTANDHOUR'],  # 160 标准工时
                        'cf_4630': d['FSTDLABORPREPARETIME'],  # 161 标准人员准备工时
                        'cf_4631': d['FSTDLABORPROCESSTIME'],  # 162 标准人员实作工时
                        'cf_4632': d['FSTDMACHINEPREPARETIME'],  # 163 标准机器准备工时
                        'cf_4633': d['FSTDMACHINEPROCESSTIME'],  # 164 标准机器实作工时
                        'cf_4634': d['FMDLID'],  # 165 产品模型
                        'cf_4635': d['FMDLMATERIALID'],  # 166 模型物料
                        'cf_4636': d['FPlanningStrategy'],  # 167 计划策略
                        'cf_4637': d['FMFGPOLICYID'],  # 168 制造策略
                        'cf_4638': d['FOrderPolicy'],  # 169 订货策略
                        'cf_4639': d['FPLANWORKSHOP'],  # 170 计划区
                        'cf_4640': d['FFixLeadTime'],  # 171 固定提前期
                        'cf_4641': d['FVarLeadTime'],  # 172 变动提前期
                        'cf_4642': d['FCHECKLEADTIME'],  # 173 检验提前期
                        'cf_4643': d['FACCULEADTIME'],  # 174 累计提前期
                        'cf_4644': d['FOrderIntervalTimeType'],  # 175 订货间隔期单位
                        'cf_4645': d['FOrderIntervalTime'],  # 176 订货间隔期
                        'cf_4646': d['FMaxPOQty'],  # 177 最大订货量
                        'cf_4647': d['FMinPOQty'],  # 178 最小订货量
                        'cf_4648': d['FIncreaseQty'],  # 179 最小包装量
                        'cf_4649': d['FEOQ'],  # 180 固定/经济批量
                        'cf_4650': d['FVarLeadTimeLotSize'],  # 181 变动提前期批量
                        'cf_4651': d['FDAILYOUTQTY'],  # 182 日产量
                        'cf_4652': d['FPLANBATCHSPLITQTY'],  # 183 拆分批量
                        'cf_4653': d['FPLANINTERVALSDAYS'],  # 184 批量拆分间隔天数
                        'cf_4654': d['FREQUESTTIMEZONE'],  # 185 需求时界
                        'cf_4655': d['FPLANTIMEZONE'],  # 186 计划时界
                        'cf_4656': d['FPLANGROUPID'],  # 187 计划组
                        'cf_4657': d['FPLANERID'],  # 188 计划员
                        'cf_4658': d['FPLANIDENT'],  # 189 计划标识
                        'cf_4659': d['FDSMATCHBYLOT'],  # 190 按批号匹配供需,logical
                        'cf_4660': d['FRESERVETYPE'],  # 191 预留类型
                        'cf_4661': d['FSafeStock'],  # 192 安全库存
                        'cf_4662': d['FATOSCHEMEID'],  # 193 ATO预测冲销方案
                        'cf_4663': d['FPRODUCTLINE'],  # 194 产品系列
                        'cf_4664': d['FWRITEOFFQTY'],  # 195 冲销数量
                        'cf_4665': d['FCANLEADDAYS'],  # 196 允许提前天数
                        'cf_4666': d['FLEADEXTENDDAY'],  # 197 提前宽限期
                        'cf_4667': d['FALLOWPARTAHEAD'],  # 198 预计入库允许部分提前
                        'cf_4668': d['FDELAYEXTENDDAY'],  # 199 允许延后天数
                        'cf_4669': d['FDELAYEXTENDDAY'],  # 200 延后宽限期
                        'cf_4670': d['FALLOWPARTDELAY'],  # 201 预计入库允许部分延后
                        'cf_4671': d['FPLANOFFSETTIMETYPE'],  # 202 时间单位
                        'cf_4672': d['FPLANOFFSETTIME'],  # 203 偏置时间
                        'cf_4673': d['FSUPPLYSOURCEID'],  # 204 供应来源
                        'cf_4674': d['FTIMEFACTORID'],  # 205 时间紧迫系数
                        'cf_4675': d['FQTYFACTORID'],  # 206 数量负荷系数
                        'cf_4676': d['FPROSCHETRACKID'],  # 207 订单进度分组
                        'cf_4773': d['FPURCHASEGROUPID'],  # 208 采购组
                        'cf_4774': d['FISRETURNMATERIAL'],  # 209 允许退料
                    }
                ]
            }
            log_res = requests.post(url, json=model)
            res = log_res.json()
            if res['code'] != '200':
                self.inser_logging('物料', d['FNumber'], res['msg'], 2)
            else:
                self.inser_logging('物料', d['FNumber'], res['msg'][0]['status'], 1)
            sql = "update a set a.FIsdo=1 from RDS_CRM_SRC_MaterialDetail a where FNumber = '{}'".format(d['FNumber'])
            self.app3.update(sql)
            print(res)

    def get_name(self, word, table, parm, value):
        sql = f"select {word} from {table} where {parm} = '{value}'"
        d = self.app2.select(sql)
        if d:
            return d[0][word]
        else:
            return ""


if __name__ == '__main__':
    p = Product()
    print(p.log_crm())
