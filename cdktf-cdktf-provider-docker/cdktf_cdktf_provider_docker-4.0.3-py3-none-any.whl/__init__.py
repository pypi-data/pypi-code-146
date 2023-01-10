'''
# Terraform CDK docker Provider ~> 2.12

This repo builds and publishes the Terraform docker Provider bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-docker](https://www.npmjs.com/package/@cdktf/provider-docker).

`npm install @cdktf/provider-docker`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-docker](https://pypi.org/project/cdktf-cdktf-provider-docker).

`pipenv install cdktf-cdktf-provider-docker`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Docker](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Docker).

`dotnet add package HashiCorp.Cdktf.Providers.Docker`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-docker](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-docker).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-docker</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-docker-go`](https://github.com/cdktf/cdktf-provider-docker-go) package.

`go get github.com/cdktf/cdktf-provider-docker-go/docker`

## Docs

Find auto-generated docs for this provider here: [./API.md](./API.md)
You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-docker).

## Versioning

This project is explicitly not tracking the Terraform docker Provider version 1:1. In fact, it always tracks `latest` of `~> 2.12` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform docker Provider](https://github.com/terraform-providers/terraform-provider-docker)
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
    "config",
    "container",
    "data_docker_image",
    "data_docker_logs",
    "data_docker_network",
    "data_docker_plugin",
    "data_docker_registry_image",
    "image",
    "network",
    "plugin",
    "provider",
    "registry_image",
    "secret",
    "service",
    "tag",
    "volume",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import config
from . import container
from . import data_docker_image
from . import data_docker_logs
from . import data_docker_network
from . import data_docker_plugin
from . import data_docker_registry_image
from . import image
from . import network
from . import plugin
from . import provider
from . import registry_image
from . import secret
from . import service
from . import tag
from . import volume
