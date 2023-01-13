# handler.py
import traceback
import time
import logging
from logging import config as logging_config
from importlib import import_module
import akerbp.mlops.cdf.helpers as cdf
from akerbp.mlops.core import config
from typing import Dict, Union, Any
from akerbp.mlops.core.logger_config import LOGGING_CONFIG


service_name = config.envs.service_name
service = import_module(f"akerbp.mlops.services.{service_name}").service

logging_config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logging.captureWarnings(True)


def handle(
    data: Dict, secrets: Dict, function_call_info: Dict
) -> Union[Any, Dict[Any, Any]]:
    """Handler function for deploying models to CDF

    Args:
        data (Dict): model payload
        secrets (Dict): API keys to be used by the service
        function_call_info (Dict): dictionary containing function id and whether the function call is scheduled

    Returns:
        Union[Any, Dict[Any, Any]]: Function call response
    """
    try:
        cdf.api_keys = secrets
        logger.info("Setting up CDF Client with access to Data, Files and Functions")
        cdf.set_up_cdf_client(context="deploy")
        logger.info("Set up complete")
        if data:
            logger.info("Calling model using provided payload")
            start = time.time()
            output = service(data, secrets)
            elapsed = time.time() - start
            logger.info(f"Model call complete. Duration: {elapsed:.2f} s")
        else:
            logger.info("Calling model with empty payload")
            output = dict(status="ok")
            logger.info("Model call complete")
        logger.info("Querying metadata from the function call")
        function_call_metadata = cdf.get_function_call_response_metadata(
            function_call_info["function_id"]
        )
        logger.info("Function call metadata obtained")
        logger.info("Writing function call metadata to response")
        output.update(dict(metadata=function_call_metadata))
        logger.info("Function call metadata successfully written to response")
        return output
    except Exception:
        trace = traceback.format_exc()
        error_message = f"{service_name} service failed.\n{trace}"
        logger.critical(error_message)
        return dict(status="error", error_message=error_message)
