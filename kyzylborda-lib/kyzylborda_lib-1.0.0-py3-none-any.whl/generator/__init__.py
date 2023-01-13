import os


__all__ = ("get_attachments_dir",)


def get_attachments_dir():
    if "KYZYLBORDA_ATTACHMENTS_DIR" not in os.environ:
        raise ValueError("Cannot find the attachments directory. Is the generator invoked via kyzylborda-generate?")
    return os.environ["KYZYLBORDA_ATTACHMENTS_DIR"]
