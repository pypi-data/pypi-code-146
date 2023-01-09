import enum


class WorkingEnvironment(enum.Enum):
    GOOGLE_COLAB = "google colab"
    IPYTHON_TERMINAL = "ipython terminal"
    NOTEBOOK = "jupyter notebook"
    SCRIPT = "plain python script"
    UNKNOWN = "unknown"
