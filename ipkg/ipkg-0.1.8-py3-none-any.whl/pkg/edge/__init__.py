from pathlib import Path

NAME = "microsoft-edge-stable"
BASE_URL = "https://packages.microsoft.com"
KEY_NAME = "microsoft.asc"
KEY_URL = f"{BASE_URL}/keys/{KEY_NAME}"
APT_DIR: Path = Path("/etc/apt")
TRUSTED_KEY_PATH = APT_DIR / "trusted.gpg.d" / "microsoft-edge.gpg"
SOURCES_LIST_PATH: Path = APT_DIR / "sources.list.d" / "microsoft-edge.list"
SOURCES_LIST = f"deb {BASE_URL}/repos/edge stable main"
