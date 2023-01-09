import os

DEFAULT_MODEL_FOLDER_PATH = os.getenv("MODEL_FOLDER_PATH", "/mnt/models")

DEFAULT_MODEL_NAME = os.getenv("MODEL_NAME", "model")

DEFAULT_MODEL_PATH = os.getenv(
    "MODEL_PATH", str(os.path.join(DEFAULT_MODEL_FOLDER_PATH, DEFAULT_MODEL_NAME))
)


KUBEFLOW_USER_ID = os.getenv("KUBEFLOW_USER_ID")

METAAI_APP = os.getenv("METAAI_APP", "f").lower() in ("1", "t", "true")

SERVING_LOG_LEVEL = os.getenv("SERVING_LOG_LEVEL", "INFO")
