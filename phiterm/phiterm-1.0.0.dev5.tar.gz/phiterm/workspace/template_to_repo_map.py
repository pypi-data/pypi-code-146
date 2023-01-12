from typing import Dict

from phiterm.workspace.ws_enums import WorkspaceStarterTemplate

template_to_repo_map: Dict[WorkspaceStarterTemplate, str] = {
    WorkspaceStarterTemplate.aws: "https://github.com/phidatahq/starter-aws.git",
    WorkspaceStarterTemplate.aws_snowflake: "https://github.com/phidatahq/starter-aws-snowflake.git",
    WorkspaceStarterTemplate.aws_duckdb: "https://github.com/phidatahq/starter-aws-duckdb.git",
    WorkspaceStarterTemplate.aws_backend: "https://github.com/phidatahq/starter-aws-backend.git",
}
