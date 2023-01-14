# A default config (required when building the package).
# Declare the required fields here.
DEFAULT_CONFIG = """
[RemoteIKernelsManager]

[SSHKeysManager]
GET_SSH_KEY_SCRIPT=

[PlatformTokensManager]
BACKEND_API_ACCESS_TOKEN_LOC=
BACKEND_API_REFRESH_TOKEN_LOC=
AUTH_API = https://auth.bodo.ai

[PlatformClusterManager]
BACKEND_API = https://api.bodo.ai/api

[Security]
ALLOW_LOCAL_EXECUTION=true

[PlatformCatalogManager]
"""


import os
import configparser
import logging

config_file_loc = os.environ.get(
    "BODO_JUPYTERLAB_SERVERAPP_CONFIGFILE",
    os.path.expanduser("~/bodo_jupyterlab_serverapp.ini"),
)
logger = logging.getLogger()


config = configparser.ConfigParser()
if os.path.exists(config_file_loc):
    logger.warning(
        f"[Bodo Jupyter Server Extension] Found config file {config_file_loc}. Reading from it now..."
    )
    config.read(config_file_loc)
else:
    logger.warning(
        f"[Bodo Jupyter Server Extension] Config file {config_file_loc} not found. Loading default config..."
    )
    config.read_string(DEFAULT_CONFIG)


RemoteIKernelsManagerConfig = config["RemoteIKernelsManager"]
KERNEL_DIR = RemoteIKernelsManagerConfig.get("KERNEL_DIR", os.path.expanduser("~"))
KERNEL_NAME = RemoteIKernelsManagerConfig.get("KERNEL_NAME", "Remote-Kernel")
KERNEL_CLEANUP_PERIOD_SECONDS = RemoteIKernelsManagerConfig.getint(
    "KERNEL_CLEANUP_PERIOD_SECONDS", 10 * 60
)
KERNEL_CMD = RemoteIKernelsManagerConfig.get(
    "KERNEL_CMD", "python -m bodo_platform_ipyparallel_kernel -f {connection_file}"
)
CLUSTER_USER = RemoteIKernelsManagerConfig.get("CLUSTER_USER", "bodo")
BASTION_IP = RemoteIKernelsManagerConfig.get("BASTION_IP", None)
BASTION_USER = RemoteIKernelsManagerConfig.get("BASTION_USER", "ec2-user")

SSHKeysManagerConfig = config["SSHKeysManager"]
GET_SSH_KEY_SCRIPT = SSHKeysManagerConfig.get("GET_SSH_KEY_SCRIPT")
SSH_KEY_DIR = SSHKeysManagerConfig.get("SSH_KEY_DIR", os.path.expanduser("~"))
SSH_KEY_FILE_PREFIX = SSHKeysManagerConfig.get("SSH_KEY_FILE_PREFIX", "id_rsa-")
GET_SSH_KEY_TIMEOUT_SECONDS = SSHKeysManagerConfig.getint(
    "GET_SSH_KEY_TIMEOUT_SECONDS", 30
)
SSH_KEYS_CLEANUP_PERIOD_SECONDS = SSHKeysManagerConfig.getint(
    "SSH_KEYS_CLEANUP_PERIOD_SECONDS", 10 * 60
)

PlatformTokensManagerConfig = config["PlatformTokensManager"]
BACKEND_API_CLIENT_ID_LOC = PlatformTokensManagerConfig.get("BACKEND_API_CLIENT_ID_LOC")
BACKEND_API_SECRET_LOC = PlatformTokensManagerConfig.get("BACKEND_API_SECRET_LOC")
BACKEND_API_TOKEN_LOC = PlatformTokensManagerConfig.get("BACKEND_API_TOKEN_LOC")
AUTH_API = PlatformTokensManagerConfig.get("AUTH_API")

PlatformClusterManagerConfig = config["PlatformClusterManager"]
BACKEND_API = PlatformClusterManagerConfig.get("BACKEND_API")
NOTEBOOK_UUID = PlatformClusterManagerConfig.get("NOTEBOOK_UUID", None)
AUTO_ATTACH = PlatformClusterManagerConfig.getboolean(
    "JLAB_EXT_AUTO_ATTACH_CLUSTER", False
)
GET_CLUSTER_LIST_REFRESH_PERIOD_SECONDS = PlatformClusterManagerConfig.getint(
    "GET_CLUSTER_LIST_REFRESH_PERIOD_SECONDS", 30
)
GET_CLUSTER_INFO_REFRESH_PERIOD_SECONDS = PlatformClusterManagerConfig.getint(
    "GET_CLUSTER_INFO_REFRESH_PERIOD_SECONDS", 60
)
GET_CLUSTER_INFO_MAX_CACHE_SIZE = PlatformClusterManagerConfig.getint(
    "GET_CLUSTER_INFO_MAX_CACHE_SIZE", 64
)
GET_CLUSTER_LIST_MAX_RETRIES = PlatformClusterManagerConfig.getint(
    "GET_CLUSTER_LIST_MAX_RETRIES", 5
)
GET_CLUSTER_INFO_MAX_RETRIES = PlatformClusterManagerConfig.getint(
    "GET_CLUSTER_INFO_MAX_RETRIES", 5
)

RESUME_CLUSTER_MAX_RETRIES = PlatformClusterManagerConfig.getint(
    "RESUME_CLUSTER_MAX_RETRIES", 3
)

PAUSE_CLUSTER_MAX_RETRIES = PlatformClusterManagerConfig.getint(
    "PAUSE_CLUSTER_MAX_RETRIES", 3
)

if "Security" in config:
    SecurityConfig = config["Security"]
    ALLOW_LOCAL_EXECUTION = SecurityConfig.getboolean("ALLOW_LOCAL_EXECUTION", True)
else:
    ALLOW_LOCAL_EXECUTION=True

# CATALOG MANAGER CONFIG
PlatformCatalogManagerConfig = config["PlatformCatalogManager"]
CATALOG_MODE = PlatformCatalogManagerConfig.getboolean("CATALOG_MODE", False)
GET_CATALOG_REFRESH_PERIOD_SECONDS = PlatformCatalogManagerConfig.getint("GET_CATALOG_REFRESH_PERIOD_SECONDS", 60)
GET_CATALOG_MAX_RETRIES = PlatformCatalogManagerConfig.getint("GET_CATALOG_MAX_RETRIES", 5)



