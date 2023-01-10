'''
# Terraform CDK vault Provider ~> 3.7

This repo builds and publishes the Terraform vault Provider bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-vault](https://www.npmjs.com/package/@cdktf/provider-vault).

`npm install @cdktf/provider-vault`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-vault](https://pypi.org/project/cdktf-cdktf-provider-vault).

`pipenv install cdktf-cdktf-provider-vault`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Vault](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Vault).

`dotnet add package HashiCorp.Cdktf.Providers.Vault`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-vault](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-vault).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-vault</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-vault-go`](https://github.com/cdktf/cdktf-provider-vault-go) package.

`go get github.com/cdktf/cdktf-provider-vault-go/vault`

## Docs

Find auto-generated docs for this provider here: [./API.md](./API.md)
You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-vault).

## Versioning

This project is explicitly not tracking the Terraform vault Provider version 1:1. In fact, it always tracks `latest` of `~> 3.7` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform vault Provider](https://github.com/terraform-providers/terraform-provider-vault)
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
    "ad_secret_backend",
    "ad_secret_library",
    "ad_secret_role",
    "alicloud_auth_backend_role",
    "approle_auth_backend_login",
    "approle_auth_backend_role",
    "approle_auth_backend_role_secret_id",
    "audit",
    "auth_backend",
    "aws_auth_backend_cert",
    "aws_auth_backend_client",
    "aws_auth_backend_identity_whitelist",
    "aws_auth_backend_login",
    "aws_auth_backend_role",
    "aws_auth_backend_role_tag",
    "aws_auth_backend_roletag_blacklist",
    "aws_auth_backend_sts_role",
    "aws_secret_backend",
    "aws_secret_backend_role",
    "azure_auth_backend_config",
    "azure_auth_backend_role",
    "azure_secret_backend",
    "azure_secret_backend_role",
    "cert_auth_backend_role",
    "consul_secret_backend",
    "consul_secret_backend_role",
    "data_vault_ad_access_credentials",
    "data_vault_approle_auth_backend_role_id",
    "data_vault_auth_backend",
    "data_vault_aws_access_credentials",
    "data_vault_azure_access_credentials",
    "data_vault_gcp_auth_backend_role",
    "data_vault_generic_secret",
    "data_vault_identity_entity",
    "data_vault_identity_group",
    "data_vault_identity_oidc_client_creds",
    "data_vault_identity_oidc_openid_config",
    "data_vault_identity_oidc_public_keys",
    "data_vault_kubernetes_auth_backend_config",
    "data_vault_kubernetes_auth_backend_role",
    "data_vault_kubernetes_service_account_token",
    "data_vault_kv_secret",
    "data_vault_kv_secret_subkeys_v2",
    "data_vault_kv_secret_v2",
    "data_vault_kv_secrets_list",
    "data_vault_kv_secrets_list_v2",
    "data_vault_nomad_access_token",
    "data_vault_policy_document",
    "data_vault_raft_autopilot_state",
    "data_vault_transform_decode",
    "data_vault_transform_encode",
    "data_vault_transit_decrypt",
    "data_vault_transit_encrypt",
    "database_secret_backend_connection",
    "database_secret_backend_role",
    "database_secret_backend_static_role",
    "database_secrets_mount",
    "egp_policy",
    "gcp_auth_backend",
    "gcp_auth_backend_role",
    "gcp_secret_backend",
    "gcp_secret_roleset",
    "gcp_secret_static_account",
    "generic_endpoint",
    "generic_secret",
    "github_auth_backend",
    "github_team",
    "github_user",
    "identity_entity",
    "identity_entity_alias",
    "identity_entity_policies",
    "identity_group",
    "identity_group_alias",
    "identity_group_member_entity_ids",
    "identity_group_member_group_ids",
    "identity_group_policies",
    "identity_mfa_duo",
    "identity_mfa_login_enforcement",
    "identity_mfa_okta",
    "identity_mfa_pingid",
    "identity_mfa_totp",
    "identity_oidc",
    "identity_oidc_assignment",
    "identity_oidc_client",
    "identity_oidc_key",
    "identity_oidc_key_allowed_client_id",
    "identity_oidc_provider",
    "identity_oidc_role",
    "identity_oidc_scope",
    "jwt_auth_backend",
    "jwt_auth_backend_role",
    "kmip_secret_backend",
    "kmip_secret_role",
    "kmip_secret_scope",
    "kubernetes_auth_backend_config",
    "kubernetes_auth_backend_role",
    "kubernetes_secret_backend",
    "kubernetes_secret_backend_role",
    "kv_secret",
    "kv_secret_backend_v2",
    "kv_secret_v2",
    "ldap_auth_backend",
    "ldap_auth_backend_group",
    "ldap_auth_backend_user",
    "managed_keys",
    "mfa_duo",
    "mfa_okta",
    "mfa_pingid",
    "mfa_totp",
    "mount",
    "namespace",
    "nomad_secret_backend",
    "nomad_secret_role",
    "okta_auth_backend",
    "okta_auth_backend_group",
    "okta_auth_backend_user",
    "password_policy",
    "pki_secret_backend_cert",
    "pki_secret_backend_config_ca",
    "pki_secret_backend_config_urls",
    "pki_secret_backend_crl_config",
    "pki_secret_backend_intermediate_cert_request",
    "pki_secret_backend_intermediate_set_signed",
    "pki_secret_backend_role",
    "pki_secret_backend_root_cert",
    "pki_secret_backend_root_sign_intermediate",
    "pki_secret_backend_sign",
    "policy",
    "provider",
    "quota_lease_count",
    "quota_rate_limit",
    "rabbitmq_secret_backend",
    "rabbitmq_secret_backend_role",
    "raft_autopilot",
    "raft_snapshot_agent_config",
    "rgp_policy",
    "ssh_secret_backend_ca",
    "ssh_secret_backend_role",
    "terraform_cloud_secret_backend",
    "terraform_cloud_secret_creds",
    "terraform_cloud_secret_role",
    "token",
    "token_auth_backend_role",
    "transform_alphabet",
    "transform_role",
    "transform_template",
    "transform_transformation",
    "transit_secret_backend_key",
    "transit_secret_cache_config",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import ad_secret_backend
from . import ad_secret_library
from . import ad_secret_role
from . import alicloud_auth_backend_role
from . import approle_auth_backend_login
from . import approle_auth_backend_role
from . import approle_auth_backend_role_secret_id
from . import audit
from . import auth_backend
from . import aws_auth_backend_cert
from . import aws_auth_backend_client
from . import aws_auth_backend_identity_whitelist
from . import aws_auth_backend_login
from . import aws_auth_backend_role
from . import aws_auth_backend_role_tag
from . import aws_auth_backend_roletag_blacklist
from . import aws_auth_backend_sts_role
from . import aws_secret_backend
from . import aws_secret_backend_role
from . import azure_auth_backend_config
from . import azure_auth_backend_role
from . import azure_secret_backend
from . import azure_secret_backend_role
from . import cert_auth_backend_role
from . import consul_secret_backend
from . import consul_secret_backend_role
from . import data_vault_ad_access_credentials
from . import data_vault_approle_auth_backend_role_id
from . import data_vault_auth_backend
from . import data_vault_aws_access_credentials
from . import data_vault_azure_access_credentials
from . import data_vault_gcp_auth_backend_role
from . import data_vault_generic_secret
from . import data_vault_identity_entity
from . import data_vault_identity_group
from . import data_vault_identity_oidc_client_creds
from . import data_vault_identity_oidc_openid_config
from . import data_vault_identity_oidc_public_keys
from . import data_vault_kubernetes_auth_backend_config
from . import data_vault_kubernetes_auth_backend_role
from . import data_vault_kubernetes_service_account_token
from . import data_vault_kv_secret
from . import data_vault_kv_secret_subkeys_v2
from . import data_vault_kv_secret_v2
from . import data_vault_kv_secrets_list
from . import data_vault_kv_secrets_list_v2
from . import data_vault_nomad_access_token
from . import data_vault_policy_document
from . import data_vault_raft_autopilot_state
from . import data_vault_transform_decode
from . import data_vault_transform_encode
from . import data_vault_transit_decrypt
from . import data_vault_transit_encrypt
from . import database_secret_backend_connection
from . import database_secret_backend_role
from . import database_secret_backend_static_role
from . import database_secrets_mount
from . import egp_policy
from . import gcp_auth_backend
from . import gcp_auth_backend_role
from . import gcp_secret_backend
from . import gcp_secret_roleset
from . import gcp_secret_static_account
from . import generic_endpoint
from . import generic_secret
from . import github_auth_backend
from . import github_team
from . import github_user
from . import identity_entity
from . import identity_entity_alias
from . import identity_entity_policies
from . import identity_group
from . import identity_group_alias
from . import identity_group_member_entity_ids
from . import identity_group_member_group_ids
from . import identity_group_policies
from . import identity_mfa_duo
from . import identity_mfa_login_enforcement
from . import identity_mfa_okta
from . import identity_mfa_pingid
from . import identity_mfa_totp
from . import identity_oidc
from . import identity_oidc_assignment
from . import identity_oidc_client
from . import identity_oidc_key
from . import identity_oidc_key_allowed_client_id
from . import identity_oidc_provider
from . import identity_oidc_role
from . import identity_oidc_scope
from . import jwt_auth_backend
from . import jwt_auth_backend_role
from . import kmip_secret_backend
from . import kmip_secret_role
from . import kmip_secret_scope
from . import kubernetes_auth_backend_config
from . import kubernetes_auth_backend_role
from . import kubernetes_secret_backend
from . import kubernetes_secret_backend_role
from . import kv_secret
from . import kv_secret_backend_v2
from . import kv_secret_v2
from . import ldap_auth_backend
from . import ldap_auth_backend_group
from . import ldap_auth_backend_user
from . import managed_keys
from . import mfa_duo
from . import mfa_okta
from . import mfa_pingid
from . import mfa_totp
from . import mount
from . import namespace
from . import nomad_secret_backend
from . import nomad_secret_role
from . import okta_auth_backend
from . import okta_auth_backend_group
from . import okta_auth_backend_user
from . import password_policy
from . import pki_secret_backend_cert
from . import pki_secret_backend_config_ca
from . import pki_secret_backend_config_urls
from . import pki_secret_backend_crl_config
from . import pki_secret_backend_intermediate_cert_request
from . import pki_secret_backend_intermediate_set_signed
from . import pki_secret_backend_role
from . import pki_secret_backend_root_cert
from . import pki_secret_backend_root_sign_intermediate
from . import pki_secret_backend_sign
from . import policy
from . import provider
from . import quota_lease_count
from . import quota_rate_limit
from . import rabbitmq_secret_backend
from . import rabbitmq_secret_backend_role
from . import raft_autopilot
from . import raft_snapshot_agent_config
from . import rgp_policy
from . import ssh_secret_backend_ca
from . import ssh_secret_backend_role
from . import terraform_cloud_secret_backend
from . import terraform_cloud_secret_creds
from . import terraform_cloud_secret_role
from . import token
from . import token_auth_backend_role
from . import transform_alphabet
from . import transform_role
from . import transform_template
from . import transform_transformation
from . import transit_secret_backend_key
from . import transit_secret_cache_config
