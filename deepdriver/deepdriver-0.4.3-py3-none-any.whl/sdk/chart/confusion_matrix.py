import numpy as np
from assertpy import assert_that

from deepdriver.sdk.chart.chart import Chart, TYPE_CONFUSION_MATRIX


def confusion_matrix(y_true: list, probs: list = None, preds: list = None, class_names: list = None,
                     title: str = None) -> Chart:
    assert_that(y_true).is_not_none()
    if (probs is None) and (preds is None):
        raise Exception("probs, preds one must have value")
        return

    if (probs is not None) and (preds is None):
        preds = np.argmax(probs, axis=1).tolist()

    if class_names is None:
        class_inds = set(preds).union(set(y_true))
        n_classes = len(class_inds)
        class_names = [f"Class_{i}" for i in range(1, n_classes + 1)]
    else:
        n_classes = len(class_names)
        class_inds = [i for i in range(n_classes)]

    class_mapping = {}
    for i, val in enumerate(sorted(list(class_inds))):
        class_mapping[val] = i
    counts = np.zeros((n_classes, n_classes))
    for i in range(len(preds)):
        counts[class_mapping[y_true[i]], class_mapping[preds[i]]] += 1

    data = []
    for i in range(n_classes):
        for j in range(n_classes):
            data.append([class_names[i], class_names[j], counts[i, j]])

    from deepdriver import DataFrame
    dataframe = DataFrame(columns=["Actual", "Predicted", "nPredictions"], data=data)

    fields = {
        "Actual": "Actual",
        "Predicted": "Predicted",
        "nPredictions": "nPredictions",
    }
    return Chart(chart_type=TYPE_CONFUSION_MATRIX, data=dataframe, data_fields=fields, label_fields={"title": title})
