from rdassemblydis import operation as db
from rdassemblydis import metadata as mt
from rdassemblydis import EcsInterface as ae

def data_splicing(app2,app3,FNumber):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给 FSaleOrderEntry
    :param data:
    :return:
    '''

    data=db.getSubEntityCode(app3,FNumber)

    list=[]

    for i in data:

        list.append(mt.json_model(app2,i))

    return list


def writeSRCA(startDate, endDate, app3):
    '''
    将ECS数据取过来插入SRC表中
    :param startDate:
    :param endDate:
    :return:
    '''

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = ae.viewPage(url, 1, 1000, "ge", "le", "v_processing_storage", startDate, endDate, "Fdate")

    for i in range(1, page + 1):
        df = ae.ECS_post_info2(url, i, 1000, "ge", "le", "v_processing_storage", startDate, endDate, "Fdate")

        df=df.fillna("")

        db.insert_assembly_order(app3, df)

    pass

def writeSRCD(startDate, endDate, app3):
    '''
    将ECS数据取过来插入SRC表中
    :param startDate:
    :param endDate:
    :return:
    '''

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = ae.viewPage(url, 1, 1000, "ge", "le", "v_disassemble_discharge", startDate, endDate, "Fdate")

    for i in range(1, page + 1):
        df = ae.ECS_post_info2(url, i, 1000, "ge", "le", "v_disassemble_discharge", startDate, endDate, "Fdate")

        df = df.fillna("")

        db.insert_remove_order(app3, df)

    pass