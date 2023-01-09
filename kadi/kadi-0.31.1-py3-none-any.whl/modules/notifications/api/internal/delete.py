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
from flask_login import current_user
from flask_login import login_required

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.modules.notifications.core import (
    dismiss_notification as _dismiss_notification,
)
from kadi.modules.notifications.models import Notification


@bp.delete("/notifications/<int:id>", v=None)
@login_required
@internal
def dismiss_notification(id):
    """Dismiss a notification."""
    notification = Notification.query.get_or_404(id)

    if notification.user != current_user:
        return json_error_response(404)

    _dismiss_notification(notification)
    db.session.commit()

    return json_response(204)
