'''
查询入参
'''


class InQueryParam(object):
    ''' 查询入参 '''

    def __init__(self, in_param_key, in_param_value):
        self.__in_param_key = in_param_key
        self.__in_param_value = in_param_value

    @property
    def in_param_key(self):
        return self.__in_param_key

    @property
    def in_param_value(self):
        return self.__in_param_value
