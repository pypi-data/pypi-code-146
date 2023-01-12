# encoding: utf-8
"""
@project: djangoModel->j_valuation
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 计价服务类
@created_time: 2022/10/13 16:58
"""
import re


# 计算器基类
class JBaseExpression:
    __result = None  # 结果
    __expression = None
    fun_type = ""

    # 获取所有子类
    @staticmethod
    def get_child_info():
        try:
            return {getattr(i, "name"): i for i in JBaseExpression.__subclasses__() if not getattr(i, "name", None) is None}, None
        except AttributeError:
            return {}, "扩展类name属性可以重复"

    # 解析变量
    @staticmethod
    def parse_variables(expression_string, input_dict):
        if expression_string is None:
            return "0"
        # 变量解析替换
        this_cell_value_match = re.compile("{{.*?}}").findall(str(expression_string))
        # 得到变量解析的键值对
        parsed_variable_map = {}
        for i in this_cell_value_match:
            parsed_variable_map.update({i: input_dict.get(i.replace("{{", "").replace("}}", ""), "0")})

        # 比那辆键值对替换
        for k, v in parsed_variable_map.items():
            expression_string = expression_string.replace(k, str(v) if v else "0")
        return expression_string, parsed_variable_map
        # 解析括号，成对解析

    @staticmethod
    def parsed_brackets(expression, need_list=False):
        twain_index_map = {}
        twain_index_list = []
        forward_index_list = []
        for char, index in zip(expression, range(len(expression))):
            if char == "(":
                forward_index_list.append(index)
            if char == ")":
                forward_bracket = forward_index_list.pop(-1)
                twain_index_map[forward_bracket] = (forward_bracket, index)
                twain_index_list.append((forward_bracket, index))
        return twain_index_list if need_list else twain_index_map

    # 检测是否可直接解析的公式，是否存在公式。
    def has_expression(self, expression_string):
        child_class, err = self.get_child_info()
        fun_patt = ""
        for name, instance in child_class.items():
            if not name:
                continue
            fun_patt = "(" + name + ")" if fun_patt == "" else fun_patt + "|" + "(" + name + ")"
        fun_patt = "(" + fun_patt + ")"

        return True if re.search(fun_patt, expression_string) else False

    # 解析公式
    def parse_expression_new(self, expression_string):
        child_class, err = self.get_child_info()
        # 公式匹配
        fun_patt = ""
        for name, instance in child_class.items():
            fun_patt = "(" + name + ")" if fun_patt == "" else fun_patt + "|" + "(" + name + ")"
        fun_patt = "(" + fun_patt + ")" + "?\([^\(]*?\)"
        match_string = re.search(fun_patt, expression_string)
        if not match_string:
            return None

        # 执行公式
        match_string = match_string.group()
        for name, instance in child_class.items():
            match_res = re.search(instance.patt, match_string)
            if match_res and match_res.group() == match_string:
                result = instance().process(match_string)
                expression_string = expression_string.replace(match_string, str(result))
                # print("expression_string:", expression_string, "result:", result, "name:", name)
                break

        # 递归解析
        if re.search("\([^\(]*?\)", expression_string):
            result = self.parse_expression_new(expression_string)
            expression_string = result if result else expression_string
        return expression_string

    # 解析公式 复杂度比较高 有优化的空间
    def parse_expression(self, expression_string):
        # 解析括号和函数
        brackets_twain_map = self.parsed_brackets(expression_string)

        # 解析函数
        replace_list = []
        child_class, err = self.get_child_info()
        for name, instance in child_class.items():
            if not name:
                continue
            for r in re.finditer(name, expression_string):
                name_start, name_end = r.span()
                bracket_start, bracket_end = brackets_twain_map[name_end]

                full_fun_string = expression_string[name_start:bracket_end + 1]
                fun_inner_string = expression_string[bracket_start:bracket_end + 1]
                # print("full_fun_string:", full_fun_string, "fun_inner_string:", fun_inner_string, "self.has_expression(fun_inner_string):", self.has_expression(fun_inner_string))
                if not self.has_expression(fun_inner_string):
                    result = instance().process(full_fun_string)
                    replace_list.append((full_fun_string, result))

        # 结果替换
        for full_fun_string, result in replace_list:
            expression_string = expression_string.replace(full_fun_string, str(result))

        if self.has_expression(expression_string):
            expression_string = self.parse_expression(expression_string)
        return expression_string


# 计算器 对外暴露的类
class JExpression(JBaseExpression):

    def process(self, expression_string):
        # 数据预处理
        if expression_string is None:
            return "", None
        if not len(re.findall("\(", expression_string)) == len(re.findall("\)", expression_string)):
            return None, "语法错误，括号应该成对存在"
        child_class, err = self.get_child_info()
        if err:
            return None, err
        expression_string = expression_string.upper().replace(" ", "").replace("=", "==").replace(">==", ">=").replace("<==", "<=")  # 公式字符串预处理

        # 解析公式
        # expression_string = self.parse_expression_new(expression_string)
        expression_string = self.parse_expression(expression_string)

        result = CalculateExpression().process(expression_string)
        return result, None


# ================================= 公式封装类 =======================================
#  基础计算
class CalculateExpression(JBaseExpression):
    name = ""
    patt = "\([^\(]*?\)"

    def process(self, expression_string):
        try:
            return eval(expression_string)  # 加加减乘除
        except ZeroDivisionError:
            return 0  # 0/n  的情况
        except Exception as e:
            # print("CalculateExpression e", str(e))
            return expression_string


# 布尔值判断、三元运算
class IFExpression(JBaseExpression):
    name = "IF"
    patt = "IF\([^\(]*?\)"

    def process(self, expression, *args, ):
        bool_expression, yes_expression, no_expression = expression.replace(IFExpression.name, "").replace("(", "").replace(")", "").split(",")
        if CalculateExpression().process(bool_expression):
            return yes_expression
        else:
            return no_expression


# 求和计算、（多参数在服务中获取）
class SUMExpression(JBaseExpression):
    name = "SUM"
    patt = "SUM\([^\(]*?\)"  # SUM(a,b,c) == a+b+c

    def process(self, expression):
        try:
            args = expression.replace(self.name, "").replace("(", "").replace(")", "").split(",")
            result = 0
            for i in args:
                result += int(i)
            return result
        except Exception as e:
            return 0
