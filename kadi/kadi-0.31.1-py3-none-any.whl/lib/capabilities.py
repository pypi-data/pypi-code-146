# Copyright 2022 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import current_app


def has_capabilities(*capabilities):
    """Check if the current Kadi instance has all given capabilities.

    :param capabilities: One or more capabilities to check.
    :return: ``True`` if all given capabilities are available, ``False`` otherwise.
    """
    satisfied_capabilities = [
        c in current_app.config["CAPABILITIES"] for c in capabilities
    ]
    return all(satisfied_capabilities)
