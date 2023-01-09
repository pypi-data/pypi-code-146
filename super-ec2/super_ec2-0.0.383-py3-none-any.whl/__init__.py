'''
[![NPM version](https://badge.fury.io/js/%40cdk-constructs-zone%2Fsuper-ec2.svg)](https://badge.fury.io/js/%40cdk-constructs-zone%2Fsuper-ec2)
[![PyPI version](https://badge.fury.io/py/super-ec2.svg)](https://badge.fury.io/py/super-ec2)
![Release](https://github.com/cdk-constructs-zone/super-ec2/workflows/release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/@cdk-constructs-zone/super-ec2?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/super-ec2?label=pypi&color=blue)

![](https://img.shields.io/badge/jenkins-ec2-green=?style=plastic&logo=appveyor)

# Welcome to `@cdk-constructs-zone/super-ec2`

This repository template helps you create EC2 .

## Sample

### Jenkins

* Simplest deployment: It would creat a VPC and ALB by default.

```python
import * as cdk from '@aws-cdk/core';
import { JenkinsEC2, ELBtype } from '@cdk-constructs-zone/super-ec2';

const app = new cdk.App();

const stack = new cdk.Stack(app, 'demo');

const jks = new JenkinsEC2(stack, 'superJks', {});

new cdk.CfnOutput(stack, 'loadbalancerDNS', {
  value: jks.loadbalancer.loadBalancerDnsName,
});
new cdk.CfnOutput(stack, 'connect-to-instance', {
  value: `aws ssm start-session --target ${jks.instance.instanceId}`,
});
```

* Deploy Jenkins with self-defined VPC and NLB

```python
const jks = new JenkinsEC2(stack, 'superJks', {
  vpc: Vpc.fromLookup(stack, 'defaultVPC', { isDefault: true }),
  loadbalancerType: ELBtype.NLB,
});
```

* Deploy Jenkins with R53 records: If `acm` is not given, it would create a certificate validated from DNS by default.

```python
const jks = new JenkinsEC2(stack, 'superJks', {
  vpc: Vpc.fromLookup(stack, 'defaultVPC', { isDefault: true }),
  loadbalancerType: ELBtype.NLB,
  domain: {
    acm: Certificate.fromCertificateArn(stack, 'cert',
      'arn:aws:xxx',
    ),
    hostedZoneId: 'xxx',
    zoneName: 'bbb.ccc',
    recordName: 'aaa',
  },
});
```

Note: Jenkins initial admin password has been written to `/home/ec2-user/jenkins-data/secrets/initialAdminPassword`. You can access EC2 instance using [ssm tool](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-sessions-start.html).

```
aws ssm start-session --target instance-id
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

from ._jsii import *

import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_1662be0d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_67de8e8d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_e93c784f
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_f47b29d4
import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.enum(jsii_type="@cdk-constructs-zone/super-ec2.AmiOSType")
class AmiOSType(enum.Enum):
    '''
    :stability: experimental
    '''

    UBUNTU_18_04 = "UBUNTU_18_04"
    '''(experimental) Ubuntu 18.04 ami.

    :stability: experimental
    '''
    UBUNTU_20_04 = "UBUNTU_20_04"
    '''(experimental) Ubuntu 20.04 ami.

    :stability: experimental
    '''
    CENTOS_7 = "CENTOS_7"
    '''(experimental) CentOS 7 ami.

    :stability: experimental
    '''
    CENTOS_8 = "CENTOS_8"
    '''(experimental) CentOS 8 ami.

    :stability: experimental
    '''
    AMAZON_LINUX_2 = "AMAZON_LINUX_2"
    '''(experimental) Amazon Linux 2 ami.

    :stability: experimental
    '''
    AMAZON_LINUX = "AMAZON_LINUX"
    '''(experimental) Amazon Linux  ami.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@cdk-constructs-zone/super-ec2.ELBtype")
class ELBtype(enum.Enum):
    '''
    :stability: experimental
    '''

    ALB = "ALB"
    '''(experimental) Application Load Balancer.

    :stability: experimental
    '''
    NLB = "NLB"
    '''(experimental) Network Load Balancer.

    :stability: experimental
    '''


@jsii.interface(jsii_type="@cdk-constructs-zone/super-ec2.IDomainProps")
class IDomainProps(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> builtins.str:
        '''(experimental) HostZoneID.

        :stability: experimental
        '''
        ...

    @hosted_zone_id.setter
    def hosted_zone_id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="recordName")
    def record_name(self) -> builtins.str:
        '''(experimental) recordname (e.g., superjks).

        :stability: experimental
        '''
        ...

    @record_name.setter
    def record_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> builtins.str:
        '''(experimental) zonename (e.g., ``cdk-construct-zone.com``).

        :stability: experimental
        '''
        ...

    @zone_name.setter
    def zone_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="acm")
    def acm(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate]:
        '''(experimental) Provide a certificate.

        :default: - Create a new certificate (validate from DNS)

        :stability: experimental
        '''
        ...

    @acm.setter
    def acm(
        self,
        value: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''(experimental) record cache time.

        :stability: experimental
        :deafult: - 5 mins.
        '''
        ...

    @ttl.setter
    def ttl(self, value: typing.Optional[_aws_cdk_core_f4b25747.Duration]) -> None:
        ...


class _IDomainPropsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdk-constructs-zone/super-ec2.IDomainProps"

    @builtins.property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> builtins.str:
        '''(experimental) HostZoneID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "hostedZoneId"))

    @hosted_zone_id.setter
    def hosted_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c692ae01a578f319c82c1747becb29200dca6563504a6f771314a0494a54718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostedZoneId", value)

    @builtins.property
    @jsii.member(jsii_name="recordName")
    def record_name(self) -> builtins.str:
        '''(experimental) recordname (e.g., superjks).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "recordName"))

    @record_name.setter
    def record_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0895dc2d385cddc3efcb533ff5b5b2ef94961f5fded6374e719c439aec12a039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordName", value)

    @builtins.property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> builtins.str:
        '''(experimental) zonename (e.g., ``cdk-construct-zone.com``).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "zoneName"))

    @zone_name.setter
    def zone_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43eb4d441de3aca8f22be140e1a267fb6e1e41a1687e3024fe4f0db7468b7879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneName", value)

    @builtins.property
    @jsii.member(jsii_name="acm")
    def acm(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate]:
        '''(experimental) Provide a certificate.

        :default: - Create a new certificate (validate from DNS)

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate], jsii.get(self, "acm"))

    @acm.setter
    def acm(
        self,
        value: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3690bb2d4561c678f1aba812efe23f932e7c1dad17f86fad852844373501c2b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acm", value)

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''(experimental) record cache time.

        :stability: experimental
        :deafult: - 5 mins.
        '''
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: typing.Optional[_aws_cdk_core_f4b25747.Duration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4559fd375fd7b87164ba6d98a0aa716360eaadf8d6027692b02adeba96a469a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDomainProps).__jsii_proxy_class__ = lambda : _IDomainPropsProxy


@jsii.interface(jsii_type="@cdk-constructs-zone/super-ec2.ISuperDomainProps")
class ISuperDomainProps(IDomainProps, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="loadbalancer")
    def loadbalancer(
        self,
    ) -> typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer]:
        '''
        :stability: experimental
        '''
        ...

    @loadbalancer.setter
    def loadbalancer(
        self,
        value: typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer],
    ) -> None:
        ...


class _ISuperDomainPropsProxy(
    jsii.proxy_for(IDomainProps), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdk-constructs-zone/super-ec2.ISuperDomainProps"

    @builtins.property
    @jsii.member(jsii_name="loadbalancer")
    def loadbalancer(
        self,
    ) -> typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer], jsii.get(self, "loadbalancer"))

    @loadbalancer.setter
    def loadbalancer(
        self,
        value: typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6e927513162a51b91fa3dd6303cd3b8fd5c6b06c7ca5d063c34935f9755ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadbalancer", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISuperDomainProps).__jsii_proxy_class__ = lambda : _ISuperDomainPropsProxy


@jsii.interface(jsii_type="@cdk-constructs-zone/super-ec2.ISuperEC2BaseProps")
class ISuperEC2BaseProps(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="amiOSType")
    def ami_os_type(self) -> typing.Optional[AmiOSType]:
        '''(experimental) Super EC2 OS you want.

        :default: - Amzaon Linux 2.

        :stability: experimental
        '''
        ...

    @ami_os_type.setter
    def ami_os_type(self, value: typing.Optional[AmiOSType]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType]:
        '''(experimental) Super EC2 Instance Type.

        :default: - t3.small.

        :stability: experimental
        '''
        ...

    @instance_type.setter
    def instance_type(
        self,
        value: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''(experimental) Super EC2 Vpc.

        :default: - Create a new Vpc.

        :stability: experimental
        '''
        ...

    @vpc.setter
    def vpc(self, value: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]) -> None:
        ...


class _ISuperEC2BasePropsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdk-constructs-zone/super-ec2.ISuperEC2BaseProps"

    @builtins.property
    @jsii.member(jsii_name="amiOSType")
    def ami_os_type(self) -> typing.Optional[AmiOSType]:
        '''(experimental) Super EC2 OS you want.

        :default: - Amzaon Linux 2.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[AmiOSType], jsii.get(self, "amiOSType"))

    @ami_os_type.setter
    def ami_os_type(self, value: typing.Optional[AmiOSType]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2421dc2d3b1edfbfdad5c9d4af98fbc60f4d24b1687b3b955d6b31bee2e35f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "amiOSType", value)

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType]:
        '''(experimental) Super EC2 Instance Type.

        :default: - t3.small.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType], jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(
        self,
        value: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b86c1506b300d484e93052e486df6e4831818e83dbdfb3dbad32df7683e331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''(experimental) Super EC2 Vpc.

        :default: - Create a new Vpc.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a5bd5fd199d68b3b8f03b40b65cd72b7823f6edce1156ff0ebdf82a8643610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISuperEC2BaseProps).__jsii_proxy_class__ = lambda : _ISuperEC2BasePropsProxy


class SuperDomain(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-constructs-zone/super-ec2.SuperDomain",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        props: ISuperDomainProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51234b5f6a13111471696311d40a30d896e3bac5ef3a50866a3745126aba79ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="acm")
    def acm(self) -> _aws_cdk_aws_certificatemanager_1662be0d.ICertificate:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_certificatemanager_1662be0d.ICertificate, jsii.get(self, "acm"))

    @builtins.property
    @jsii.member(jsii_name="record")
    def record(self) -> _aws_cdk_aws_route53_f47b29d4.ARecord:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_route53_f47b29d4.ARecord, jsii.get(self, "record"))

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> _aws_cdk_aws_route53_f47b29d4.IHostedZone:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_route53_f47b29d4.IHostedZone, jsii.get(self, "zone"))


class SuperEC2Base(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdk-constructs-zone/super-ec2.SuperEC2Base",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        props: ISuperEC2BaseProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947c1ace77a787a3db686413c7eb0939031143d9f9241a4830550a19ecf664e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="defaultSecurityGroup")
    def default_security_group(self) -> _aws_cdk_aws_ec2_67de8e8d.SecurityGroup:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.SecurityGroup, jsii.get(self, "defaultSecurityGroup"))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> _aws_cdk_aws_ec2_67de8e8d.Instance:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.Instance, jsii.get(self, "instance"))

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> _aws_cdk_aws_ec2_67de8e8d.UserData:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.UserData, jsii.get(self, "userData"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_67de8e8d.IVpc:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.IVpc, jsii.get(self, "vpc"))


class _SuperEC2BaseProxy(SuperEC2Base):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, SuperEC2Base).__jsii_proxy_class__ = lambda : _SuperEC2BaseProxy


@jsii.interface(jsii_type="@cdk-constructs-zone/super-ec2.IJenkinsEC2Props")
class IJenkinsEC2Props(ISuperEC2BaseProps, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[IDomainProps]:
        '''(experimental) Provide domain attribute.

        :default: - Not use certificate and route53

        :stability: experimental
        '''
        ...

    @domain.setter
    def domain(self, value: typing.Optional[IDomainProps]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="loadbalancer")
    def loadbalancer(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer]]:
        '''(experimental) Provide a loadbalancer.

        Only support ALB and NLB.

        :default: - Create ApplicationLoadBalancer

        :stability: experimental
        '''
        ...

    @loadbalancer.setter
    def loadbalancer(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="loadbalancerType")
    def loadbalancer_type(self) -> typing.Optional[ELBtype]:
        '''(experimental) ELB type.

        :default: - ELBtype.ALB

        :stability: experimental
        '''
        ...

    @loadbalancer_type.setter
    def loadbalancer_type(self, value: typing.Optional[ELBtype]) -> None:
        ...


class _IJenkinsEC2PropsProxy(
    jsii.proxy_for(ISuperEC2BaseProps), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cdk-constructs-zone/super-ec2.IJenkinsEC2Props"

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[IDomainProps]:
        '''(experimental) Provide domain attribute.

        :default: - Not use certificate and route53

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IDomainProps], jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: typing.Optional[IDomainProps]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3471c5e14f10e13eeac08861b41f036b5988e4793270ddd00bce6f10d4433d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="loadbalancer")
    def loadbalancer(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer]]:
        '''(experimental) Provide a loadbalancer.

        Only support ALB and NLB.

        :default: - Create ApplicationLoadBalancer

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer]], jsii.get(self, "loadbalancer"))

    @loadbalancer.setter
    def loadbalancer(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86e168dfde690047a97559e0a3e24ff281c500a389e25dc90b4c513cc4a4dffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadbalancer", value)

    @builtins.property
    @jsii.member(jsii_name="loadbalancerType")
    def loadbalancer_type(self) -> typing.Optional[ELBtype]:
        '''(experimental) ELB type.

        :default: - ELBtype.ALB

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ELBtype], jsii.get(self, "loadbalancerType"))

    @loadbalancer_type.setter
    def loadbalancer_type(self, value: typing.Optional[ELBtype]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391c11aae6c6ed53ad5ab3f0182c16a8f6831cf1ac5494ee597d6656467660d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadbalancerType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJenkinsEC2Props).__jsii_proxy_class__ = lambda : _IJenkinsEC2PropsProxy


class JenkinsEC2(
    SuperEC2Base,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-constructs-zone/super-ec2.JenkinsEC2",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        props: IJenkinsEC2Props,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8bac3ef7906d3855bc1717fb2a80920a09f05b6ab30e5ba2657c0d3dc4533fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="jenkinsUserData")
    def jenkins_user_data(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "jenkinsUserData", []))

    @builtins.property
    @jsii.member(jsii_name="loadbalancer")
    def loadbalancer(
        self,
    ) -> typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer], jsii.get(self, "loadbalancer"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[SuperDomain]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[SuperDomain], jsii.get(self, "domain"))


__all__ = [
    "AmiOSType",
    "ELBtype",
    "IDomainProps",
    "IJenkinsEC2Props",
    "ISuperDomainProps",
    "ISuperEC2BaseProps",
    "JenkinsEC2",
    "SuperDomain",
    "SuperEC2Base",
]

publication.publish()

def _typecheckingstub__5c692ae01a578f319c82c1747becb29200dca6563504a6f771314a0494a54718(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0895dc2d385cddc3efcb533ff5b5b2ef94961f5fded6374e719c439aec12a039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43eb4d441de3aca8f22be140e1a267fb6e1e41a1687e3024fe4f0db7468b7879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3690bb2d4561c678f1aba812efe23f932e7c1dad17f86fad852844373501c2b7(
    value: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4559fd375fd7b87164ba6d98a0aa716360eaadf8d6027692b02adeba96a469a(
    value: typing.Optional[_aws_cdk_core_f4b25747.Duration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6e927513162a51b91fa3dd6303cd3b8fd5c6b06c7ca5d063c34935f9755ef0(
    value: typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2421dc2d3b1edfbfdad5c9d4af98fbc60f4d24b1687b3b955d6b31bee2e35f2(
    value: typing.Optional[AmiOSType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b86c1506b300d484e93052e486df6e4831818e83dbdfb3dbad32df7683e331(
    value: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a5bd5fd199d68b3b8f03b40b65cd72b7823f6edce1156ff0ebdf82a8643610(
    value: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51234b5f6a13111471696311d40a30d896e3bac5ef3a50866a3745126aba79ec(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    props: ISuperDomainProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947c1ace77a787a3db686413c7eb0939031143d9f9241a4830550a19ecf664e9(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    props: ISuperEC2BaseProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3471c5e14f10e13eeac08861b41f036b5988e4793270ddd00bce6f10d4433d(
    value: typing.Optional[IDomainProps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e168dfde690047a97559e0a3e24ff281c500a389e25dc90b4c513cc4a4dffb(
    value: typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391c11aae6c6ed53ad5ab3f0182c16a8f6831cf1ac5494ee597d6656467660d3(
    value: typing.Optional[ELBtype],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8bac3ef7906d3855bc1717fb2a80920a09f05b6ab30e5ba2657c0d3dc4533fd(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    props: IJenkinsEC2Props,
) -> None:
    """Type checking stubs"""
    pass
