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
from flask_babel import lazy_gettext as _l

import kadi.lib.constants as const
from kadi.ext.db import db
from kadi.lib.db import generate_check_constraints
from kadi.lib.db import StateTimestampMixin
from kadi.lib.favorites.core import FavoriteMixin
from kadi.lib.search.core import SearchableMixin
from kadi.lib.utils import SimpleReprMixin
from kadi.lib.utils import StringEnum
from kadi.modules.records.extras import ExtrasJSONB


class TemplateVisibility(StringEnum):
    """String enum containing all possible visibility values for templates."""

    __values__ = [const.MODEL_VISIBILITY_PRIVATE, const.MODEL_VISIBILITY_PUBLIC]


class TemplateType(StringEnum):
    """String enum containing all possible type values for templates."""

    __values__ = ["record", "extras"]


class TemplateState(StringEnum):
    """String enum containing all possible state values for templates."""

    __values__ = [const.MODEL_STATE_ACTIVE, const.MODEL_STATE_DELETED]


class Template(
    SimpleReprMixin, SearchableMixin, StateTimestampMixin, FavoriteMixin, db.Model
):
    """Model to represent templates."""

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "user_id", "identifier", "visibility", "type", "state"]
        """See :class:`.SimpleReprMixin`."""

        search_mapping = "kadi.modules.templates.mappings.TemplateMapping"
        """See :class:`.SearchableMixin`."""

        revision = ["identifier", "title", "description", "visibility", "data", "state"]
        """See :func:`kadi.lib.revisions.core.setup_revisions`."""

        permissions = {
            "actions": [
                ("read", _l("View this template.")),
                ("update", _l("Edit this template.")),
                ("permissions", _l("Manage permissions of this template.")),
                ("delete", _l("Delete this template.")),
            ],
            "roles": [
                ("member", ["read"]),
                ("editor", ["read", "update"]),
                ("admin", ["read", "update", "permissions", "delete"]),
            ],
            "global_actions": [
                ("create", "Create templates."),
                ("read", "View any template."),
                ("update", "Edit any template."),
                ("permissions", "Manage permissions of any template."),
                ("delete", "Delete any template."),
            ],
            "default_permissions": {"read": {"visibility": TemplateVisibility.PUBLIC}},
        }
        """Possible permissions and roles for templates.

        See :mod:`kadi.lib.permissions`.
        """

        check_constraints = {
            "identifier": {"length": {"max": 50}},
            "title": {"length": {"max": 150}},
            "description": {"length": {"max": 10_000}},
            "visibility": {"values": TemplateVisibility.__values__},
            "type": {"values": TemplateType.__values__},
            "state": {"values": TemplateState.__values__},
        }
        """See :func:`kadi.lib.db.generate_check_constraints`."""

    __tablename__ = "template"

    __table_args__ = generate_check_constraints(Meta.check_constraints)

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the template, auto incremented."""

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    """The ID of the user who created the template."""

    identifier = db.Column(db.Text, index=True, unique=True, nullable=False)
    """The unique identifier of the template.

    Restricted to a maximum length of 50 characters.
    """

    title = db.Column(db.Text, nullable=False)
    """The title of the template.

    Restricted to a maximum length of 150 characters.
    """

    description = db.Column(db.Text, nullable=False)
    """The description of the template.

    Restricted to a maximum length of 10_000 characters.
    """

    plain_description = db.Column(db.Text, nullable=False)
    """The plain description of the template.

    Equal to the normal description with the difference that most markdown is stripped
    out.
    """

    visibility = db.Column(db.Text, index=True, nullable=False)
    """The default visibility of the template."""

    type = db.Column(db.Text, index=True, nullable=False)
    """The type of the template."""

    data = db.Column(ExtrasJSONB, nullable=False)
    """The data of the template depending on its type.

    The data is stored in JSON format. For each of the template types, it consists of:

    * ``"record"``: An object containing all relevant record properties as keys with
      corresponding values. See also :class:`.Record`.
    * ``"extras"``: An array of objects containing the extra metadata of a record. See
      also :attr:`.Record.extras`.
    """

    state = db.Column(db.Text, index=True, nullable=False)
    """The state of the template."""

    creator = db.relationship("User", back_populates="templates")

    @classmethod
    def create(
        cls,
        *,
        creator,
        identifier,
        title,
        type,
        data,
        description="",
        plain_description="",
        visibility=TemplateVisibility.PRIVATE,
        state=TemplateState.ACTIVE,
    ):
        """Create a new template and add it to the database session.

        :param creator: The creator of the template.
        :param identifier: The identifier of the template.
        :param title: The title of the template.
        :param type: The type of the template.
        :param data: The data of the template.
        :param description: (optional) The description of the template.
        :param plain_description: (optional) The plain description of the template.
        :param visibility: (optional) The default visibility of the template.
        :param state: (optional) The state of the template.
        :return: The new :class:`Template` object.
        """
        template = cls(
            creator=creator,
            identifier=identifier,
            title=title,
            type=type,
            data=data,
            description=description,
            plain_description=plain_description,
            visibility=visibility,
            state=state,
        )
        db.session.add(template)

        return template
