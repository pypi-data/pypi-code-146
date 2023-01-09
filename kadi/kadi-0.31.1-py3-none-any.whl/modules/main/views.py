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
from flask import abort
from flask import redirect
from flask import render_template
from flask_babel import gettext as _
from flask_login import current_user
from flask_login import login_required

import kadi.lib.constants as const
from .blueprint import bp
from .forms import LegalsAcceptanceForm
from .utils import get_favorite_resources
from .utils import get_latest_resources
from kadi import __version__
from kadi.ext.db import db
from kadi.lib.config.core import get_sys_config
from kadi.lib.web import get_preferred_locale
from kadi.lib.web import url_for


@bp.get("/")
def index():
    """The index/home page.

    Will change depending on whether the current user is authenticated or not.
    """
    preferred_locale = get_preferred_locale()

    if not current_user.is_authenticated:
        return render_template("main/index.html", preferred_locale=preferred_locale)

    return render_template(
        "main/home.html",
        title=_("Home"),
        version=__version__,
        preferred_locale=preferred_locale,
        js_context={
            "version": __version__,
            "favorite_resources": get_favorite_resources(),
            "latest_resources": get_latest_resources(),
        },
    )


@bp.get("/about")
def about():
    """The about page."""
    return render_template("main/about.html", title=_("About"), version=__version__)


@bp.get("/help")
def help():
    """The help page."""
    return render_template("main/help.html", title=_("Help"))


@bp.get("/terms-of-use")
def terms_of_use():
    """Page showing the terms of use, if configured."""
    config_item = const.SYS_CONFIG_TERMS_OF_USE

    if not get_sys_config(config_item):
        abort(404)

    return render_template(
        "main/legals.html",
        title=_("Terms of use"),
        endpoint="terms_of_use",
        config_item=config_item,
    )


@bp.get("/privacy-policy")
def privacy_policy():
    """Page showing the privacy policy, if configured."""
    config_item = const.SYS_CONFIG_PRIVACY_POLICY

    if not get_sys_config(config_item):
        abort(404)

    return render_template(
        "main/legals.html",
        title=_("Privacy policy"),
        endpoint="privacy_policy",
        config_item=config_item,
    )


@bp.get("/legal-notice")
def legal_notice():
    """Page showing the legal notice, if configured."""
    config_item = const.SYS_CONFIG_LEGAL_NOTICE

    if not get_sys_config(config_item):
        abort(404)

    return render_template(
        "main/legals.html",
        title=_("Legal notice"),
        endpoint="legal_notice",
        config_item=config_item,
    )


@bp.route("/accept-legals", methods=["GET", "POST"])
@login_required
def request_legals_acceptance():
    """Page to request acceptance of all legal notices."""
    if not current_user.needs_legals_acceptance:
        return redirect(url_for("main.index"))

    form = LegalsAcceptanceForm()

    if form.validate_on_submit():
        current_user.accept_legals()
        db.session.commit()

        return redirect(url_for("main.index"))

    return render_template(
        "main/request_legals_acceptance.html",
        title=_("Accept legal notices"),
        form=form,
    )
