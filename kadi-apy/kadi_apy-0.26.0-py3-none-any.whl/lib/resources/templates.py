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
from kadi_apy.lib import commons
from kadi_apy.lib.resource import Resource


class Template(Resource):
    r"""Model to represent templates.

    :param manager: Manager to use for all API requests.
    :type manager: KadiManager
    :param type: Type of the template. Can either be ``record`` or ``extras``.
    :type type: str
    :param data: Dict in case of a record template or a list in case of a extras
        template containing the content for the template.
    :param id: The ID of an existing resource.
    :type id: int, optional
    :param identifier: The unique identifier of a new or existing resource,
        which is only relevant if no ID was given. If present, the identifier will be
        used to check for an existing resource instead. If no existing resource could be
        found or the resource to check does not use a unique identifier, it will be used
        to create a new resource instead, together with the additional metadata. The
        identifier is adjusted if it contains spaces, invalid characters or exceeds the
        length of 50 valid characters.
    :type identifier: str, optional
    :param skip_request: Flag to skip the initial request.
    :type skip_request: bool, optional
    :param create: Flag to determine if a resource should be created in case
        a identifier is given and the resource does not exist.
    :type create: bool, optional
    :param \**kwargs: Additional metadata of the new resource to create.
    :type \**kwargs: dict
    """

    base_path = "/templates"
    name = "template"

    def set_attribute(self, attribute, value):
        """Set attribute.

        :param attribute: The attribute to set.
        :type attribute: str
        :param value: The value of the attribute.
        :return: The response object.
        """

        return commons.set_attribute(self, attribute, value)

    def get_users(self, **params):
        r"""Get users from a template. Supports pagination.

        :param \**params: Additional parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/roles/users"
        return self._get(endpoint, params=params)

    def add_user(self, user_id, role_name):
        r"""Add a user to a template.

        :param user_id: The ID of the user to add.
        :type user_id: int
        :param role_name: Role of the user.
        :type role_name: str
        :return: The response object.
        """

        return commons.add_user(self, user_id, role_name)

    def remove_user(self, user_id):
        """Remove a user from a template.

        :param user_id: The ID of the user to remove.
        :type user_id: int
        :return: The response object.
        """

        return commons.remove_user(self, user_id)

    def change_user_role(self, user_id, role_name):
        """Change user role.

        :param user_id: The ID of the user whose role should be changed.
        :type user_id: int
        :param role_name: Name of the new role.
        :type role_name: str
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/roles/users/{user_id}"
        data = {"name": role_name}
        return self._patch(endpoint, json=data)

    def get_groups(self, **params):
        r"""Get group roles from a template. Supports pagination.

        :param \**params: Additional parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/roles/groups"
        return self._get(endpoint, params=params)

    def add_group_role(self, group_id, role_name):
        """Add a group role to a template.

        :param group_id: The ID of the group to add.
        :type group_id: int
        :param role_name: Role of the group.
        :type role_name: str
        :return: The response object.
        """

        return commons.add_group_role(self, group_id, role_name)

    def remove_group_role(self, group_id):
        """Remove a group role from a template.

        :param group_id: The ID of the group to remove.
        :type group_id: int
        :return: The response object.
        """

        return commons.remove_group_role(self, group_id)

    def change_group_role(self, group_id, role_name):
        """Change group role.

        :param group_id: The ID of the group whose role should be changed.
        :type group_id: int
        :param role_name: Name of the new role.
        :type role_name: str
        :return: The response object.
        """

        return commons.change_group_role(self, group_id, role_name)

    def export(self, path, export_type="json", pipe=False, **params):
        r"""Export the template using a specific export type.

        :param path: The path (including name of the file) to store the exported data.
        :type path: str
        :param export_type: The export format.
        :type export_type: str
        :param pipe: If ``True``, nothing is written here.
        :type pipe: bool
        :param \**params: Additional parameters.
        :return: The response object.
        """
        return commons.export(self, path, export_type=export_type, pipe=pipe, **params)
