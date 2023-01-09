'''
ES 查询组件异常
'''


class ESUtilBaseException(BaseException):
    ''' 基础错误类 '''
    error_desc = ""

    def __init__(self, message="", error_desc=""):
        self.message = message

        if not error_desc:
            error_desc = self.__class__.error_desc
        if not error_desc:
            self.error_desc = self.__class__.__name__

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}."


class ESUtilESClusterException(ESUtilBaseException):
    ''' 集群异常: 集群不可达或集群状态异常 '''
    error_desc = "集群异常"


class ESUtilInvalidDocType(ESUtilBaseException):
    ''' 无效的文档类型 '''
    error_desc = "无效的文档类型"


class ESUtilConfException(ESUtilBaseException):
    ''' 配置错误, 当注册某个文档类型时, 发现配置不正确 '''
    error_desc = "无效的配置"


class ESUtilParamException(BaseException):
    ''' ES 查询时 参数错误, 这可能是由在配置中无法找到该查询关键字有关 '''
    error_desc = "参数错误"


class ESUtilValueException(BaseException):
    ''' ValueError '''
    pass


class ESUtilTypeException(BaseException):
    ''' TypeError '''
    pass
