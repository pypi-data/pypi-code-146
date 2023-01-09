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
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import current_user


def _app_limits():
    if current_user.is_authenticated:
        return current_app.config["RATELIMIT_AUTHENTICATED_USER"]

    return current_app.config["RATELIMIT_ANONYMOUS_USER"]


limiter = Limiter(application_limits=[_app_limits], key_func=get_remote_address)


@limiter.request_filter
def _ip_whitelist():
    return request.remote_addr in current_app.config["RATELIMIT_IP_WHITELIST"]
