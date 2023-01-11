import sys
from pathlib import Path
from typing import Optional

import pydantic

prefix = Path(sys.prefix)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
in_git = (PROJECT_ROOT / ".git").exists()

if in_git:
    # for development we use the prefix directory instead of the real prefix
    prefix = PROJECT_ROOT / "prefix"


domino_snippet_builtin_dir_default = prefix / "share" / "low-code-assistant" / "snippets"


class Settings(pydantic.BaseSettings):
    low_code_assistant_dev: Optional[bool]
    snowflake_user: Optional[str]
    snowflake_password: Optional[str]
    snowflake_account: Optional[str]

    redshift_host: Optional[str]
    redshift_user: Optional[str]
    redshift_password: Optional[str]

    domino_api_class: Optional[str]

    domino_user_api_key: Optional[str]
    domino_project_id: Optional[str]
    domino_project_owner: Optional[str]
    domino_project_name: Optional[str]
    domino_api_host: Optional[str]
    domino_alternative_api_host: Optional[str]
    domino_run_id: Optional[str]
    domino_hardware_tier_id: Optional[str]

    domino_working_dir: str
    domino_datasets_dir: str = "/domino/datasets/"

    domino_snippet_builtin_dir: Path = domino_snippet_builtin_dir_default

    path_translated: Optional[str]
    domino_repos_dir: Optional[str]
    domino_imported_code_dir: Optional[str]
    domino_notebook_deploy_filename = ".lca_deployed.ipynb"

    domino_is_git_based: Optional[bool]

    class Config:
        case_sensitive = False
        env_file = ".env"


settings = Settings()
