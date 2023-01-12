'''
# Terraform CDK datadog Provider ~> 3.0

This repo builds and publishes the Terraform datadog Provider bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-datadog](https://www.npmjs.com/package/@cdktf/provider-datadog).

`npm install @cdktf/provider-datadog`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-datadog](https://pypi.org/project/cdktf-cdktf-provider-datadog).

`pipenv install cdktf-cdktf-provider-datadog`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Datadog](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Datadog).

`dotnet add package HashiCorp.Cdktf.Providers.Datadog`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-datadog](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-datadog).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-datadog</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-datadog-go`](https://github.com/cdktf/cdktf-provider-datadog-go) package.

`go get github.com/cdktf/cdktf-provider-datadog-go/datadog`

## Docs

Find auto-generated docs for this provider here: [./API.md](./API.md)
You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-datadog).

## Versioning

This project is explicitly not tracking the Terraform datadog Provider version 1:1. In fact, it always tracks `latest` of `~> 3.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform datadog Provider](https://github.com/terraform-providers/terraform-provider-datadog)
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
    "api_key",
    "application_key",
    "authn_mapping",
    "child_organization",
    "cloud_configuration_rule",
    "cloud_workload_security_agent_rule",
    "dashboard",
    "dashboard_json",
    "dashboard_list",
    "data_datadog_api_key",
    "data_datadog_application_key",
    "data_datadog_cloud_workload_security_agent_rules",
    "data_datadog_dashboard",
    "data_datadog_dashboard_list",
    "data_datadog_integration_aws_logs_services",
    "data_datadog_ip_ranges",
    "data_datadog_logs_archives_order",
    "data_datadog_logs_indexes",
    "data_datadog_logs_indexes_order",
    "data_datadog_logs_pipelines",
    "data_datadog_monitor",
    "data_datadog_monitors",
    "data_datadog_permissions",
    "data_datadog_role",
    "data_datadog_roles",
    "data_datadog_rum_application",
    "data_datadog_security_monitoring_filters",
    "data_datadog_security_monitoring_rules",
    "data_datadog_service_level_objective",
    "data_datadog_service_level_objectives",
    "data_datadog_synthetics_global_variable",
    "data_datadog_synthetics_locations",
    "data_datadog_synthetics_test",
    "data_datadog_user",
    "downtime",
    "integration_aws",
    "integration_aws_lambda_arn",
    "integration_aws_log_collection",
    "integration_aws_tag_filter",
    "integration_azure",
    "integration_gcp",
    "integration_opsgenie_service_object",
    "integration_pagerduty",
    "integration_pagerduty_service_object",
    "integration_slack_channel",
    "logs_archive",
    "logs_archive_order",
    "logs_custom_pipeline",
    "logs_index",
    "logs_index_order",
    "logs_integration_pipeline",
    "logs_metric",
    "logs_pipeline_order",
    "metric_metadata",
    "metric_tag_configuration",
    "monitor",
    "monitor_json",
    "organization_settings",
    "provider",
    "role",
    "rum_application",
    "security_monitoring_default_rule",
    "security_monitoring_filter",
    "security_monitoring_rule",
    "service_account",
    "service_definition_yaml",
    "service_level_objective",
    "slo_correction",
    "synthetics_global_variable",
    "synthetics_private_location",
    "synthetics_test",
    "user",
    "webhook",
    "webhook_custom_variable",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import api_key
from . import application_key
from . import authn_mapping
from . import child_organization
from . import cloud_configuration_rule
from . import cloud_workload_security_agent_rule
from . import dashboard
from . import dashboard_json
from . import dashboard_list
from . import data_datadog_api_key
from . import data_datadog_application_key
from . import data_datadog_cloud_workload_security_agent_rules
from . import data_datadog_dashboard
from . import data_datadog_dashboard_list
from . import data_datadog_integration_aws_logs_services
from . import data_datadog_ip_ranges
from . import data_datadog_logs_archives_order
from . import data_datadog_logs_indexes
from . import data_datadog_logs_indexes_order
from . import data_datadog_logs_pipelines
from . import data_datadog_monitor
from . import data_datadog_monitors
from . import data_datadog_permissions
from . import data_datadog_role
from . import data_datadog_roles
from . import data_datadog_rum_application
from . import data_datadog_security_monitoring_filters
from . import data_datadog_security_monitoring_rules
from . import data_datadog_service_level_objective
from . import data_datadog_service_level_objectives
from . import data_datadog_synthetics_global_variable
from . import data_datadog_synthetics_locations
from . import data_datadog_synthetics_test
from . import data_datadog_user
from . import downtime
from . import integration_aws
from . import integration_aws_lambda_arn
from . import integration_aws_log_collection
from . import integration_aws_tag_filter
from . import integration_azure
from . import integration_gcp
from . import integration_opsgenie_service_object
from . import integration_pagerduty
from . import integration_pagerduty_service_object
from . import integration_slack_channel
from . import logs_archive
from . import logs_archive_order
from . import logs_custom_pipeline
from . import logs_index
from . import logs_index_order
from . import logs_integration_pipeline
from . import logs_metric
from . import logs_pipeline_order
from . import metric_metadata
from . import metric_tag_configuration
from . import monitor
from . import monitor_json
from . import organization_settings
from . import provider
from . import role
from . import rum_application
from . import security_monitoring_default_rule
from . import security_monitoring_filter
from . import security_monitoring_rule
from . import service_account
from . import service_definition_yaml
from . import service_level_objective
from . import slo_correction
from . import synthetics_global_variable
from . import synthetics_private_location
from . import synthetics_test
from . import user
from . import webhook
from . import webhook_custom_variable
