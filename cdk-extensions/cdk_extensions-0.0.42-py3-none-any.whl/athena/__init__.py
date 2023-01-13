'''
# Vibe-io CDK-Extensions Athena Construct Library

The @cdk-extensions/athena package contains advanced constructs and patterns for
setting up named queries. The constructs presented here are intended
to be replacements for equivalent AWS constructs in the CDK Athena module, but with
additional features included.

[AWS CDK Athena API Reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_athena-readme.html)

To import and use this module within your CDK project:

```python
import * as athena from 'cdk-extensions/athena';
```

## Objective

The Athena module is a component of the logging strategy provided by this project defined by **stacks/AwsLoggingStack**. Athena uses the AWS Glue Data Catalog to store and retrieve table metadata for the Amazon S3 data in your Amazon Web Services account. The table metadata lets the Athena query engine know how to find, read, and process the data that you want to query.

The logging strategy defined in this project accounts for all AWS services that log to S3 including ALB, CloudFront, CloudTrail, Flow Logs, S3 access logs, SES, and WAF. For each service a Glue crawler preforms an ETL process to analyze and categorize data in Amazon S3 and store the associated metadata in AWS Glue Data Catalog.

## Usage

The Athena module creates `CfnNamedQuery` resources when the `createQueries` property is set to `true` in the `glue-tables` module. Several default named queires are defined that aid in improving the security posture of your AWS Account. This package introduces several named queries for the following AWS services:

Examples for each of the services below can be found in **src/glue-tables**

Example of an Athena query to retrive the 100 most active IP addresses by request count:

```python
if (this.createQueries) {
    this.topIpsNamedQuery = new NamedQuery(this, 'top-ips-named-query', {
    database: this.database,
    description: 'Gets the 100 most actvie IP addresses by request count.',
    name: this.friendlyQueryNames ? 'alb-top-ips' : undefined,
    queryString: [
        'SELECT client_ip,',
        '    COUNT(*) AS requests,',
        '    COUNT_IF(elb_status_code BETWEEN 400 AND 499) AS errors_4xx,',
        '    COUNT_IF(elb_status_code BETWEEN 500 AND 599) AS errors_5xx,',
        '    SUM(sent_bytes) AS sent,',
        '    SUM(received_bytes) AS received,',
        '    SUM(sent_bytes + received_bytes) AS total,',
        '    ARBITRARY(user_agent) as user_agent',
        `FROM ${this.tableName}`,
        "WHERE day >= DATE_FORMAT(NOW() - PARSE_DURATION('1d'), '%Y/%m/%d')",
        "    AND FROM_ISO8601_TIMESTAMP(time) >= NOW() - PARSE_DURATION('1d')",
        'GROUP BY client_ip',
        'ORDER by total DESC LIMIT 100;',
    ].join('\n'),
    });
```

### ALB

See **src/glue-tables/alb-logs-table.ts**

Gets the 100 most actvie IP addresses by request count.

Gets the 100 most recent ELB 5XX responses.

### CloudFront

See **src/glue-tables/cloudfront-logs-table.ts**

Gets statistics for CloudFront distributions for the last day.

Gets the 100 most recent requests that resulted in an error from CloudFront.

Gets the 100 most active IP addresses by request count.

Gets the 100 most requested CloudFront objects.

### CloudTrail

See **src/glue-tables/cloudtrail-logs-table.ts**

Gets the 100 most recent unauthorized AWS API calls.

Gets the 100 most recent AWS user logins.

### Flow Logs

See **src/glue-tables/flow-logs-table.ts**

Gets the 100 most recent rejected packets that stayed within the private network ranges.

### S3 Access Logs

See **src/glue-tables/s3-access-logs-table.ts**

Gets the 100 most recent failed S3 access requests.

### SES Logs

See **src/glue-tables/ses-logs-table.ts**

Gets the 100 most recent bounces from the last day.

Gets the 100 most recent complaints from the last day.

### WAF Logs

See **src/glue-tables/waf-logs-table.ts**
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
import aws_cdk.aws_athena
import constructs
from ..glue import Database as _Database_5971ae38


class NamedQuery(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.athena.NamedQuery",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        database: _Database_5971ae38,
        query_string: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the NamedQuery class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param database: The Glue database to which the query belongs.
        :param query_string: The SQL statements that make up the query.
        :param description: A human friendly description explaining the functionality of the query.
        :param name: The name of the query.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NamedQuery.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NamedQueryProps(
            database=database,
            query_string=query_string,
            description=description,
            name=name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> _Database_5971ae38:
        '''The Glue database to which the query belongs.

        :see: `NamedQuery Database <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-database>`_
        :group: Inputs
        '''
        return typing.cast(_Database_5971ae38, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="namedQueryId")
    def named_query_id(self) -> builtins.str:
        '''The unique ID of the query.'''
        return typing.cast(builtins.str, jsii.get(self, "namedQueryId"))

    @builtins.property
    @jsii.member(jsii_name="namedQueryName")
    def named_query_name(self) -> builtins.str:
        '''The name of the query.'''
        return typing.cast(builtins.str, jsii.get(self, "namedQueryName"))

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> builtins.str:
        '''The SQL statements that make up the query.

        :see: `Athena SQL reference <https://docs.aws.amazon.com/athena/latest/ug/ddl-sql-reference.html>`_
        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "queryString"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_athena.CfnNamedQuery:
        '''The underlying NamedQuery CloudFormation resource.

        :see: `AWS::Athena::NamedQuery <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html>`_
        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_athena.CfnNamedQuery, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A human friendly description explaining the functionality of the query.

        :see: `NamedQuery Description <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-description>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the query.

        :see: `NamedQuery Name <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-name>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdk-extensions.athena.NamedQueryProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "database": "database",
        "query_string": "queryString",
        "description": "description",
        "name": "name",
    },
)
class NamedQueryProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        database: _Database_5971ae38,
        query_string: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for Database.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param database: The Glue database to which the query belongs.
        :param query_string: The SQL statements that make up the query.
        :param description: A human friendly description explaining the functionality of the query.
        :param name: The name of the query.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NamedQueryProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {
            "database": database,
            "query_string": query_string,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

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
    def database(self) -> _Database_5971ae38:
        '''The Glue database to which the query belongs.

        :see: `NamedQuery Database <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-database>`_
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(_Database_5971ae38, result)

    @builtins.property
    def query_string(self) -> builtins.str:
        '''The SQL statements that make up the query.

        :see: `Athena SQL reference <https://docs.aws.amazon.com/athena/latest/ug/ddl-sql-reference.html>`_
        '''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human friendly description explaining the functionality of the query.

        :see: `NamedQuery Description <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-description>`_
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the query.

        :see: `NamedQuery Name <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-name>`_
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NamedQueryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NamedQuery",
    "NamedQueryProps",
]

publication.publish()
