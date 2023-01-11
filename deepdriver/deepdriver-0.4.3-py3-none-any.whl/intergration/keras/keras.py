from typing import Dict

import tensorflow as tf
import copy

from deepdriver.sdk.data_types.run import get_run
from deepdriver import logger


class MLCallback(tf.keras.callbacks.Callback):

    def __init__(self):
        pass

    def on_epoch_end(self, epoch: int, logs: Dict = {}):
        logger.debug(f"logs:{logs}")
        logger.debug(f"epoch:{epoch}")

        to_send_log = copy.deepcopy(logs)
        if "accuracy" in logs:
            to_send_log["acc"] = logs["accuracy"]

        if "val_accuracy" in logs:
            to_send_log["val_acc"] = logs["val_accuracy"]

        logger.debug(f"to_send_logs:{to_send_log}")
        get_run().log(to_send_log)
