from typing import Any
from typing import Dict

from tecton._internals.sdk_decorators import sdk_public_method
from tecton._internals.spark_utils import get_or_create_spark_session
from tecton_core import logger as logger_lib


logger = logger_lib.get_logger("TectonContext")


class TectonContext:
    """
    Execute Spark SQL queries; access various utils.
    """

    _current_context_instance = None
    _config: Dict[str, Any] = {}

    def __init__(self, spark):
        self._spark = spark

    @classmethod
    def _set_config(cls, custom_spark_options=None):
        """
        Sets the configs for TectonContext instance.
        To take effect it must be called before any calls to TectonContext.get_instance().

        :param custom_spark_options: If spark session gets created by TectonContext, custom spark options/
        """
        cls._config = {"custom_spark_options": custom_spark_options}

    @classmethod
    @sdk_public_method
    def get_instance(cls) -> "TectonContext":
        """
        Get the singleton instance of TectonContext.
        """
        # If the instance doesn't exist, creates a new TectonContext from
        # an existing Spark context. Alternatively, creates a new Spark context on the fly.
        if cls._current_context_instance is not None:
            return cls._current_context_instance
        else:
            return cls._generate_and_set_new_instance()

    @classmethod
    def _generate_and_set_new_instance(cls) -> "TectonContext":
        logger.debug(f"Generating new Spark session")
        spark = get_or_create_spark_session(
            cls._config.get("custom_spark_options"),
        )
        cls._current_context_instance = cls(spark)
        return cls._current_context_instance

    def _get_spark(self):
        return self._spark
