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
from kadi.lib.api.models import AccessToken
from kadi.lib.api.schemas import AccessTokenSchema
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.web import paginated


@bp.get("/settings/access-tokens", v=None)
@login_required
@internal
@paginated
def get_access_tokens(page, per_page):
    """Get all access tokens of the current user."""
    paginated_tokens = current_user.access_tokens.order_by(
        AccessToken.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    data = {
        "items": AccessTokenSchema(many=True).dump(paginated_tokens),
        **create_pagination_data(paginated_tokens.total, page, per_page),
    }

    return json_response(200, data)
