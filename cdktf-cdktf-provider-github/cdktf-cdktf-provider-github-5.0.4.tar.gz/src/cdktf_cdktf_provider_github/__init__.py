'''
# Terraform CDK github Provider ~> 5.0

This repo builds and publishes the Terraform github Provider bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-github](https://www.npmjs.com/package/@cdktf/provider-github).

`npm install @cdktf/provider-github`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-github](https://pypi.org/project/cdktf-cdktf-provider-github).

`pipenv install cdktf-cdktf-provider-github`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Github](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Github).

`dotnet add package HashiCorp.Cdktf.Providers.Github`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-github](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-github).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-github</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-github-go`](https://github.com/cdktf/cdktf-provider-github-go) package.

`go get github.com/cdktf/cdktf-provider-github-go/github`

## Docs

Find auto-generated docs for this provider here: [./API.md](./API.md)
You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-github).

## Versioning

This project is explicitly not tracking the Terraform github Provider version 1:1. In fact, it always tracks `latest` of `~> 5.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform github Provider](https://github.com/terraform-providers/terraform-provider-github)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [terraform cdk](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### projen

This is mostly based on [projen](https://github.com/eladb/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on projen

There's a custom [project builder](https://github.com/hashicorp/cdktf-provider-project) which encapsulate the common settings for all `cdktf` providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [Repository Manager](https://github.com/hashicorp/cdktf-repository-manager/)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

__all__ = [
    "actions_environment_secret",
    "actions_organization_oidc_subject_claim_customization_template",
    "actions_organization_permissions",
    "actions_organization_secret",
    "actions_organization_secret_repositories",
    "actions_repository_access_level",
    "actions_repository_oidc_subject_claim_customization_template",
    "actions_repository_permissions",
    "actions_runner_group",
    "actions_secret",
    "app_installation_repositories",
    "app_installation_repository",
    "branch",
    "branch_default",
    "branch_protection",
    "branch_protection_v3",
    "data_github_actions_organization_oidc_subject_claim_customization_template",
    "data_github_actions_organization_registration_token",
    "data_github_actions_organization_secrets",
    "data_github_actions_public_key",
    "data_github_actions_registration_token",
    "data_github_actions_repository_oidc_subject_claim_customization_template",
    "data_github_actions_secrets",
    "data_github_app",
    "data_github_branch",
    "data_github_collaborators",
    "data_github_dependabot_organization_secrets",
    "data_github_dependabot_public_key",
    "data_github_dependabot_secrets",
    "data_github_enterprise",
    "data_github_external_groups",
    "data_github_ip_ranges",
    "data_github_membership",
    "data_github_organization",
    "data_github_organization_ip_allow_list",
    "data_github_organization_team_sync_groups",
    "data_github_organization_teams",
    "data_github_organization_webhooks",
    "data_github_ref",
    "data_github_release",
    "data_github_repositories",
    "data_github_repository",
    "data_github_repository_branches",
    "data_github_repository_deploy_keys",
    "data_github_repository_file",
    "data_github_repository_milestone",
    "data_github_repository_pull_request",
    "data_github_repository_pull_requests",
    "data_github_repository_teams",
    "data_github_repository_webhooks",
    "data_github_team",
    "data_github_tree",
    "data_github_user",
    "data_github_users",
    "dependabot_organization_secret",
    "dependabot_organization_secret_repositories",
    "dependabot_secret",
    "emu_group_mapping",
    "enterprise_organization",
    "issue",
    "issue_label",
    "membership",
    "organization_block",
    "organization_project",
    "organization_security_manager",
    "organization_settings",
    "organization_webhook",
    "project_card",
    "project_column",
    "provider",
    "release",
    "repository",
    "repository_autolink_reference",
    "repository_collaborator",
    "repository_deploy_key",
    "repository_environment",
    "repository_file",
    "repository_milestone",
    "repository_project",
    "repository_pull_request",
    "repository_tag_protection",
    "repository_webhook",
    "team",
    "team_members",
    "team_membership",
    "team_repository",
    "team_settings",
    "team_sync_group_mapping",
    "user_gpg_key",
    "user_invitation_accepter",
    "user_ssh_key",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import actions_environment_secret
from . import actions_organization_oidc_subject_claim_customization_template
from . import actions_organization_permissions
from . import actions_organization_secret
from . import actions_organization_secret_repositories
from . import actions_repository_access_level
from . import actions_repository_oidc_subject_claim_customization_template
from . import actions_repository_permissions
from . import actions_runner_group
from . import actions_secret
from . import app_installation_repositories
from . import app_installation_repository
from . import branch
from . import branch_default
from . import branch_protection
from . import branch_protection_v3
from . import data_github_actions_organization_oidc_subject_claim_customization_template
from . import data_github_actions_organization_registration_token
from . import data_github_actions_organization_secrets
from . import data_github_actions_public_key
from . import data_github_actions_registration_token
from . import data_github_actions_repository_oidc_subject_claim_customization_template
from . import data_github_actions_secrets
from . import data_github_app
from . import data_github_branch
from . import data_github_collaborators
from . import data_github_dependabot_organization_secrets
from . import data_github_dependabot_public_key
from . import data_github_dependabot_secrets
from . import data_github_enterprise
from . import data_github_external_groups
from . import data_github_ip_ranges
from . import data_github_membership
from . import data_github_organization
from . import data_github_organization_ip_allow_list
from . import data_github_organization_team_sync_groups
from . import data_github_organization_teams
from . import data_github_organization_webhooks
from . import data_github_ref
from . import data_github_release
from . import data_github_repositories
from . import data_github_repository
from . import data_github_repository_branches
from . import data_github_repository_deploy_keys
from . import data_github_repository_file
from . import data_github_repository_milestone
from . import data_github_repository_pull_request
from . import data_github_repository_pull_requests
from . import data_github_repository_teams
from . import data_github_repository_webhooks
from . import data_github_team
from . import data_github_tree
from . import data_github_user
from . import data_github_users
from . import dependabot_organization_secret
from . import dependabot_organization_secret_repositories
from . import dependabot_secret
from . import emu_group_mapping
from . import enterprise_organization
from . import issue
from . import issue_label
from . import membership
from . import organization_block
from . import organization_project
from . import organization_security_manager
from . import organization_settings
from . import organization_webhook
from . import project_card
from . import project_column
from . import provider
from . import release
from . import repository
from . import repository_autolink_reference
from . import repository_collaborator
from . import repository_deploy_key
from . import repository_environment
from . import repository_file
from . import repository_milestone
from . import repository_project
from . import repository_pull_request
from . import repository_tag_protection
from . import repository_webhook
from . import team
from . import team_members
from . import team_membership
from . import team_repository
from . import team_settings
from . import team_sync_group_mapping
from . import user_gpg_key
from . import user_invitation_accepter
from . import user_ssh_key
