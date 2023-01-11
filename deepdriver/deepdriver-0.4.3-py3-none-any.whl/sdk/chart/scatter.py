from assertpy import assert_that

from deepdriver.sdk.chart.chart import Chart, TYPE_SCATTER
from deepdriver.sdk.data_types.dataFrame import DataFrame

def scatter(data: DataFrame, x: str, y: str, title: str=None) -> Chart:
    assert_that(data).is_not_none()
    assert_that(x).is_not_none()
    assert_that(y).is_not_none()

    return Chart(chart_type=TYPE_SCATTER, data=data, data_fields={"x": x, "y": y}, label_fields={"title": title})
