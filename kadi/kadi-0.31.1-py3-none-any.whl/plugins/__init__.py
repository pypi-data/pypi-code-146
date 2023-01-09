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
import kadi.lib.constants as const
from .core import get_plugin_config
from .core import hookimpl
from .core import PluginConfigForm
from kadi.ext.db import db
from kadi.lib.api.blueprint import bp as api_bp
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.capabilities import has_capabilities
from kadi.lib.config.core import get_user_config
from kadi.lib.config.core import MISSING
from kadi.lib.config.core import remove_user_config
from kadi.lib.config.core import set_user_config
from kadi.lib.db import has_extension
from kadi.lib.forms import BooleanField
from kadi.lib.forms import IntegerField
from kadi.lib.forms import JSONField
from kadi.lib.forms import KadiForm
from kadi.lib.forms import LFTextAreaField
from kadi.lib.forms import PasswordField
from kadi.lib.forms import SelectField
from kadi.lib.forms import StringField
from kadi.lib.forms import SubmitField
from kadi.lib.forms import UTCDateTimeField
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.permissions.core import has_permission
from kadi.lib.permissions.utils import permission_required
from kadi.lib.schemas import KadiSchema
from kadi.lib.web import url_for
from kadi.modules.collections.models import Collection
from kadi.modules.groups.models import Group
from kadi.modules.records.files import open_file
from kadi.modules.records.models import File
from kadi.modules.records.models import Record
from kadi.modules.templates.models import Template
