'''
# Terraform CDK azuread Provider ~> 2.0

This repo builds and publishes the Terraform azuread Provider bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-azuread](https://www.npmjs.com/package/@cdktf/provider-azuread).

`npm install @cdktf/provider-azuread`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-azuread](https://pypi.org/project/cdktf-cdktf-provider-azuread).

`pipenv install cdktf-cdktf-provider-azuread`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Azuread](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Azuread).

`dotnet add package HashiCorp.Cdktf.Providers.Azuread`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-azuread](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-azuread).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-azuread</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-azuread-go`](https://github.com/cdktf/cdktf-provider-azuread-go) package.

`go get github.com/cdktf/cdktf-provider-azuread-go/azuread`

## Docs

Find auto-generated docs for this provider here: [./API.md](./API.md)
You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-azuread).

## Versioning

This project is explicitly not tracking the Terraform azuread Provider version 1:1. In fact, it always tracks `latest` of `~> 2.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform azuread Provider](https://github.com/terraform-providers/terraform-provider-azuread)
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
    "administrative_unit",
    "administrative_unit_member",
    "app_role_assignment",
    "application",
    "application_certificate",
    "application_federated_identity_credential",
    "application_password",
    "application_pre_authorized",
    "claims_mapping_policy",
    "conditional_access_policy",
    "custom_directory_role",
    "data_azuread_administrative_unit",
    "data_azuread_application",
    "data_azuread_application_published_app_ids",
    "data_azuread_application_template",
    "data_azuread_client_config",
    "data_azuread_directory_object",
    "data_azuread_directory_roles",
    "data_azuread_domains",
    "data_azuread_group",
    "data_azuread_groups",
    "data_azuread_service_principal",
    "data_azuread_service_principals",
    "data_azuread_user",
    "data_azuread_users",
    "directory_role",
    "directory_role_assignment",
    "directory_role_member",
    "group",
    "group_member",
    "invitation",
    "named_location",
    "provider",
    "service_principal",
    "service_principal_certificate",
    "service_principal_claims_mapping_policy_assignment",
    "service_principal_delegated_permission_grant",
    "service_principal_password",
    "synchronization_job",
    "synchronization_secret",
    "user",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import administrative_unit
from . import administrative_unit_member
from . import app_role_assignment
from . import application
from . import application_certificate
from . import application_federated_identity_credential
from . import application_password
from . import application_pre_authorized
from . import claims_mapping_policy
from . import conditional_access_policy
from . import custom_directory_role
from . import data_azuread_administrative_unit
from . import data_azuread_application
from . import data_azuread_application_published_app_ids
from . import data_azuread_application_template
from . import data_azuread_client_config
from . import data_azuread_directory_object
from . import data_azuread_directory_roles
from . import data_azuread_domains
from . import data_azuread_group
from . import data_azuread_groups
from . import data_azuread_service_principal
from . import data_azuread_service_principals
from . import data_azuread_user
from . import data_azuread_users
from . import directory_role
from . import directory_role_assignment
from . import directory_role_member
from . import group
from . import group_member
from . import invitation
from . import named_location
from . import provider
from . import service_principal
from . import service_principal_certificate
from . import service_principal_claims_mapping_policy_assignment
from . import service_principal_delegated_permission_grant
from . import service_principal_password
from . import synchronization_job
from . import synchronization_secret
from . import user
