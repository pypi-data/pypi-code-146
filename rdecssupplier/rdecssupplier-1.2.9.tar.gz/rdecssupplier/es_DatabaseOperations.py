def insertData(app2, sql):
    '''
    将从OA接口里面获得的数据插入到对应的数据表中
    :param app2: 执行sql语句对象
    :param sql:  sql语句
    :return:
    '''
    app2.insert(sql)


def getData(app2, sql):
    '''
    从数据表中获得数据
    :param app2: 执行sql语句对象
    :param sql: sql语句
    :return: 返回查询到的数据
    '''
    result = app2.select(sql)

    return result

def insertLog(app2,FProgramName,FNumber,Message,FIsdo,cp='赛普'):
    '''
    异常数据日志
    :param app2:
    :param FNumber:
    :param Message:
    :return:
    '''

    sql="insert into RDS_ECS_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('"+FProgramName+"','"+FNumber+"','"+Message+"',getdate(),'"+cp+"','"+FIsdo+"')"

    app2.insert(sql)
