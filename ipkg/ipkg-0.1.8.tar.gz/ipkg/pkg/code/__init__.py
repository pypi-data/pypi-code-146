from pathlib import Path

NAME = "code"
BASE_URL = "https://packages.microsoft.com"
KEY_NAME = "microsoft.asc"
KEY_URL = f"{BASE_URL}/keys/{KEY_NAME}"
APT_DIR: Path = Path("/etc/apt")
TRUSTED_KEY_PATH = APT_DIR / "trusted.gpg.d" / "microsoft.gpg"
SOURCES_LIST_PATH: Path = APT_DIR / "sources.list.d/vscode.list"
SOURCES_LIST = f"deb {BASE_URL}/repos/code stable main"
EXTENSIONS: list[str] = [
    "aaron-bond.better-comments",
    "donjayamanne.python-extension-pack",
    "eamodio.gitlens",
    "esbenp.prettier-vscode",
    "foxundermoon.shell-format",
    "Gruntfuggly.todo-tree",
    "James-Yu.latex-workshop",
    "llvm-vs-code-extensions.vscode-clangd",
    "ms-python.isort",
    "ms-vscode.cpptools-extension-pack",
    "oderwat.indent-rainbow",
    "redhat.vscode-xml",
    "redhat.vscode-yaml",
    "streetsidesoftware.code-spell-checker",
    "tamasfe.even-better-toml",
    "WakaTime.vscode-wakatime",
    "wwm.better-align",
]
