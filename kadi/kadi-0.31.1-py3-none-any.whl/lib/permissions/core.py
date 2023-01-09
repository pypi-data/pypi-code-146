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
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

from .models import Permission
from .models import Role
from .models import RoleRule
from .models import RoleRuleType
from kadi.ext.db import db
from kadi.lib.cache import memoize_request
from kadi.lib.db import BaseTimestampMixin
from kadi.lib.db import escape_like
from kadi.lib.db import get_class_by_tablename
from kadi.lib.db import NestedTransaction
from kadi.lib.utils import rgetattr
from kadi.modules.accounts.models import User
from kadi.modules.groups.models import Group


def _get_permissions(subject, action, object_name, check_groups=True):
    from kadi.modules.groups.utils import get_user_groups

    group_permissions_query = None

    if isinstance(subject, User) and check_groups:
        group_ids_query = get_user_groups(subject).with_entities(Group.id)

        # Role permissions of the user's groups.
        group_permissions_query = (
            Permission.query.join(Permission.roles)
            .join(Role.groups)
            .filter(
                Permission.action == action,
                Permission.object == object_name,
                Group.id.in_(group_ids_query),
            )
        )

    # Role permissions of the subject.
    permissions_query = (
        Permission.query.join(Permission.roles)
        .join(Role.users if isinstance(subject, User) else Role.groups)
        .filter(
            Permission.action == action,
            Permission.object == object_name,
            subject.__class__.id == subject.id,
        )
    )

    if group_permissions_query:
        permissions_query = permissions_query.union(group_permissions_query)

    return permissions_query


@memoize_request
def has_permission(
    subject, action, object_name, object_id, check_groups=True, check_defaults=True
):
    """Check if a user or group has permission to perform a specific action.

    Checks all permissions grouped by the roles of the given subject.

    :param subject: The :class:`.User` or :class:`.Group`.
    :param action: The action to check for.
    :param object_name: The type of object.
    :param object_id: The ID of a specific object or ``None`` for a global permission.
    :param check_groups: (optional) Flag indicating whether the groups of a user should
        be checked as well for their permissions.
    :param check_defaults: (optional) Flag indicating whether the default permissions of
        any object should be checked as well.
    :return: ``True`` if permission is granted, ``False`` otherwise or if the object
        instance to check does not exist.
    """
    model = get_class_by_tablename(object_name)

    if model is None:
        return False

    permissions_query = _get_permissions(
        subject, action, object_name, check_groups=check_groups
    )

    # Check for any global action.
    if permissions_query.filter(Permission.object_id.is_(None)).first() is not None:
        return True

    if object_id is None:
        return False

    object_instance = model.query.get(object_id)

    if object_instance is None:
        return False

    # Check the default permissions.
    if check_defaults:
        default_permissions = rgetattr(object_instance, "Meta.permissions", {}).get(
            "default_permissions", {}
        )

        if action in default_permissions:
            for attr, val in default_permissions[action].items():
                if getattr(object_instance, attr, None) == val:
                    return True

    # Finally, check the regular permissions.
    return (
        permissions_query.filter(Permission.object_id == object_id).first() is not None
    )


def get_permitted_objects(
    subject, action, object_name, check_groups=True, check_defaults=True
):
    """Get all objects a user or group has a specific permission for.

    Checks all permissions grouped by the roles of the given subject.

    :param subject: The :class:`.User` or :class:`.Group`.
    :param action: The action to check for.
    :param object_name: The type of object.
    :param check_groups: (optional) Flag indicating whether the groups of a user should
        be checked as well for their permissions.
    :param check_defaults: (optional) Flag indicating whether the default permissions of
        the objects should be checked as well.
    :return: The permitted objects as query or ``None`` if the object type does not
        exist.
    """
    model = get_class_by_tablename(object_name)

    if model is None:
        return None

    permissions_query = _get_permissions(
        subject, action, object_name, check_groups=check_groups
    )

    # Check for any global action.
    if permissions_query.filter(Permission.object_id.is_(None)).first() is not None:
        return model.query

    # Get all objects for the regular permissions.
    objects_query = model.query.filter(
        model.id.in_(permissions_query.with_entities(Permission.object_id))
    )

    # Get all objects for the default permissions.
    if check_defaults:
        default_permissions = rgetattr(model, "Meta.permissions", {}).get(
            "default_permissions", {}
        )

        if action in default_permissions:
            filters = []
            for attr, val in default_permissions[action].items():
                filters.append(getattr(model, attr, None) == val)

            if filters:
                return objects_query.union(model.query.filter(db.or_(*filters)))

    return objects_query


def add_role(subject, object_name, object_id, role_name, update_timestamp=True):
    """Add an existing role to a user or group.

    :param subject: The :class:`.User` or :class:`.Group`.
    :param object_name: The type of object the role refers to.
    :param object_id: The ID of the object.
    :param role_name: The name of the role.
    :param update_timestamp: (optional) Flag indicating whether the timestamp of the
        underlying object should be updated or not. The object needs to implement
        :class:`.BaseTimestampMixin` in that case.
    :return: ``True`` if the role was added successfully, ``False`` if the subject
        already has a role related to the given object.
    :raises ValueError: If no object or role with the given arguments exists or when
        trying to add a role to the object that is being referred to by that role.
    """
    model = get_class_by_tablename(object_name)

    if model is None:
        raise ValueError(f"Object type '{object_name}' does not exist.")

    object_instance = model.query.get(object_id)

    if object_instance is None:
        raise ValueError(f"Object '{object_name}' with ID {object_id} does not exist.")

    if subject.__tablename__ == object_name and subject.id == object_id:
        raise ValueError("Cannot add a role to the object to which the role refers.")

    roles = subject.roles.filter(
        Role.object == object_name, Role.object_id == object_id
    )

    if roles.count() > 0:
        return False

    role = Role.query.filter_by(
        name=role_name, object=object_name, object_id=object_id
    ).first()

    if not role:
        raise ValueError("A role with that name does not exist.")

    with NestedTransaction(exc=IntegrityError) as t:
        subject.roles.append(role)

    if (
        t.success
        and update_timestamp
        and isinstance(object_instance, BaseTimestampMixin)
    ):
        object_instance.update_timestamp()

    return t.success


def remove_role(subject, object_name, object_id, update_timestamp=True):
    """Remove an existing role of a user or group.

    :param subject: The :class:`.User` or :class:`.Group`.
    :param object_name: The type of object the role refers to.
    :param object_id: The ID of the object.
    :param update_timestamp: (optional) Flag indicating whether the timestamp of the
        underlying object should be updated or not. The object needs to implement
        :class:`.BaseTimestampMixin` in that case.
    :return: ``True`` if the role was removed successfully, ``False`` if there was no
        role to remove.
    :raises ValueError: If no object with the given arguments exists.
    """
    model = get_class_by_tablename(object_name)

    if model is None:
        raise ValueError(f"Object type '{object_name}' does not exist.")

    object_instance = model.query.get(object_id)

    if object_instance is None:
        raise ValueError(f"Object '{object_name}' with ID {object_id} does not exist.")

    roles = subject.roles.filter(
        Role.object == object_name, Role.object_id == object_id
    )

    if roles.count() == 0:
        return False

    with NestedTransaction(exc=StaleDataError) as t:
        # As in certain circumstances (e.g. merging two users or potential race
        # conditions when adding roles) a subject may have different roles, all roles
        # related to the given object will be removed.
        for role in roles:
            subject.roles.remove(role)

    if (
        t.success
        and update_timestamp
        and isinstance(object_instance, BaseTimestampMixin)
    ):
        object_instance.update_timestamp()

    return t.success


def set_system_role(user, system_role):
    """Set an existing system role for a given user.

    :param user: The user to set the system role for.
    :param system_role: The name of the system role to set.
    :return: ``True`` if the system role was set successfully, ``False`` otherwise or if
        the given system role does not exist.
    """
    new_role = Role.query.filter_by(
        name=system_role, object=None, object_id=None
    ).first()

    if new_role is None:
        return False

    user_roles = user.roles.filter(Role.object.is_(None), Role.object_id.is_(None))

    with NestedTransaction(exc=StaleDataError) as t:
        # As in certain circumstances (e.g. merging two users) a user may have different
        # system roles, all of them will be removed.
        for role in user_roles:
            user.roles.remove(role)

    if not t.success:
        return False

    with NestedTransaction(exc=IntegrityError) as t:
        user.roles.append(new_role)

    return t.success


def setup_permissions(object_name, object_id):
    """Setup the default permissions of an object.

    The default actions and roles have to be specified in a ``Meta.permissions``
    attribute in each model.

    **Example:**

    .. code-block:: python3

        class Foo:
            class Meta:
                permissions = {
                    "actions": [
                        ("read", "Read this object."),
                        ("update", "Edit this object."),
                    ],
                    "roles": [("admin", ["read", "update"])],
                }

    :param object_name: The type of object the permissions refer to.
    :param object_id: The ID of the object.
    :raises ValueError: If no object with the given arguments exists.
    """
    model = get_class_by_tablename(object_name)

    if model is None:
        raise ValueError(f"Object type '{object_name}' does not exist.")

    object_instance = model.query.get(object_id)

    if object_instance is None:
        raise ValueError(f"Object '{object_name}' with ID {object_id} does not exist.")

    permissions = {}
    for action, _ in model.Meta.permissions["actions"]:
        permission = Permission.create(
            action=action, object=object_name, object_id=object_id
        )

        permissions[action] = permission

    for name, actions in model.Meta.permissions["roles"]:
        role = Role.create(name=name, object=object_name, object_id=object_id)

        for action in actions:
            role.permissions.append(permissions[action])


def delete_permissions(object_name, object_id):
    """Delete all permissions of an object.

    :param object_name: The type of object the permissions refer to.
    :param object_id: The ID of the object.
    """
    roles = Role.query.filter(Role.object == object_name, Role.object_id == object_id)

    for role in roles:
        db.session.delete(role)

    permissions = Permission.query.filter(
        Permission.object == object_name, Permission.object_id == object_id
    )

    for permission in permissions:
        db.session.delete(permission)


def create_role_rule(
    object_name, object_id, role_name, rule_type, condition, update_timestamp=True
):
    """Create a new role rule.

    :param object_name: The type of object the role refers to.
    :param object_id: The ID of the object.
    :param role_name: The name of the role.
    :param rule_type: The type of the role rule.
    :param condition: The condition of the role rule.
    :param update_timestamp: (optional) Flag indicating whether the timestamp of the
        underlying object should be updated or not. The object needs to implement
        :class:`.BaseTimestampMixin` in that case.
    :return: The created role rule or ``None`` if the role rule could not be created.
    """
    model = get_class_by_tablename(object_name)

    if model is None:
        return None

    object_instance = model.query.get(object_id)

    if object_instance is None:
        return None

    # Basic structure check of the condition data.
    if rule_type == RoleRuleType.USERNAME and not isinstance(condition, dict):
        return None

    role = Role.query.filter_by(
        name=role_name, object=object_name, object_id=object_id
    ).first()

    if not role:
        return None

    if update_timestamp and isinstance(object_instance, BaseTimestampMixin):
        object_instance.update_timestamp()

    return RoleRule.create(role=role, type=rule_type, condition=condition)


def remove_role_rule(role_rule, update_timestamp=True):
    """Remove an existing role rule.

    :param role_role: The role rule to remove.
    :param update_timestamp: (optional) Flag indicating whether the timestamp of the
        underlying object should be updated or not. The object needs to implement
        :class:`.BaseTimestampMixin` in that case.
    """
    role = role_rule.role

    model = get_class_by_tablename(role.object)
    object_instance = model.query.get(role.object_id)

    if update_timestamp and isinstance(object_instance, BaseTimestampMixin):
        object_instance.update_timestamp()

    db.session.delete(role_rule)


def apply_role_rule(role_rule, user=None):
    """Apply a given role rule.

    :param role_rule: The role rule to apply.
    :param user: (optional) A specific user to apply the role rule to. If not given, all
        existing users are considered.
    """
    role = role_rule.role

    if role_rule.type == RoleRuleType.USERNAME:
        identity_type = role_rule.condition.get("identity_type")
        provider = current_app.config["AUTH_PROVIDERS"].get(identity_type)

        if provider is None:
            return

        pattern = role_rule.condition.get("pattern", "")
        # As the pattern is used in a LIKE query, escape it first and then replace all
        # wildcards (*) with the ones used by the database (%).
        pattern = escape_like(pattern).replace("*", "%")

        identity_class = provider["identity_class"]
        identities_query = identity_class.query.filter(
            identity_class.username.like(pattern)
        )

        if user is not None:
            # The role only needs to be added once, even if a user has multiple matching
            # identities.
            identity = identities_query.filter(
                identity_class.user_id == user.id
            ).first()

            if identity is not None:
                add_role(identity.user, role.object, role.object_id, role.name)
        else:
            for identity in identities_query:
                add_role(identity.user, role.object, role.object_id, role.name)
