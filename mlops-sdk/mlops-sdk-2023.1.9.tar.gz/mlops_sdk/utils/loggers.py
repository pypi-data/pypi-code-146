# import os
# import logging
# from datetime import datetime
"""Logging utils for emartdt AI-Engineering-Chapter.
Updated 2021-12-16

Supported logging
 - Google cloud logging api (single entry)
Todo's
 - Python logging
 - Gcloud logging - batch logging

"""
__version__ = "0.1.0"

from functools import lru_cache

from google.cloud import logging as glogging
from google.cloud.logging import Resource

glogging_client = None


class GCloudLogger:
    def __init__(self, logging_client, logger_name, project_id="emart-dt-dev-ds", resource=None):
        """Gcloud logging"""

        self.logger = logging_client.logger(logger_name)
        res = Resource(
            type="global",
            labels={
                "project_id": project_id,
            },
        )

        self.resource = resource or res

    def __enter__(self):
        return self

    def write(self, message, log_level="INFO"):
        """Write message to google cloud logging"""

        assert any([isinstance(message, dict), isinstance(message, str)]), "message type should be dict or str."

        res = self.resource
        if isinstance(message, dict):
            self.logger.log_struct(message, resource=res, severity=log_level)
        else:
            self.logger.log_text(message, resource=res, severity=log_level)

    def list(self, *args, **kwargs):
        """List messages written to google cloud logging.
        Todo
            - support log filtering
        """
        return list(self.logger.list_entries())

    def delete(self, *args, **kwargs):
        """Delete all log messages by logname."""
        print("This method is not directly run, self.logger.delete() ")


@lru_cache()
def get_glogger(logger_name="mlops-serving-inference", project_id="emart-dt-dev-ds", resource_dict=None):
    """Helper for Google cloud logging api.
    https://cloud.google.com/logging/docs/structured-logging

    Usage
        ```python
        from mlops_sdk.utils import get_glogger
        glogger = get_glogger()
        message = {"message": "some very very important message."}
        glogger.write(message)
        message = "simple message"
        glogger.write(message)

        ```

    Args:
        logger_name(str, optional) : LogName, default to "mlops-serving-inference"
        project_id(str, optional) : project_id, default to "emart-dt-dev-ds"
        resource_dict(dict, optional) : dict for resource object, project_id ignored if exist.
                            refer to https://cloud.google.com/monitoring/api/resources#tag_global
                            ex) resource_dict = {"type": "global",
                                                labels={
                                                    "project_id": <project_id>
                                                    }
                                                }

    Return:
       GCloudLogger object instance handling google cloud logger
       self.logger <- glogging_client.logger()

       Usage :
            1. Write log : dict/string type
            logger.write(message = dict(message="message"))
            logger.write(message = "message"))
            2. List logs
            logger.list()
            3. Detele logs
            logger.delete()

    """

    global glogging_client
    glogging_client = glogging_client or glogging.Client()

    resource_dict = resource_dict or dict(
        type="global",
        labels={
            "project_id": project_id,
        },
    )

    resource = Resource(**resource_dict)
    logger = GCloudLogger(glogging_client, logger_name, project_id, resource=resource)
    return logger


# %%
