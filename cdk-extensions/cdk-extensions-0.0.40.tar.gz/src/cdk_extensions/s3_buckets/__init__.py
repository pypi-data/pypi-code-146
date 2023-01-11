'''
# Vibe-io CDK-Extensions S3 Buckets Construct Library

The cdk-extensions/s3_buckets package contains advanced constructs and patterns
for setting up S3 Buckets. The constructs presented here are intended to be replacements
for equivalent AWS constructs in the CDK module, but with additional features included.
All defaults follow best practices, and utilize secure settings.

[AWS CDK S3 API Reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3-readme.html)

To import and use this module within your CDK project:

#### Typescript

```python
import * as s3_buckets from 'cdk-extensions/s3-buckets';
```

#### Python

```python
import cdk_extensions.s3_buckets as s3_buckets
```

## Common defaults

All S3 buckets extend the private RawBucket resource, which implements the
[`iBucket`](https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-s3.IBucket.html) interface to expose all
resource configurations and creates a [`CfnBucket`](https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-s3.CfnBucket.html) resource.

All buckets have a default Removal Policy applied, retaining them if the stack
is deleted.

* **ApplyRemovalPolicy**: Defaults to `RETAIN`.

# AWS Logging Buckets

These buckets are utilized as part of the logging strategy defined by
**stacks/AwsLoggingStack**, but can be deployed individually. When applicable, storing
these logs in S3 offers significant cost savings over CloudWatch. Additionally,
Glue and Athena can be utilized for fast and efficient analysis of data stored in S3.

* [Common Settings](#CommonSettings)
* [Buckets](#Buckets)

  * [AlbLogsBucket](#AlbLogsBucket)
  * [CloudFrontLogsBucket](#CloudFrontLogsBucket)
  * [CloudTrailBucket](#CloudTrailBucket)
  * [FlowLogsBucket](#FlowLogsBucket)
  * [S3AccessLogsBucket](#S3AccessLogsBucket)
  * [SesLogsBucket](#SesLogsBucket)
  * [WafLogsBucket](#WafLogsBucket)

## Common Settings

By default, for each service in the **AwsLoggingStack** a Glue crawler performs
an ETL process to analyze and categorize the stored data and store the associated
metadata in the AWS Glue Data Catalog.

Several default named Athena queries are defined that aid in improving the security posture
of your AWS Account. These default named queries have been defined for each AWS
service.

Set `createQueries` to `false` to skip query creation.

*Examples*

**TypeScript**

```python
const alb_bucket_with_queries = new s3_buckets.AlbLogsBucket(this, "AlbLogsBucket")
const cloudtrail_bucket_without_queries = new s3_buckets.CloudtrailBucket(this, 'CloudtrailBucket', {
  createQueries: false
})
```

**Python**

```Python
alb_bucket_with_queries = s3_buckets.AlbLogsBucket(self, 'AlbLogsBucket')

cloudtrail_bucket_without_queries = s3_buckets.CloudTrailBucket(self, 'CloudTrailBucket', create_queries=False)
```

## Buckets

All log buckets are [`CfnBucket`](https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-s3.CfnBucket.html) constructs
with the additional secure defaults:

* All `PublicAccessBlockConfiguration` properties default to `true`. (i.e.
  `blockPublicAcls`, `blockPublicPolicy`, `ignorePublicAcls`,
  `restrictPublicBuckets`)
* Versioning is set to `Enabled`
* Server side bucket encryption using AES256

  * Managed KMS encryption is *not* supported for Service logs

### AlbLogsBucket

Creates an S3 Bucket and Glue jobs for storing and analyzing Elastic Load Balancer
access logs. By default, creates named Athena Queries useful in querying ELB access
log data.

#### Usage

**TypeScript**

```python
import { AlbLogsBucket } from 'cdk-extensions/s3-buckets';
```

```python
new AlbLogsBucket(this, 'AlbLogsBucket')
```

**Python**

```python
from cdk_extensions.s3_buckets import (
  AlbLogsBucket
)
```

```python
alb_logs_bucket = AlbLogsBucket(self, 'AlbLogsBucket')
```

#### Glue

By default creates database and tables from ALB logs bucket, using cdk-extensions
construct **AlbLogTables**, from the **glue-tables** module. Glue crawler performs
an ETL process to analyze and categorize data in Amazon S3 and store the associated
metadata in the AWS Glue Data Catalog.

#### Athena Queries

Two Athena [`CfnNamedQueries`](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html) are created by default:

* **alb-top-ips**: Gets the 100 most active IP addresses by request count.
* **alb-5xx-errors**: Gets the 100 most recent ELB 5XX responses

### CloudFrontLogsBucket

Creates an S3 Bucket and Glue jobs for storing and analyzing CloudFront access logs.
By default generates a Glue Database and Table, and creates named Athena
Queries useful in querying CloudFront log data.

#### Usage

**TypeScript**

```python
import { CloudFrontLogsBucket } from 'cdk-extensions/s3-buckets';
```

```python
new CloudFrontLogsBucket(this, 'CloudFrontLogsBucket')
```

**Python**

```python
from cdk_extensions.s3_buckets import (
  CloudFrontLogsBucket
)
```

```python
cloudfront_logs_bucket = CloudFrontLogsBucket(self, 'CloudFrontLogsBucket')
```

#### Glue

By default creates database and tables from CloudFront logs bucket, using cdk-extensions
construct **CloudFrontLogTable**, from the **glue-tables** module. Glue crawler
performs an ETL process to analyze and categorize data in Amazon S3 and store the
associated metadata in the AWS Glue Data Catalog.

#### Athena Queries

Four Athena [`CfnNamedQueries`](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html) are created by default:

* **cloudfront-distribution-statistics**: Gets statistics for CloudFront distributions
  for the last day.
* **cloudfront-request-errors**: Gets the 100 most recent requests that resulted
  in an error from CloudFront.
* **cloudfront-top-ips**: Gets the 100 most active IP addresses by request count.
* **cloudfront-top-objects**: Gets the 100 most requested CloudFront objects.

### CloudTrailBucket

Creates an S3 Bucket and Glue jobs for storing and analyzing CloudTrail logs.
By default generates a Glue Database and Table, and creates named Athena
Queries useful in querying CloudTrail log data.

#### Usage

**TypeScript**

```python
import { CloudTrailBucket } from 'cdk-extensions/s3-buckets';
```

```python
new CloudTrailBucket(this, 'CloudTrailBucket')
```

**Python**

```python
from cdk_extensions.s3_buckets import (
  CloudTrailBucket
)
```

```python
cloudtrail_logs_bucket = CloudTrailBucket(self, 'CloudTrailBucket')
```

#### Glue

By default creates database and tables from CloudTrail logs bucket, using cdk-extensions
construct **CloudTrailTable**, from the **glue-tables** module. Glue crawler performs
an ETL process to analyze and categorize data in Amazon S3 and store the associated
metadata in the AWS Glue Data Catalog.

#### Athena Queries

Two Athena [`CfnNamedQueries`](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html) are created by default:

* **cloudtrail-unauthorized-errors**: Gets the 100 most recent unauthorized AWS
  API calls.
* **cloudtrail-user-logins**: Gets the 100 most recent AWS user logins.

### FlowLogsBucket

Creates an S3 Bucket and Glue jobs for storing and analyzing VPC FlowLogs.
By default generates a Glue Database and Table, and creates named Athena
Queries useful in querying FlowLog data.

#### Usage

**TypeScript**

```python
import { FlowLogsBucket } from 'cdk-extensions/s3-buckets';
```

```python
new FlowLogsBucket(this, 'FlowLogsBucket')
```

**Python**

```python
from cdk_extensions.s3_buckets import (
  FlowLogsBucket
)
```

```python
flowlogs_bucket = FlowLogsBucket(self, 'FlowLogsBucket')
```

#### Glue

By default creates database and tables from FlowLogs bucket, using cdk-extensions
construct **FlowLogsTable**, from the **glue-tables** module. Glue crawler performs
an ETL process to analyze and categorize data in Amazon S3 and store the associated
metadata in the AWS Glue Data Catalog.

#### Athena Queries

One AthenaNamedQuery is created by default:

* **flow-logs-internal-rejected**: Gets the 100 most recent rejected packets that
  stayed within the private network ranges.

### S3AccessLogsBucket

Creates an S3 Bucket and Glue jobs for storing and analyzing VPC S3AccessLogs.
By default generates a Glue Database and Table, and creates named Athena
Queries useful in querying S3 access log data.

#### Usage

**TypeScript**

```python
import { S3AccessLogsBucket } from 'cdk-extensions/s3-buckets';
```

```python
new S3AccessLogsBucket(this, 'S3AccessLogsBucket')
```

**Python**

```python
from cdk_extensions.s3_buckets import (
  S3AccessLogsLogsBucket
)
```

```python
s3_access_logs_bucket = S3AccessLogsBucket(self, 'S3AccessLogsBucket')
```

#### Glue

By default creates database and tables from S3 Access logs bucket, using cdk-extensions
construct **S3AccessLogsTable**, from the **glue-tables** module. Glue crawler performs
an ETL process to analyze and categorize data in Amazon S3 and store the associated
metadata in the AWS Glue Data Catalog.

#### Athena Queries

One AthenaNamedQuery is created by default:

* **s3-request-errors**: Gets the 100 most recent failed S3 access requests.

### SesLogsBucket

Creates an S3 Bucket and Glue jobs for storing and analyzing SES Logs.
By default, generates a Glue Database and Table and creates named Athena
Queries useful in querying SES log data.

#### Usage

**TypeScript**

```python
import { SesLogsBucket } from 'cdk-extensions/s3-buckets';
```

```python
new SesLogsBucket(this, 'SesLogsBucket')
```

**Python**

```python
from cdk_extensions.s3_buckets import (
  SesLogsLogsBucket
)
```

```python
ses_logs_bucket = SesLogsBucket(self, 'SesLogsBucket')
```

#### Glue

By default creates database and tables from SES logs bucket, using cdk-extensions
construct **SesLogsTable**, from the **glue-tables** module. Glue crawler performs
an ETL process to analyze and categorize data in Amazon S3 and store the associated
metadata in the AWS Glue Data Catalog.

#### Athena Queries

Two Athena [`CfnNamedQueries`](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_athena/CfnNamedQuery.html) are created by default:

* **ses-bounces**: Gets the 100 most recent bounces from the last day.
* **ses-complaints**: Gets the 100 most recent complaints from the last day.

### WafLogsBucket

Creates an S3 Bucket and Glue jobs for storing and analyzing Web Applications
Firewall Logs. By default, generates a Glue Database and Table and creates named
Athena Queries useful in querying WAF log data.

#### Usage

**TypeScript**

```python
import { WafLogsBucket } from 'cdk-extensions/s3-buckets';
```

```python
new WafLogsBucket(this, 'WafLogsBucket')
```

**Python**

```python
from cdk_extensions.s3_buckets import (
  WafLogsLogsBucket
)
```

```python
waf_logs_bucket = WafLogsBucket(self, 'WafLogsBucket')
```

#### Glue

By default creates database and tables from WAF logs bucket, using cdk-extensions
construct **WafLogsTable**, from the **glue-tables** module. Glue crawler performs
an ETL process to analyze and categorize data in Amazon S3 and store the associated
metadata in the AWS Glue Data Catalog.

#### Athena Queries

No default Named Athena Queries have been implemented for WAF logs at this time.
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
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import constructs
from ..ec2 import FlowLogFormat as _FlowLogFormat_b7c2ba34
from ..glue import Crawler as _Crawler_96455303, Database as _Database_5971ae38
from ..glue_tables import (
    AlbLogsTable as _AlbLogsTable_03497db2,
    CloudfrontLogsTable as _CloudfrontLogsTable_f83f287b,
    CloudtrailTable as _CloudtrailTable_e3a95430,
    FlowLogsTable as _FlowLogsTable_4c0c73c1,
    S3AccessLogsTable as _S3AccessLogsTable_cd828e2c,
    SesLogsTable as _SesLogsTable_15e214c8,
    WafLogsTable as _WafLogsTable_2c2a9653,
)


@jsii.data_type(
    jsii_type="cdk-extensions.s3_buckets.AlbLogsBucketProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket_name": "bucketName",
        "create_queries": "createQueries",
        "database": "database",
        "friendly_query_names": "friendlyQueryNames",
        "table_name": "tableName",
    },
)
class AlbLogsBucketProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for objects bucket.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AlbLogsBucketProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if database is not None:
            self._values["database"] = database
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if table_name is not None:
            self._values["table_name"] = table_name

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
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database(self) -> typing.Optional[_Database_5971ae38]:
        result = self._values.get("database")
        return typing.cast(typing.Optional[_Database_5971ae38], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlbLogsBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.s3_buckets.CloudfrontLogsBucketProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket_name": "bucketName",
        "create_queries": "createQueries",
        "database": "database",
        "friendly_query_names": "friendlyQueryNames",
        "table_name": "tableName",
    },
)
class CloudfrontLogsBucketProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for objects bucket.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudfrontLogsBucketProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if database is not None:
            self._values["database"] = database
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if table_name is not None:
            self._values["table_name"] = table_name

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
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database(self) -> typing.Optional[_Database_5971ae38]:
        result = self._values.get("database")
        return typing.cast(typing.Optional[_Database_5971ae38], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontLogsBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.s3_buckets.CloudtrailBucketProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket_name": "bucketName",
        "create_queries": "createQueries",
        "database": "database",
        "friendly_query_names": "friendlyQueryNames",
        "table_name": "tableName",
    },
)
class CloudtrailBucketProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for objects bucket.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudtrailBucketProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if database is not None:
            self._values["database"] = database
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if table_name is not None:
            self._values["table_name"] = table_name

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
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database(self) -> typing.Optional[_Database_5971ae38]:
        result = self._values.get("database")
        return typing.cast(typing.Optional[_Database_5971ae38], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudtrailBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.s3_buckets.FlowLogsBucketProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket_name": "bucketName",
        "crawler_schedule": "crawlerSchedule",
        "create_queries": "createQueries",
        "database": "database",
        "format": "format",
        "friendly_query_names": "friendlyQueryNames",
        "table_name": "tableName",
    },
)
class FlowLogsBucketProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        crawler_schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        format: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for objects bucket.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket_name: 
        :param crawler_schedule: 
        :param create_queries: 
        :param database: 
        :param format: 
        :param friendly_query_names: 
        :param table_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogsBucketProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument crawler_schedule", value=crawler_schedule, expected_type=type_hints["crawler_schedule"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if crawler_schedule is not None:
            self._values["crawler_schedule"] = crawler_schedule
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if database is not None:
            self._values["database"] = database
        if format is not None:
            self._values["format"] = format
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if table_name is not None:
            self._values["table_name"] = table_name

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
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def crawler_schedule(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        result = self._values.get("crawler_schedule")
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database(self) -> typing.Optional[_Database_5971ae38]:
        result = self._values.get("database")
        return typing.cast(typing.Optional[_Database_5971ae38], result)

    @builtins.property
    def format(self) -> typing.Optional[_FlowLogFormat_b7c2ba34]:
        result = self._values.get("format")
        return typing.cast(typing.Optional[_FlowLogFormat_b7c2ba34], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogsBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.s3_buckets.LoggingAspectOptions",
    jsii_struct_bases=[],
    name_mapping={"exclusions": "exclusions", "force": "force", "prefix": "prefix"},
)
class LoggingAspectOptions:
    def __init__(
        self,
        *,
        exclusions: typing.Optional[typing.Sequence[constructs.IConstruct]] = None,
        force: typing.Optional[builtins.bool] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclusions: 
        :param force: 
        :param prefix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LoggingAspectOptions.__init__)
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[str, typing.Any] = {}
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if force is not None:
            self._values["force"] = force
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[constructs.IConstruct]]:
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[constructs.IConstruct]], result)

    @builtins.property
    def force(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("force")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingAspectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_s3.IBucket)
class RawBucket(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.s3_buckets.RawBucket",
):
    '''Do not use directly.

    Will be removed once a better replacemnt is written.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        accelerate_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.AccelerateConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        access_control: typing.Optional[builtins.str] = None,
        analytics_configurations: typing.Optional[typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.AnalyticsConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]]] = None,
        bucket_encryption: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.BucketEncryptionProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.CorsConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.IntelligentTieringConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]]] = None,
        inventory_configurations: typing.Optional[typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.InventoryConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]]] = None,
        lifecycle_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.LifecycleConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        logging_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.LoggingConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        metrics_configurations: typing.Optional[typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.MetricsConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]]] = None,
        notification_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.NotificationConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        object_lock_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.ObjectLockConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        object_lock_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.IResolvable]] = None,
        ownership_controls: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.OwnershipControlsProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        public_access_block_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.PublicAccessBlockConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        replication_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.ReplicationConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[aws_cdk.CfnTag, typing.Dict[str, typing.Any]]]] = None,
        versioning_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.VersioningConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        website_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.WebsiteConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
    ) -> None:
        '''Creates a new instance of the ReplicatedBucket class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param accelerate_configuration: Configures the transfer acceleration state for an Amazon S3 bucket. For more information, see `Amazon S3 Transfer Acceleration <https://docs.aws.amazon.com/AmazonS3/latest/dev/transfer-acceleration.html>`_ in the *Amazon S3 User Guide* .
        :param access_control: A canned access control list (ACL) that grants predefined permissions to the bucket. For more information about canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl>`_ in the *Amazon S3 User Guide* . Be aware that the syntax for this property differs from the information provided in the *Amazon S3 User Guide* . The AccessControl property is case-sensitive and must be one of the following values: Private, PublicRead, PublicReadWrite, AuthenticatedRead, LogDeliveryWrite, BucketOwnerRead, BucketOwnerFullControl, or AwsExecRead.
        :param analytics_configurations: Specifies the configuration and any analyses for the analytics filter of an Amazon S3 bucket.
        :param bucket_encryption: Specifies default encryption for a bucket using server-side encryption with Amazon S3-managed keys (SSE-S3) or AWS KMS-managed keys (SSE-KMS) bucket. For information about the Amazon S3 default encryption feature, see `Amazon S3 Default Encryption for S3 Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-encryption.html>`_ in the *Amazon S3 User Guide* .
        :param bucket_name: A name for the bucket. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must contain only lowercase letters, numbers, periods (.), and dashes (-) and must follow `Amazon S3 bucket restrictions and limitations <https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html>`_ . For more information, see `Rules for naming Amazon S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html#bucketnamingrules>`_ in the *Amazon S3 User Guide* . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.
        :param cors_configuration: Describes the cross-origin access configuration for objects in an Amazon S3 bucket. For more information, see `Enabling Cross-Origin Resource Sharing <https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html>`_ in the *Amazon S3 User Guide* .
        :param intelligent_tiering_configurations: Defines how Amazon S3 handles Intelligent-Tiering storage.
        :param inventory_configurations: Specifies the inventory configuration for an Amazon S3 bucket. For more information, see `GET Bucket inventory <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETInventoryConfig.html>`_ in the *Amazon S3 API Reference* .
        :param lifecycle_configuration: Specifies the lifecycle configuration for objects in an Amazon S3 bucket. For more information, see `Object Lifecycle Management <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html>`_ in the *Amazon S3 User Guide* .
        :param logging_configuration: Settings that define where logs are stored.
        :param metrics_configurations: Specifies a metrics configuration for the CloudWatch request metrics (specified by the metrics configuration ID) from an Amazon S3 bucket. If you're updating an existing metrics configuration, note that this is a full replacement of the existing metrics configuration. If you don't include the elements you want to keep, they are erased. For more information, see `PutBucketMetricsConfiguration <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTMetricConfiguration.html>`_ .
        :param notification_configuration: Configuration that defines how Amazon S3 handles bucket notifications.
        :param object_lock_configuration: Places an Object Lock configuration on the specified bucket. The rule specified in the Object Lock configuration will be applied by default to every new object placed in the specified bucket. For more information, see `Locking Objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock.html>`_ . .. epigraph:: - The ``DefaultRetention`` settings require both a mode and a period. - The ``DefaultRetention`` period can be either ``Days`` or ``Years`` but you must select one. You cannot specify ``Days`` and ``Years`` at the same time. - You can only enable Object Lock for new buckets. If you want to turn on Object Lock for an existing bucket, contact AWS Support.
        :param object_lock_enabled: Indicates whether this bucket has an Object Lock configuration enabled. Enable ``ObjectLockEnabled`` when you apply ``ObjectLockConfiguration`` to a bucket.
        :param ownership_controls: Configuration that defines how Amazon S3 handles Object Ownership rules.
        :param public_access_block_configuration: Configuration that defines how Amazon S3 handles public access.
        :param replication_configuration: Configuration for replicating objects in an S3 bucket. To enable replication, you must also enable versioning by using the ``VersioningConfiguration`` property. Amazon S3 can store replicated objects in a single destination bucket or multiple destination buckets. The destination bucket or buckets must already exist.
        :param tags: An arbitrary set of tags (key-value pairs) for this S3 bucket.
        :param versioning_configuration: Enables multiple versions of all objects in this bucket. You might enable versioning to prevent objects from being deleted or overwritten by mistake or to archive objects so that you can retrieve previous versions of them.
        :param website_configuration: Information used to configure the bucket as a static website. For more information, see `Hosting Websites on Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RawBucketProps(
            accelerate_configuration=accelerate_configuration,
            access_control=access_control,
            analytics_configurations=analytics_configurations,
            bucket_encryption=bucket_encryption,
            bucket_name=bucket_name,
            cors_configuration=cors_configuration,
            intelligent_tiering_configurations=intelligent_tiering_configurations,
            inventory_configurations=inventory_configurations,
            lifecycle_configuration=lifecycle_configuration,
            logging_configuration=logging_configuration,
            metrics_configurations=metrics_configurations,
            notification_configuration=notification_configuration,
            object_lock_configuration=object_lock_configuration,
            object_lock_enabled=object_lock_enabled,
            ownership_controls=ownership_controls,
            public_access_block_configuration=public_access_block_configuration,
            replication_configuration=replication_configuration,
            tags=tags,
            versioning_configuration=versioning_configuration,
            website_configuration=website_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addEventNotification")
    def add_event_notification(
        self,
        _event: aws_cdk.aws_s3.EventType,
        _dest: aws_cdk.aws_s3.IBucketNotificationDestination,
        *_filters: aws_cdk.aws_s3.NotificationKeyFilter,
    ) -> None:
        '''Adds a bucket notification event destination.

        :param _event: -
        :param _dest: -
        :param _filters: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.add_event_notification)
            check_type(argname="argument _event", value=_event, expected_type=type_hints["_event"])
            check_type(argname="argument _dest", value=_dest, expected_type=type_hints["_dest"])
            check_type(argname="argument _filters", value=_filters, expected_type=typing.Tuple[type_hints["_filters"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addEventNotification", [_event, _dest, *_filters]))

    @jsii.member(jsii_name="addObjectCreatedNotification")
    def add_object_created_notification(
        self,
        _dest: aws_cdk.aws_s3.IBucketNotificationDestination,
        *_filters: aws_cdk.aws_s3.NotificationKeyFilter,
    ) -> None:
        '''Subscribes a destination to receive notifications when an object is created in the bucket.

        This is identical to calling
        ``onEvent(s3.EventType.OBJECT_CREATED)``.

        :param _dest: -
        :param _filters: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.add_object_created_notification)
            check_type(argname="argument _dest", value=_dest, expected_type=type_hints["_dest"])
            check_type(argname="argument _filters", value=_filters, expected_type=typing.Tuple[type_hints["_filters"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addObjectCreatedNotification", [_dest, *_filters]))

    @jsii.member(jsii_name="addObjectRemovedNotification")
    def add_object_removed_notification(
        self,
        _dest: aws_cdk.aws_s3.IBucketNotificationDestination,
        *_filters: aws_cdk.aws_s3.NotificationKeyFilter,
    ) -> None:
        '''Subscribes a destination to receive notifications when an object is removed from the bucket.

        This is identical to calling
        ``onEvent(EventType.OBJECT_REMOVED)``.

        :param _dest: -
        :param _filters: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.add_object_removed_notification)
            check_type(argname="argument _dest", value=_dest, expected_type=type_hints["_dest"])
            check_type(argname="argument _filters", value=_filters, expected_type=typing.Tuple[type_hints["_filters"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addObjectRemovedNotification", [_dest, *_filters]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        permission: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        '''Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this bucket and/or its contents. Use ``bucketArn`` and ``arnForObjects(keys)`` to obtain ARNs for this bucket or objects.

        Note that the policy statement may or may not be added to the policy.
        For example, when an ``IBucket`` is created from an existing bucket,
        it's not possible to tell whether the bucket already has a policy
        attached, let alone to re-use that policy to add more statements to it.
        So it's safest to do nothing in these cases.

        :param permission: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.add_to_resource_policy)
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        return typing.cast(aws_cdk.aws_iam.AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [permission]))

    @jsii.member(jsii_name="arnForObjects")
    def arn_for_objects(self, _key_pattern: builtins.str) -> builtins.str:
        '''Returns an ARN that represents all objects within the bucket that match the key pattern specified.

        To represent all keys, specify ``"*"``.

        :param _key_pattern: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.arn_for_objects)
            check_type(argname="argument _key_pattern", value=_key_pattern, expected_type=type_hints["_key_pattern"])
        return typing.cast(builtins.str, jsii.invoke(self, "arnForObjects", [_key_pattern]))

    @jsii.member(jsii_name="enableEventBridgeNotification")
    def enable_event_bridge_notification(self) -> None:
        '''Enables event bridge notification, causing all events below to be sent to EventBridge:.

        - Object Deleted (DeleteObject)
        - Object Deleted (Lifecycle expiration)
        - Object Restore Initiated
        - Object Restore Completed
        - Object Restore Expired
        - Object Storage Class Changed
        - Object Access Tier Changed
        - Object ACL Updated
        - Object Tags Added
        - Object Tags Deleted
        '''
        return typing.cast(None, jsii.invoke(self, "enableEventBridgeNotification", []))

    @jsii.member(jsii_name="grantDelete")
    def grant_delete(
        self,
        _identity: aws_cdk.aws_iam.IGrantable,
        _objects_key_pattern: typing.Any = None,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grants s3:DeleteObject* permission to an IAM principal for objects in this bucket.

        :param _identity: -
        :param _objects_key_pattern: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.grant_delete)
            check_type(argname="argument _identity", value=_identity, expected_type=type_hints["_identity"])
            check_type(argname="argument _objects_key_pattern", value=_objects_key_pattern, expected_type=type_hints["_objects_key_pattern"])
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantDelete", [_identity, _objects_key_pattern]))

    @jsii.member(jsii_name="grantPublicAccess")
    def grant_public_access(
        self,
        _key_prefix: typing.Optional[builtins.str] = None,
        *_allowed_actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        '''Allows unrestricted access to objects from this bucket.

        IMPORTANT: This permission allows anyone to perform actions on S3 objects
        in this bucket, which is useful for when you configure your bucket as a
        website and want everyone to be able to read objects in the bucket without
        needing to authenticate.

        Without arguments, this method will grant read ("s3:GetObject") access to
        all objects ("*") in the bucket.

        The method returns the ``iam.Grant`` object, which can then be modified
        as needed. For example, you can add a condition that will restrict access only
        to an IPv4 range like this::

            const grant = bucket.grantPublicAccess();
            grant.resourceStatement!.addCondition(‘IpAddress’, { “aws:SourceIp”: “54.240.143.0/24” });

        :param _key_prefix: -
        :param _allowed_actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.grant_public_access)
            check_type(argname="argument _key_prefix", value=_key_prefix, expected_type=type_hints["_key_prefix"])
            check_type(argname="argument _allowed_actions", value=_allowed_actions, expected_type=typing.Tuple[type_hints["_allowed_actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantPublicAccess", [_key_prefix, *_allowed_actions]))

    @jsii.member(jsii_name="grantPut")
    def grant_put(
        self,
        _identity: aws_cdk.aws_iam.IGrantable,
        _objects_key_pattern: typing.Any = None,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grants s3:PutObject* and s3:Abort* permissions for this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        :param _identity: -
        :param _objects_key_pattern: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.grant_put)
            check_type(argname="argument _identity", value=_identity, expected_type=type_hints["_identity"])
            check_type(argname="argument _objects_key_pattern", value=_objects_key_pattern, expected_type=type_hints["_objects_key_pattern"])
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantPut", [_identity, _objects_key_pattern]))

    @jsii.member(jsii_name="grantPutAcl")
    def grant_put_acl(
        self,
        _identity: aws_cdk.aws_iam.IGrantable,
        _objects_key_pattern: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grant the given IAM identity permissions to modify the ACLs of objects in the given Bucket.

        If your application has the '@aws-cdk/aws-s3:grantWriteWithoutAcl' feature flag set,
        calling {@link grantWrite} or {@link grantReadWrite} no longer grants permissions to modify the ACLs of the objects;
        in this case, if you need to modify object ACLs, call this method explicitly.

        :param _identity: -
        :param _objects_key_pattern: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.grant_put_acl)
            check_type(argname="argument _identity", value=_identity, expected_type=type_hints["_identity"])
            check_type(argname="argument _objects_key_pattern", value=_objects_key_pattern, expected_type=type_hints["_objects_key_pattern"])
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantPutAcl", [_identity, _objects_key_pattern]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        _identity: aws_cdk.aws_iam.IGrantable,
        _objects_key_pattern: typing.Any = None,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grant read permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to decrypt the contents
        of the bucket will also be granted to the same principal.

        :param _identity: -
        :param _objects_key_pattern: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.grant_read)
            check_type(argname="argument _identity", value=_identity, expected_type=type_hints["_identity"])
            check_type(argname="argument _objects_key_pattern", value=_objects_key_pattern, expected_type=type_hints["_objects_key_pattern"])
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantRead", [_identity, _objects_key_pattern]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        _identity: aws_cdk.aws_iam.IGrantable,
        _objects_key_pattern: typing.Any = None,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grants read/write permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        Before CDK version 1.85.0, this method granted the ``s3:PutObject*`` permission that included ``s3:PutObjectAcl``,
        which could be used to grant read/write object access to IAM principals in other accounts.
        If you want to get rid of that behavior, update your CDK version to 1.85.0 or later,
        and make sure the ``@aws-cdk/aws-s3:grantWriteWithoutAcl`` feature flag is set to ``true``
        in the ``context`` key of your cdk.json file.
        If you've already updated, but still need the principal to have permissions to modify the ACLs,
        use the {@link grantPutAcl} method.

        :param _identity: -
        :param _objects_key_pattern: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.grant_read_write)
            check_type(argname="argument _identity", value=_identity, expected_type=type_hints["_identity"])
            check_type(argname="argument _objects_key_pattern", value=_objects_key_pattern, expected_type=type_hints["_objects_key_pattern"])
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantReadWrite", [_identity, _objects_key_pattern]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        _identity: aws_cdk.aws_iam.IGrantable,
        _objects_key_pattern: typing.Any = None,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grant write permissions to this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        Before CDK version 1.85.0, this method granted the ``s3:PutObject*`` permission that included ``s3:PutObjectAcl``,
        which could be used to grant read/write object access to IAM principals in other accounts.
        If you want to get rid of that behavior, update your CDK version to 1.85.0 or later,
        and make sure the ``@aws-cdk/aws-s3:grantWriteWithoutAcl`` feature flag is set to ``true``
        in the ``context`` key of your cdk.json file.
        If you've already updated, but still need the principal to have permissions to modify the ACLs,
        use the {@link grantPutAcl} method.

        :param _identity: -
        :param _objects_key_pattern: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.grant_write)
            check_type(argname="argument _identity", value=_identity, expected_type=type_hints["_identity"])
            check_type(argname="argument _objects_key_pattern", value=_objects_key_pattern, expected_type=type_hints["_objects_key_pattern"])
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantWrite", [_identity, _objects_key_pattern]))

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        _id: builtins.str,
        *,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[constructs.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[aws_cdk.aws_events.EventPattern, typing.Dict[str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines a CloudWatch event that triggers when something happens to this bucket.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param _id: -
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.on_cloud_trail_event)
            check_type(argname="argument _id", value=_id, expected_type=type_hints["_id"])
        _options = aws_cdk.aws_s3.OnCloudTrailBucketEventOptions(
            paths=paths,
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(aws_cdk.aws_events.Rule, jsii.invoke(self, "onCloudTrailEvent", [_id, _options]))

    @jsii.member(jsii_name="onCloudTrailPutObject")
    def on_cloud_trail_put_object(
        self,
        _id: builtins.str,
        *,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[constructs.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[aws_cdk.aws_events.EventPattern, typing.Dict[str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines an AWS CloudWatch event that triggers when an object is uploaded to the specified paths (keys) in this bucket using the PutObject API call.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using ``onCloudTrailWriteObject`` may be preferable.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param _id: -
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.on_cloud_trail_put_object)
            check_type(argname="argument _id", value=_id, expected_type=type_hints["_id"])
        _options = aws_cdk.aws_s3.OnCloudTrailBucketEventOptions(
            paths=paths,
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(aws_cdk.aws_events.Rule, jsii.invoke(self, "onCloudTrailPutObject", [_id, _options]))

    @jsii.member(jsii_name="onCloudTrailWriteObject")
    def on_cloud_trail_write_object(
        self,
        _id: builtins.str,
        *,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[constructs.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[aws_cdk.aws_events.EventPattern, typing.Dict[str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines an AWS CloudWatch event that triggers when an object at the specified paths (keys) in this bucket are written to.

        This includes
        the events PutObject, CopyObject, and CompleteMultipartUpload.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using this method may be preferable to ``onCloudTrailPutObject``.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param _id: -
        :param paths: Only watch changes to these object paths. Default: - Watch changes to all objects
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.on_cloud_trail_write_object)
            check_type(argname="argument _id", value=_id, expected_type=type_hints["_id"])
        _options = aws_cdk.aws_s3.OnCloudTrailBucketEventOptions(
            paths=paths,
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(aws_cdk.aws_events.Rule, jsii.invoke(self, "onCloudTrailWriteObject", [_id, _options]))

    @jsii.member(jsii_name="s3UrlForObject")
    def s3_url_for_object(
        self,
        _key: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''The S3 URL of an S3 object.

        For example:

        - ``s3://onlybucket``
        - ``s3://bucket/key``

        :param _key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.s3_url_for_object)
            check_type(argname="argument _key", value=_key, expected_type=type_hints["_key"])
        return typing.cast(builtins.str, jsii.invoke(self, "s3UrlForObject", [_key]))

    @jsii.member(jsii_name="transferAccelerationUrlForObject")
    def transfer_acceleration_url_for_object(
        self,
        _key: typing.Optional[builtins.str] = None,
        *,
        dual_stack: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''The https Transfer Acceleration URL of an S3 object.

        Specify ``dualStack: true`` at the options
        for dual-stack endpoint (connect to the bucket over IPv6). For example:

        - ``https://bucket.s3-accelerate.amazonaws.com``
        - ``https://bucket.s3-accelerate.amazonaws.com/key``

        :param _key: -
        :param dual_stack: Dual-stack support to connect to the bucket over IPv6. Default: - false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.transfer_acceleration_url_for_object)
            check_type(argname="argument _key", value=_key, expected_type=type_hints["_key"])
        _options = aws_cdk.aws_s3.TransferAccelerationUrlOptions(dual_stack=dual_stack)

        return typing.cast(builtins.str, jsii.invoke(self, "transferAccelerationUrlForObject", [_key, _options]))

    @jsii.member(jsii_name="urlForObject")
    def url_for_object(
        self,
        _key: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''The https URL of an S3 object. For example:.

        - ``https://s3.us-west-1.amazonaws.com/onlybucket``
        - ``https://s3.us-west-1.amazonaws.com/bucket/key``
        - ``https://s3.cn-north-1.amazonaws.com.cn/china-bucket/mykey``

        :param _key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.url_for_object)
            check_type(argname="argument _key", value=_key, expected_type=type_hints["_key"])
        return typing.cast(builtins.str, jsii.invoke(self, "urlForObject", [_key]))

    @jsii.member(jsii_name="virtualHostedUrlForObject")
    def virtual_hosted_url_for_object(
        self,
        _key: typing.Optional[builtins.str] = None,
        *,
        regional: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''The virtual hosted-style URL of an S3 object. Specify ``regional: false`` at the options for non-regional URL. For example:.

        - ``https://only-bucket.s3.us-west-1.amazonaws.com``
        - ``https://bucket.s3.us-west-1.amazonaws.com/key``
        - ``https://bucket.s3.amazonaws.com/key``
        - ``https://china-bucket.s3.cn-north-1.amazonaws.com.cn/mykey``

        :param _key: -
        :param regional: Specifies the URL includes the region. Default: - true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucket.virtual_hosted_url_for_object)
            check_type(argname="argument _key", value=_key, expected_type=type_hints["_key"])
        _options = aws_cdk.aws_s3.VirtualHostedStyleUrlOptions(regional=regional)

        return typing.cast(builtins.str, jsii.invoke(self, "virtualHostedUrlForObject", [_key, _options]))

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        '''The ARN of the bucket.'''
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @builtins.property
    @jsii.member(jsii_name="bucketDomainName")
    def bucket_domain_name(self) -> builtins.str:
        '''The IPv4 DNS name of the specified bucket.'''
        return typing.cast(builtins.str, jsii.get(self, "bucketDomainName"))

    @builtins.property
    @jsii.member(jsii_name="bucketDualStackDomainName")
    def bucket_dual_stack_domain_name(self) -> builtins.str:
        '''The IPv6 DNS name of the specified bucket.'''
        return typing.cast(builtins.str, jsii.get(self, "bucketDualStackDomainName"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''The name of the bucket.'''
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @builtins.property
    @jsii.member(jsii_name="bucketRegionalDomainName")
    def bucket_regional_domain_name(self) -> builtins.str:
        '''The regional domain name of the specified bucket.'''
        return typing.cast(builtins.str, jsii.get(self, "bucketRegionalDomainName"))

    @builtins.property
    @jsii.member(jsii_name="bucketWebsiteDomainName")
    def bucket_website_domain_name(self) -> builtins.str:
        '''The Domain name of the static website.'''
        return typing.cast(builtins.str, jsii.get(self, "bucketWebsiteDomainName"))

    @builtins.property
    @jsii.member(jsii_name="bucketWebsiteUrl")
    def bucket_website_url(self) -> builtins.str:
        '''The URL of the static website.'''
        return typing.cast(builtins.str, jsii.get(self, "bucketWebsiteUrl"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_s3.CfnBucket:
        return typing.cast(aws_cdk.aws_s3.CfnBucket, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''Optional KMS encryption key associated with this bucket.'''
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="isWebsite")
    def is_website(self) -> typing.Optional[builtins.bool]:
        '''If this bucket has been configured for static website hosting.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "isWebsite"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[aws_cdk.aws_s3.BucketPolicy]:
        '''The resource policy associated with this bucket.

        If ``autoCreatePolicy`` is true, a ``BucketPolicy`` will be created upon the
        first call to addToResourcePolicy(s).
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BucketPolicy], jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Optional[aws_cdk.aws_s3.BucketPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(RawBucket, "policy").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)


@jsii.data_type(
    jsii_type="cdk-extensions.s3_buckets.RawBucketProps",
    jsii_struct_bases=[aws_cdk.aws_s3.CfnBucketProps],
    name_mapping={
        "accelerate_configuration": "accelerateConfiguration",
        "access_control": "accessControl",
        "analytics_configurations": "analyticsConfigurations",
        "bucket_encryption": "bucketEncryption",
        "bucket_name": "bucketName",
        "cors_configuration": "corsConfiguration",
        "intelligent_tiering_configurations": "intelligentTieringConfigurations",
        "inventory_configurations": "inventoryConfigurations",
        "lifecycle_configuration": "lifecycleConfiguration",
        "logging_configuration": "loggingConfiguration",
        "metrics_configurations": "metricsConfigurations",
        "notification_configuration": "notificationConfiguration",
        "object_lock_configuration": "objectLockConfiguration",
        "object_lock_enabled": "objectLockEnabled",
        "ownership_controls": "ownershipControls",
        "public_access_block_configuration": "publicAccessBlockConfiguration",
        "replication_configuration": "replicationConfiguration",
        "tags": "tags",
        "versioning_configuration": "versioningConfiguration",
        "website_configuration": "websiteConfiguration",
    },
)
class RawBucketProps(aws_cdk.aws_s3.CfnBucketProps):
    def __init__(
        self,
        *,
        accelerate_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.AccelerateConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        access_control: typing.Optional[builtins.str] = None,
        analytics_configurations: typing.Optional[typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.AnalyticsConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]]] = None,
        bucket_encryption: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.BucketEncryptionProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.CorsConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.IntelligentTieringConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]]] = None,
        inventory_configurations: typing.Optional[typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.InventoryConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]]] = None,
        lifecycle_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.LifecycleConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        logging_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.LoggingConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        metrics_configurations: typing.Optional[typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.MetricsConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]]] = None,
        notification_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.NotificationConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        object_lock_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.ObjectLockConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        object_lock_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.IResolvable]] = None,
        ownership_controls: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.OwnershipControlsProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        public_access_block_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.PublicAccessBlockConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        replication_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.ReplicationConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[aws_cdk.CfnTag, typing.Dict[str, typing.Any]]]] = None,
        versioning_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.VersioningConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
        website_configuration: typing.Optional[typing.Union[typing.Union[aws_cdk.aws_s3.CfnBucket.WebsiteConfigurationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]] = None,
    ) -> None:
        '''Configuration for objects bucket.

        :param accelerate_configuration: Configures the transfer acceleration state for an Amazon S3 bucket. For more information, see `Amazon S3 Transfer Acceleration <https://docs.aws.amazon.com/AmazonS3/latest/dev/transfer-acceleration.html>`_ in the *Amazon S3 User Guide* .
        :param access_control: A canned access control list (ACL) that grants predefined permissions to the bucket. For more information about canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl>`_ in the *Amazon S3 User Guide* . Be aware that the syntax for this property differs from the information provided in the *Amazon S3 User Guide* . The AccessControl property is case-sensitive and must be one of the following values: Private, PublicRead, PublicReadWrite, AuthenticatedRead, LogDeliveryWrite, BucketOwnerRead, BucketOwnerFullControl, or AwsExecRead.
        :param analytics_configurations: Specifies the configuration and any analyses for the analytics filter of an Amazon S3 bucket.
        :param bucket_encryption: Specifies default encryption for a bucket using server-side encryption with Amazon S3-managed keys (SSE-S3) or AWS KMS-managed keys (SSE-KMS) bucket. For information about the Amazon S3 default encryption feature, see `Amazon S3 Default Encryption for S3 Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-encryption.html>`_ in the *Amazon S3 User Guide* .
        :param bucket_name: A name for the bucket. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must contain only lowercase letters, numbers, periods (.), and dashes (-) and must follow `Amazon S3 bucket restrictions and limitations <https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html>`_ . For more information, see `Rules for naming Amazon S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html#bucketnamingrules>`_ in the *Amazon S3 User Guide* . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.
        :param cors_configuration: Describes the cross-origin access configuration for objects in an Amazon S3 bucket. For more information, see `Enabling Cross-Origin Resource Sharing <https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html>`_ in the *Amazon S3 User Guide* .
        :param intelligent_tiering_configurations: Defines how Amazon S3 handles Intelligent-Tiering storage.
        :param inventory_configurations: Specifies the inventory configuration for an Amazon S3 bucket. For more information, see `GET Bucket inventory <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETInventoryConfig.html>`_ in the *Amazon S3 API Reference* .
        :param lifecycle_configuration: Specifies the lifecycle configuration for objects in an Amazon S3 bucket. For more information, see `Object Lifecycle Management <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html>`_ in the *Amazon S3 User Guide* .
        :param logging_configuration: Settings that define where logs are stored.
        :param metrics_configurations: Specifies a metrics configuration for the CloudWatch request metrics (specified by the metrics configuration ID) from an Amazon S3 bucket. If you're updating an existing metrics configuration, note that this is a full replacement of the existing metrics configuration. If you don't include the elements you want to keep, they are erased. For more information, see `PutBucketMetricsConfiguration <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTMetricConfiguration.html>`_ .
        :param notification_configuration: Configuration that defines how Amazon S3 handles bucket notifications.
        :param object_lock_configuration: Places an Object Lock configuration on the specified bucket. The rule specified in the Object Lock configuration will be applied by default to every new object placed in the specified bucket. For more information, see `Locking Objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock.html>`_ . .. epigraph:: - The ``DefaultRetention`` settings require both a mode and a period. - The ``DefaultRetention`` period can be either ``Days`` or ``Years`` but you must select one. You cannot specify ``Days`` and ``Years`` at the same time. - You can only enable Object Lock for new buckets. If you want to turn on Object Lock for an existing bucket, contact AWS Support.
        :param object_lock_enabled: Indicates whether this bucket has an Object Lock configuration enabled. Enable ``ObjectLockEnabled`` when you apply ``ObjectLockConfiguration`` to a bucket.
        :param ownership_controls: Configuration that defines how Amazon S3 handles Object Ownership rules.
        :param public_access_block_configuration: Configuration that defines how Amazon S3 handles public access.
        :param replication_configuration: Configuration for replicating objects in an S3 bucket. To enable replication, you must also enable versioning by using the ``VersioningConfiguration`` property. Amazon S3 can store replicated objects in a single destination bucket or multiple destination buckets. The destination bucket or buckets must already exist.
        :param tags: An arbitrary set of tags (key-value pairs) for this S3 bucket.
        :param versioning_configuration: Enables multiple versions of all objects in this bucket. You might enable versioning to prevent objects from being deleted or overwritten by mistake or to archive objects so that you can retrieve previous versions of them.
        :param website_configuration: Information used to configure the bucket as a static website. For more information, see `Hosting Websites on Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RawBucketProps.__init__)
            check_type(argname="argument accelerate_configuration", value=accelerate_configuration, expected_type=type_hints["accelerate_configuration"])
            check_type(argname="argument access_control", value=access_control, expected_type=type_hints["access_control"])
            check_type(argname="argument analytics_configurations", value=analytics_configurations, expected_type=type_hints["analytics_configurations"])
            check_type(argname="argument bucket_encryption", value=bucket_encryption, expected_type=type_hints["bucket_encryption"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument cors_configuration", value=cors_configuration, expected_type=type_hints["cors_configuration"])
            check_type(argname="argument intelligent_tiering_configurations", value=intelligent_tiering_configurations, expected_type=type_hints["intelligent_tiering_configurations"])
            check_type(argname="argument inventory_configurations", value=inventory_configurations, expected_type=type_hints["inventory_configurations"])
            check_type(argname="argument lifecycle_configuration", value=lifecycle_configuration, expected_type=type_hints["lifecycle_configuration"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument metrics_configurations", value=metrics_configurations, expected_type=type_hints["metrics_configurations"])
            check_type(argname="argument notification_configuration", value=notification_configuration, expected_type=type_hints["notification_configuration"])
            check_type(argname="argument object_lock_configuration", value=object_lock_configuration, expected_type=type_hints["object_lock_configuration"])
            check_type(argname="argument object_lock_enabled", value=object_lock_enabled, expected_type=type_hints["object_lock_enabled"])
            check_type(argname="argument ownership_controls", value=ownership_controls, expected_type=type_hints["ownership_controls"])
            check_type(argname="argument public_access_block_configuration", value=public_access_block_configuration, expected_type=type_hints["public_access_block_configuration"])
            check_type(argname="argument replication_configuration", value=replication_configuration, expected_type=type_hints["replication_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument versioning_configuration", value=versioning_configuration, expected_type=type_hints["versioning_configuration"])
            check_type(argname="argument website_configuration", value=website_configuration, expected_type=type_hints["website_configuration"])
        self._values: typing.Dict[str, typing.Any] = {}
        if accelerate_configuration is not None:
            self._values["accelerate_configuration"] = accelerate_configuration
        if access_control is not None:
            self._values["access_control"] = access_control
        if analytics_configurations is not None:
            self._values["analytics_configurations"] = analytics_configurations
        if bucket_encryption is not None:
            self._values["bucket_encryption"] = bucket_encryption
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if cors_configuration is not None:
            self._values["cors_configuration"] = cors_configuration
        if intelligent_tiering_configurations is not None:
            self._values["intelligent_tiering_configurations"] = intelligent_tiering_configurations
        if inventory_configurations is not None:
            self._values["inventory_configurations"] = inventory_configurations
        if lifecycle_configuration is not None:
            self._values["lifecycle_configuration"] = lifecycle_configuration
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if metrics_configurations is not None:
            self._values["metrics_configurations"] = metrics_configurations
        if notification_configuration is not None:
            self._values["notification_configuration"] = notification_configuration
        if object_lock_configuration is not None:
            self._values["object_lock_configuration"] = object_lock_configuration
        if object_lock_enabled is not None:
            self._values["object_lock_enabled"] = object_lock_enabled
        if ownership_controls is not None:
            self._values["ownership_controls"] = ownership_controls
        if public_access_block_configuration is not None:
            self._values["public_access_block_configuration"] = public_access_block_configuration
        if replication_configuration is not None:
            self._values["replication_configuration"] = replication_configuration
        if tags is not None:
            self._values["tags"] = tags
        if versioning_configuration is not None:
            self._values["versioning_configuration"] = versioning_configuration
        if website_configuration is not None:
            self._values["website_configuration"] = website_configuration

    @builtins.property
    def accelerate_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.AccelerateConfigurationProperty, aws_cdk.IResolvable]]:
        '''Configures the transfer acceleration state for an Amazon S3 bucket.

        For more information, see `Amazon S3 Transfer Acceleration <https://docs.aws.amazon.com/AmazonS3/latest/dev/transfer-acceleration.html>`_ in the *Amazon S3 User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-accelerateconfiguration
        '''
        result = self._values.get("accelerate_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.AccelerateConfigurationProperty, aws_cdk.IResolvable]], result)

    @builtins.property
    def access_control(self) -> typing.Optional[builtins.str]:
        '''A canned access control list (ACL) that grants predefined permissions to the bucket.

        For more information about canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl>`_ in the *Amazon S3 User Guide* .

        Be aware that the syntax for this property differs from the information provided in the *Amazon S3 User Guide* . The AccessControl property is case-sensitive and must be one of the following values: Private, PublicRead, PublicReadWrite, AuthenticatedRead, LogDeliveryWrite, BucketOwnerRead, BucketOwnerFullControl, or AwsExecRead.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-accesscontrol
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def analytics_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_s3.CfnBucket.AnalyticsConfigurationProperty, aws_cdk.IResolvable]]]]:
        '''Specifies the configuration and any analyses for the analytics filter of an Amazon S3 bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-analyticsconfigurations
        '''
        result = self._values.get("analytics_configurations")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_s3.CfnBucket.AnalyticsConfigurationProperty, aws_cdk.IResolvable]]]], result)

    @builtins.property
    def bucket_encryption(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.BucketEncryptionProperty, aws_cdk.IResolvable]]:
        '''Specifies default encryption for a bucket using server-side encryption with Amazon S3-managed keys (SSE-S3) or AWS KMS-managed keys (SSE-KMS) bucket.

        For information about the Amazon S3 default encryption feature, see `Amazon S3 Default Encryption for S3 Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-encryption.html>`_ in the *Amazon S3 User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-bucketencryption
        '''
        result = self._values.get("bucket_encryption")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.BucketEncryptionProperty, aws_cdk.IResolvable]], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''A name for the bucket.

        If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must contain only lowercase letters, numbers, periods (.), and dashes (-) and must follow `Amazon S3 bucket restrictions and limitations <https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html>`_ . For more information, see `Rules for naming Amazon S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html#bucketnamingrules>`_ in the *Amazon S3 User Guide* .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-name
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.CorsConfigurationProperty, aws_cdk.IResolvable]]:
        '''Describes the cross-origin access configuration for objects in an Amazon S3 bucket.

        For more information, see `Enabling Cross-Origin Resource Sharing <https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html>`_ in the *Amazon S3 User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-crossoriginconfig
        '''
        result = self._values.get("cors_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.CorsConfigurationProperty, aws_cdk.IResolvable]], result)

    @builtins.property
    def intelligent_tiering_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_s3.CfnBucket.IntelligentTieringConfigurationProperty, aws_cdk.IResolvable]]]]:
        '''Defines how Amazon S3 handles Intelligent-Tiering storage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-intelligenttieringconfigurations
        '''
        result = self._values.get("intelligent_tiering_configurations")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_s3.CfnBucket.IntelligentTieringConfigurationProperty, aws_cdk.IResolvable]]]], result)

    @builtins.property
    def inventory_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_s3.CfnBucket.InventoryConfigurationProperty, aws_cdk.IResolvable]]]]:
        '''Specifies the inventory configuration for an Amazon S3 bucket.

        For more information, see `GET Bucket inventory <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETInventoryConfig.html>`_ in the *Amazon S3 API Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-inventoryconfigurations
        '''
        result = self._values.get("inventory_configurations")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_s3.CfnBucket.InventoryConfigurationProperty, aws_cdk.IResolvable]]]], result)

    @builtins.property
    def lifecycle_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.LifecycleConfigurationProperty, aws_cdk.IResolvable]]:
        '''Specifies the lifecycle configuration for objects in an Amazon S3 bucket.

        For more information, see `Object Lifecycle Management <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html>`_ in the *Amazon S3 User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-lifecycleconfig
        '''
        result = self._values.get("lifecycle_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.LifecycleConfigurationProperty, aws_cdk.IResolvable]], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.LoggingConfigurationProperty, aws_cdk.IResolvable]]:
        '''Settings that define where logs are stored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-loggingconfig
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.LoggingConfigurationProperty, aws_cdk.IResolvable]], result)

    @builtins.property
    def metrics_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_s3.CfnBucket.MetricsConfigurationProperty, aws_cdk.IResolvable]]]]:
        '''Specifies a metrics configuration for the CloudWatch request metrics (specified by the metrics configuration ID) from an Amazon S3 bucket.

        If you're updating an existing metrics configuration, note that this is a full replacement of the existing metrics configuration. If you don't include the elements you want to keep, they are erased. For more information, see `PutBucketMetricsConfiguration <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTMetricConfiguration.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-metricsconfigurations
        '''
        result = self._values.get("metrics_configurations")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.IResolvable, typing.List[typing.Union[aws_cdk.aws_s3.CfnBucket.MetricsConfigurationProperty, aws_cdk.IResolvable]]]], result)

    @builtins.property
    def notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.NotificationConfigurationProperty, aws_cdk.IResolvable]]:
        '''Configuration that defines how Amazon S3 handles bucket notifications.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-notification
        '''
        result = self._values.get("notification_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.NotificationConfigurationProperty, aws_cdk.IResolvable]], result)

    @builtins.property
    def object_lock_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.ObjectLockConfigurationProperty, aws_cdk.IResolvable]]:
        '''Places an Object Lock configuration on the specified bucket.

        The rule specified in the Object Lock configuration will be applied by default to every new object placed in the specified bucket. For more information, see `Locking Objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock.html>`_ .
        .. epigraph::

           - The ``DefaultRetention`` settings require both a mode and a period.
           - The ``DefaultRetention`` period can be either ``Days`` or ``Years`` but you must select one. You cannot specify ``Days`` and ``Years`` at the same time.
           - You can only enable Object Lock for new buckets. If you want to turn on Object Lock for an existing bucket, contact AWS Support.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-objectlockconfiguration
        '''
        result = self._values.get("object_lock_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.ObjectLockConfigurationProperty, aws_cdk.IResolvable]], result)

    @builtins.property
    def object_lock_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.IResolvable]]:
        '''Indicates whether this bucket has an Object Lock configuration enabled.

        Enable ``ObjectLockEnabled`` when you apply ``ObjectLockConfiguration`` to a bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-objectlockenabled
        '''
        result = self._values.get("object_lock_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.IResolvable]], result)

    @builtins.property
    def ownership_controls(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.OwnershipControlsProperty, aws_cdk.IResolvable]]:
        '''Configuration that defines how Amazon S3 handles Object Ownership rules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-ownershipcontrols
        '''
        result = self._values.get("ownership_controls")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.OwnershipControlsProperty, aws_cdk.IResolvable]], result)

    @builtins.property
    def public_access_block_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.PublicAccessBlockConfigurationProperty, aws_cdk.IResolvable]]:
        '''Configuration that defines how Amazon S3 handles public access.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-publicaccessblockconfiguration
        '''
        result = self._values.get("public_access_block_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.PublicAccessBlockConfigurationProperty, aws_cdk.IResolvable]], result)

    @builtins.property
    def replication_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.ReplicationConfigurationProperty, aws_cdk.IResolvable]]:
        '''Configuration for replicating objects in an S3 bucket.

        To enable replication, you must also enable versioning by using the ``VersioningConfiguration`` property.

        Amazon S3 can store replicated objects in a single destination bucket or multiple destination buckets. The destination bucket or buckets must already exist.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-replicationconfiguration
        '''
        result = self._values.get("replication_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.ReplicationConfigurationProperty, aws_cdk.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.CfnTag]]:
        '''An arbitrary set of tags (key-value pairs) for this S3 bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.CfnTag]], result)

    @builtins.property
    def versioning_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.VersioningConfigurationProperty, aws_cdk.IResolvable]]:
        '''Enables multiple versions of all objects in this bucket.

        You might enable versioning to prevent objects from being deleted or overwritten by mistake or to archive objects so that you can retrieve previous versions of them.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-versioning
        '''
        result = self._values.get("versioning_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.VersioningConfigurationProperty, aws_cdk.IResolvable]], result)

    @builtins.property
    def website_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.WebsiteConfigurationProperty, aws_cdk.IResolvable]]:
        '''Information used to configure the bucket as a static website.

        For more information, see `Hosting Websites on Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-websiteconfiguration
        '''
        result = self._values.get("website_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.aws_s3.CfnBucket.WebsiteConfigurationProperty, aws_cdk.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RawBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3AccessLogsBucket(
    RawBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.s3_buckets.S3AccessLogsBucket",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the S3AccessLogsBucket class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3AccessLogsBucket.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3AccessLogsBucketProps(
            bucket_name=bucket_name,
            create_queries=create_queries,
            database=database,
            friendly_query_names=friendly_query_names,
            table_name=table_name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addLoggingAspect")
    def add_logging_aspect(
        self,
        scope: constructs.IConstruct,
        *,
        exclusions: typing.Optional[typing.Sequence[constructs.IConstruct]] = None,
        force: typing.Optional[builtins.bool] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param exclusions: 
        :param force: 
        :param prefix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3AccessLogsBucket.add_logging_aspect)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = LoggingAspectOptions(
            exclusions=exclusions, force=force, prefix=prefix
        )

        return typing.cast(None, jsii.invoke(self, "addLoggingAspect", [scope, options]))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> _Database_5971ae38:
        return typing.cast(_Database_5971ae38, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _S3AccessLogsTable_cd828e2c:
        return typing.cast(_S3AccessLogsTable_cd828e2c, jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "friendlyQueryNames"))


@jsii.data_type(
    jsii_type="cdk-extensions.s3_buckets.S3AccessLogsBucketProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket_name": "bucketName",
        "create_queries": "createQueries",
        "database": "database",
        "friendly_query_names": "friendlyQueryNames",
        "table_name": "tableName",
    },
)
class S3AccessLogsBucketProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for objects bucket.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3AccessLogsBucketProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if database is not None:
            self._values["database"] = database
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if table_name is not None:
            self._values["table_name"] = table_name

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
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database(self) -> typing.Optional[_Database_5971ae38]:
        result = self._values.get("database")
        return typing.cast(typing.Optional[_Database_5971ae38], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3AccessLogsBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SesLogsBucket(
    RawBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.s3_buckets.SesLogsBucket",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the CloudtrailBucket class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SesLogsBucket.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SesLogsBucketProps(
            bucket_name=bucket_name,
            create_queries=create_queries,
            database=database,
            friendly_query_names=friendly_query_names,
            table_name=table_name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> _Database_5971ae38:
        return typing.cast(_Database_5971ae38, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _SesLogsTable_15e214c8:
        return typing.cast(_SesLogsTable_15e214c8, jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "friendlyQueryNames"))


@jsii.data_type(
    jsii_type="cdk-extensions.s3_buckets.SesLogsBucketProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket_name": "bucketName",
        "create_queries": "createQueries",
        "database": "database",
        "friendly_query_names": "friendlyQueryNames",
        "table_name": "tableName",
    },
)
class SesLogsBucketProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for objects bucket.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SesLogsBucketProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if database is not None:
            self._values["database"] = database
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if table_name is not None:
            self._values["table_name"] = table_name

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
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database(self) -> typing.Optional[_Database_5971ae38]:
        result = self._values.get("database")
        return typing.cast(typing.Optional[_Database_5971ae38], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SesLogsBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafLogsBucket(
    RawBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.s3_buckets.WafLogsBucket",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the WafLogsBucket class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WafLogsBucket.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WafLogsBucketProps(
            bucket_name=bucket_name,
            create_queries=create_queries,
            database=database,
            friendly_query_names=friendly_query_names,
            table_name=table_name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> _Database_5971ae38:
        return typing.cast(_Database_5971ae38, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _WafLogsTable_2c2a9653:
        return typing.cast(_WafLogsTable_2c2a9653, jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "friendlyQueryNames"))


@jsii.data_type(
    jsii_type="cdk-extensions.s3_buckets.WafLogsBucketProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "bucket_name": "bucketName",
        "create_queries": "createQueries",
        "database": "database",
        "friendly_query_names": "friendlyQueryNames",
        "table_name": "tableName",
    },
)
class WafLogsBucketProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for objects bucket.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WafLogsBucketProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument create_queries", value=create_queries, expected_type=type_hints["create_queries"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if create_queries is not None:
            self._values["create_queries"] = create_queries
        if database is not None:
            self._values["database"] = database
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if table_name is not None:
            self._values["table_name"] = table_name

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
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_queries(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database(self) -> typing.Optional[_Database_5971ae38]:
        result = self._values.get("database")
        return typing.cast(typing.Optional[_Database_5971ae38], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafLogsBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlbLogsBucket(
    RawBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.s3_buckets.AlbLogsBucket",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the ElbLogsBucket class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AlbLogsBucket.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AlbLogsBucketProps(
            bucket_name=bucket_name,
            create_queries=create_queries,
            database=database,
            friendly_query_names=friendly_query_names,
            table_name=table_name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> _Database_5971ae38:
        return typing.cast(_Database_5971ae38, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _AlbLogsTable_03497db2:
        return typing.cast(_AlbLogsTable_03497db2, jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "friendlyQueryNames"))


class CloudfrontLogsBucket(
    RawBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.s3_buckets.CloudfrontLogsBucket",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the ElbLogsBucket class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudfrontLogsBucket.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudfrontLogsBucketProps(
            bucket_name=bucket_name,
            create_queries=create_queries,
            database=database,
            friendly_query_names=friendly_query_names,
            table_name=table_name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> _Database_5971ae38:
        return typing.cast(_Database_5971ae38, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _CloudfrontLogsTable_f83f287b:
        return typing.cast(_CloudfrontLogsTable_f83f287b, jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "friendlyQueryNames"))


class CloudtrailBucket(
    RawBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.s3_buckets.CloudtrailBucket",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the CloudtrailBucket class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket_name: 
        :param create_queries: 
        :param database: 
        :param friendly_query_names: 
        :param table_name: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudtrailBucket.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudtrailBucketProps(
            bucket_name=bucket_name,
            create_queries=create_queries,
            database=database,
            friendly_query_names=friendly_query_names,
            table_name=table_name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> _Database_5971ae38:
        return typing.cast(_Database_5971ae38, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _CloudtrailTable_e3a95430:
        return typing.cast(_CloudtrailTable_e3a95430, jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "friendlyQueryNames"))


class FlowLogsBucket(
    RawBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.s3_buckets.FlowLogsBucket",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        crawler_schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        create_queries: typing.Optional[builtins.bool] = None,
        database: typing.Optional[_Database_5971ae38] = None,
        format: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the FlowLogsBucket class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param bucket_name: 
        :param crawler_schedule: 
        :param create_queries: 
        :param database: 
        :param format: 
        :param friendly_query_names: 
        :param table_name: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogsBucket.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FlowLogsBucketProps(
            bucket_name=bucket_name,
            crawler_schedule=crawler_schedule,
            create_queries=create_queries,
            database=database,
            format=format,
            friendly_query_names=friendly_query_names,
            table_name=table_name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="crawler")
    def crawler(self) -> _Crawler_96455303:
        return typing.cast(_Crawler_96455303, jsii.get(self, "crawler"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> _Database_5971ae38:
        return typing.cast(_Database_5971ae38, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> _FlowLogFormat_b7c2ba34:
        return typing.cast(_FlowLogFormat_b7c2ba34, jsii.get(self, "format"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _FlowLogsTable_4c0c73c1:
        return typing.cast(_FlowLogsTable_4c0c73c1, jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="crawlerSchedule")
    def crawler_schedule(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], jsii.get(self, "crawlerSchedule"))

    @builtins.property
    @jsii.member(jsii_name="createQueries")
    def create_queries(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "createQueries"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "friendlyQueryNames"))


__all__ = [
    "AlbLogsBucket",
    "AlbLogsBucketProps",
    "CloudfrontLogsBucket",
    "CloudfrontLogsBucketProps",
    "CloudtrailBucket",
    "CloudtrailBucketProps",
    "FlowLogsBucket",
    "FlowLogsBucketProps",
    "LoggingAspectOptions",
    "RawBucket",
    "RawBucketProps",
    "S3AccessLogsBucket",
    "S3AccessLogsBucketProps",
    "SesLogsBucket",
    "SesLogsBucketProps",
    "WafLogsBucket",
    "WafLogsBucketProps",
]

publication.publish()
