"""
This module contains classes related to the definition and usage of the Sampling
Configuration defined for a gateway device.
"""

# ============================ imports =========================================

from txp.common.configuration import SamplingWindow
from txp.common.configuration import SamplingParameters


class SamplingTask:
    """A sampling task to be performed by a Driver.

    This structure works as an abstraction to contain any kind of information required
    by the driver to perform sampling tasks.
    """

    def __init__(self, configuration_id: str, parameters: SamplingParameters, tenant_id: str):
        """
        Args:
            configuration_id: the configuration id under which this task was assigned.
            task_configuration: The SamplingParameters for this task.
            tenant_id (str): The tenant_id to which this Gateway belongs
        """
        self.sampling_window: SamplingWindow = parameters.sampling_window
        self.parameters: SamplingParameters = parameters
        self.configuration_id: str = configuration_id
        self.tenant_id: str = tenant_id
