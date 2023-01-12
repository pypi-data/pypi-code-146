import json
import pandas as pd
from assertpy import assert_that
from typing import List

class DataFrame:

    def __init__(self, data: List[List]=None, columns: List[str]=None, dataframe: pd.DataFrame=None) -> None:
        # columns와 data, dataframe중 하나의 파라미터는 입력이 되어야함
        if dataframe is not None:
            # dataframe이 입력된 경우 멤버변수의 dataframe으로 설정하고
            self.dataframe = dataframe

            # columns와 data 멤버변수를 dataframe으로부터 추출하여 설정한다
            self.data: List[List] = dataframe.values.tolist()
            self.columns: List[str] = dataframe.columns.tolist()
        else:
            assert_that(data).is_not_none()
            assert_that(columns).is_not_none()

            # columns와 data가 입력된 경우 추후 visualize에서 사용하기 쉽도록 pd.DataFrame를 columns와 data를 통해 생성하고 멤버변수 dataframe에 설정한다
            self.dataframe = pd.DataFrame(data=data, columns=columns)
            self.data = data
            self.columns = columns

    def to_dict(self) -> str:
        return {
            "columns" : self.columns,
            "data" : self.data,
        }
