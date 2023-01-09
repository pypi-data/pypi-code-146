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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import validates

from kadi.ext.db import db
from kadi.lib.db import check_constraint
from kadi.lib.db import composite_index
from kadi.lib.db import SimpleTimestampMixin
from kadi.lib.db import unique_constraint
from kadi.lib.utils import SimpleReprMixin
from kadi.lib.utils import StringEnum


class Permission(SimpleReprMixin, db.Model):
    """Model representing fine-grained permissions.

    Each permission is associated with a specific type of object, a related action and
    optionally an ID referring to a specific object instance.
    """

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "action", "object", "object_id"]
        """See :class:`.SimpleReprMixin`."""

    __tablename__ = "permission"

    __table_args__ = (
        unique_constraint(__tablename__, "action", "object", "object_id"),
    )

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the permission, auto incremented."""

    action = db.Column(db.Text, nullable=False)
    """The action the permission refers to with respect to its object type."""

    object = db.Column(db.Text, nullable=False)
    """The type of object the permission refers to.

    Currently always refers to a specific model, in which case the object type is equal
    to that model's table name.
    """

    object_id = db.Column(db.Integer, nullable=True)
    """The ID of an object the permission refers to.

    If not set, the permission counts for all object instances of its type.
    """

    roles = db.relationship(
        "Role",
        secondary="role_permission",
        lazy="dynamic",
        back_populates="permissions",
    )

    users = db.relationship(
        "User",
        secondary="user_permission",
        lazy="dynamic",
        back_populates="permissions",
    )

    groups = db.relationship(
        "Group",
        secondary="group_permission",
        lazy="dynamic",
        back_populates="permissions",
    )

    @classmethod
    def create(cls, *, action, object, object_id=None):
        """Create a new permission and add it to the database session.

        :param action: The action the permission refers to.
        :param object: The object the permission refers to.
        :param object_id: (optional) The ID of an object.
        :return: The new :class:`Permission` object.
        """
        permission = cls(action=action, object=object, object_id=object_id)
        db.session.add(permission)

        return permission


class Role(SimpleReprMixin, db.Model):
    """Model representing roles.

    A role is a grouping of multiple permissions. There are two kinds of roles specified
    through this model:

    * Roles belonging to a specific object instance. Both its :attr:`object` and
      :attr:`object_id` are set in this case and all permissions that belong to this
      role have to refer to the same object instance.
    * Global system roles. Both the :attr:`object` and :attr:`object_id` are not set in
      this case and the permissions that belong to this role can refer to multiple
      object types and instances (usually to all instances of a specific object type).
    """

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "name", "object", "object_id"]
        """See :class:`.SimpleReprMixin`."""

    __tablename__ = "role"

    __table_args__ = (
        unique_constraint(__tablename__, "name", "object", "object_id"),
        check_constraint(
            "(object IS NULL AND object_id IS NULL)"
            " OR (object IS NOT NULL AND object_id IS NOT NULL)",
            "system_role",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the role, auto incremented."""

    name = db.Column(db.Text, nullable=False)
    """The name of the role."""

    object = db.Column(db.Text, nullable=True)
    """The type of object the role refers to.

    Currently always refers to a specific model, in which case the object type is equal
    to that model's table name. If not set, :attr:`object_id` has to be ``None`` as
    well.
    """

    object_id = db.Column(db.Integer, nullable=True)
    """The ID of an object the role refers to.

    If not set, the :attr:`object` has to be ``None`` as well.
    """

    permissions = db.relationship(
        "Permission",
        secondary="role_permission",
        lazy="dynamic",
        back_populates="roles",
    )

    users = db.relationship(
        "User", secondary="user_role", lazy="dynamic", back_populates="roles"
    )

    groups = db.relationship(
        "Group", secondary="group_role", lazy="dynamic", back_populates="roles"
    )

    role_rules = db.relationship(
        "RoleRule", back_populates="role", cascade="all, delete-orphan"
    )

    @validates("permissions")
    def _validate_permission(self, key, permission):
        if self.object and self.object_id:
            assert (
                permission.object == self.object
                and permission.object_id == self.object_id
            )

        return permission

    @classmethod
    def create(cls, *, name, object=None, object_id=None):
        """Create a new role and add it to the database session.

        :param name: The name of the role.
        :param object: (optional) The object the role refers to.
        :param object_id: (optional) The ID of an object.
        :return: The new :class:`Role` object.
        """
        role = cls(name=name, object=object, object_id=object_id)
        db.session.add(role)

        return role


class RoleRuleType(StringEnum):
    """String enum containing all possible type values for role rules."""

    __values__ = ["username"]


class RoleRule(SimpleReprMixin, SimpleTimestampMixin, db.Model):
    """Model to represent role rules.

    Role rules can be used to automate permission management by automatically granting
    users or groups roles for different resources based on different conditions.
    """

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "role_id", "type", "condition"]
        """See :class:`.SimpleReprMixin`."""

    __tablename__ = "role_rule"

    __table_args__ = (composite_index(__tablename__, "role_id", "type"),)

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the role rule, auto incremented."""

    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    """The ID of the role the role rule refers to."""

    type = db.Column(db.Text, nullable=False)
    """The type of the role rule."""

    condition = db.Column(JSONB, nullable=False)
    """The condition of the role rule, depending on its type.

    For each of the role rule types, the data consists of:

    * ``"username"``: An object containing the type of a user's identity and a pattern
      to check the corresponding username with.
    """

    role = db.relationship("Role", back_populates="role_rules")

    @classmethod
    def create(cls, *, role, type, condition):
        """Create a new role rule and add it to the database session.

        :param role: The role the role rule refers to.
        :param type: The type of the role rule.
        :param condition: The condition of the role rule.
        :return: The new :class:`RoleRule` object.
        """
        role_rule = cls(role=role, type=type, condition=condition)
        db.session.add(role_rule)

        return role_rule


# Auxiliary table to group permissions into roles.
db.Table(
    "role_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permission.id"), primary_key=True
    ),
)
