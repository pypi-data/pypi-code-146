'''
[![GitHub](https://img.shields.io/github/license/pepperize/cdk-route53-health-check?style=flat-square)](https://github.com/pepperize/cdk-route53-health-check/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@pepperize/cdk-route53-health-check?style=flat-square)](https://www.npmjs.com/package/@pepperize/cdk-route53-health-check)
[![PyPI](https://img.shields.io/pypi/v/pepperize.cdk-route53-health-check?style=flat-square)](https://pypi.org/project/pepperize.cdk-route53-health-check/)
[![Nuget](https://img.shields.io/nuget/v/Pepperize.CDK.Route53HealthCheck?style=flat-square)](https://www.nuget.org/packages/Pepperize.CDK.Route53HealthCheck/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.pepperize/cdk-route53-health-check?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/pepperize/cdk-route53-health-check/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/pepperize/cdk-route53-health-check/release/main?label=release&style=flat-square)](https://github.com/pepperize/cdk-route53-health-check/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/pepperize/cdk-route53-health-check?sort=semver&style=flat-square)](https://github.com/pepperize/cdk-route53-health-check/releases)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod&style=flat-square)](https://gitpod.io/#https://github.com/pepperize/cdk-route53-health-check)

# AWS CDK Route53 HealthCheck

Create Route53 HealthChecks to monitor TCP, HTTP, HTTPS endpoints, to monitor CloudWatch Alarms and to monitor other Route53 HealthChecks.

Currently supported types of Route53 HealthChecks:

* [Health checks that monitor an endpoint](https://github.com/pepperize/cdk-route53-health-check#healthcheck-for-an-endpoint)
* [Health checks that monitor other health checks](https://github.com/pepperize/cdk-route53-health-check#healthcheck-to-monitor-cloudwatch-alarms)
* [Health checks that monitor CloudWatch alarms](https://github.com/pepperize/cdk-route53-health-check#healthcheck-to-monitor-other-healthchecks)
* [Configure DNS failover](https://github.com/pepperize/cdk-route53-health-check#configuring-dns-failover)

Easily create a CloudWatch Alarm based on the Route53 HealthCheck:

```python
const healthCheck = new EndpointHealthCheck(scope, "HealthCheck", {
  domainName: "pepperize.com",
});

const alarm = new cloudwatch.Alarm(scope, "Alarm", {
  metric: healthCheck.metricHealthCheckStatus(),
  comparisonOperator: cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
  threshold: 1,
  evaluationPeriods: 1,
});
```

See more options [API Reference](https://github.com/pepperize/cdk-route53-health-check/blob/main/API.md#@pepperize/cdk-route53-health-check.EndpointHealthCheckProps)

## Install

### TypeScript

```shell
npm install @pepperize/cdk-route53-health-check
```

or

```shell
yarn add @pepperize/cdk-route53-health-check
```

### Python

```shell
pip install pepperize.cdk-route53-health-check
```

### C# / .Net

```
dotnet add package Pepperize.CDK.Route53HealthCheck
```

### Java

```xml
<dependency>
  <groupId>com.pepperize</groupId>
  <artifactId>cdk-route53-health-check</artifactId>
  <version>${cdkRoute53HealthCheck.version}</version>
</dependency>
```

## Usage

```shell
npm install @pepperize/cdk-route53-health-check
```

See [API.md](https://github.com/pepperize/cdk-route53-health-check/blob/main/API.md).

### HealthCheck for an endpoint

**HTTPS health check**

```python
new EndpointHealthCheck(scope, "HealthCheck", {
  domainName: "pepperize.com",
});
```

Generates

```yaml
Resources:
  Type: AWS::Route53::HealthCheck
  Properties:
    HealthCheckConfig:
      FullyQualifiedDomainName: "pepperize.com"
      Port: 443
      Type: "HTTPS"
      EnableSNI: true
```

**Additional configuration options**

```python
new EndpointHealthCheck(scope, "HealthCheck", {
  domainName: "pepperize.com", // The domain name that Route53 performs health checks on. Route53 resolves the IP address and performs the lookup.
  enableSni: true, // Specify that Route53 sends the host name for TLS negotiation.
  failureThreshold: 3, // The number of consecutive health checks that an endpoint must pass or fail for Route53 to change the current status of the endpoint between healthy and unhealthy.
  healthCheckName: "pepperize.com", //	The display name of this Route53 HealthCheck.
  inverted: false, // Whether to invert the status of the Route53 health check status.
  ipAddress: "1.1.1.1", // The ip address that Route53 performs health checks on. Optionally a domain name may be given.
  latencyGraphs: true, // Whether Route53 measures the latency between health checkers in multiple AWS regions and your endpoint, and displays a CloudWatch latency graphs in the Route53 console.
  port: 443, // The port that Route53 performs health checks.
  protocol: Protocol.HTTPS, // The protocol that Route53 uses to communicate with the endpoint.
  regions: [HealthCheckerRegions.EU_WEST_1, HealthCheckerRegions.US_EAST_1, HealthCheckerRegions.US_WEST_1], // The list of regions from which Route53 health checkers check the endpoint.
  requestInterval: 30, // The number of seconds between the time that Route53 gets a response from your endpoint and the time that it sends the next health check request.
  resourcePath: "/health-check", // The path for HTTP or HTTPS health checks.
  searchString: "OK", // The search string for HTTP or HTTPS health checks.
});
```

See for more options [API Reference - EndpointHealthCheckProps](https://github.com/pepperize/cdk-route53-health-check/blob/main/API.md#endpointhealthcheckprops-)

### HealthCheck to monitor other HealthChecks

```python
const healthCheck1 = new EndpointHealthCheck(stack, "HealthCheck1", {
  domainName: "pepperize.com",
});
const healthCheck2 = EndpointHealthCheck.fromHealthCheckId(
  scope,
  "HealthCheck2",
  "9ebee2db-6292-4803-9838-327e6example"
);
new CalculatedHealthCheck(scope, "CalculatedHealthCheck", {
  childHealthChecks: [healthCheck1, healthCheck2],
});
```

See for more options [API Reference - CalculatedHealthCheckProps](https://github.com/pepperize/cdk-route53-health-check/blob/main/API.md#calculatedhealthcheckprops-)

### HealthCheck to monitor CloudWatch Alarms

```python
const alarm = cloudwatch.Alarm.fromAlarmArn(
  scope,
  "Alarm",
  "arn:aws:cloudwatch:us-east-1:123456789012:alarm:any-alarm"
);
new AlarmHealthCheck(scope, "HealthCheck", {
  alarm: alarm,
});
```

See for more options [API Reference - AlarmHealthCheckProps](https://github.com/pepperize/cdk-route53-health-check/blob/main/API.md#alarmhealthcheckprops-)

### Configuring DNS Failover

An example active-passive DNS failover configuration

![DNS failover](https://github.com/pepperize/cdk-route53-health-check/blob/main/diagram.png)

**Primary**

```python
// An alias record set for a CloudFront distribution
const recordSetPrimary = new route53.ARecord(scope, "RecordSetPrimary", {
  recordName: "www.pepperize.com",
  zone: hostedZone,
  target: route53.RecordTarget.fromAlias(new targets.CloudFrontTarget(distribution)),
});
// The health check for the CloudFront distribution
const healthCheckPrimary = new EndpointHealthCheck(scope, "HealthCheckPrimary", {
  domainName: "www.pepperize.com",
});
// Configure the HealthCheckId and Failover on the record set
healthCheckPrimary.failoverPrimary(recordSetPrimary);
```

**Secondary**

```python
// An alias record set for an Application Load Balancer
const recordSetSecondary = new route53.ARecord(scope, "RecordSetSecondary", {
  recordName: "www-1.pepperize.com",
  zone: hostedZone,
  target: route53.RecordTarget.fromAlias(new targets.LoadBalancerTarget(alb)),
});
// The health check for the Application Load Balancer
const healthCheckSecondary = new EndpointHealthCheck(scope, "HealthCheckSecondary", {
  domainName: "www-1.pepperize.com",
});
// Configure the HealthCheckId and Failover on the record set
healthCheckSecondary.failoverSecondary(recordSetSecondary, true);
```

See for more options [API Reference - IHealthCheck](https://github.com/pepperize/cdk-route53-health-check/blob/main/API.md#ihealthcheck-)

[How health checks work in complex Amazon Route 53 configurations](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-complex-configs.html)
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@pepperize/cdk-route53-health-check.AlarmHealthCheckProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm": "alarm",
        "health_check_name": "healthCheckName",
        "insufficient_data_health_status": "insufficientDataHealthStatus",
        "inverted": "inverted",
    },
)
class AlarmHealthCheckProps:
    def __init__(
        self,
        *,
        alarm: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
        health_check_name: typing.Optional[builtins.str] = None,
        insufficient_data_health_status: typing.Optional["InsufficientDataHealthStatus"] = None,
        inverted: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param alarm: The alarm that Route53 monitors.
        :param health_check_name: The display name of this Route53 HealthCheck.
        :param insufficient_data_health_status: The status to assign to the HealthCheck when CloudWatch has insufficient data about the metric.
        :param inverted: Whether to invert the status of the Route53 health check status.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639153b296f45bd8c248c52158a6493c4845bdb55b7de3975f909413a7b84ae2)
            check_type(argname="argument alarm", value=alarm, expected_type=type_hints["alarm"])
            check_type(argname="argument health_check_name", value=health_check_name, expected_type=type_hints["health_check_name"])
            check_type(argname="argument insufficient_data_health_status", value=insufficient_data_health_status, expected_type=type_hints["insufficient_data_health_status"])
            check_type(argname="argument inverted", value=inverted, expected_type=type_hints["inverted"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm": alarm,
        }
        if health_check_name is not None:
            self._values["health_check_name"] = health_check_name
        if insufficient_data_health_status is not None:
            self._values["insufficient_data_health_status"] = insufficient_data_health_status
        if inverted is not None:
            self._values["inverted"] = inverted

    @builtins.property
    def alarm(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm:
        '''The alarm that Route53 monitors.'''
        result = self._values.get("alarm")
        assert result is not None, "Required property 'alarm' is missing"
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.IAlarm, result)

    @builtins.property
    def health_check_name(self) -> typing.Optional[builtins.str]:
        '''The display name of this Route53 HealthCheck.'''
        result = self._values.get("health_check_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insufficient_data_health_status(
        self,
    ) -> typing.Optional["InsufficientDataHealthStatus"]:
        '''The status to assign to the HealthCheck when CloudWatch has insufficient data about the metric.'''
        result = self._values.get("insufficient_data_health_status")
        return typing.cast(typing.Optional["InsufficientDataHealthStatus"], result)

    @builtins.property
    def inverted(self) -> typing.Optional[builtins.bool]:
        '''Whether to invert the status of the Route53 health check status.'''
        result = self._values.get("inverted")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmHealthCheckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@pepperize/cdk-route53-health-check.CalculatedHealthCheckProps",
    jsii_struct_bases=[],
    name_mapping={
        "child_health_checks": "childHealthChecks",
        "health_check_name": "healthCheckName",
        "health_threshold": "healthThreshold",
        "inverted": "inverted",
    },
)
class CalculatedHealthCheckProps:
    def __init__(
        self,
        *,
        child_health_checks: typing.Optional[typing.Sequence["IHealthCheck"]] = None,
        health_check_name: typing.Optional[builtins.str] = None,
        health_threshold: typing.Optional[jsii.Number] = None,
        inverted: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param child_health_checks: The list of HealthCheck that monitors other Route53 HealthChecks.
        :param health_check_name: The display name of this Route53 HealthCheck.
        :param health_threshold: The number of child HealthChecks that Amazon Route53 must consider healthy.
        :param inverted: Whether to invert the status of the Route53 health check status.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50716ab3df3dce42fb0a3b896e69290109228794f9a6daa26dea7eb00d9625fd)
            check_type(argname="argument child_health_checks", value=child_health_checks, expected_type=type_hints["child_health_checks"])
            check_type(argname="argument health_check_name", value=health_check_name, expected_type=type_hints["health_check_name"])
            check_type(argname="argument health_threshold", value=health_threshold, expected_type=type_hints["health_threshold"])
            check_type(argname="argument inverted", value=inverted, expected_type=type_hints["inverted"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if child_health_checks is not None:
            self._values["child_health_checks"] = child_health_checks
        if health_check_name is not None:
            self._values["health_check_name"] = health_check_name
        if health_threshold is not None:
            self._values["health_threshold"] = health_threshold
        if inverted is not None:
            self._values["inverted"] = inverted

    @builtins.property
    def child_health_checks(self) -> typing.Optional[typing.List["IHealthCheck"]]:
        '''The list of HealthCheck that monitors other Route53 HealthChecks.'''
        result = self._values.get("child_health_checks")
        return typing.cast(typing.Optional[typing.List["IHealthCheck"]], result)

    @builtins.property
    def health_check_name(self) -> typing.Optional[builtins.str]:
        '''The display name of this Route53 HealthCheck.'''
        result = self._values.get("health_check_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of child HealthChecks that Amazon Route53 must consider healthy.'''
        result = self._values.get("health_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def inverted(self) -> typing.Optional[builtins.bool]:
        '''Whether to invert the status of the Route53 health check status.'''
        result = self._values.get("inverted")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CalculatedHealthCheckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@pepperize/cdk-route53-health-check.EndpointHealthCheckProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "enable_sni": "enableSni",
        "failure_threshold": "failureThreshold",
        "health_check_name": "healthCheckName",
        "inverted": "inverted",
        "ip_address": "ipAddress",
        "latency_graphs": "latencyGraphs",
        "port": "port",
        "protocol": "protocol",
        "regions": "regions",
        "request_interval": "requestInterval",
        "resource_path": "resourcePath",
        "search_string": "searchString",
    },
)
class EndpointHealthCheckProps:
    def __init__(
        self,
        *,
        domain_name: typing.Optional[builtins.str] = None,
        enable_sni: typing.Optional[builtins.bool] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        health_check_name: typing.Optional[builtins.str] = None,
        inverted: typing.Optional[builtins.bool] = None,
        ip_address: typing.Optional[builtins.str] = None,
        latency_graphs: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional["Protocol"] = None,
        regions: typing.Optional[typing.Sequence["HealthCheckerRegions"]] = None,
        request_interval: typing.Optional[jsii.Number] = None,
        resource_path: typing.Optional[builtins.str] = None,
        search_string: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain_name: The domain name that Route53 performs health checks on. Route53 resolves the IP address and performs the lookup. If IP address is given, it's used as the host name. Either DomainName or IpAddress must be specified
        :param enable_sni: Specify that Route53 sends the host name for TLS negotiation. Default: true for HTTPS
        :param failure_threshold: The number of consecutive health checks that an endpoint must pass or fail for Route53 to change the current status of the endpoint between healthy and unhealthy. Provide a number between 1 and 10.
        :param health_check_name: The display name of this Route53 HealthCheck.
        :param inverted: Whether to invert the status of the Route53 health check status.
        :param ip_address: The ip address that Route53 performs health checks on. Optionally a domain name may be given. An IP address must be specified if protocol TCP
        :param latency_graphs: Whether Route53 measures the latency between health checkers in multiple AWS regions and your endpoint, and displays a CloudWatch latency graphs in the Route53 console. Can't be changed after HealthCheck is deployed
        :param port: The port that Route53 performs health checks. The port must be between 1 and 65535. Default: 80 for HTTP; 443 for HTTPS
        :param protocol: The protocol that Route53 uses to communicate with the endpoint. An IP address must be specified if protocol TCP Default: HTTPS
        :param regions: The list of regions from which Route53 health checkers check the endpoint. If omitted Route53 performs checks from all health checker regions.
        :param request_interval: The number of seconds between the time that Route53 gets a response from your endpoint and the time that it sends the next health check request. Each Route53 health checker makes requests at this interval. Provide a number between 10 and 30. If you choose an interval of 10 and there are 15 health checkers, the endpoint will receive approximately 1 request per second. Can't be changed after HealthCheck is deployed
        :param resource_path: The path for HTTP or HTTPS health checks. Provide a string between 1 and 255 length.
        :param search_string: The search string for HTTP or HTTPS health checks. Route53 will search in the response body. Provide a string between 1 and 255 length.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de064cce147a8183cdbdbedceafe764868f4f6e90a0f2301d6c340bdea374acc)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument enable_sni", value=enable_sni, expected_type=type_hints["enable_sni"])
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument health_check_name", value=health_check_name, expected_type=type_hints["health_check_name"])
            check_type(argname="argument inverted", value=inverted, expected_type=type_hints["inverted"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument latency_graphs", value=latency_graphs, expected_type=type_hints["latency_graphs"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument request_interval", value=request_interval, expected_type=type_hints["request_interval"])
            check_type(argname="argument resource_path", value=resource_path, expected_type=type_hints["resource_path"])
            check_type(argname="argument search_string", value=search_string, expected_type=type_hints["search_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if enable_sni is not None:
            self._values["enable_sni"] = enable_sni
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if health_check_name is not None:
            self._values["health_check_name"] = health_check_name
        if inverted is not None:
            self._values["inverted"] = inverted
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if latency_graphs is not None:
            self._values["latency_graphs"] = latency_graphs
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if regions is not None:
            self._values["regions"] = regions
        if request_interval is not None:
            self._values["request_interval"] = request_interval
        if resource_path is not None:
            self._values["resource_path"] = resource_path
        if search_string is not None:
            self._values["search_string"] = search_string

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name that Route53 performs health checks on. Route53 resolves the IP address and performs the lookup.

        If IP address is given, it's used as the host name.

        Either DomainName or IpAddress must be specified
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_sni(self) -> typing.Optional[builtins.bool]:
        '''Specify that Route53 sends the host name for TLS negotiation.

        :default: true for HTTPS
        '''
        result = self._values.get("enable_sni")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive health checks that an endpoint must pass or fail for Route53 to change the current status of the endpoint between healthy and unhealthy.

        Provide a number between 1 and 10.
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_name(self) -> typing.Optional[builtins.str]:
        '''The display name of this Route53 HealthCheck.'''
        result = self._values.get("health_check_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inverted(self) -> typing.Optional[builtins.bool]:
        '''Whether to invert the status of the Route53 health check status.'''
        result = self._values.get("inverted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''The ip address that Route53 performs health checks on. Optionally a domain name may be given.

        An IP address must be specified if protocol TCP
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def latency_graphs(self) -> typing.Optional[builtins.bool]:
        '''Whether Route53 measures the latency between health checkers in multiple AWS regions and your endpoint, and displays a CloudWatch latency graphs in the Route53 console.

        Can't be changed after HealthCheck is deployed
        '''
        result = self._values.get("latency_graphs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port that Route53 performs health checks.

        The port must be between 1 and 65535.

        :default: 80 for HTTP; 443 for HTTPS
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        '''The protocol that Route53 uses to communicate with the endpoint.

        An IP address must be specified if protocol TCP

        :default: HTTPS
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional["Protocol"], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List["HealthCheckerRegions"]]:
        '''The list of regions from which Route53 health checkers check the endpoint.

        If omitted Route53 performs checks from all health checker regions.
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List["HealthCheckerRegions"]], result)

    @builtins.property
    def request_interval(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds between the time that Route53 gets a response from your endpoint and the time that it sends the next health check request.

        Each Route53 health checker makes requests at this interval. Provide a number between 10 and 30.

        If you choose an interval of 10 and there are 15 health checkers, the endpoint will receive approximately 1 request per second.

        Can't be changed after HealthCheck is deployed
        '''
        result = self._values.get("request_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_path(self) -> typing.Optional[builtins.str]:
        '''The path for HTTP or HTTPS health checks.

        Provide a string between 1 and 255 length.
        '''
        result = self._values.get("resource_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def search_string(self) -> typing.Optional[builtins.str]:
        '''The search string for HTTP or HTTPS health checks.

        Route53 will search in the response body. Provide a string between 1 and 255 length.
        '''
        result = self._values.get("search_string")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointHealthCheckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@pepperize/cdk-route53-health-check.Failover")
class Failover(enum.Enum):
    PRIMARY = "PRIMARY"
    '''The primary record set.'''
    SECONDARY = "SECONDARY"
    '''The secondary record set.'''


@jsii.enum(jsii_type="@pepperize/cdk-route53-health-check.HealthCheckerRegions")
class HealthCheckerRegions(enum.Enum):
    '''The regions of health checker from which Route53 performs checks on the endpoint.'''

    US_EAST_1 = "US_EAST_1"
    US_WEST_1 = "US_WEST_1"
    US_WEST_2 = "US_WEST_2"
    EU_WEST_1 = "EU_WEST_1"
    AP_SOUTHEAST_1 = "AP_SOUTHEAST_1"
    AP_SOUTHEAST_2 = "AP_SOUTHEAST_2"
    AP_NORTHEAST_1 = "AP_NORTHEAST_1"
    SA_EAST_1 = "SA_EAST_1"


@jsii.interface(jsii_type="@pepperize/cdk-route53-health-check.IHealthCheck")
class IHealthCheck(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="healthCheckId")
    def health_check_id(self) -> builtins.str:
        ...

    @jsii.member(jsii_name="failover")
    def failover(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
        failover: typing.Optional[Failover] = None,
    ) -> None:
        '''Sets ``this.healthCheckId`` as the value for ``HealthCheckId`` on the given RecordSet.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: The Route53 RecordSet to configure failover.
        :param evaluate_target_health: Inherit the health of the referenced Alias RecordSet Target.
        :param failover: Sets ``PRIMARY`` or ``SECONDARY`` as the value for ``Failover`` on the given RecordSet.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-evaluatetargethealth
        '''
        ...

    @jsii.member(jsii_name="failoverPrimary")
    def failover_primary(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Sets ``PRIMARY`` as the value for ``Failover`` on the given RecordSet. Additionally, sets ``this.healthCheckId`` as the value for ``HealthCheckId``.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: The Route53 RecordSet to configure failover.
        :param evaluate_target_health: Inherit the health of the referenced Alias RecordSet Target.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-evaluatetargethealth
        '''
        ...

    @jsii.member(jsii_name="failoverSecondary")
    def failover_secondary(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Sets ``PRIMARY`` as the value for ``Failover`` on the given RecordSet. Additionally, sets ``this.healthCheckId`` as the value for ``HealthCheckId``.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: The Route53 RecordSet to configure failover.
        :param evaluate_target_health: Inherit the health of the referenced Alias RecordSet Target.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-evaluatetargethealth
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Return the given named metric for this HealthCheck.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        ...

    @jsii.member(jsii_name="metricHealthCheckStatus")
    def metric_health_check_status(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Route53 health checkers report that the HealthCheck is healthy or unhealthy.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        ...


class _IHealthCheckProxy:
    __jsii_type__: typing.ClassVar[str] = "@pepperize/cdk-route53-health-check.IHealthCheck"

    @builtins.property
    @jsii.member(jsii_name="healthCheckId")
    def health_check_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckId"))

    @jsii.member(jsii_name="failover")
    def failover(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
        failover: typing.Optional[Failover] = None,
    ) -> None:
        '''Sets ``this.healthCheckId`` as the value for ``HealthCheckId`` on the given RecordSet.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: The Route53 RecordSet to configure failover.
        :param evaluate_target_health: Inherit the health of the referenced Alias RecordSet Target.
        :param failover: Sets ``PRIMARY`` or ``SECONDARY`` as the value for ``Failover`` on the given RecordSet.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-evaluatetargethealth
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9a7ef656bb36af63e231e6e622e3a89c0b5a9ba6072c906dd908b331ad6f3e)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
            check_type(argname="argument failover", value=failover, expected_type=type_hints["failover"])
        return typing.cast(None, jsii.invoke(self, "failover", [record_set, evaluate_target_health, failover]))

    @jsii.member(jsii_name="failoverPrimary")
    def failover_primary(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Sets ``PRIMARY`` as the value for ``Failover`` on the given RecordSet. Additionally, sets ``this.healthCheckId`` as the value for ``HealthCheckId``.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: The Route53 RecordSet to configure failover.
        :param evaluate_target_health: Inherit the health of the referenced Alias RecordSet Target.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-evaluatetargethealth
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0077249ccf33344d454a3b96c20660322fed1daab0fcf9b06bb70bbaa03f0f63)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
        return typing.cast(None, jsii.invoke(self, "failoverPrimary", [record_set, evaluate_target_health]))

    @jsii.member(jsii_name="failoverSecondary")
    def failover_secondary(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Sets ``PRIMARY`` as the value for ``Failover`` on the given RecordSet. Additionally, sets ``this.healthCheckId`` as the value for ``HealthCheckId``.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: The Route53 RecordSet to configure failover.
        :param evaluate_target_health: Inherit the health of the referenced Alias RecordSet Target.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-evaluatetargethealth
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b4362695c796799be2a98452ad465f86a45fddba2695215ae8271abb48935e)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
        return typing.cast(None, jsii.invoke(self, "failoverSecondary", [record_set, evaluate_target_health]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Return the given named metric for this HealthCheck.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79618bf48b4b6a7108b5e008672bcdf3b1533e9e51c76cef2397c6efbe3f9362)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricHealthCheckStatus")
    def metric_health_check_status(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Route53 health checkers report that the HealthCheck is healthy or unhealthy.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricHealthCheckStatus", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IHealthCheck).__jsii_proxy_class__ = lambda : _IHealthCheckProxy


@jsii.enum(
    jsii_type="@pepperize/cdk-route53-health-check.InsufficientDataHealthStatus"
)
class InsufficientDataHealthStatus(enum.Enum):
    HEALTHY = "HEALTHY"
    '''Route53 considers the health check to be healthy.'''
    UNHEALTHY = "UNHEALTHY"
    '''Route53 considers the health check to be unhealthy.'''
    LAST_KNOWN_STATUS = "LAST_KNOWN_STATUS"
    '''Route53 uses the status of the health check from the last time that CloudWatch had sufficient data to determine the alarm state, otherwise healthy.'''


@jsii.enum(jsii_type="@pepperize/cdk-route53-health-check.Protocol")
class Protocol(enum.Enum):
    '''The protocol that Route53 uses to communicate with the endpoint.'''

    HTTP = "HTTP"
    HTTPS = "HTTPS"
    TCP = "TCP"


@jsii.implements(IHealthCheck, _aws_cdk_ceddda9d.ITaggable)
class AlarmHealthCheck(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@pepperize/cdk-route53-health-check.AlarmHealthCheck",
):
    '''Create a Route53 HealthCheck that monitors a CloudWatch Alarm.

    Example Example::

       const alarm new Alarm(stack, "Alarm", {
          // ...
       });
       new AlarmHealthCheck(stack, "HealthCheck", {
          alarm: alarm,
       });

    :link: https://docs.aws.amazon.com/de_de/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html#aws-resource-route53-healthcheck-properties
    :resource: AWS::Route53::HealthCheck
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alarm: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
        health_check_name: typing.Optional[builtins.str] = None,
        insufficient_data_health_status: typing.Optional[InsufficientDataHealthStatus] = None,
        inverted: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param alarm: The alarm that Route53 monitors.
        :param health_check_name: The display name of this Route53 HealthCheck.
        :param insufficient_data_health_status: The status to assign to the HealthCheck when CloudWatch has insufficient data about the metric.
        :param inverted: Whether to invert the status of the Route53 health check status.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36aac16420758dbfbae42930ff169755dabea5542db39a095016eb2b327c192)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AlarmHealthCheckProps(
            alarm=alarm,
            health_check_name=health_check_name,
            insufficient_data_health_status=insufficient_data_health_status,
            inverted=inverted,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromHealthCheckId")
    @builtins.classmethod
    def from_health_check_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        health_check_id: builtins.str,
    ) -> IHealthCheck:
        '''Import an existing Route53 HealthCheck.

        :param scope: -
        :param id: -
        :param health_check_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1645a3096c6ae2781a8b3260b0cef1717dd64e6744f32d4fc79afaaf27469079)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument health_check_id", value=health_check_id, expected_type=type_hints["health_check_id"])
        return typing.cast(IHealthCheck, jsii.sinvoke(cls, "fromHealthCheckId", [scope, id, health_check_id]))

    @jsii.member(jsii_name="failover")
    def failover(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
        failover: typing.Optional[Failover] = None,
    ) -> None:
        '''Sets ``this.healthCheckId`` as the value for ``HealthCheckId`` on the given RecordSet.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: -
        :param evaluate_target_health: -
        :param failover: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e5389aa439d069566e7e936cbf4e65349b34326f21b2eb38ade9884cc66264d)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
            check_type(argname="argument failover", value=failover, expected_type=type_hints["failover"])
        return typing.cast(None, jsii.invoke(self, "failover", [record_set, evaluate_target_health, failover]))

    @jsii.member(jsii_name="failoverPrimary")
    def failover_primary(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Sets ``PRIMARY`` as the value for ``Failover`` on the given RecordSet. Additionally, sets ``this.healthCheckId`` as the value for ``HealthCheckId``.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: -
        :param evaluate_target_health: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f8fff8075d51aefe0aa9ef527518785d6d1276bab52157b4a46002fb79fa604)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
        return typing.cast(None, jsii.invoke(self, "failoverPrimary", [record_set, evaluate_target_health]))

    @jsii.member(jsii_name="failoverSecondary")
    def failover_secondary(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Sets ``PRIMARY`` as the value for ``Failover`` on the given RecordSet. Additionally, sets ``this.healthCheckId`` as the value for ``HealthCheckId``.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: -
        :param evaluate_target_health: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46569cbabbd12efb41e94e511762c2da422bff9d63a76f34b1dd8125015e8851)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
        return typing.cast(None, jsii.invoke(self, "failoverSecondary", [record_set, evaluate_target_health]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Return the given named metric for this HealthCheck.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187d734344904617703d13b5c61336d6100026fac957ff594e33406201a71ecf)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricHealthCheckStatus")
    def metric_health_check_status(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Route53 health checkers report that the HealthCheck is healthy or unhealthy.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricHealthCheckStatus", [props]))

    @builtins.property
    @jsii.member(jsii_name="healthCheckId")
    def health_check_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckId"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_ceddda9d.TagManager:
        '''TagManager to set, remove and format tags.'''
        return typing.cast(_aws_cdk_ceddda9d.TagManager, jsii.get(self, "tags"))


@jsii.implements(IHealthCheck, _aws_cdk_ceddda9d.ITaggable)
class CalculatedHealthCheck(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@pepperize/cdk-route53-health-check.CalculatedHealthCheck",
):
    '''Create a Route53 HealthCheck that monitors other Route53 HealthChecks.

    Example Example::

       const healthCheck = new EndpointHealthCheck(stack, "HealthCheck", {
          domainName: "pepperize.com",
       });
       new CalculatedHealthCheck(stack, "CalculatedHealthCheck", {
          childHealthChecks: [healthCheck],
       });

    :link: https://docs.aws.amazon.com/de_de/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html#aws-resource-route53-healthcheck-properties
    :resource: AWS::Route53::HealthCheck
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        child_health_checks: typing.Optional[typing.Sequence[IHealthCheck]] = None,
        health_check_name: typing.Optional[builtins.str] = None,
        health_threshold: typing.Optional[jsii.Number] = None,
        inverted: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param child_health_checks: The list of HealthCheck that monitors other Route53 HealthChecks.
        :param health_check_name: The display name of this Route53 HealthCheck.
        :param health_threshold: The number of child HealthChecks that Amazon Route53 must consider healthy.
        :param inverted: Whether to invert the status of the Route53 health check status.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e89ac4b4326bbea34bfcd777269070151a02d03c8ec165a615703a3f5c55fbd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CalculatedHealthCheckProps(
            child_health_checks=child_health_checks,
            health_check_name=health_check_name,
            health_threshold=health_threshold,
            inverted=inverted,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromHealthCheckId")
    @builtins.classmethod
    def from_health_check_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        health_check_id: builtins.str,
    ) -> IHealthCheck:
        '''Import an existing Route53 HealthCheck.

        :param scope: -
        :param id: -
        :param health_check_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7146e8b74d3712e9672b89bad119949b0f1375b151e56eb489dac453df8f07f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument health_check_id", value=health_check_id, expected_type=type_hints["health_check_id"])
        return typing.cast(IHealthCheck, jsii.sinvoke(cls, "fromHealthCheckId", [scope, id, health_check_id]))

    @jsii.member(jsii_name="addChildHealthCheck")
    def add_child_health_check(self, health_check: IHealthCheck) -> None:
        '''
        :param health_check: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d05c787a0958f9d792f576cda74c0ea46b48cab3cad3e6807b0f0a8b7bb28ac0)
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
        return typing.cast(None, jsii.invoke(self, "addChildHealthCheck", [health_check]))

    @jsii.member(jsii_name="failover")
    def failover(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
        failover: typing.Optional[Failover] = None,
    ) -> None:
        '''Sets ``this.healthCheckId`` as the value for ``HealthCheckId`` on the given RecordSet.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: -
        :param evaluate_target_health: -
        :param failover: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e445238411f86cda816c1dbec8a8a947492a1c72f0f83ebc34f4173b344762)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
            check_type(argname="argument failover", value=failover, expected_type=type_hints["failover"])
        return typing.cast(None, jsii.invoke(self, "failover", [record_set, evaluate_target_health, failover]))

    @jsii.member(jsii_name="failoverPrimary")
    def failover_primary(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Sets ``PRIMARY`` as the value for ``Failover`` on the given RecordSet. Additionally, sets ``this.healthCheckId`` as the value for ``HealthCheckId``.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: -
        :param evaluate_target_health: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42ad6740de959a833a7924f057498b25cde1240d07fd4791afb57d376583884)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
        return typing.cast(None, jsii.invoke(self, "failoverPrimary", [record_set, evaluate_target_health]))

    @jsii.member(jsii_name="failoverSecondary")
    def failover_secondary(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Sets ``PRIMARY`` as the value for ``Failover`` on the given RecordSet. Additionally, sets ``this.healthCheckId`` as the value for ``HealthCheckId``.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: -
        :param evaluate_target_health: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b0b996d65cf686be1c503fa589a2837077c6e3f31e19a2fac0ea8389548fcf)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
        return typing.cast(None, jsii.invoke(self, "failoverSecondary", [record_set, evaluate_target_health]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Return the given named metric for this HealthCheck.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e12d39d9bbdf50f9bd221c15c0e36c980dd676ea1cdcd69f1743156da8adb0a)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricChildHealthCheckHealthyCount")
    def metric_child_health_check_healthy_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''The number of ChildHealthChecks that are healthy that Route53 is monitoring.

        Valid statistics: Average (recommended), Minimum, Maximum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricChildHealthCheckHealthyCount", [props]))

    @jsii.member(jsii_name="metricHealthCheckStatus")
    def metric_health_check_status(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Route53 health checkers report that the HealthCheck is healthy or unhealthy.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricHealthCheckStatus", [props]))

    @builtins.property
    @jsii.member(jsii_name="healthCheckId")
    def health_check_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckId"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_ceddda9d.TagManager:
        '''TagManager to set, remove and format tags.'''
        return typing.cast(_aws_cdk_ceddda9d.TagManager, jsii.get(self, "tags"))


@jsii.implements(IHealthCheck, _aws_cdk_ceddda9d.ITaggable)
class EndpointHealthCheck(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@pepperize/cdk-route53-health-check.EndpointHealthCheck",
):
    '''Create a Route53 HealthCheck that monitors an endpoint either by domain name or by IP address.

    Example Example::

       new EndpointHealthCheck(stack, "HealthCheck", {
          domainName: "pepperize.com",
       });

    Generates Example::

       Resources:
          Type: AWS::Route53::HealthCheck
          Properties:
            HealthCheckConfig:
              FullyQualifiedDomainName: "pepperize.com"
              Port: 443
              Type: "HTTPS"
              EnableSNI: true

    :link: https://docs.aws.amazon.com/de_de/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html#aws-resource-route53-healthcheck-properties
    :resource: AWS::Route53::HealthCheck
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain_name: typing.Optional[builtins.str] = None,
        enable_sni: typing.Optional[builtins.bool] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        health_check_name: typing.Optional[builtins.str] = None,
        inverted: typing.Optional[builtins.bool] = None,
        ip_address: typing.Optional[builtins.str] = None,
        latency_graphs: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[Protocol] = None,
        regions: typing.Optional[typing.Sequence[HealthCheckerRegions]] = None,
        request_interval: typing.Optional[jsii.Number] = None,
        resource_path: typing.Optional[builtins.str] = None,
        search_string: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domain_name: The domain name that Route53 performs health checks on. Route53 resolves the IP address and performs the lookup. If IP address is given, it's used as the host name. Either DomainName or IpAddress must be specified
        :param enable_sni: Specify that Route53 sends the host name for TLS negotiation. Default: true for HTTPS
        :param failure_threshold: The number of consecutive health checks that an endpoint must pass or fail for Route53 to change the current status of the endpoint between healthy and unhealthy. Provide a number between 1 and 10.
        :param health_check_name: The display name of this Route53 HealthCheck.
        :param inverted: Whether to invert the status of the Route53 health check status.
        :param ip_address: The ip address that Route53 performs health checks on. Optionally a domain name may be given. An IP address must be specified if protocol TCP
        :param latency_graphs: Whether Route53 measures the latency between health checkers in multiple AWS regions and your endpoint, and displays a CloudWatch latency graphs in the Route53 console. Can't be changed after HealthCheck is deployed
        :param port: The port that Route53 performs health checks. The port must be between 1 and 65535. Default: 80 for HTTP; 443 for HTTPS
        :param protocol: The protocol that Route53 uses to communicate with the endpoint. An IP address must be specified if protocol TCP Default: HTTPS
        :param regions: The list of regions from which Route53 health checkers check the endpoint. If omitted Route53 performs checks from all health checker regions.
        :param request_interval: The number of seconds between the time that Route53 gets a response from your endpoint and the time that it sends the next health check request. Each Route53 health checker makes requests at this interval. Provide a number between 10 and 30. If you choose an interval of 10 and there are 15 health checkers, the endpoint will receive approximately 1 request per second. Can't be changed after HealthCheck is deployed
        :param resource_path: The path for HTTP or HTTPS health checks. Provide a string between 1 and 255 length.
        :param search_string: The search string for HTTP or HTTPS health checks. Route53 will search in the response body. Provide a string between 1 and 255 length.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4c878d5c215d6b92e5a4681d2a3918ab898f350d63beb38250050c2b0fbd6d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EndpointHealthCheckProps(
            domain_name=domain_name,
            enable_sni=enable_sni,
            failure_threshold=failure_threshold,
            health_check_name=health_check_name,
            inverted=inverted,
            ip_address=ip_address,
            latency_graphs=latency_graphs,
            port=port,
            protocol=protocol,
            regions=regions,
            request_interval=request_interval,
            resource_path=resource_path,
            search_string=search_string,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromHealthCheckId")
    @builtins.classmethod
    def from_health_check_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        health_check_id: builtins.str,
    ) -> IHealthCheck:
        '''Import an existing Route53 HealthCheck.

        :param scope: -
        :param id: -
        :param health_check_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63b1664cc6df185e3a013bd30f67e9c593be3877e84e39df05b9300eb8cd565)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument health_check_id", value=health_check_id, expected_type=type_hints["health_check_id"])
        return typing.cast(IHealthCheck, jsii.sinvoke(cls, "fromHealthCheckId", [scope, id, health_check_id]))

    @jsii.member(jsii_name="failover")
    def failover(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
        failover: typing.Optional[Failover] = None,
    ) -> None:
        '''Sets ``this.healthCheckId`` as the value for ``HealthCheckId`` on the given RecordSet.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: -
        :param evaluate_target_health: -
        :param failover: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98787d45fd0ad7a6aeb5bfa65c81f2cc37f84ea7322dd28edffabfa481fd7aa)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
            check_type(argname="argument failover", value=failover, expected_type=type_hints["failover"])
        return typing.cast(None, jsii.invoke(self, "failover", [record_set, evaluate_target_health, failover]))

    @jsii.member(jsii_name="failoverPrimary")
    def failover_primary(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Sets ``PRIMARY`` as the value for ``Failover`` on the given RecordSet. Additionally, sets ``this.healthCheckId`` as the value for ``HealthCheckId``.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: -
        :param evaluate_target_health: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1a620a38e733e1cd1d39178c742a88d132ea4c23f1959b1205551b3857daa4)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
        return typing.cast(None, jsii.invoke(self, "failoverPrimary", [record_set, evaluate_target_health]))

    @jsii.member(jsii_name="failoverSecondary")
    def failover_secondary(
        self,
        record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
        evaluate_target_health: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Sets ``PRIMARY`` as the value for ``Failover`` on the given RecordSet. Additionally, sets ``this.healthCheckId`` as the value for ``HealthCheckId``.

        Applies only to alias, failover alias, geolocation alias, latency alias, and weighted alias resource record sets

        :param record_set: -
        :param evaluate_target_health: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7adf6d93f0936e5fb0846f9c7d0349d6350b5a09a906631d8104dac41a745cd8)
            check_type(argname="argument record_set", value=record_set, expected_type=type_hints["record_set"])
            check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
        return typing.cast(None, jsii.invoke(self, "failoverSecondary", [record_set, evaluate_target_health]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Return the given named metric for this HealthCheck.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc326233fa994ef17d91bc6d6111617414c5ce213e1025911e76fac9c834594)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricConnectionTime")
    def metric_connection_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''The time in milliseconds that it took Route53 health checkers to establish a TCP connection with the endpoint.

        Valid statistics: Average (recommended), Minimum, Maximum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricConnectionTime", [props]))

    @jsii.member(jsii_name="metricHealthCheckPercentageHealthy")
    def metric_health_check_percentage_healthy(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''The percentage of Route53 health checkers that report that the status of the health check is healthy.

        LatencyGraphs has to be enabled

        Valid statistics: Average (recommended), Minimum, Maximum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricHealthCheckPercentageHealthy", [props]))

    @jsii.member(jsii_name="metricHealthCheckStatus")
    def metric_health_check_status(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Route53 health checkers report that the HealthCheck is healthy or unhealthy.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricHealthCheckStatus", [props]))

    @jsii.member(jsii_name="metricSSLHandshakeTime")
    def metric_ssl_handshake_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''The time in milliseconds that it took Route53 health checkers to complete the SSL/TLS handshake.

        Valid statistics: Average, Minimum, Maximum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSSLHandshakeTime", [props]))

    @jsii.member(jsii_name="metricTimeToFirstByte")
    def metric_time_to_first_byte(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''The time in milliseconds that it took Route53 health checkers to receive the first byte of the response to an HTTP or HTTPS request.

        Valid statistics: Average (recommended), Minimum, Maximum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTimeToFirstByte", [props]))

    @builtins.property
    @jsii.member(jsii_name="healthCheckId")
    def health_check_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckId"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_ceddda9d.TagManager:
        '''TagManager to set, remove and format tags.'''
        return typing.cast(_aws_cdk_ceddda9d.TagManager, jsii.get(self, "tags"))


__all__ = [
    "AlarmHealthCheck",
    "AlarmHealthCheckProps",
    "CalculatedHealthCheck",
    "CalculatedHealthCheckProps",
    "EndpointHealthCheck",
    "EndpointHealthCheckProps",
    "Failover",
    "HealthCheckerRegions",
    "IHealthCheck",
    "InsufficientDataHealthStatus",
    "Protocol",
]

publication.publish()

def _typecheckingstub__639153b296f45bd8c248c52158a6493c4845bdb55b7de3975f909413a7b84ae2(
    *,
    alarm: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
    health_check_name: typing.Optional[builtins.str] = None,
    insufficient_data_health_status: typing.Optional[InsufficientDataHealthStatus] = None,
    inverted: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50716ab3df3dce42fb0a3b896e69290109228794f9a6daa26dea7eb00d9625fd(
    *,
    child_health_checks: typing.Optional[typing.Sequence[IHealthCheck]] = None,
    health_check_name: typing.Optional[builtins.str] = None,
    health_threshold: typing.Optional[jsii.Number] = None,
    inverted: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de064cce147a8183cdbdbedceafe764868f4f6e90a0f2301d6c340bdea374acc(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    enable_sni: typing.Optional[builtins.bool] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    health_check_name: typing.Optional[builtins.str] = None,
    inverted: typing.Optional[builtins.bool] = None,
    ip_address: typing.Optional[builtins.str] = None,
    latency_graphs: typing.Optional[builtins.bool] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[Protocol] = None,
    regions: typing.Optional[typing.Sequence[HealthCheckerRegions]] = None,
    request_interval: typing.Optional[jsii.Number] = None,
    resource_path: typing.Optional[builtins.str] = None,
    search_string: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9a7ef656bb36af63e231e6e622e3a89c0b5a9ba6072c906dd908b331ad6f3e(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
    failover: typing.Optional[Failover] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0077249ccf33344d454a3b96c20660322fed1daab0fcf9b06bb70bbaa03f0f63(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b4362695c796799be2a98452ad465f86a45fddba2695215ae8271abb48935e(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79618bf48b4b6a7108b5e008672bcdf3b1533e9e51c76cef2397c6efbe3f9362(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36aac16420758dbfbae42930ff169755dabea5542db39a095016eb2b327c192(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alarm: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
    health_check_name: typing.Optional[builtins.str] = None,
    insufficient_data_health_status: typing.Optional[InsufficientDataHealthStatus] = None,
    inverted: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1645a3096c6ae2781a8b3260b0cef1717dd64e6744f32d4fc79afaaf27469079(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    health_check_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5389aa439d069566e7e936cbf4e65349b34326f21b2eb38ade9884cc66264d(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
    failover: typing.Optional[Failover] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8fff8075d51aefe0aa9ef527518785d6d1276bab52157b4a46002fb79fa604(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46569cbabbd12efb41e94e511762c2da422bff9d63a76f34b1dd8125015e8851(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187d734344904617703d13b5c61336d6100026fac957ff594e33406201a71ecf(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e89ac4b4326bbea34bfcd777269070151a02d03c8ec165a615703a3f5c55fbd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    child_health_checks: typing.Optional[typing.Sequence[IHealthCheck]] = None,
    health_check_name: typing.Optional[builtins.str] = None,
    health_threshold: typing.Optional[jsii.Number] = None,
    inverted: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7146e8b74d3712e9672b89bad119949b0f1375b151e56eb489dac453df8f07f4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    health_check_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05c787a0958f9d792f576cda74c0ea46b48cab3cad3e6807b0f0a8b7bb28ac0(
    health_check: IHealthCheck,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e445238411f86cda816c1dbec8a8a947492a1c72f0f83ebc34f4173b344762(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
    failover: typing.Optional[Failover] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42ad6740de959a833a7924f057498b25cde1240d07fd4791afb57d376583884(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b0b996d65cf686be1c503fa589a2837077c6e3f31e19a2fac0ea8389548fcf(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e12d39d9bbdf50f9bd221c15c0e36c980dd676ea1cdcd69f1743156da8adb0a(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4c878d5c215d6b92e5a4681d2a3918ab898f350d63beb38250050c2b0fbd6d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain_name: typing.Optional[builtins.str] = None,
    enable_sni: typing.Optional[builtins.bool] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    health_check_name: typing.Optional[builtins.str] = None,
    inverted: typing.Optional[builtins.bool] = None,
    ip_address: typing.Optional[builtins.str] = None,
    latency_graphs: typing.Optional[builtins.bool] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[Protocol] = None,
    regions: typing.Optional[typing.Sequence[HealthCheckerRegions]] = None,
    request_interval: typing.Optional[jsii.Number] = None,
    resource_path: typing.Optional[builtins.str] = None,
    search_string: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63b1664cc6df185e3a013bd30f67e9c593be3877e84e39df05b9300eb8cd565(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    health_check_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98787d45fd0ad7a6aeb5bfa65c81f2cc37f84ea7322dd28edffabfa481fd7aa(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
    failover: typing.Optional[Failover] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1a620a38e733e1cd1d39178c742a88d132ea4c23f1959b1205551b3857daa4(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7adf6d93f0936e5fb0846f9c7d0349d6350b5a09a906631d8104dac41a745cd8(
    record_set: _aws_cdk_aws_route53_ceddda9d.RecordSet,
    evaluate_target_health: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc326233fa994ef17d91bc6d6111617414c5ce213e1025911e76fac9c834594(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass
