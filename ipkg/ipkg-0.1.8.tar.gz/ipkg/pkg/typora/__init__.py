from pathlib import Path

NAME: str = "typora"
KEY_URL: str = "https://typora.io/linux/public-key.asc"
APT_DIR: Path = Path("/etc/apt")
KEY_PATH: Path = APT_DIR / "trusted.gpg.d" / (NAME + ".asc")
SOURCES_LIST_PATH: Path = APT_DIR / "sources.list.d" / (NAME + ".list")
SOURCES_LIST: str = "deb https://typora.io/linux ./"
