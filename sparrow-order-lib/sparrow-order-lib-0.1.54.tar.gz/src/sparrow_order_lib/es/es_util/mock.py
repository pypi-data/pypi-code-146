from abc import ABC


class ESMockDSLInterface(ABC):
    ''' 抽象接口类, 所有需要对外提供 dsl 的组件都应继承该类 '''

    def get_dsl(self):
        ''' 子类必须重写该方法 '''
        raise NotImplementedError
