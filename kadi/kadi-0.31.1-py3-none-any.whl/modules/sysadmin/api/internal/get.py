# Copyright 2021 Karlsruhe Institute of Technology
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
import requests
from flask import current_app

import kadi.lib.constants as const
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal
from kadi.lib.api.core import json_response


@bp.get("/sysadmin/latest-version", v=None)
@internal
def get_latest_version():
    """Get the latest released Kadi version via PyPI."""
    latest_version = None

    try:
        response = requests.get(const.URL_PYPI, timeout=5)
        latest_version = response.json()["info"]["version"]
    except Exception as e:
        current_app.logger.exception(e)

    return json_response(200, {"latest_version": latest_version})
