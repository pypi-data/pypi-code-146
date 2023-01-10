# Version
POKIE_VERSION = ["0", "3", "5"]


def get_version():
    return ".".join(POKIE_VERSION)


# Http Codes
HTTP_OK = 200
HTTP_BADREQ = 400
HTTP_NOAUTH = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_ERROR = 500

# DI Keys
DI_CONFIG = "config"
DI_FLASK = "app"
DI_APP = "main"
DI_MODULES = "modules"
DI_SERVICES = "svc_manager"
DI_DB = "db"
DI_REDIS = "redis"
DI_EVENTS = "event_manager"
DI_TTY = "tty"
DI_SIGNAL = "signal"

# DB Configuration
CFG_DB_NAME = "db_name"
CFG_DB_HOST = "db_host"
CFG_DB_PORT = "db_port"
CFG_DB_USER = "db_user"
CFG_DB_PASSWORD = "db_password"
CFG_DB_SSL = "db_ssl"

# Redis Configuration
CFG_REDIS_HOST = "redis_host"
CFG_REDIS_PORT = "redis_port"
CFG_REDIS_PASSWORD = "redis_password"
CFG_REDIS_DB = "redis_db"
CFG_REDIS_SSL = "redis_ssl"

# Auth Configuration
CFG_AUTH_SECRET = "auth_secret"


# SMTP Configuration
CFG_SMTP_HOST = "smtp_host"
CFG_SMTP_PORT = "smtp_port"
CFG_SMTP_USE_TLS = "smtp_use_tls"
CFG_SMTP_USE_SSL = "smtp_use_ssl"
CFG_SMTP_DEBUG = "smtp_debug"
CFG_SMTP_USERNAME = "smtp_username"
CFG_SMTP_PASSWORD = "smtp_password"
CFG_SMTP_DEFAULT_SENDER = "smtp_default_sender"
CFG_SMTP_TIMEOUT = "smtp_timeout"
CFG_SMTP_SSL_KEYFILE = "smtp_ssl_keyfile"
CFG_SMTP_SSL_CERTFILE = "smtp_ssl_certfile"
