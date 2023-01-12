from types import FunctionType
import marshal
import ipyparallel.serialize.codeutil  # noqa: F401
import inspect

check_commend = [
    "rm",
    "rm -rf",
    "mv",
    "-f",
    "-i",
    "-u",
    "-v",
    "-b",
    "echo",
    "cd",
    "cp",
    "scp",
    "chmod",
    "ls",
    "import os",
    "import subprocess",
    "import sys",
    "import asyncio",
    "!",
    "&",
    "--y",
    "sudo",
    "passwd",
    "getpass",
]


class LogicConverter:
    """
    상품 선택 로직 함수를 변환하거나 변환된 함수를 다시 재변환을 지원하는 클래스입니다.

    ## Example

    ```python
    def Handler(data = None):
        if data:
            if data['prod_info'][0]['bas_fee_amt'] < 50000:
                return [{"id": "prod_id"
                         , "name": "prod_nm"
                         , "type": "vas"
                         , "props": {"class": "sub"
                                     , "priority" : 'Y'
                                     , "fee_prod_id" : data['fee_prod_id']
                                     , "score" : data['y'][1]}}]
            else:
                return [{"id": "prod_id"
                         , "name": "prod_nm"
                         , "type": "vas"
                         , "props": {"class": "sub"
                                     , "priority" : 'N'
                                     , "fee_prod_id" : data['fee_prod_id']
                                     , "score" : data['y'][1]}}]

        else:
            return [{"id": "prod_id"
                     , "name": "prod_nm"
                     , "type": "vas"
                     , "props": {"class": None
                                 , "priority" : None
                                 , "fee_prod_id" : None
                                 , "score" : None}}]

    func_convert_value = ConvertVariables(user_defined_func = Handler).FunctionToConvert() #변환
    reconvert_value = ConvertVariables(user_defined_convert_logic = func_convert_value).ConvertToFunction() #재변환
    """

    def __init__(
        self,
        user_defined_func=None,
        user_converted_logic=None,
    ):
        if user_defined_func:
            assert hasattr(user_defined_func, "__call__") is True, "`user_defined_func`은 함수이어야 합니다."
            for i in check_commend:
                for j in inspect.getsource(user_defined_func).split("\n"):
                    assert i is not j, f"금지된 명령어 {i}가 {j}로 입력되었습니다."
        if user_converted_logic:
            assert isinstance(user_converted_logic, bytes), "`user_converted_logic`는 LogicConverter를 거쳐 반환된 타입이어야 합니다."

        self.user_defined_func = user_defined_func
        self.user_converted_logic = user_converted_logic

    def dummy_handler(self):
        return {"id": "id", "name": "name", "type": "type", "props": {}}, ""

    def FunctionToConvert(self):
        func_to_bytes = marshal.dumps(self.user_defined_func.__code__)
        return func_to_bytes

    def ConvertToFunction(self, name=None):
        if self.user_converted_logic:
            assert (
                hasattr(FunctionType(marshal.loads(self.user_converted_logic), globals={}), "__call__") is True
            ), "`user_converted_logic`의 변환 값은 함수이어야 합니다."
            bytes_to_function = FunctionType(marshal.loads(self.user_converted_logic), globals={}, name=name)
            return bytes_to_function
        else:
            return self.dummy_handler()
