from typing import Any

from airflow.models import Variable
from airflow.models import BaseOperator


"""
    操控Variable的操作组件，可以继承后实现2个get方法。
    如果设置了default_value，没找到会自动创建。
    如果设置了change_value，会将变量修改给定值。
"""
class VariableOperator(BaseOperator):

    def __init__(self, variable_name, default_value=None, change_value=None, *args, **kwargs):
        super(VariableOperator, self).__init__(*args, **kwargs)
        self.variable_name = variable_name
        self.default_value = default_value
        self.change_value = change_value

    def execute(self, context):
        try:
            _vr = Variable.get(self.variable_name)
        except KeyError:
            _vr = None
        if _vr is None:
            self.log.info(f"获取不到 [{self.variable_name}]，判断是否需要自动添加...")
            if self.default_value is not None:
                Variable.set(self.variable_name, self.default_value)
                self.log.info(f"添加成功！")
            elif self.get_default() is not None:
                Variable.set(self.variable_name, self.get_default())
                self.log.info(f"添加成功！")
            else:
                self.log.info(f"没有找到默认值，不需要添加！")
                return

        _vr = Variable.get(self.variable_name)
        self.log.info(f"获取 [{self.variable_name}] 值为：[{_vr}]")
        if self.change_value is not None:
            Variable.set(self.variable_name, self.change_value)
        elif self.get_change_value(_vr) is not None:
            Variable.set(self.variable_name, self.get_change_value(_vr))
        return

    def get_default(self) -> Any:
        pass

    def get_change_value(self, origin) -> Any:
        pass
