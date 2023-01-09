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
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import request
from flask_babel import gettext as _
from flask_login import current_user
from flask_login import logout_user

import kadi.lib.constants as const
from .providers import ShibProvider
from kadi.lib.api.core import json_error_response
from kadi.lib.api.utils import is_api_request
from kadi.lib.web import flash_danger
from kadi.lib.web import url_for
from kadi.modules.accounts.models import UserState


bp = Blueprint("accounts", __name__, template_folder="templates")


@bp.before_app_request
def _before_app_request():
    if current_user.is_authenticated:
        auth_providers = current_app.config["AUTH_PROVIDERS"]

        if (
            current_user.state != UserState.ACTIVE
            or current_user.is_merged
            or current_user.identity is None
            or current_user.identity.type not in auth_providers
        ):
            url = url_for("main.index")

            if (
                current_user.identity is not None
                and current_user.identity.type == const.AUTH_PROVIDER_TYPE_SHIB
                and ShibProvider.is_registered()
            ):
                url = ShibProvider.get_logout_initiator(url)

            logout_user()

            if is_api_request():
                return json_error_response(
                    401, description="This account is currently inactive."
                )

            flash_danger(_("This account is currently inactive."))
            return redirect(url)

        # The listed endpoints should still work even if the current user does require
        # email confirmation or needs to accept the legal notices before proceeding.
        # This list should probably be adjustable in the future.
        excluded_endpoints = [
            "accounts.request_email_confirmation",
            "accounts.confirm_email",
            "accounts.logout",
            "main.about",
            "main.help",
            "main.terms_of_use",
            "main.privacy_policy",
            "main.legal_notice",
            "main.request_legals_acceptance",
            "static",
        ]

        if request.endpoint not in excluded_endpoints:
            if current_user.needs_email_confirmation:
                if is_api_request():
                    return json_error_response(
                        401, description="Please confirm your email address."
                    )

                return redirect(url_for("accounts.request_email_confirmation"))

            if current_user.needs_legals_acceptance:
                if is_api_request():
                    return json_error_response(
                        401, description="Please accept all legal notices."
                    )

                return redirect(url_for("main.request_legals_acceptance"))


from . import views  # pylint: disable=unused-import
