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
from flask import request
from flask_babel import lazy_gettext as _l

import kadi.lib.constants as const
from .core import BaseProvider
from kadi.lib.conversion import recode_string
from kadi.lib.utils import find_dict_in_list
from kadi.lib.utils import named_tuple
from kadi.modules.accounts.models import ShibIdentity


class ShibProvider(BaseProvider):
    """Shibboleth authentication provider.

    Currently tested with the official "Shibboleth Service Provider 3" in combination
    with the Apache web server using "mod_shib".
    """

    class Meta:
        """Container to store meta class attributes."""

        provider_type = const.AUTH_PROVIDER_TYPE_SHIB
        """The type of the provider."""

        defaults = {
            "title": _l("Login with Shibboleth"),
            "default_system_role": "member",
            "env_encoding": "latin-1",
            "multivalue_separator": ";",
            "sp_entity_id": "/shibboleth",
            "sp_session_initiator": "/Shibboleth.sso/Login",
            "sp_logout_initiator": "/Shibboleth.sso/Logout",
            "idp_entity_id_attr": "Shib-Identity-Provider",
            "idp_displayname_attr": "Meta-displayName",
            "idp_support_contact_attr": "Meta-supportContact",
            "username_attr": "eppn",
            "email_attr": "mail",
            "displayname_attr": "displayName",
            "firstname_attr": "givenName",
            "lastname_attr": "sn",
            "idps": [],
        }
        """The default configuration values of the provider.

        The configured identity providers (``"idps"``) must be specified as a list of
        dictionaries, each dictionary containing the entity ID (``"entity_id"``) and
        display name (``"name"``) of the provider.
        """

    @classmethod
    def _get_current_environment(cls):
        try:
            return request.environ
        except:
            return {}

    @classmethod
    def _get_env_value(cls, key, multivalued=False):
        config = cls.get_config()
        environ = cls._get_current_environment()

        value = environ.get(key)

        env_encoding = config["env_encoding"]
        if env_encoding != "utf-8":
            # Environment variables may not always be utf-8 encoded, at least those
            # coming from Apache seem to be not.
            value = recode_string(value, from_encoding=env_encoding)

        # We currently assume that multivalied attributes are separated via simple
        # characters or strings.
        if multivalued and value is not None:
            return value.split(config["multivalue_separator"])

        return value

    @classmethod
    def get_choices(cls):
        """Get all configured identity providers for use in a selection.

        :return: A list of tuples, each tuple containing the entity ID and display name
            of the identity provider, sorted by display name. The first entry in the
            list represents the empty default choice in a selection where both values
            are set to an empty string. If this provider is not registered in the
            application, the returned list will only contain the default choice.
        """
        if not cls.is_registered():
            return [("", "")]

        config = cls.get_config()

        choices = []
        for idp in config["idps"]:
            choices.append((idp.get("entity_id", ""), idp.get("name", "")))

        choices = sorted(choices, key=lambda x: x[1])
        choices.insert(0, ("", ""))
        return choices

    @classmethod
    def get_session_initiator(cls, entity_id, target):
        """Get the configured Shibboleth session initiator.

        The session initiator is simply an URL consisting of the configured login
        endpoint of the service provider and containing the given arguments, the
        ``entity_id`` and ``target`` URL, as query parameters.

        :param entity_id: The entity ID of the identity provider to use for login.
        :param target: The URL to redirect to after logging in successfully.
        :return: The generated session initiator URL. If this provider is not registered
            in the application, an empty string will be returned.
        """
        if not cls.is_registered():
            return ""

        config = cls.get_config()
        return f"{config['sp_session_initiator']}?entityID={entity_id}&target={target}"

    @classmethod
    def get_logout_initiator(cls, target):
        """Get the configured Shibboleth local logout initiator.

        The local logout initiator is simply an URL consisting of the configured logout
        endpoint of the service provider and containing the given argument, the
        ``target`` URL, as query parameter.

        :param target: The URL to redirect to after logging out successfully.
        :return: The generated local logout initiator URL. If this provider is not
            registered in the application, an empty string will be returned.
        """
        if not cls.is_registered():
            return ""

        return f"{cls.get_config()['sp_logout_initiator']}?return={target}"

    @classmethod
    def contains_valid_idp(cls):
        """Check if the Shibboleth session contains a valid identity provider.

        In this case, valid means that the entity ID of an identity provider is
        contained in the configured list of identity providers. This requires the entity
        ID to check to be available as an environment variable, so a valid Shibboleth
        session is required.

        :return: ``True`` if the identity provider is valid, ``False`` if it is not or
            if there is no valid Shibboleth session or if this provider is not
            registered in the application.
        """
        if not cls.is_registered():
            return False

        config = cls.get_config()
        environ = cls._get_current_environment()

        entity_id = environ.get(config["idp_entity_id_attr"])
        if entity_id is not None:
            idp = find_dict_in_list(config["idps"], "entity_id", entity_id)
            return idp is not None

        return False

    @classmethod
    def get_metadata(cls):
        """Get the metadata of the Shibboleth session.

        :return: An object containing the entity ID of the service provider, the entity
            ID of the identity provider, its displayname and its support contact email
            address as attributes ``sp_entity_id``, ``idp_entity_id``,
            ``idp_displayname`` and ``idp_support_contact`` respectively.  This requires
            those attributes to be available as an environment variables, so a valid
            Shibboleth session is required. If this provider is not registered in the
            application, ``None`` will be returned.
        """
        if not cls.is_registered():
            return None

        config = cls.get_config()

        sp_entity_id = request.url_root[:-1] + config["sp_entity_id"]
        idp_entity_id = cls._get_env_value(config["idp_entity_id_attr"])
        idp_displayname = cls._get_env_value(config["idp_displayname_attr"])
        idp_support_contact = cls._get_env_value(config["idp_support_contact_attr"])

        if idp_support_contact is not None:
            # The contact email address should generally be specified as a "mailto:"
            # attribute, so we extract the actual email address.
            parts = idp_support_contact.split(":", 1)
            if len(parts) > 1:
                idp_support_contact = parts[1]

        return named_tuple(
            "ShibMeta",
            sp_entity_id=sp_entity_id,
            idp_entity_id=idp_entity_id,
            idp_displayname=idp_displayname,
            idp_support_contact=idp_support_contact,
        )

    @classmethod
    def get_required_attributes(cls):
        """Get all attributes required for successful authentication.

        Currently, the only required attributes are the user's unique username and email
        address.

        :return: A dictionary containing the required keys to get as environment
            variables and their respective values. If the identity provider did not
            provide an attribute, the value will be ``None`` for the respective key or
            for all of them if no valid Shibboleth session exists. If this provider is
            not registered in the application, ``None`` will be returned.
        """
        if not cls.is_registered():
            return None

        config = cls.get_config()

        username = cls._get_env_value(config["username_attr"])
        emails = cls._get_env_value(config["email_attr"], multivalued=True)

        return {
            config["username_attr"]: username,
            config["email_attr"]: emails[0] if emails is not None else emails,
        }

    @classmethod
    def register(
        cls,
        *,
        username,
        email,
        displayname,
        system_role=None,
        apply_role_rules=True,
        **kwargs,
    ):
        """Register a new Shibboleth user.

        If an identity with the given ``username`` already exists, that identity will be
        updated with the given ``email``.

        Note that this function may issue a database commit or rollback.

        :param username: The user's unique name.
        :param email: The user's email address.
        :param displayname: The user's display name.
        :param system_role: (optional) The user's system role. Defaults to ``"member"``.
        :param apply_role_rules: (optional) Flag indicating whether to apply all
            existing role rules to the newly registered user.
        :return: A new :class:`.ShibIdentity` object linked with a new user or an
            existing, updated :class:`.ShibIdentity`. Returns ``None`` if the identity
            could not be created or if this provider is not registered in the
            application.
        """
        # pylint: disable=arguments-differ
        if not cls.is_registered():
            return None

        config = cls.get_config()
        identity = ShibIdentity.query.filter_by(username=username).first()

        if identity:
            identity.email = email
            return identity

        system_role = (
            system_role if system_role is not None else config["default_system_role"]
        )
        return cls.create_identity(
            system_role=system_role,
            identity_model=ShibIdentity,
            apply_role_rules=apply_role_rules,
            username=username,
            email=email,
            displayname=displayname,
        )

    @classmethod
    def authenticate(cls, **kwargs):
        """Authenticate a Shibboleth user.

        No arguments need to be given, as the necessary user attributes need to be
        available as environment variables if a valid Shibboleth session exists.

        :return: An instance of :class:`.UserInfo` or ``None`` if this provider is not
            registered in the application. In case the authentication is successful, the
            contained data is an object containing the username, email and display name
            of the user as attributes ``username``, ``email`` and ``displayname``
            respectively.
        """
        # pylint: disable=arguments-differ
        if not cls.is_registered():
            return None

        config = cls.get_config()

        username = cls._get_env_value(config["username_attr"])
        emails = cls._get_env_value(config["email_attr"], multivalued=True)

        if username is None or emails is None:
            return cls.UserInfo(False)

        displayname = cls._get_env_value(config["displayname_attr"])

        if displayname is None:
            firstname = cls._get_env_value(config["firstname_attr"], multivalued=True)
            lastname = cls._get_env_value(config["lastname_attr"], multivalued=True)

            if firstname is not None and lastname is not None:
                displayname = f"{' '.join(firstname)} {' '.join(lastname)}"

        if displayname is None:
            displayname = username

        shib_info = named_tuple(
            "ShibInfo", username=username, email=emails[0], displayname=displayname
        )

        return cls.UserInfo(True, shib_info)

    @classmethod
    def change_password(cls, username, old_password, new_password):
        raise NotImplementedError
