from typing import Dict


def create_waiter_config(
    hub,
    default_delay: int = 15,
    default_max_attempts: int = 40,
    timeout_config: Dict = None,
) -> Dict[str, int]:
    """
    Create a waiter configuration that can be used as input in waiter calls. The configuration is based on
    the default values and the customized value in timeout_config.

    Args:
        hub: The redistributed pop central hub.
        default_delay: The amount of time in seconds to wait between attempts.
        default_max_attempts: The maximum number of attempts to be made.
        timeout_config: Customized timeout configuration containing delay and max attempts.

    Returns:
        {"delay": delay-time, "max_attempts": max-attempts}
    """
    result = {"delay": default_delay, "max_attempts": default_max_attempts}
    if timeout_config:
        if "delay" in timeout_config:
            result["delay"] = timeout_config["delay"]
        if "max_attempts" in timeout_config:
            result["max_attempts"] = timeout_config["max_attempts"]
    return result


def create_waiter(hub, **kwargs):
    class CustomWaiter:
        def __init__(self):
            self.api_class_name = kwargs.get("api_class_name")
            self.operation = kwargs.get("operation")
            self.arguments = kwargs.get("arguments")
            self.result_arguments = kwargs.get("result_arguments")
            self.acceptor_function = kwargs.get("acceptor_function")
            self.waiter_config = kwargs.get("waiter_config")

    return CustomWaiter()
