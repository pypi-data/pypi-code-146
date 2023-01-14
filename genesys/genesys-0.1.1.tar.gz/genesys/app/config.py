import os
SVN_PARENT_PATH = os.getenv("SVN_PARENT_PATH", '/opt/svn/repositories')
SVN_PARENT_URL = os.getenv("SVN_PARENT_URL", "file:////opt/svn/repositories")
LOGIN_NAME = os.getenv("LOGIN_NAME", "email")
TEMPLATE_FILES_DIR =os.path.join(os.path.dirname(__file__), 'template_files')

ENABLE_JOB_QUEUE = os.getenv("ENABLE_JOB_QUEUE", "False").lower() == "true"
ENABLE_JOB_QUEUE_REMOTE = (
    os.getenv("ENABLE_JOB_QUEUE_REMOTE", "False").lower() == "true"
)

KEY_VALUE_STORE = {
    "host": os.getenv("KV_HOST", "localhost"),
    "port": os.getenv("KV_PORT", "6379"),
}
KV_JOB_DB_INDEX = 7