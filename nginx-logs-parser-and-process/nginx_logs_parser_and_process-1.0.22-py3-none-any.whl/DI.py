import os


class DI:
    def __init__(self):
        pass

    @staticmethod
    def project_root() -> str:
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def logs_path() -> str:
        return f"{DI.project_root()}/logs/"
