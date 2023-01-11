import logging
import os


class PredictProbaWrapper(object):

    def __init__(self, model):
        self.model = model

    def get_model(self):
        return self.model


def _load_model_from_local_file(path):
    import pyspark
    from pyspark import SparkConf
    from pyspark import SparkContext
    from pyspark.ml.classification import DecisionTreeClassificationModel
    from pyspark.ml.classification import GBTClassificationModel
    from pyspark.ml.classification import RandomForestClassificationModel
    supported_spark_classification_models = [
        GBTClassificationModel, DecisionTreeClassificationModel,
        RandomForestClassificationModel
    ]

    username_for_spark = "hduser"

    # Needed for spark init to avoid hadoop UserGroupInformation login.
    os.environ["SPARK_USER"] = username_for_spark

    # Apache Ivy is assuming that ivy home will be set or user.home will
    # be set (not true when there is no user as in open shift)
    _logger = logging.getLogger(__name__)
    conf = SparkConf()
    conf.setMaster("local").setAppName("model_runner_spark")
    temp_dir = os.environ.get("TMPDIR", "/tmp/")
    conf.set("spark.jars.ivy", os.path.join(temp_dir, "ivy"))
    # Disabling the spark UI to prevent ports from being taken up.
    # Without this, Spark Context initialization fails after spark.port.maxRetries (16) runs.
    conf.set("spark.ui.enabled", "false")

    sc = SparkContext.getOrCreate(conf=conf)

    # Now that we have a spark context, set remote user the "correct" way. This avoids calls to
    # UserGroupInformation for subsequent calls including model load.
    user = sc._jvm.org.apache.hadoop.security.UserGroupInformation.createRemoteUser(
        username_for_spark
    )
    sc._jvm.org.apache.hadoop.security.UserGroupInformation.setLoginUser(user)

    deserialized_model = None
    for model_type in supported_spark_classification_models:
        try:
            deserialized_model = model_type.load(path)
            _logger.info(f"Successfully loaded model as {model_type}")
            break
        except Exception as ex:
            _logger.info(
                f"Failed to load model as {model_type}: Exception: {ex}"
            )

    if not deserialized_model:
        raise ValueError(
            f"Model could not be loaded. Verify that model is one of {supported_spark_classification_models}"
        )

    return PredictProbaWrapper(deserialized_model)


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
