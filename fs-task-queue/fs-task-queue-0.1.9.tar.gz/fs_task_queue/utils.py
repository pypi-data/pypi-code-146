import contextlib
import time
import os


@contextlib.contextmanager
def timer(logger, prefix: str):
    start_time = time.time()
    logger.info(f"Starting {prefix}")
    yield
    logger.info(f"Finished {prefix} took {time.time() - start_time:.2f} [s]")


def eval_boolean_env_var(variable: str, default: bool):
    """
    Attempt to evaluate a boolean environment variable according to its value.

    Args:
        variable (str): Name of the environment variable to evaluate.
        default (bool): Default value to return if the variable is not found.

    Raises:
        ValueError: If the value of the environment variable is not a valid boolean.

    Returns:
        bool: The value of the environment variable or the default.
    """

    value = os.getenv(variable)

    if value:
        if value.lower() in ["true", "1"]:
            return True
        elif value.lower() in ["false", "0"]:
            return False
        else:
            raise ValueError(f"Invalid value for {variable}")
    else:
        return default
