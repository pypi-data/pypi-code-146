# Copyright 2020 Karlsruhe Institute of Technology
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
from flask import request
from flask_wtf.csrf import CSRFProtect

from kadi.lib.api.blueprint import bp as api_bp


class KadiCSRFProtect(CSRFProtect):
    """Custom CSRF protection.

    Reimplements the original "_get_csrf_token" method, but checks the headers for the
    CSRF token before the form to prevent the full read of the data input stream when
    the CSRF token can already be found in the HTTP headers.

    :param app: (optional) The application object.
    """

    def __init__(self, app=None):
        super().__init__(app=app)

    def _get_csrf_token(self):
        # Check the headers for the token.
        for header_name in current_app.config["WTF_CSRF_HEADERS"]:
            csrf_token = request.headers.get(header_name)

            if csrf_token:
                return csrf_token

        # Check the form for the token. Note that accessing the form via "request.form"
        # causes a full read of the data input stream.
        field_name = current_app.config["WTF_CSRF_FIELD_NAME"]
        base_token = request.form.get(field_name)

        if base_token:
            return base_token

        for key in request.form:
            if key.endswith(field_name):
                csrf_token = request.form[key]

                if csrf_token:
                    return csrf_token

        return None


csrf = KadiCSRFProtect()
csrf.exempt(api_bp)
