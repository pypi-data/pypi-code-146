from rdotherinstock import operation as db
def classification_process(app3,data):
    '''
    将编码进行去重，然后进行分类
    :param data:
    :return:
    '''

    res=fuz(app3,data)

    return res


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


def data_splicing(app2,data):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给
    :param data:
    :return:
    '''

    list=[]

    for i in data:

        list.append(json_model(app2,i))

    return list

def json_model(app2, model_data):

    try:

        model = {
            "FMATERIALID": {
                "FNumber": "7.1.000001" if model_data['FGOODSID'] == '1' else db.code_conversion_org(app2,"rds_vw_material","F_SZSP_SKUNUMBER",model_data['FGOODSID'],                                                                                         "104", "FNUMBER")
            },
            # "FUnitID": {
            #     "FNumber": "01"
            # },
            "FSTOCKID": {
                "FNumber": "SK01"
            },
            "FSTOCKSTATUSID": {
                "FNumber": "KCZT01_SYS"
            },
            "FLOT": {
                "FNumber": str(model_data['FLOT'])
            },
            "FQty": str(model_data['FINSTOCKQTY']),
            # "FPRODUCEDATE": "2022-11-04 00:00:00",
            "FOWNERTYPEID": "BD_OwnerOrg",
            "FOWNERID": {
                "FNumber": "104"
            },
            "FKEEPERTYPEID": "BD_KeeperOrg",
            "FKEEPERID": {
                "FNumber": "104"
            }
        }

        return model

    except Exception as e:

        return {}
