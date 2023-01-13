'''
# Vibe-io CDK-Extensions Glue Tables Construct Library

The **cdk-extensions/glue-tables** package contains advanced constructs and patterns
for setting up commonly needed Glue tables and Athena Named Queries. The constructs
presented here are intended to be replacements for equivalent AWS constructs in
the CDK module, but with additional features included.

[AWS CDK Glue API Reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-glue-alpha-readme.html)

The patterns here extend and depend on the Glue constructs in the **cdk-extensions/glue** module(`crawler`, `table`, et al) to
ensure all defaults follow best practices, and utilize most secure settings.

To import and use this module within your CDK project:

#### Typescript

```python
import * as glue_tables from 'cdk-extensions/glue-tables';
```

#### Python

```python
import cdk_extensions.glue_tables as glue_tables
```

# AWS Logging Tables

These constructs are utilized as part of the logging strategy defined by
**stacks/AwsLoggingStack**, but can be deployed individually. They define Glue tables
and named Athena queries for ingesting and analyzing each services log data from
an S3 Bucket.

* [Usage](#Usage)

  * [Required Parameters](#RequiredParameters)
* [GlueTables](#GlueTables)

  * [AlbLogsTable](#AlbLogsTable)
  * [CloudFrontLogsTable](#CloudFrontLogsTable)
  * [CloudTrailTable](#CloudTrailTable)
  * [FlowLogsTable](#FlowLogsTable)
  * [S3AccessLogsTable](#S3AccessLogsTable)
  * [SesLogsTable](#SesLogsTable)
  * [WafLogsTable](#WafLogsTable)

### Usage

These tables all expect input from S3_buckets. By default, for each service in
the **AwsLoggingStack**, a Glue crawler performs an ETL process to analyze and categorize
the stored data and store the associated metadata in the AWS Glue Data Catalog.
All fields are represented, with handling for nested data as structs.

For each service, projections are configured where necessary and tables constructed
to patterns expected for that service, including any necessary SerDe Info.

Several default named **Athena** queries are defined using the **cdk_extensions/athena**
module that aid in improving the security posture of your AWS Account. These named
queries have been defined for each AWS service.

#### Required Parameters

These constructs are intended to be used internally by the **AwsLoggingStack**. If
using them directly, requires:

* **bucket**: An [AWS S3 iBucket](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html)
  representing the s3 bucket logs are stored in
* **database**: A **cdk-extensions/glue** `Database` to create the table in.

### About ETL

ETL stands for **E**xtract, **T**ransform, **L**oad. Data is *extracted* from the
service logs by the Glue crawler, and *transformed* to a proper schema and format
for *loading* into a Glue table.

## AlbLogsTable

### Usage

#### Required Parameters

* **bucket**: An [AWS S3 iBucket](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html)
  representing the s3 bucket logs are stored in
* **database**: A **cdk-extensions/glue** `Database` to create the table in.

**TypeScript**

```Typescript
import { AlbLogsTable } from 'cdk-extensions/glue-tables'
```

```Typescript
new AlbLogsTable(this, 'AlbLogsTable', {
  'bucket': bucket,
  'database': database
})
```

**Python**

```Python
from cdk_extensions.glue_tables import (
  AlbLogsTable
)
```

```Python
alb_logging_stack = AlbLogsTable(self, 'AwsLoggingStack',
                                 bucket=bucket,
                                 database=database
                                 )
```

### Glue

Creates a Glue table using constructs from the **cdk_extensions/glue** module.
Table schema is configured for expected ALB log fields.

The following partition keys are set:

* `source`
* `logname`
* `regionname`
* `day`

Projection is enabled and configured for the expected `yyyy/MM/dd` log format.

### Athena Queries

Creates Athena Queries using the **cdk-extensions/athena** module.
Two Athena [`CfnNamedQueries`](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html) are created by default:

* **alb-top-ips**: Gets the 100 most active IP addresses by request count.
* **alb-5xx-errors**: Gets the 100 most recent ELB 5XX responses

## CloudFrontLogsTable

### Usage

#### Required Parameters

* **bucket**: An [AWS S3 iBucket](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html)
  representing the s3 bucket logs are stored in
* **database**: A **cdk-extensions/glue** `Database` to create the table in.

**TypeScript**

```Typescript
import { CloudFrontLogsTable } from 'cdk-extensions/glue-tables'
```

```Typescript
new CloudFrontLogsTable(this, 'CloudFrontLogsTable', {
  'bucket': bucket,
  'database': database
})
```

**Python**

```Python
from cdk_extensions.glue_tables import (
  CloudFrontLogsTable
)
```

```Python
cloudfront_logging_stack = CloudFrontLogsTable(self, 'AwsLoggingStack',
                                 bucket=bucket,
                                 database=database
                                 )
```

### Glue

Creates a Glue table using constructs from the **cdk_extensions/glue** module.
Table schema is configured for expected CloudFront log fields.

### Athena Queries

Creates Athena Queries using the **cdk-extensions/athena** constructs.
Four Athena [`CfnNamedQueries`](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html) are created by default:

* **cloudfront-distribution-statistics**: Gets statistics for CloudFront distributions
  for the last day.
* **cloudfront-request-errors**: Gets the 100 most recent requests that resulted
  in an error from CloudFront.
* **cloudfront-top-ips**: Gets the 100 most active IP addresses by request count.
* **cloudfront-top-objects**: Gets the 100 most requested CloudFront objects.

## CloudTrailTable

### Usage

#### Required Parameters

* **bucket**: An [AWS S3 iBucket](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html)
  representing the s3 bucket logs are stored in
* **database**: A **cdk-extensions/glue** `Database` to create the table in.

**TypeScript**

```Typescript
import { CloudTrailTable } from 'cdk-extensions/glue-tables'
```

```Typescript
new CloudTrailTable(this, 'CloudTrailTable', {
  'bucket': bucket,
  'database': database
})
```

**Python**

```Python
from cdk_extensions.glue_tables import (
  CloudTrailTable
)
```

```Python
cloudtrail_table_stack = CloudTrailTable(self, 'AwsLoggingStack',
                                 bucket=bucket,
                                 database=database
                                 )
```

### Glue

Creates a Glue table using constructs from the **cdk_extensions/glue** module.
Table schema is configured for expected CloudTrail event logs data.

The following partition keys are set:

* `source`
* `logname`
* `regionname`
* `day`

Projection is enabled and configured for the expected `yyyy/MM/dd` log format.

### Athena Queries

Creates Athena Queries using the **cdk-extensions/athena** constructs.
Two Athena [`CfnNamedQueries`](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html) are created by default:

* **cloudtrail-unauthorized-errors**: Gets the 100 most recent unauthorized AWS
  API calls.
* **cloudtrail-user-logins**: Gets the 100 most recent AWS user logins.

## FlowLogsTable

### Usage

#### Required Parameters

* **bucket**: An [AWS S3 iBucket](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html)
  representing the s3 bucket logs are stored in
* **database**: A **cdk-extensions/glue** `Database` to create the table in.

**TypeScript**

```Typescript
import { FlowLogsTable } from 'cdk-extensions/glue-tables'
```

```Typescript
new FlowLogsTable(this, 'FlowLogsTable', {
  'bucket': bucket,
  'database': database
})
```

**Python**

```Python
from cdk_extensions.glue_tables import (
  FlowLogsTable
)
```

```Python
flowlogs_stack = FlowLogsTable(self, 'AwsLoggingStack',
                                 bucket=bucket,
                                 database=database
                                 )
```

### Glue

Creates a Glue table using constructs from the **cdk_extensions/glue** module.
Table schema is configured for expected VPC FlowLog data.

The following partition keys are set:

* `source`
* `logname`
* `regionname`
* `day`

Projection is enabled and configured for the expected `yyyy/MM/dd` log format.

### Athena Queries

One AthenaNamedQuery is created by default:

* **flow-logs-internal-rejected**: Gets the 100 most recent rejected packets that
  stayed within the private network ranges.

## S3AccessLogsTable

### Usage

#### Required Parameters

* **bucket**: An [AWS S3 iBucket](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html)
  representing the s3 bucket logs are stored in
* **database**: A **cdk-extensions/glue** `Database` to create the table in.

**TypeScript**

```Typescript
import { S3AccessLogsTable } from 'cdk-extensions/glue-tables'
```

```Typescript
new S3AccessLogsTable(this, 'S3AccessLogsTable', {
  'bucket': bucket,
  'database': database
})
```

**Python**

```Python
from cdk_extensions.glue_tables import (
  S3AccessLogsTable
)
```

```Python
s3_access_logging_stack = S3AccessLogsTable(self, 'AwsLoggingStack',
                                 bucket=bucket,
                                 database=database
                                 )
```

### Glue

Creates a Glue table using constructs from the **cdk_extensions/glue** module.
Table schema is configured for expected S3 Access log data.

### Athena Queries

Creates an Athena Query using the **cdk-extensions/athena** constructs.
One AthenaNamedQuery is created by default:

* **s3-request-errors**: Gets the 100 most recent failed S3 access requests.

## SesLogsTable

### Usage

#### Required Parameters

* **bucket**: An [AWS S3 iBucket](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html)
  representing the s3 bucket logs are stored in
* **database**: A **cdk-extensions/glue** `Database` to create the table in.

**TypeScript**

```Typescript
import { SesLogsTable } from 'cdk-extensions/glue-tables'
```

```Typescript
new SesLogsTable(this, 'SesLogsTable', {
  'bucket': bucket,
  'database': database
})
```

**Python**

```Python
from cdk_extensions.glue_tables import (
  SesLogsTable
)
```

```Python
ses_logging_stack = SesLogsTable(self, 'AwsLoggingStack',
                                 bucket=bucket,
                                 database=database
                                 )
```

### Glue

Creates a Glue table using constructs from the **cdk_extensions/glue** module.
Table schema is configured for the expected SES event logs.

Projection is enabled and configured for the expected `yyyy/MM/dd` log format.

The following partition keys are set:

* `day`

### Athena Queries

Creates Athena Queries using the **cdk-extensions/athena** constructs.
Two Athena [`CfnNamedQueries`](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html) are created by default:

* **ses-bounces**: Gets the 100 most recent bounces from the last day.
* **ses-complaints**: Gets the 100 most recent complaints from the last day.

## WafLogsTable

### Usage

#### Required Paramaters

* **bucket**: An [AWS S3 iBucket](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html)
  representing the s3 bucket logs are stored in
* **database**: A **cdk-extensions/glue** `Database` to create the table in.
  **TypeScript**

```Typescript
import { WafLogsTable } from 'cdk-extensions/glue-tables'
```

```Typescript
new WafLogsTable(this, 'WafLogsTable', {
  'bucket': bucket,
  'database': database
})
```

**Python**

```Python
from cdk_extensions.glue_tables import (
  WafLogsTable
)
```

```Python
waf_logging_stack = WafLogsTable(self, 'AwsLoggingStack',
                                 bucket=bucket,
                                 database=database
                                 )
```

### Glue

Creates a Glue table using constructs from the **cdk_extensions/glue** module.
Table schema is configured for expected WAF log data.

The following partition keys are set:

* `account`
* `region`

Projection is enabled.

### Athena Queries

No default Athena Queries have been implemented at this time.

### Examples

Creates an ALB Logging stack, with an S3 logging bucket, **cdk_extensions/glue** `Database`, and `AlbLogsTable` with its default Athena Queries.

**TypeScript**

```python
import { App, Stack, StackProps, RemovalPolicy, aws_s3 as s3 } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Database } from 'cdk-extensions/glue/database';
import { AlbLogsTable } from 'cdk-extensions/glue-tables';

export class AlbLogStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // If we were to use the cdk-extensions AlbLogsBucket pattern,
    // Glue tables would be created for us. Instead, we use the
    // standard library, remembering to set some secure best practices
    // like encryption and removal policy
    const bucket = new s3.Bucket(this, 'MyEncryptedBucket', {
      encryption: s3.BucketEncryption.KMS,
      removalPolicy: RemovalPolicy.RETAIN
    });

    // Create a cdk-extensions/glue Database with secure defaults
    const database = new Database(this, 'GlueDatabase');

    // Create the AlbLogsTable Glue table with defaults
    const alb_logs_table = new AlbLogsTable(this, 'AlbLogsTable', {
      'bucket': bucket,
      'database': database
    })
  }
}
```

**Python**

```Python
from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_s3 as s3
)
from cdk_extensions.glue import (
  Database
)
from cdk_extensions.glue_tables import (
  AlbLogsTable
)


class AlbLogStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # If we were to use the cdk-extensions AlbLogsBucket pattern,
        # Glue tables would be created for us. Instead, we use the
        # standard library, remembering to set some secure best practices
        # like encryption and removal policy
        bucket = s3.Bucket(self, 'MyEncryptedBucket',
                           encryption=s3.BucketEncryption.KMS,
                           removalPolicy=RemovalPolicy.RETAIN
                           )
        # Create a cdk-extensions/glue Database with secure defaults
        database = Database(self, 'MyGlueDatabase')

        # Create the AlbLogsTable Glue table with defaults
        alb_logging_stack = AlbLogsTable(self, 'AwsLoggingStack',
                                         bucket=bucket,
                                         database=database
                                         )
```
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

from .._jsii import *

import aws_cdk
import aws_cdk.aws_glue
import aws_cdk.aws_s3
import constructs
from ..athena import NamedQuery as _NamedQuery_9313a1de
from ..ec2 import FlowLogFormat as _FlowLogFormat_b7c2ba34
from ..glue import Database as _Database_5971ae38, Table as _Table_114d5aef


class AlbLogsTable(
    _Table_114d5aef,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue_tables.AlbLogsTable",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the AlbLogsTable class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the ALB Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for Alb Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AlbLogsTable.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AlbLogsTableProps(
            bucket=bucket,
            database=database,
            create_queries=create_queries,
            friendly_query_names=friendly_query_names,
            name=name,
            s3_prefix=s3_prefix,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> builtins.bool:
        '''Boolean indicating whether to create default Athena queries for the ALB Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        return typing.cast(builtins.bool, jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> builtins.bool:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        return typing.cast(builtins.bool, jsii.get(self, "friendlyQueryNames"))

    @builtins.property
    @jsii.member(jsii_name="status5xxNamedQuery")
    def status5xx_named_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "status5xxNamedQuery"))

    @builtins.property
    @jsii.member(jsii_name="topIpsNamedQuery")
    def top_ips_named_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "topIpsNamedQuery"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue_tables.AlbLogsTableProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket": "bucket",
        "database": "database",
        "create_queries": "createQueries",
        "friendly_query_names": "friendlyQueryNames",
        "name": "name",
        "s3_prefix": "s3Prefix",
    },
)
class AlbLogsTableProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for AlbLogsTable.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the ALB Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for Alb Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AlbLogsTableProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "database": database,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if name is not None:
            self._values["name"] = name
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''A bucket where logs will be stored.

        :see: `AWS S3 iBucket <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html>`_
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def database(self) -> _Database_5971ae38:
        '''A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.

        :see: `AWS::Glue::Database <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html>`_
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(_Database_5971ae38, result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        '''Boolean indicating whether to create default Athena queries for the ALB Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name for Alb Logs Table.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''Set a custom prefix for the S3 Bucket.'''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbLogsTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontLogsTable(
    _Table_114d5aef,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue_tables.CloudfrontLogsTable",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the CloudfrontAccessLogsTable class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket: The bucket where logs will be contained.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the Cloudfront Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for Cloudfront Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudfrontLogsTable.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudfrontLogsTableProps(
            bucket=bucket,
            database=database,
            create_queries=create_queries,
            friendly_query_names=friendly_query_names,
            name=name,
            s3_prefix=s3_prefix,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> builtins.bool:
        '''Boolean indicating whether to create default Athena queries for the Cloudfront Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        return typing.cast(builtins.bool, jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> builtins.bool:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        return typing.cast(builtins.bool, jsii.get(self, "friendlyQueryNames"))

    @builtins.property
    @jsii.member(jsii_name="distributionStatisticsNamedQuery")
    def distribution_statistics_named_query(
        self,
    ) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "distributionStatisticsNamedQuery"))

    @builtins.property
    @jsii.member(jsii_name="requestErrorsNamedQuery")
    def request_errors_named_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "requestErrorsNamedQuery"))

    @builtins.property
    @jsii.member(jsii_name="topIpsNamedQuery")
    def top_ips_named_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "topIpsNamedQuery"))

    @builtins.property
    @jsii.member(jsii_name="topObjectsNamedQuery")
    def top_objects_named_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "topObjectsNamedQuery"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue_tables.CloudfrontLogsTableProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket": "bucket",
        "database": "database",
        "create_queries": "createQueries",
        "friendly_query_names": "friendlyQueryNames",
        "name": "name",
        "s3_prefix": "s3Prefix",
    },
)
class CloudfrontLogsTableProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for CloudfrontAccessLogsTable.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket: The bucket where logs will be contained.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the Cloudfront Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for Cloudfront Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudfrontLogsTableProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "database": database,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if name is not None:
            self._values["name"] = name
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''The bucket where logs will be contained.

        :see: `AWS S3 iBucket <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html>`_
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def database(self) -> _Database_5971ae38:
        '''A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.

        :see: `AWS::Glue::Database <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html>`_
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(_Database_5971ae38, result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        '''Boolean indicating whether to create default Athena queries for the Cloudfront Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name for Cloudfront Logs Table.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''Set a custom prefix for the S3 Bucket.'''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontLogsTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudtrailTable(
    _Table_114d5aef,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue_tables.CloudtrailTable",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the FlowLogsTable class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the Cloudtrail Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for Cloudtrail Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudtrailTable.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudtrailTableProps(
            bucket=bucket,
            database=database,
            create_queries=create_queries,
            friendly_query_names=friendly_query_names,
            name=name,
            s3_prefix=s3_prefix,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> builtins.bool:
        '''Boolean indicating whether to create default Athena queries for the Cloudtrail Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        return typing.cast(builtins.bool, jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> builtins.bool:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        return typing.cast(builtins.bool, jsii.get(self, "friendlyQueryNames"))

    @builtins.property
    @jsii.member(jsii_name="unauthorizedNamedQuery")
    def unauthorized_named_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "unauthorizedNamedQuery"))

    @builtins.property
    @jsii.member(jsii_name="userLoginsNamedQuery")
    def user_logins_named_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "userLoginsNamedQuery"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue_tables.CloudtrailTableProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket": "bucket",
        "database": "database",
        "create_queries": "createQueries",
        "friendly_query_names": "friendlyQueryNames",
        "name": "name",
        "s3_prefix": "s3Prefix",
    },
)
class CloudtrailTableProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for FlowLogsTable.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the Cloudtrail Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for Cloudtrail Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudtrailTableProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "database": database,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if name is not None:
            self._values["name"] = name
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''A bucket where logs will be stored.

        :see: `AWS S3 iBucket <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html>`_
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def database(self) -> _Database_5971ae38:
        '''A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.

        :see: `AWS::Glue::Database <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html>`_
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(_Database_5971ae38, result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        '''Boolean indicating whether to create default Athena queries for the Cloudtrail Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name for Cloudtrail Logs Table.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''Set a custom prefix for the S3 Bucket.'''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudtrailTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FlowLogsTable(
    _Table_114d5aef,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue_tables.FlowLogsTable",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        format: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the FlowLogsTable class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the Flow Logs.
        :param format: A cdk-extentions/ec2 {@link aws-ec2!FlowLogFormat } object defining the desired formatting for Flow Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for Flow Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogsTable.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FlowLogsTableProps(
            bucket=bucket,
            database=database,
            create_queries=create_queries,
            format=format,
            friendly_query_names=friendly_query_names,
            name=name,
            s3_prefix=s3_prefix,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="renderStorageDescriptor")
    def _render_storage_descriptor(
        self,
    ) -> typing.Optional[aws_cdk.aws_glue.CfnTable.StorageDescriptorProperty]:
        return typing.cast(typing.Optional[aws_cdk.aws_glue.CfnTable.StorageDescriptorProperty], jsii.invoke(self, "renderStorageDescriptor", []))

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> builtins.bool:
        '''Boolean indicating whether to create default Athena queries for the Flow Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        return typing.cast(builtins.bool, jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> _FlowLogFormat_b7c2ba34:
        '''A cdk-extentions/ec2 {@link aws-ec2!FlowLogFormat } object defining the desired formatting for Flow Logs.'''
        return typing.cast(_FlowLogFormat_b7c2ba34, jsii.get(self, "format"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> builtins.bool:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        return typing.cast(builtins.bool, jsii.get(self, "friendlyQueryNames"))

    @builtins.property
    @jsii.member(jsii_name="internalRejectedNamedQuery")
    def internal_rejected_named_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "internalRejectedNamedQuery"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue_tables.FlowLogsTableProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket": "bucket",
        "database": "database",
        "create_queries": "createQueries",
        "format": "format",
        "friendly_query_names": "friendlyQueryNames",
        "name": "name",
        "s3_prefix": "s3Prefix",
    },
)
class FlowLogsTableProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        format: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for FlowLogsTable.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the Flow Logs.
        :param format: A cdk-extentions/ec2 {@link aws-ec2!FlowLogFormat } object defining the desired formatting for Flow Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for Flow Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogsTableProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "database": database,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if format is not None:
            self._values["format"] = format
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if name is not None:
            self._values["name"] = name
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''A bucket where logs will be stored.

        :see: `AWS S3 iBucket <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html>`_
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def database(self) -> _Database_5971ae38:
        '''A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.

        :see: `AWS::Glue::Database <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html>`_
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(_Database_5971ae38, result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        '''Boolean indicating whether to create default Athena queries for the Flow Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def format(self) -> typing.Optional[_FlowLogFormat_b7c2ba34]:
        '''A cdk-extentions/ec2 {@link aws-ec2!FlowLogFormat } object defining the desired formatting for Flow Logs.'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[_FlowLogFormat_b7c2ba34], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name for Flow Logs Table.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''Set a custom prefix for the S3 Bucket.'''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogsTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3AccessLogsTable(
    _Table_114d5aef,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue_tables.S3AccessLogsTable",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the S3AccessLogsTable class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the S3 Access Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for S3 Access Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3AccessLogsTable.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3AccessLogsTableProps(
            bucket=bucket,
            database=database,
            create_queries=create_queries,
            friendly_query_names=friendly_query_names,
            name=name,
            s3_prefix=s3_prefix,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> builtins.bool:
        '''Boolean indicating whether to create default Athena queries for the S3 Access Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        return typing.cast(builtins.bool, jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> builtins.bool:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        return typing.cast(builtins.bool, jsii.get(self, "friendlyQueryNames"))

    @builtins.property
    @jsii.member(jsii_name="requestErrorsNamedQuery")
    def request_errors_named_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "requestErrorsNamedQuery"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue_tables.S3AccessLogsTableProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket": "bucket",
        "database": "database",
        "create_queries": "createQueries",
        "friendly_query_names": "friendlyQueryNames",
        "name": "name",
        "s3_prefix": "s3Prefix",
    },
)
class S3AccessLogsTableProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for S3AccessLogsTable.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the S3 Access Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for S3 Access Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3AccessLogsTableProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "database": database,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if name is not None:
            self._values["name"] = name
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''A bucket where logs will be stored.

        :see: `AWS S3 iBucket <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html>`_
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def database(self) -> _Database_5971ae38:
        '''A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.

        :see: `AWS::Glue::Database <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html>`_
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(_Database_5971ae38, result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        '''Boolean indicating whether to create default Athena queries for the S3 Access Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name for S3 Access Logs Table.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''Set a custom prefix for the S3 Bucket.'''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3AccessLogsTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SesLogsTable(
    _Table_114d5aef,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue_tables.SesLogsTable",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the SesLogsTable class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the Ses Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for SES Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SesLogsTable.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SesLogsTableProps(
            bucket=bucket,
            database=database,
            create_queries=create_queries,
            friendly_query_names=friendly_query_names,
            name=name,
            s3_prefix=s3_prefix,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> builtins.bool:
        '''Boolean indicating whether to create default Athena queries for the Ses Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        return typing.cast(builtins.bool, jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> builtins.bool:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        return typing.cast(builtins.bool, jsii.get(self, "friendlyQueryNames"))

    @builtins.property
    @jsii.member(jsii_name="bouncesQuery")
    def bounces_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "bouncesQuery"))

    @builtins.property
    @jsii.member(jsii_name="complaintsQuery")
    def complaints_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "complaintsQuery"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue_tables.SesLogsTableProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket": "bucket",
        "database": "database",
        "create_queries": "createQueries",
        "friendly_query_names": "friendlyQueryNames",
        "name": "name",
        "s3_prefix": "s3Prefix",
    },
)
class SesLogsTableProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for SesLogsTable.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the Ses Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for SES Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SesLogsTableProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "database": database,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if name is not None:
            self._values["name"] = name
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''A bucket where logs will be stored.

        :see: `AWS S3 iBucket <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html>`_
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def database(self) -> _Database_5971ae38:
        '''A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.

        :see: `AWS::Glue::Database <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html>`_
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(_Database_5971ae38, result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        '''Boolean indicating whether to create default Athena queries for the Ses Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name for SES Logs Table.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''Set a custom prefix for the S3 Bucket.'''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SesLogsTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafLogsTable(
    _Table_114d5aef,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue_tables.WafLogsTable",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the S3AccessLogsTable class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the WAF Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for WAF Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WafLogsTable.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WafLogsTableProps(
            bucket=bucket,
            database=database,
            create_queries=create_queries,
            friendly_query_names=friendly_query_names,
            name=name,
            s3_prefix=s3_prefix,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> builtins.bool:
        '''Boolean indicating whether to create default Athena queries for the WAF Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        return typing.cast(builtins.bool, jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> builtins.bool:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        return typing.cast(builtins.bool, jsii.get(self, "friendlyQueryNames"))

    @builtins.property
    @jsii.member(jsii_name="status5xxNamedQuery")
    def status5xx_named_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "status5xxNamedQuery"))

    @builtins.property
    @jsii.member(jsii_name="topIpsNamedQuery")
    def top_ips_named_query(self) -> typing.Optional[_NamedQuery_9313a1de]:
        return typing.cast(typing.Optional[_NamedQuery_9313a1de], jsii.get(self, "topIpsNamedQuery"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue_tables.WafLogsTableProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket": "bucket",
        "database": "database",
        "create_queries": "createQueries",
        "friendly_query_names": "friendlyQueryNames",
        "name": "name",
        "s3_prefix": "s3Prefix",
    },
)
class WafLogsTableProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket: aws_cdk.aws_s3.IBucket,
        database: _Database_5971ae38,
        create_queries: typing.Optional[builtins.bool] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for S3AccessLogsTable.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket: A bucket where logs will be stored.
        :param database: A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.
        :param create_queries: Boolean indicating whether to create default Athena queries for the WAF Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param name: Name for WAF Logs Table.
        :param s3_prefix: Set a custom prefix for the S3 Bucket.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WafLogsTableProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "database": database,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if name is not None:
            self._values["name"] = name
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''A bucket where logs will be stored.

        :see: `AWS S3 iBucket <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.IBucket.html>`_
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def database(self) -> _Database_5971ae38:
        '''A cdk-extensions/glue {@link aws-glue!Database } object that the table should be created in.

        :see: `AWS::Glue::Database <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html>`_
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(_Database_5971ae38, result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        '''Boolean indicating whether to create default Athena queries for the WAF Logs.

        :see: ```CfnNamedQueries`` <https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html>`_
        '''
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name for WAF Logs Table.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''Set a custom prefix for the S3 Bucket.'''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafLogsTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AlbLogsTable",
    "AlbLogsTableProps",
    "CloudfrontLogsTable",
    "CloudfrontLogsTableProps",
    "CloudtrailTable",
    "CloudtrailTableProps",
    "FlowLogsTable",
    "FlowLogsTableProps",
    "S3AccessLogsTable",
    "S3AccessLogsTableProps",
    "SesLogsTable",
    "SesLogsTableProps",
    "WafLogsTable",
    "WafLogsTableProps",
]

publication.publish()
