# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


from abc import abstractmethod, ABC
from ..utils.utils import ApiInputs

class GuideRetrySupportTask(ABC):
    @property
    @abstractmethod
    def check_retry(self, api_inputs: ApiInputs) -> bool:
        """"True when Task should be reprocessed; otherwise False"""
        return False
