from pathlib import Path

GITIGNORE_API: str = "https://www.toptal.com/developers/gitignore/api/"
INITIAL_COMMIT: str = "fix: initial commit"
TEMPLATE_BRANCHES: list[str] = ["main", "python"]
TEMPLATE_FILES: list[Path] = [Path("entry_point.py"), Path("mkdocs.yaml")]
TEMPLATE_GIT: str = "https://github.com/liblaf/template.git"
