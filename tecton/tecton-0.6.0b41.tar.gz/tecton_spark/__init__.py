import logging
import sys

from tecton_core import materialization_context

# TODO(deprecated_after=0.5): handle backward-compatibility for customer copies of builtin transformations that did not use tecton.materialization_context
# but instead directly accessed tecton_spark.materialization_context
sys.modules["tecton_spark.materialization_context"] = materialization_context

try:
    logging.getLogger("py4j").setLevel(logging.WARN)
except:
    pass
