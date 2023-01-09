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
from flask import json

import kadi.lib.constants as const
from kadi.modules.records.files import open_file


def get_custom_mimetype(file, base_mimetype):
    """Get a custom MIME type of a dashboard based on its content.

    :param file: The file to get the MIME type of.
    :param base_mimetype: The base MIME type of the file on which to base the custom
        MIME type.
    :return: The custom MIME type or ``None`` if no custom MIME type was found.
    """
    if file.size > 10 * const.ONE_MB or base_mimetype != const.MIMETYPE_JSON:
        return None

    with open_file(file) as f:
        try:
            data = json.load(f)
        except:
            return None

        if (
            isinstance(data, dict)
            and len(data) <= 2
            and isinstance(data.get("name"), str)
            and isinstance(data.get("panels"), list)
        ):
            return const.MIMETYPE_DASHBOARD

    return None
