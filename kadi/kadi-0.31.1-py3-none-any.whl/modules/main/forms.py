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
from flask_babel import lazy_gettext as _l
from wtforms.validators import DataRequired

from kadi.lib.forms import BooleanField
from kadi.lib.forms import KadiForm
from kadi.lib.forms import SubmitField


class LegalsAcceptanceForm(KadiForm):
    """A form for use in mandatory acceptance of legal notices."""

    accept_legals = BooleanField(validators=[DataRequired()])

    submit = SubmitField(_l("Continue"))
