# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Provide access to the TextGrid Authorization Service."""
import logging
from typing import Optional, List

from zeep import Client
from zeep.exceptions import Fault, TransportError

from tgclients.config import TextgridConfig

TG_STANDARD_ROLE_MANAGER = 'Projektleiter'
TG_STANDARD_ROLE_ADMINISTRATOR = 'Administrator'
TG_STANDARD_ROLE_EDITOR = 'Bearbeiter'
TG_STANDARD_ROLE_OBSERVER = 'Beobachter'

logger = logging.getLogger(__name__)
# prevent the zeep "Forcing soap:address location to HTTPS" warning
logging.getLogger('zeep.wsdl.bindings.soap').setLevel(logging.ERROR)


class TextgridAuth:
    """Provide access to the TextGrid Authorization Service."""

    def __init__(self, config: TextgridConfig = TextgridConfig()) -> None:
        self._config = config
        self._client = self._connect()
        self._extra_crud_client = self._connect_extra_crud()

    def _connect(self) -> Client:
        """Internal helper that provides a SOAP client that is configured for
        the use with the Textgrid Auth service.

        Returns:
            Client: A SOAP client
        """
        client = Client(self._config.auth_wsdl)
        # this is a dirty hack; should be remediated
        client.service._binding_options['address'] = self._config.auth_address
        return client

    def _connect_extra_crud(self) -> Client:
        """Internal helper that provides a SOAP client that is configured for
        the use with the Textgrid Auth service (the extra crud service).

        Returns:
            Client: A SOAP client
        """
        client = Client(self._config.extra_crud_wsdl)
        # this is a dirty hack; should be remediated
        client.service._binding_options['address'] = self._config.extra_crud_address
        return client

    def list_assigned_projects(self, sid: str) -> List[str]:
        """Get assigned projects.

        Args:
            sid (str): Session ID

        Raises:
            TextgridAuthException: in case of transport exceptions

        Returns:
            List: A list of project id strings
        """
        try:
            return self._client.service.tgAssignedProjects(sid)
        except TransportError as error:
            message = 'Error listing assigned projects. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from error

    def list_all_projects(self) -> List[str]:
        """Returns all projects stored in this RBAC instance with ID, name,
        and description. See also getProjectDescription(). SID
        is not needed as this information can be reviewed publicly.

        Returns:
            list: list of each project with ID, name and description
        """
        # sid is optional, so we pass empty sid
        return self._client.service.getAllProjects('')

    def get_project_description(self, project_id: str):
        """Returns name and description of project identified by ID. See also getAllProjects().

        Args:
            project_id (str): the project ID

        Returns:
            zeep.objects.projectInfo: project info with id, name and description
        """
        return self._client.service.getProjectDescription('', '', project_id)

    def create_project(self, sid: str, name: str, description: str,
                       default_owner_roles: Optional[bool] = True) -> str:
        """Create a new project

        Args:
            sid (str): TextGrid Session ID
            name (str): name of the project
            description (str): description for the project
            default_owner_roles (bool, optional): whether to assign the default roles to the owner
                                                  (editor, authority to delete). Defaults to True.

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            str: the project ID of the created project
        """
        try:
            project_id = self._client.service.createProject(auth=sid, name=name,
                                                            description=description)
        except Fault as fault:
            message = 'Error creating project. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from fault

        if default_owner_roles:
            eppn = self.get_eppn_for_sid(sid)
            self.add_editor_to_project(sid, project_id, eppn)
            self.add_admin_to_project(sid, project_id, eppn)

        return project_id

    def get_eppn_for_sid(self, sid: str) -> str:
        """Get the EPPN belonging to a sessionID

        Args:
            sid (str): TextGrid Session ID

        Raises:
            TextgridAuthException: in case of transport exceptions

        Returns:
            str: the EPPN
        """
        try:
            eppn = self._extra_crud_client.service.getEPPN(auth=sid, secret='')
        except TransportError as error:
            message = 'Error getting eppn. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from error
        return eppn

    def delete_project(self, sid: str, project_id: str) -> bool:
        """Delete a project

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            status = self._client.service.deleteProject(
                auth=sid, project=project_id)
        except Fault as fault:
            message = 'Error deleting project. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from fault
        return status

    def add_admin_to_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Give an user the admin role in a project

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._add_role_to_project(sid, project_id, eppn, TG_STANDARD_ROLE_ADMINISTRATOR)
        except TextgridAuthException as exception:
            raise exception

    def add_editor_to_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Give an user the editor role in a project

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._add_role_to_project(sid, project_id, eppn, TG_STANDARD_ROLE_EDITOR)
        except TextgridAuthException as exception:
            raise exception

    def add_manager_to_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Give an user the manager role in a project

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._add_role_to_project(sid, project_id, eppn, TG_STANDARD_ROLE_MANAGER)
        except TextgridAuthException as exception:
            raise exception

    def add_observer_to_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Give an user the observer role in a project

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._add_role_to_project(sid, project_id, eppn, TG_STANDARD_ROLE_OBSERVER)
        except TextgridAuthException as exception:
            raise exception

    def _add_role_to_project(self, sid: str, project_id: str, eppn: str, role: str) -> bool:
        rolename = role + ',' + project_id + ',Projekt-Teilnehmer'
        try:
            status = self._client.service.addMember(
                auth=sid, username=eppn, role=rolename)
        except Fault as fault:
            message = 'Error adding role to project. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from fault
        return status


class TextgridAuthException(Exception):
    """Exception communicating with tgauth"""
