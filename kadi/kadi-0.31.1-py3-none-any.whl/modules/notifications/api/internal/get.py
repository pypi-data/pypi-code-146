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

from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal
from kadi.lib.api.core import json_response
from kadi.modules.notifications.models import Notification
from kadi.modules.notifications.schemas import NotificationSchema


@bp.get("/notifications", v=None)
@login_required
@internal
def get_notifications():
    """Get all notifications of the current user."""
    notifications = current_user.notifications.order_by(Notification.created_at.desc())
    return json_response(200, NotificationSchema(many=True).dump(notifications))
