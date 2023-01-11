from truera.utils.general import safe_isinstance

SUPPORTED_PYSPARK_MODELS = [
    "pyspark.ml.classification.GBTClassificationModel",
    "pyspark.ml.classification.DecisionTreeClassificationModel",
    "pyspark.ml.classification.RandomForestClassificationModel",
    "pyspark.ml.regression.GBTRegressionModel",
    "pyspark.ml.regression.DecisionTreeRegressionModel",
    "pyspark.ml.regression.RandomForestRegressionModel"
]


def is_supported_pyspark_tree_model(obj):
    return safe_isinstance(obj, SUPPORTED_PYSPARK_MODELS)
