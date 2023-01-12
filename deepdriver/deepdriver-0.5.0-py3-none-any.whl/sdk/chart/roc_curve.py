import numpy as np
import pandas as pd
from assertpy import assert_that

from deepdriver.sdk.lib.lazyloader import LazyLoader
sklearn_matric = LazyLoader('deepdriver.metrics.roc_curve', globals(), 'sklearn.metrics')  #layzyload
#
# try:
#     from sklearn.metrics import roc_curve as sklearn_roc_curve
# except ImportError:
#     raise ImportError("sklearn package is required")

from deepdriver.sdk.chart.chart import Chart, TYPE_ROC_CURVE


def roc_curve(y_true: list, probs: list, class_names: list = None, title: str = None) -> Chart:
    # 필수값 체크 !!
    assert_that(y_true).is_not_none().is_type_of(list)
    assert_that(probs).is_not_none().is_type_of(list)


    y_true = np.array(y_true)
    y_probas = np.array(probs)
    classes = np.unique(y_true)

    fpr = dict()
    tpr = dict()
    indices_to_plot = np.where(np.isin(classes, classes))[0]
    for i in indices_to_plot:
        if class_names is not None and (
                isinstance(classes[i], int) or isinstance(classes[0], np.integer)
        ):
            class_label = class_names[classes[i]]
        else:
            class_label = classes[i]

        fpr[class_label], tpr[class_label], _ = sklearn_matric.roc_curve(
            y_true, y_probas[..., i], pos_label=classes[i]
        )

    df = pd.DataFrame(
        {
            "class": np.hstack([[k] * len(v) for k, v in fpr.items()]),
            "fpr": np.hstack(list(fpr.values())),
            "tpr": np.hstack(list(tpr.values())),
        }
    )
    df = df.round(3)
    # deepdriver data 프레임으로 변환
    from deepdriver import DataFrame
    dataframe = DataFrame(dataframe=df)
    fields = {"x": "fpr", "y": "tpr", "class": "class"}

    return Chart(chart_type=TYPE_ROC_CURVE, data=dataframe, data_fields=fields, label_fields={"title": title})
