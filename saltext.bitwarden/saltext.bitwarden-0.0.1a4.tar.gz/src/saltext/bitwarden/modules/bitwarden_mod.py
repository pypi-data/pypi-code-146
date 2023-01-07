"""
Bitwarden execution module

This module allows access to a Bitwarden vault.

:depends: dateparser, pyhumps, validators

This module requires the ``bw`` Bitwarden CLI utility to be installed.
Installation instructions are available
`here <https://bitwarden.com/help/cli/#download-and-install>`_.

This module primarily relies on the `Bitwarden Vault Management API
<https://bitwarden.com/help/vault-management-api/>`_ running locally on the minion
using the ``bw serve`` feature of the Bitwarden CLI utility, as well as the
`Bitwarden Public (Organization Management) API
<https://bitwarden.com/help/api/>`_ for its functionality. A
small number of functions also rely on executing the `bw` client directly
(mostly for login/logout since those methods are not exposed through any other
API).

.. warning::
    The Bitwarden Vault Management API running on the minion, once the vault is
    unlocked, has no authentication or other protection. All traffic is
    unencrypted. Any users who access HTTP server or observe traffic to it
    can gain access to the contents of the entire vault.

    Please ensure you take adequate measures to protect the HTTP server, such as
    ensuring it only binds to localhost, using firewall rules to limit access to
    the port to specific users (where possible), and limiting which users have
    access to any system on which it is running.

This module also requires a configuration profile to be configured in either the
minion or master configuration file.

Configuration example:

.. code-block:: yaml

    my-bitwarden-vault:
      driver: bitwarden
      cli_path: /bin/bw
      cli_conf_dir: /etc/salt/.bitwarden
      vault_url: https://bitwarden.com
      email: user@example.com
      password: CorrectHorseBatteryStaple
      vault_api_url: http://localhost:8087
      public_api_url: https://api.bitwarden.com
      client_id: user.25fa6fc6-deeb-4b42-a279-5e680b51aa58
      client_secret: AofieD0oexiex1mie3eigi9oojooF3
      org_client_id: organization.d0e19db4-38aa-4284-be3d-e80cff306e6c
      org_client_secret: aWMk2MBf4NWXfaevrKyxa3uqNXYVQy

The ``driver`` refers to the Bitwarden module, and must be set to ``bitwarden``
in order to use this driver.

Other configuration options:

cli_path: ``None``
    The path to the bitwarden cli binary on the local system. If set to ``None``
    the module will use ``bw`` (Unix-like) or ``bw.exe`` (Windows) from the Salt
    user's `PATH`.

cli_conf_dir: ``None``
    The path specifying a folder where the Bitwarden CLI will store configuration
    data.

vault_url: ``https://bitwarden.com``
    The URL for the Bitwarden vault.

email: ``None``
    The email address of the Bitwarden account to use.

password: ``None``
    The master password for the Bitwarden vault.

vault_api_url: ``http://localhost:8087``
    The URL for the Bitwarden Vault Management API.

public_api_url: ``https://api.bitwarden.com``
    The URL for the Bitwarden Bitwarden Public (Organization Management) API.

client_id: ``None``
    The OAUTH client_id

client_secret: ``None``
    The OAUTH client_secret

org_client_id: ``None``
    The OAUTH organizational client_id

org_client_secret: ``None``
    The OAUTH organizational client_secret

"""
import logging

import saltext.bitwarden.utils.bitwarden_mod as utils

log = logging.getLogger(__name__)

__virtualname__ = "bitwarden"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The bitwarden execution module is not implemented yet")
    return __virtualname__


def _get_config(profile=None):  # pylint: disable=C0116
    config = {}
    if profile:
        config = __salt__["config.get"](profile)
        if config.get("driver") != "bitwarden":
            log.error("The specified profile is not a bitwarden profile")
            return {}
    else:
        config = __salt__["config.get"]("bitwarden")
    if not config:
        log.debug("The config is not set")
        return {}

    return config


def login(profile=None):
    """
    Login to Bitwarden vault

    CLI Example:

    .. code-block:: bash

        salt '*' bitwarden.login
    """
    opts = _get_config(profile=profile)
    return utils.login(opts=opts)


def logout(profile=None):
    """
    Logout of Bitwarden vault

    CLI Example:

    .. code-block:: bash

        salt '*' bitwarden.logout
    """
    opts = _get_config(profile=profile)
    return utils.logout(opts=opts)


def lock(profile=None):
    """
    Lock the Bitwarden vault

    CLI Example:

    .. code-block:: bash

        salt '*' bitwarden.lock
    """
    opts = _get_config(profile=profile)
    return utils.lock(opts=opts)


def unlock(profile=None):
    """
    Unlock the Bitwarden vault

    CLI Example:

    .. code-block:: bash

        salt '*' bitwarden.unlock
    """
    opts = _get_config(profile=profile)
    return utils.unlock(opts=opts)
