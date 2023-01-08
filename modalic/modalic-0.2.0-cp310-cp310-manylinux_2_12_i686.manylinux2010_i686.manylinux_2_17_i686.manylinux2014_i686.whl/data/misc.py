#  Copyright (c) modalic 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

"""Handling datasets."""
from logging import DEBUG
from typing import Any, Optional

from modalic.logging.logging import logger


def get_dataset_length(dataset: Any, client_id: Optional[int] = 0) -> int:
    r"""Returns the length of the dataset.

    :param dataset: (Any) Custom dataset object.
    :returns: Length of dataset object. If len() cannot be called, 1 is returned.
    """
    if hasattr(dataset, "__len__"):
        return len(dataset)
    else:
        logger.log(
            DEBUG,
            f"Dataset type {type(dataset)} unknown for client {client_id}.\
            Data length cannot be computed, therefore factor 1 is used.",
        )
        return 1
