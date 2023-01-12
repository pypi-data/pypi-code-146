from typing import List, Dict, Any, Callable

from functools import partial

from sktmls.filters import Filter
from sktmls.utils import LogicProcessor

FILTER_OPERATORS = ["==", "!=", "<=", ">=", "<", ">", "contains"]


class FilterUtil:
    """
    필터 로직관련 클래스 입니다.

    ## Example

    ```python
    filter = filter_client.get_filter(id=10)

    filter_util = FilterUtil()
    filter_func = filter_util.generate_filter_applier_fn(filter)

    data = {"key1": "good1", "key2": 3, "mbr_discount_amt_cum_bakery": "N", "gender": ["M", "F"]} # (필터를 적용할 Key-Value 값, contains의 경우 list값 필요)
    filter_func(data)
    ```
    """

    def __init__(self):
        self.logic_processor = LogicProcessor()

    def apply(self, data: Dict[str, Any], conditions: List[dict]) -> bool:
        """
        필터 로직 적용 함수

        ## Args
        - data: (dict) 필터를 적용할 Key-Value 값
        - conditions: (list(dict)) 필터 조건 리스트

        ## Returns
        bool
            - True : 필터 로직 통과
            - False : 필터 로직 걸림
        """
        for filter_dict in conditions:
            key_value = data.get(filter_dict.get("key"))

            if not key_value:
                continue

            operator = filter_dict.get("operator")
            operator_value = filter_dict.get("value")

            if operator == "contains" and not isinstance(key_value, list):
                raise ValueError("contains operator의 경우 list타입의 값이 필요합니다.")

            if self.logic_processor.apply({operator: [key_value, operator_value]}):
                return False

        return True

    def generate_filter_applier_fn(self, filter: Filter) -> Callable[[dict], bool]:
        """
        필터 로직을 적용하는 함수를 리턴하는 함수 (filter 디펜던시)

        ## Args
        - filter: (`sktmls.filters.Filter`) 필터 객체

        ## Returns
        필터 로직 적용 함수
        """
        assert type(filter) == Filter, "`filter`는 `sktmls.filters.Filter`객체여야 합니다."
        conditions = filter.conditions

        for filter_dict in conditions:
            if filter_dict.get("operator") not in FILTER_OPERATORS:
                raise ValueError("없는 operator입니다. %s" % filter_dict.get("operator"))

        return partial(self.apply, conditions=conditions)
