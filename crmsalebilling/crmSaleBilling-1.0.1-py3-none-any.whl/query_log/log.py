from pyrda.dbms.rds import RdClient


def run_crm_log(FProgramName=None, FNumber=None, FIsdo=None, FOccurrenceTime_min=None, FOccurrenceTime_max=None,
                FCompanyName=None):
    token_erp = '9B6F803F-9D37-41A2-BDA0-70A7179AF0F3'
    app3 = RdClient(token=token_erp)
    sql = "select FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName from RDS_CRM_Log where "
    if FCompanyName:
        sql = sql + "FCompanyName = '" + str(FCompanyName) + "'"
    else:
        sql = sql + "FCompanyName = '" + "赛普'"
    if FProgramName:
        sql = sql + " and " + "FProgramName like '%" + str(FProgramName) + "%'"
    if FNumber:
        sql = sql + " and " + "FNumber = '" + str(FNumber) + "'"
    if FOccurrenceTime_min:
        sql = sql + " and " + "FOccurrenceTime BETWEEN '" + str(FOccurrenceTime_min) + "' and '" + str(
            FOccurrenceTime_max) + "'"
    if FIsdo:
        sql = sql + " and " + "FIsdo = " + str(FIsdo)

    res = app3.select(sql)
    return res


def run_ecs_log(FProgramName=None, FNumber=None, FIsdo=None, FOccurrenceTime_min=None, FOccurrenceTime_max=None,
                FCompanyName=None):
    token_erp = '9B6F803F-9D37-41A2-BDA0-70A7179AF0F3'
    app3 = RdClient(token=token_erp)
    sql = "select FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName from RDS_ECS_Log where "
    if FCompanyName:
        sql = sql + "FCompanyName = '" + str(FCompanyName) + "'"
    else:
        sql = sql + "FCompanyName = '" + "赛普'"
    if FProgramName:
        sql = sql + " and " + "FProgramName like '%" + str(FProgramName) + "%'"
    if FNumber:
        sql = sql + " and " + "FNumber = '" + str(FNumber) + "'"
    if FOccurrenceTime_min:
        sql = sql + " and " + "FOccurrenceTime BETWEEN '" + str(FOccurrenceTime_min) + "' and '" + str(
            FOccurrenceTime_max) + "'"
    if FIsdo:
        sql = sql + " and " + "FIsdo = " + str(FIsdo)

    res = app3.select(sql)
    return res

