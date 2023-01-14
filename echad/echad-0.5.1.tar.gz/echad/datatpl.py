from typing import List, Optional, Any
from pydantic import BaseModel
from pydantic.main import create_model


class SimpleBar:

    example = {
        "title": {"text": "ECharts 入门示例"},
        "tooltip": {},
        "legend": {"data": ["销量"]},
        "xAxis": {"data": ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]},
        "yAxis": {},
        "series": [{"name": "销量", "type": "bar", "data": [5, 20, 36, 10, 10, 20]}],
    }

    @staticmethod
    def config(
        title: str,
        legend: List[str],
        x_axis: List[Any],
        name: str,
        data: List[Any],
    ):
        return {
            "title": {"text": title},
            "tooltip": {},
            "legend": {"data": legend},
            "xAxis": {"data": x_axis},
            "yAxis": {},
            "series": [{"name": name, "type": "bar", "data": data}],
        }

    class Model(BaseModel):
        ...
