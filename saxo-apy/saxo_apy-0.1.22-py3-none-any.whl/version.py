"""Version info."""

__all__ = "VERSION", "version_info"

VERSION = "0.1.22"


def version_info() -> str:
    """Construct version info."""
    import platform
    import sys
    from pathlib import Path

    info = {
        "saxo-apy version": VERSION,
        "install path": Path(__file__).resolve().parent,
        "python version": sys.version,
        "platform": platform.platform(),
    }
    return "".join([f"| {k}: {v} " for k, v in info.items()])
