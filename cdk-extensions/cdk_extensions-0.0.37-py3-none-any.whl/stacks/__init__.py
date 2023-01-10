'''
# Vibe-io CDK-Extensions Stacks Library

These are full-stack solutions, offering rapid deployment of commonly used enterprise
scale patterns with little to no configuration needed.

All Stacks utilize patterns and constructs from the **cdk-extensions** library.

* [About](#AboutTheCDK-ExtensionsLibraries)
* [Stacks](#Stacks)
* [AwsLoggingStack](#AwsLoggingStack)

# Stacks

## AwsLoggingStack

* [Summary](#Summary)
* [Usage](#Usage)
* [The Athena Queries](#The-Athena-Queries)
* [Application Load Balancer](#Application-Load-Balancer)
* [CloudFront](#CloudFront-Distribution)
* [CloudTrail](#CloudTrail)
* [VPC FlowLogs](#VPC-Flowlogs)
* [S3 Access Logs](#S3-Access-Logs)
* [SES](#SES)
* [WAF](#WAF)
* [More Info About The Resources](#More-Info-About-The-Resources)
* [Examples](#Examples)

### Summary

Having a good logging strategy for your AWS Services is a recommended best
practice in every case. It increases operational visibility and strengthens an
enterprise's security posture in a measurable manner.

**It is *recommended*, but it is not always easy to set up, and it is rarely done
for you.**

A good logging strategy for AWS services should utilize the most cost effective,
secure, and reliable solutions available, and include data analysis that can yield
actionable intelligence.

* This will mean storing logs in S3, typically with secure encryption and versioning
  enabled, as well as Cfn Retention set.
* Creating a secure Glue Database for storage and analysis of log data
* Writing custom Glue jobs that can extract and transform logs from S3, and store
  them in the Glue database
* Writing Athena queries tuned for that particular service's log data, that can
  produce good information, and saving them as named queries

The **AwsLoggingStack** sets that up for seven of the AWS services where it
is most frequently needed, handling everything from bucket to query for:

* Application Load Balancer
* CloudFront
* CloudTrail
* VPC FlowLogs
* S3(Access Logs)
* SES
* WAF

S3 Access logging is enabled for all the logging buckets, with logs delivered to the
`S3AccessLogsBucket`.

### Usage

All S3 buckets, Glue resources, and Athena queries are created using **cdk_extensions**
modules. As such, this stack can be initialized with no parameters to rapidly
deploy an industry standard logging strategy into an AWS account, including recommended
named Athena Queries for each service.

#### Install

To import and use this module within your CDK project:

**TypeScript**

```TypeScript
import { AwsLoggingStack } from 'cdk-extensions/stacks';
```

```TypeScript
new AwsLoggingStack(this, 'AwsLoggingStack')
```

**Python**

```Python
from cdk_extensions.stacks import (
AwsLoggingStack
)
```

```Python
aws_logging_stack = AwsLoggingStack(self, 'AwsLoggingStack')
```

#### Enable Logging

**AwsLoggingStack** manages buckets, glue tables, and permissions. All that is left is to
start delivering the logs.

Remember that logging configuration for most **aws-cdk-lib** constructs will require
an L2 construct(i.e. `iBucket`), but the resources created by the AwsLoggingStack
are L1 constructs(i.e. `CfnBucket`). In order to configure **cdk-extensions** logging
buckets, they must be first wrapped in an L2 construct.

```Typescript
logging_stack = new AwsLoggingStack(this, 'LoggingStack')

const l2_cloudtrail_bucket = s3.Bucket.fromCfnBucket(
  logging_stack.cloudtraillogsBucket.resource
);

const trail = new cloudtrail.Trail(this, 'myCloudTrail', {
  bucket: l2_cloudtrail_bucket
});
```

Follow the docs for each service or resource to enable logging to the respective
`AwsLoggingStack` S3 buckets:

* [Enable Logging on an ALB](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationLoadBalancer.html#logwbraccesswbrlogsbucket-prefix)
* [Enable Logging on a CloudFront Distribution](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_cloudfront.Distribution.html#logbucket)
* [Create A Trail on CloudTrail](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_cloudtrail.Trail.html)
* [Publish VPC Flow Logs to S3](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.FlowLogDestination.html#static-towbrs3bucket-keyprefix-options)
* [Enable Server Access logging for S3 Access Logs](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.CfnBucket.LoggingConfigurationProperty.html)
* [Stream SES Event logs](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ses.CfnConfigurationSetEventDestination.EventDestinationProperty.html)
* As described in the documentation linked above, SES event logs first need to
  publish to an intermediate service, such as [Kinesis Firehose](https://docs.aws.amazon.com/cdk/api/v1/docs/aws-kinesisfirehose-readme.html#s3), and then be streamed to the S3 bucket(opinionated Firehose constructs are also
  available in [cdk-extensions/kinesis-firehose](../kinesis-firehose))

  * [Enable WAF logging to S3](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_wafv2.CfnLoggingConfiguration.html)

  ### The Athena Queries

  Once beyond the nuts and bolts of setting up logging buckets and glue jobs to get
  important data into a secure format that can be queried, your data provides its best
  value through well written Athena queries that draw out important metrics and actionable
  intelligence. The **AwsLoggingStack** creates a few immediately useful [`CfnNamedQueries`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_athena.CfnNamedQuery.html) for
  each service to get you started.

  #### Application Load Balancer

  Two Athena queries provide valuable insight into traffic to your ALB:

  * **alb-top-ips**: Gets the 100 most active IP addresses by request count.
  * **alb-5xx-errors**: Gets the 100 most recent ELB 5XX responses

  #### CloudFront Distribution

  Four Athena queries provide valuable insight into traffic across your CDNs.

  * **cloudfront-distribution-statistics**: Gets statistics for CloudFront distributions
    for the last day.
  * **cloudfront-request-errors**: Gets the 100 most recent requests that resulted
    in an error from CloudFront.
  * **cloudfront-top-ips**: Gets the 100 most active IP addresses by request count.
  * **cloudfront-top-objects**: Gets the 100 most requested CloudFront objects.

  #### CloudTrail

  Two Athena queries provide valuable insight into user activity on your AWS account.

  * **cloudtrail-unauthorized-errors**: Gets the 100 most recent unauthorized AWS
    API calls.
  * **cloudtrail-user-logins**: Gets the 100 most recent AWS user logins.

  #### VPC FlowLogs

  An Athena query is created to expose info about rejected internal traffic

  * **flow-logs-internal-rejected**: Gets the 100 most recent rejected packets that
    stayed within the private network ranges.

  #### S3 Access Logs

  An Athena query is created that exposes failed attempts to access your S3 buckets

  * **s3-request-errors**: Gets the 100 most recent failed S3 access requests.

  #### SES

  Protect your domain, and your enterprise's, sending reputation by tracking **bounces**
  and **complaints**

  * **ses-bounces**: Gets the 100 most recent bounces from the last day.
  * **ses-complaints**: Gets the 100 most recent complaints from the last day.

  #### WAF

  Strategy is implemented for storage of WAF logs in S3 with ETL jobs loading to the
  Glue table, but no default Athena queries have been added yet.

  ### More Info About The Resources

  This solution utilizes the **AwsLoggingStack** patterns from the **cdk-extensions/glue-tables** and **cdk-extensions/s3-buckets** libraries, which in turn utilize constructs from
  **cdk-extensions** **Glue** and **Athena** libraries. Detailed info about each is
  covered their respective documentation.

  ### Examples

  #### TypeScript

  *bin/demo.ts*

  ```python
  #!/usr/bin/env node
  import * as cdk from 'aws-cdk-lib';
  import { DemoStack } from '../lib/demo-stack';
  import { AwsLoggingStack } from 'cdk-extensions/stacks';

  const app = new cdk.App();

  // For some cases, like ALB and Flow Logs, we can not have an environment agnostic
  // stack
  const env = {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION
  }

  const aws_logging_stack = new AwsLoggingStack(app, 'AwsLoggingStack', {
    env: env
  });

  new DemoStack(app, 'DemoStack', {
    env: env,
    aws_logging_stack: aws_logging_stack
  });
  ```

  */lib/demo-stack*

  ```TypeScript
  import {
    App,
    Stack,
    StackProps,
    aws_s3 as s3,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ec2 as ec2,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_cloudtrail as cloudtrail,
    aws_iam as iam,
    aws_ses as ses,
    aws_wafv2 as wafv2
  } from 'aws-cdk-lib';
  import { Construct } from 'constructs';
  import { AwsLoggingStack } from 'cdk-extensions/stacks';
  import * as firehose from '@aws-cdk/aws-kinesisfirehose-alpha';
  import { S3Bucket } from '@aws-cdk/aws-kinesisfirehose-destinations-alpha';

  export interface DemoProps extends StackProps {
    readonly aws_logging_stack: AwsLoggingStack;
  }

  export class DemoStack extends Stack {
    // input properties
    public readonly aws_logging_stack: AwsLoggingStack;

    constructor(scope: Construct, id: string, props: DemoProps) {
      super(scope, id, props);

      /**************
      VPC FLOW LOGS
      ***************/
      // Wrap L1 logging bucket in L2 Construct
      const flow_logs_bucket = s3.Bucket.fromCfnBucket(
        props.aws_logging_stack.flowLogsBucket.resource
      );
      // Create a VPC
      const vpc = new ec2.Vpc(this, 'VPC');
      // Enable flow log output to the FlowLogs bucket for the new VPC
      new ec2.FlowLog(this, 'FlowLog', {
        resourceType: ec2.FlowLogResourceType.fromVpc(vpc),
        destination: ec2.FlowLogDestination.toS3(
          flow_logs_bucket
        )
      });


      /***************
      S3 ACCESS LOGS
      ****************/
      const s3_access_logs_bucket = s3.Bucket.fromCfnBucket(
        props.aws_logging_stack.s3AccessLogsBucket.resource
      );
      // Create a simple S3 bucket, with access logging sent to
      // the s3AccessLogsBucket
      const s3Bucket = new s3.Bucket(this, 'WebsiteBucket', {
        serverAccessLogsBucket: s3_access_logs_bucket
      });


      /****************
      CLOUDFRONT LOGS
      *****************/
      // Wrap L1 logging bucket in L2 Construct
      const cloudfront_logs_bucket = s3.Bucket.fromCfnBucket(
        props.aws_logging_stack.cloudfrontLogsBucket.resource
      );
      // Create a CDN in front of the demo bucket, with logBucket configured
      // to the cloudfrontLogsBucket
      const cdn = new cloudfront.Distribution(this, 'Distro', {
        defaultBehavior: {
          origin: new origins.S3Origin(s3Bucket)
        },
        logBucket: cloudfront_logs_bucket
      });


      /****************
      ALB ACCESS LOGS
      *****************/
      //  Wrap L1 bucket in L2 construct
      // Create a simple Load Balancer
      const lb = new elbv2.ApplicationLoadBalancer(this, 'LB', {
        vpc
      });

      // Send logs to the AlbLogsBucket
      lb.logAccessLogs(
        s3.Bucket.fromCfnBucket(props.aws_logging_stack.albLogsBucket.resource )
      );


      /***********
      CLOUDTRAIL
      ************/
      // //  Wrap L1 logging bucket in L2 Construct
      const cloudtrail_logs_bucket = s3.Bucket.fromCfnBucket(
        props.aws_logging_stack.cloudtrailLogsBucket.resource
      );
      // // Create a Cloudtrail trail that sends logs to the CloudtrailLogsBucket
      const trail = new cloudtrail.Trail(this, 'myCloudTrail', {
        bucket: cloudtrail_logs_bucket
      });


      /*********
      SES LOGS
      **********/
      // Wrap L1 logging bucket in L2 Construct
      const ses_logs_bucket =  s3.Bucket.fromCfnBucket(
        props.aws_logging_stack.sesLogsBucket.resource
      );

      // Creates IAM roles for firehose to assume
      const destinationRole = new iam.Role(this, 'Destination Role', {
        assumedBy: new iam.ServicePrincipal('firehose.amazonaws.com'),
      });
      const deliveryStreamRole = new iam.Role(this, 'Delivery Stream Role', {
        assumedBy: new iam.ServicePrincipal('firehose.amazonaws.com'),
      });

      // Specify the roles created above when defining the destination and delivery stream.
      // Connects Kinesis Firehose to the SES Logs Bucket
      const destination = new S3Bucket(ses_logs_bucket, {role: destinationRole});

      // Create the Kinesis DeliveryStream for the SES log destination
      const delivery_stream = new firehose.DeliveryStream(this, 'KinesisStream', {
        destinations: [destination],
        role: deliveryStreamRole
      });

      // Creates an SES ConfigurationSet with reputation metrics enabled
      const config_set = new ses.ConfigurationSet(this, 'ConfigurationSet', {
        reputationMetrics: true
      });

      // Set up permissions for SES to publish events to Kinesis Firehose
      // Creates service principal we can use to restrict the IAM role to the ConfigurationSet
      const service_principal = new iam.PrincipalWithConditions(new iam.ServicePrincipal('ses.amazonaws.com'), {
        "StringEquals": {
          "AWS:SourceAccount": [process.env.CDK_DEFAULT_ACCOUNT],
          "AWS:SourceArn": [
              `arn:aws:ses:${process.env.CDK_DEFAULT_REGION}:${process.env.CDK_DEFAULT_ACCOUNT}:configuration-set/${config_set.configurationSetName}`
            ]
          }
        }
      );
      // Create the IAM Role
      const sesRole = new iam.Role(this, 'SES Role', {
        assumedBy: new iam.ServicePrincipal('ses.amazonaws.com'),
        // It's important to add the firehose permissions as inline
        // policies. If policies are added after role creation, CDK
        // will not know to wait, and may fail to create the ConfigurationSet
        // due to insufficient permissions
        inlinePolicies: {
          'root': new iam.PolicyDocument({
            statements: [
              new iam.PolicyStatement({
                effect: iam.Effect.ALLOW,
                actions: [
                  'firehose:PutRecord',
                  'firehose:PutRecordBatch'
                ],
                resources: [
                  delivery_stream.deliveryStreamArn
                ]
              })
            ]
          })
        }
      });

      // Creates a Configuraton Set Event Destination that will send all SES events
      // to the Kinesis Firehose Stream.
      const cfnConfigurationSetEventDestination = new ses.CfnConfigurationSetEventDestination(this, 'MyCfnConfigurationSetEventDestination', {
        configurationSetName: config_set.configurationSetName,
        eventDestination: {
          matchingEventTypes: [
            'send',
            'reject',
            'bounce',
            'complaint',
            'delivery',
            'open',
            'click',
            'renderingFailure'
          ],
          enabled: true,
          kinesisFirehoseDestination: {
            deliveryStreamArn: delivery_stream.deliveryStreamArn,
            iamRoleArn: sesRole.roleArn
          }
        }
      });
      // TODO: Manually configure any verified SES sending domains, or emails, for which
      // event publishing is desired to use the above configuration set


      /*****
       WAF
      ******/
      // Create a simple WAF with default settings and no rules
      const cfnWebACL = new wafv2.CfnWebACL(this, 'MyCfnWebACL', {
        defaultAction: {
          allow: {}
        },
        scope: 'REGIONAL',
        visibilityConfig: {
          cloudWatchMetricsEnabled: true,
          metricName:'MetricForWebACLCDK',
          sampledRequestsEnabled: true,
        },
      });
      // Create a logging configuration for the WAF logging bucket
      const cfnLoggingConfiguration = new wafv2.CfnLoggingConfiguration(this, 'MyCfnLoggingConfiguration', {
        logDestinationConfigs: [props.aws_logging_stack.wafLogsBucket.bucketArn],
        resourceArn: cfnWebACL.attrArn
      });
    }
  ```

}
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
import constructs
from ..ec2 import FlowLogFormat as _FlowLogFormat_b7c2ba34
from ..glue import Database as _Database_5971ae38
from ..s3_buckets import (
    AlbLogsBucket as _AlbLogsBucket_93df9b00,
    CloudfrontLogsBucket as _CloudfrontLogsBucket_34407447,
    CloudtrailBucket as _CloudtrailBucket_aa5784e2,
    FlowLogsBucket as _FlowLogsBucket_2af17beb,
    S3AccessLogsBucket as _S3AccessLogsBucket_c740f099,
    SesLogsBucket as _SesLogsBucket_bc9a3d3a,
    WafLogsBucket as _WafLogsBucket_0ad870de,
)


class AwsLoggingStack(
    aws_cdk.Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.stacks.AwsLoggingStack",
):
    '''Creates a Stack that deploys a logging strategy for several AWS services.

    Stack creates a Glue Database using cdk-extensions Database, deploys
    cdk-extensions/s3-buckets patterns for each service, and utilizes methods exposed
    by cdk-extensions/s3-buckets S3AccessLogsBucket to enable logging for each created
    bucket.

    :see: {@link aws-s3-buckets!WafLogsBucket | cdk-extensions/s3-buckets WafLogsBucket}
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        alb_logs_bucket: typing.Optional[_AlbLogsBucket_93df9b00] = None,
        cloudfront_logs_bucket: typing.Optional[_CloudfrontLogsBucket_34407447] = None,
        cloudtrail_logs_bucket: typing.Optional[_CloudtrailBucket_aa5784e2] = None,
        database_name: typing.Optional[builtins.str] = None,
        flow_logs_bucket: typing.Optional[_FlowLogsBucket_2af17beb] = None,
        flow_logs_format: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        ses_logs_bucket: typing.Optional[_SesLogsBucket_bc9a3d3a] = None,
        standardize_names: typing.Optional[builtins.bool] = None,
        waf_logs_bucket: typing.Optional[_WafLogsBucket_0ad870de] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[aws_cdk.Environment, typing.Dict[str, typing.Any]]] = None,
        permissions_boundary: typing.Optional[aws_cdk.PermissionsBoundary] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Creates a new instance of the AwsLoggingStack class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param alb_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!AlbLogsBucket} object.
        :param cloudfront_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!CloudfrontLogsBucket} object.
        :param cloudtrail_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!CloudtrailBucket} object.
        :param database_name: Name used for the Glue Database that will be created.
        :param flow_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!FlowLogsBucket} object.
        :param flow_logs_format: A cdk-extentions/ec2 {@link aws-ec2!FlowLogFormat } object defining the desired formatting for Flow Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param ses_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!SesLogsBucket} object.
        :param standardize_names: Boolean for using "standardized" naming (i.e. "aws-${service}-logs-${account} -${region}") for the created S3 Buckets.
        :param waf_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!WafLogsBucket} object.
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AwsLoggingStack.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AwsLoggingStackProps(
            alb_logs_bucket=alb_logs_bucket,
            cloudfront_logs_bucket=cloudfront_logs_bucket,
            cloudtrail_logs_bucket=cloudtrail_logs_bucket,
            database_name=database_name,
            flow_logs_bucket=flow_logs_bucket,
            flow_logs_format=flow_logs_format,
            friendly_query_names=friendly_query_names,
            ses_logs_bucket=ses_logs_bucket,
            standardize_names=standardize_names,
            waf_logs_bucket=waf_logs_bucket,
            analytics_reporting=analytics_reporting,
            cross_region_references=cross_region_references,
            description=description,
            env=env,
            permissions_boundary=permissions_boundary,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="albLogsBucket")
    def alb_logs_bucket(self) -> _AlbLogsBucket_93df9b00:
        return typing.cast(_AlbLogsBucket_93df9b00, jsii.get(self, "albLogsBucket"))

    @builtins.property
    @jsii.member(jsii_name="cloudfrontLogsBucket")
    def cloudfront_logs_bucket(self) -> _CloudfrontLogsBucket_34407447:
        return typing.cast(_CloudfrontLogsBucket_34407447, jsii.get(self, "cloudfrontLogsBucket"))

    @builtins.property
    @jsii.member(jsii_name="cloudtrailLogsBucket")
    def cloudtrail_logs_bucket(self) -> _CloudtrailBucket_aa5784e2:
        return typing.cast(_CloudtrailBucket_aa5784e2, jsii.get(self, "cloudtrailLogsBucket"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> _Database_5971ae38:
        return typing.cast(_Database_5971ae38, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        '''Name for the AWS Logs Glue Database.'''
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="flowLogsBucket")
    def flow_logs_bucket(self) -> _FlowLogsBucket_2af17beb:
        return typing.cast(_FlowLogsBucket_2af17beb, jsii.get(self, "flowLogsBucket"))

    @builtins.property
    @jsii.member(jsii_name="flowLogsFormat")
    def flow_logs_format(self) -> _FlowLogFormat_b7c2ba34:
        '''A cdk-extentions/ec2 {@link aws-ec2!FlowLogFormat } object defining the desired formatting for Flow Logs.'''
        return typing.cast(_FlowLogFormat_b7c2ba34, jsii.get(self, "flowLogsFormat"))

    @builtins.property
    @jsii.member(jsii_name="s3AccessLogsBucket")
    def s3_access_logs_bucket(self) -> _S3AccessLogsBucket_c740f099:
        return typing.cast(_S3AccessLogsBucket_c740f099, jsii.get(self, "s3AccessLogsBucket"))

    @builtins.property
    @jsii.member(jsii_name="sesLogsBucket")
    def ses_logs_bucket(self) -> _SesLogsBucket_bc9a3d3a:
        return typing.cast(_SesLogsBucket_bc9a3d3a, jsii.get(self, "sesLogsBucket"))

    @builtins.property
    @jsii.member(jsii_name="standardizeNames")
    def standardize_names(self) -> builtins.bool:
        '''Boolean for using standardized names (i.e. "aws-${service}-logs-${account} -${region}") for the created S3 Buckets.'''
        return typing.cast(builtins.bool, jsii.get(self, "standardizeNames"))

    @builtins.property
    @jsii.member(jsii_name="wafLogsBucket")
    def waf_logs_bucket(self) -> _WafLogsBucket_0ad870de:
        return typing.cast(_WafLogsBucket_0ad870de, jsii.get(self, "wafLogsBucket"))

    @builtins.property
    @jsii.member(jsii_name="friendlyQueryNames")
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "friendlyQueryNames"))


@jsii.data_type(
    jsii_type="cdk-extensions.stacks.AwsLoggingStackProps",
    jsii_struct_bases=[aws_cdk.StackProps],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "cross_region_references": "crossRegionReferences",
        "description": "description",
        "env": "env",
        "permissions_boundary": "permissionsBoundary",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "alb_logs_bucket": "albLogsBucket",
        "cloudfront_logs_bucket": "cloudfrontLogsBucket",
        "cloudtrail_logs_bucket": "cloudtrailLogsBucket",
        "database_name": "databaseName",
        "flow_logs_bucket": "flowLogsBucket",
        "flow_logs_format": "flowLogsFormat",
        "friendly_query_names": "friendlyQueryNames",
        "ses_logs_bucket": "sesLogsBucket",
        "standardize_names": "standardizeNames",
        "waf_logs_bucket": "wafLogsBucket",
    },
)
class AwsLoggingStackProps(aws_cdk.StackProps):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[aws_cdk.Environment, typing.Dict[str, typing.Any]]] = None,
        permissions_boundary: typing.Optional[aws_cdk.PermissionsBoundary] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        alb_logs_bucket: typing.Optional[_AlbLogsBucket_93df9b00] = None,
        cloudfront_logs_bucket: typing.Optional[_CloudfrontLogsBucket_34407447] = None,
        cloudtrail_logs_bucket: typing.Optional[_CloudtrailBucket_aa5784e2] = None,
        database_name: typing.Optional[builtins.str] = None,
        flow_logs_bucket: typing.Optional[_FlowLogsBucket_2af17beb] = None,
        flow_logs_format: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
        friendly_query_names: typing.Optional[builtins.bool] = None,
        ses_logs_bucket: typing.Optional[_SesLogsBucket_bc9a3d3a] = None,
        standardize_names: typing.Optional[builtins.bool] = None,
        waf_logs_bucket: typing.Optional[_WafLogsBucket_0ad870de] = None,
    ) -> None:
        '''Configuration for AwsLoggingStack.

        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param alb_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!AlbLogsBucket} object.
        :param cloudfront_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!CloudfrontLogsBucket} object.
        :param cloudtrail_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!CloudtrailBucket} object.
        :param database_name: Name used for the Glue Database that will be created.
        :param flow_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!FlowLogsBucket} object.
        :param flow_logs_format: A cdk-extentions/ec2 {@link aws-ec2!FlowLogFormat } object defining the desired formatting for Flow Logs.
        :param friendly_query_names: Boolean for adding "friendly names" for the created Athena queries.
        :param ses_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!SesLogsBucket} object.
        :param standardize_names: Boolean for using "standardized" naming (i.e. "aws-${service}-logs-${account} -${region}") for the created S3 Buckets.
        :param waf_logs_bucket: A cdk-extensions/s3-buckets {@link aws-s3-buckets!WafLogsBucket} object.
        '''
        if isinstance(env, dict):
            env = aws_cdk.Environment(**env)
        if __debug__:
            type_hints = typing.get_type_hints(AwsLoggingStackProps.__init__)
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument cross_region_references", value=cross_region_references, expected_type=type_hints["cross_region_references"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
            check_type(argname="argument alb_logs_bucket", value=alb_logs_bucket, expected_type=type_hints["alb_logs_bucket"])
            check_type(argname="argument cloudfront_logs_bucket", value=cloudfront_logs_bucket, expected_type=type_hints["cloudfront_logs_bucket"])
            check_type(argname="argument cloudtrail_logs_bucket", value=cloudtrail_logs_bucket, expected_type=type_hints["cloudtrail_logs_bucket"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument flow_logs_bucket", value=flow_logs_bucket, expected_type=type_hints["flow_logs_bucket"])
            check_type(argname="argument flow_logs_format", value=flow_logs_format, expected_type=type_hints["flow_logs_format"])
            check_type(argname="argument friendly_query_names", value=friendly_query_names, expected_type=type_hints["friendly_query_names"])
            check_type(argname="argument ses_logs_bucket", value=ses_logs_bucket, expected_type=type_hints["ses_logs_bucket"])
            check_type(argname="argument standardize_names", value=standardize_names, expected_type=type_hints["standardize_names"])
            check_type(argname="argument waf_logs_bucket", value=waf_logs_bucket, expected_type=type_hints["waf_logs_bucket"])
        self._values: typing.Dict[str, typing.Any] = {}
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if cross_region_references is not None:
            self._values["cross_region_references"] = cross_region_references
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection
        if alb_logs_bucket is not None:
            self._values["alb_logs_bucket"] = alb_logs_bucket
        if cloudfront_logs_bucket is not None:
            self._values["cloudfront_logs_bucket"] = cloudfront_logs_bucket
        if cloudtrail_logs_bucket is not None:
            self._values["cloudtrail_logs_bucket"] = cloudtrail_logs_bucket
        if database_name is not None:
            self._values["database_name"] = database_name
        if flow_logs_bucket is not None:
            self._values["flow_logs_bucket"] = flow_logs_bucket
        if flow_logs_format is not None:
            self._values["flow_logs_format"] = flow_logs_format
        if friendly_query_names is not None:
            self._values["friendly_query_names"] = friendly_query_names
        if ses_logs_bucket is not None:
            self._values["ses_logs_bucket"] = ses_logs_bucket
        if standardize_names is not None:
            self._values["standardize_names"] = standardize_names
        if waf_logs_bucket is not None:
            self._values["waf_logs_bucket"] = waf_logs_bucket

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_region_references(self) -> typing.Optional[builtins.bool]:
        '''Enable this flag to allow native cross region stack references.

        Enabling this will create a CloudFormation custom resource
        in both the producing stack and consuming stack in order to perform the export/import

        This feature is currently experimental

        :default: false
        '''
        result = self._values.get("cross_region_references")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[aws_cdk.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            // Use a concrete account and region to deploy this stack to:
            // `.account` and `.region` will simply return these values.
            new Stack(app, 'Stack1', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              },
            });
            
            // Use the CLI's current credentials to determine the target environment:
            // `.account` and `.region` will reflect the account+region the CLI
            // is configured to use (based on the user CLI credentials)
            new Stack(app, 'Stack2', {
              env: {
                account: process.env.CDK_DEFAULT_ACCOUNT,
                region: process.env.CDK_DEFAULT_REGION
              },
            });
            
            // Define multiple stacks stage associated with an environment
            const myStage = new Stage(app, 'MyStage', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              }
            });
            
            // both of these stacks will use the stage's account/region:
            // `.account` and `.region` will resolve to the concrete values as above
            new MyStack(myStage, 'Stack1');
            new YourStack(myStage, 'Stack2');
            
            // Define an environment-agnostic stack:
            // `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            // which will only resolve to actual values by CloudFormation during deployment.
            new MyStack(app, 'Stack1');
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[aws_cdk.Environment], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[aws_cdk.PermissionsBoundary]:
        '''Options for applying a permissions boundary to all IAM Roles and Users created within this Stage.

        :default: - no permissions boundary is applied
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[aws_cdk.PermissionsBoundary], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[aws_cdk.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
        is set, ``LegacyStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[aws_cdk.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def alb_logs_bucket(self) -> typing.Optional[_AlbLogsBucket_93df9b00]:
        '''A cdk-extensions/s3-buckets {@link aws-s3-buckets!AlbLogsBucket} object.'''
        result = self._values.get("alb_logs_bucket")
        return typing.cast(typing.Optional[_AlbLogsBucket_93df9b00], result)

    @builtins.property
    def cloudfront_logs_bucket(self) -> typing.Optional[_CloudfrontLogsBucket_34407447]:
        '''A cdk-extensions/s3-buckets {@link aws-s3-buckets!CloudfrontLogsBucket} object.'''
        result = self._values.get("cloudfront_logs_bucket")
        return typing.cast(typing.Optional[_CloudfrontLogsBucket_34407447], result)

    @builtins.property
    def cloudtrail_logs_bucket(self) -> typing.Optional[_CloudtrailBucket_aa5784e2]:
        '''A cdk-extensions/s3-buckets {@link aws-s3-buckets!CloudtrailBucket} object.'''
        result = self._values.get("cloudtrail_logs_bucket")
        return typing.cast(typing.Optional[_CloudtrailBucket_aa5784e2], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''Name used for the Glue Database that will be created.'''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flow_logs_bucket(self) -> typing.Optional[_FlowLogsBucket_2af17beb]:
        '''A cdk-extensions/s3-buckets {@link aws-s3-buckets!FlowLogsBucket} object.'''
        result = self._values.get("flow_logs_bucket")
        return typing.cast(typing.Optional[_FlowLogsBucket_2af17beb], result)

    @builtins.property
    def flow_logs_format(self) -> typing.Optional[_FlowLogFormat_b7c2ba34]:
        '''A cdk-extentions/ec2 {@link aws-ec2!FlowLogFormat } object defining the desired formatting for Flow Logs.'''
        result = self._values.get("flow_logs_format")
        return typing.cast(typing.Optional[_FlowLogFormat_b7c2ba34], result)

    @builtins.property
    def friendly_query_names(self) -> typing.Optional[builtins.bool]:
        '''Boolean for adding "friendly names" for the created Athena queries.'''
        result = self._values.get("friendly_query_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ses_logs_bucket(self) -> typing.Optional[_SesLogsBucket_bc9a3d3a]:
        '''A cdk-extensions/s3-buckets {@link aws-s3-buckets!SesLogsBucket} object.'''
        result = self._values.get("ses_logs_bucket")
        return typing.cast(typing.Optional[_SesLogsBucket_bc9a3d3a], result)

    @builtins.property
    def standardize_names(self) -> typing.Optional[builtins.bool]:
        '''Boolean for using "standardized" naming (i.e. "aws-${service}-logs-${account} -${region}") for the created S3 Buckets.'''
        result = self._values.get("standardize_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def waf_logs_bucket(self) -> typing.Optional[_WafLogsBucket_0ad870de]:
        '''A cdk-extensions/s3-buckets {@link aws-s3-buckets!WafLogsBucket} object.'''
        result = self._values.get("waf_logs_bucket")
        return typing.cast(typing.Optional[_WafLogsBucket_0ad870de], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsLoggingStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsLoggingStack",
    "AwsLoggingStackProps",
]

publication.publish()
