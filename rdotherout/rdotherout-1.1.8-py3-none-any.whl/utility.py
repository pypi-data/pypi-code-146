from rdotherout import operation as db
def classification_process(app3,data):
    '''
    将编码进行去重，然后进行分类
    :param data:
    :return:
    '''

    res=fuz(app3,data)

    return res

def data_splicing(app2,data):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给
    :param data:
    :return:
    '''

    list=[]

    for i in data:
        if json_model(app2,i):

            list.append(json_model(app2,i))

        else:
            return []

    return list

def fuz(app3,codeList):
    '''
    通过编码分类，将分类好的数据装入列表
    :param app2:
    :param codeList:
    :return:
    '''

    singleList=[]

    for i in codeList:

        data=db.getClassfyData(app3,i)
        singleList.append(data)

    return singleList

def json_model(app2, model_data):

    try:

        if model_data['FPRDNUMBER']=='1' or db.code_conversion_org(app2,"rds_vw_material","F_SZSP_SKUNUMBER",model_data['FPRDNUMBER'],"104","FNUMBER"):

            model = {
                "FMaterialId": {
                    "FNumber": "7.1.000001" if model_data['FPRDNUMBER']=='1' else db.code_conversion_org(app2,"rds_vw_material","F_SZSP_SKUNUMBER",model_data['FPRDNUMBER'],"104","FNUMBER"),
                },
                "FQty": str(model_data['FNBASEUNITQTY']),
                "FStockId": {
                    "FNumber": "SK01"
                },
                "FLot": {
                    "FNumber": str(model_data['FLOT'])
                },
                "FOwnerTypeId": "BD_OwnerOrg",
                "FOwnerId": {
                    "FNumber": "104"
                },
                "FStockStatusId": {
                    "FNumber": "KCZT01_SYS"
                },
                "FKeeperTypeId": "BD_KeeperOrg",
                "FDistribution": False,
                "FKeeperId": {
                    "FNumber": "104"
                }
            }

            return model

        else:
            return {}

    except Exception as e:

        return {}
