'''
# AWS::Route53RecoveryControl Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Route53RecoveryControl construct libraries](https://constructs.dev/search?q=route53recoverycontrol)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Route53RecoveryControl resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Route53RecoveryControl.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Route53RecoveryControl](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Route53RecoveryControl.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCluster(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnCluster",
):
    '''A CloudFormation ``AWS::Route53RecoveryControl::Cluster``.

    Returns an array of all the clusters in an account.

    :cloudformationResource: AWS::Route53RecoveryControl::Cluster
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
        
        cfn_cluster = route53recoverycontrol.CfnCluster(self, "MyCfnCluster",
            cluster_endpoints=[route53recoverycontrol.CfnCluster.ClusterEndpointProperty(
                endpoint="endpoint",
                region="region"
            )],
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        cluster_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnCluster.ClusterEndpointProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryControl::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster_endpoints: ``AWS::Route53RecoveryControl::Cluster.ClusterEndpoints``.
        :param name: Name of the cluster. You can use any non-white space character in the name.
        :param tags: The value for a tag.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d41dfe645334ead300abc5a285bc74cb9134e11a757d1862ae8b874d1bbdf5e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnClusterProps(
            cluster_endpoints=cluster_endpoints, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3b3ab44594c0393df1cd3695fd7d56988e7781e1dce09a861fad6eac938fd1)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a335bdfa86babdd8dce2f447f06bd098edc3d356c97fd0c26062020814c2212d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrClusterArn")
    def attr_cluster_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the cluster.

        :cloudformationAttribute: ClusterArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrClusterArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''Deployment status of a resource.

        Status can be one of the following: PENDING, DEPLOYED, PENDING_DELETION.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html#cfn-route53recoverycontrol-cluster-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoints")
    def cluster_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnCluster.ClusterEndpointProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''``AWS::Route53RecoveryControl::Cluster.ClusterEndpoints``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html#cfn-route53recoverycontrol-cluster-clusterendpoints
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnCluster.ClusterEndpointProperty", _aws_cdk_core_f4b25747.IResolvable]]]], jsii.get(self, "clusterEndpoints"))

    @cluster_endpoints.setter
    def cluster_endpoints(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnCluster.ClusterEndpointProperty", _aws_cdk_core_f4b25747.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1536579d807b43a9677de858e54e0bc5ecee68e1ecf47d640fe7535b31e33ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterEndpoints", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the cluster.

        You can use any non-white space character in the name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html#cfn-route53recoverycontrol-cluster-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97350e787b2f12863d7abe1387aa6089336ea03e7e0348c7051a08aea4371e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnCluster.ClusterEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint": "endpoint", "region": "region"},
    )
    class ClusterEndpointProperty:
        def __init__(
            self,
            *,
            endpoint: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A cluster endpoint.

            Specify an endpoint when you want to set or retrieve a routing control state in the cluster.

            :param endpoint: A cluster endpoint. Specify an endpoint and AWS Region when you want to set or retrieve a routing control state in the cluster. To get or update the routing control state, see the Amazon Route 53 Application Recovery Controller Routing Control Actions.
            :param region: The AWS Region for a cluster endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-cluster-clusterendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
                
                cluster_endpoint_property = route53recoverycontrol.CfnCluster.ClusterEndpointProperty(
                    endpoint="endpoint",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1596b12cf4bea6d59f07a3f028e502e3b10c184f6015358541657920042a220d)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''A cluster endpoint.

            Specify an endpoint and AWS Region when you want to set or retrieve a routing control state in the cluster.

            To get or update the routing control state, see the Amazon Route 53 Application Recovery Controller Routing Control Actions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-cluster-clusterendpoint.html#cfn-route53recoverycontrol-cluster-clusterendpoint-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region for a cluster endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-cluster-clusterendpoint.html#cfn-route53recoverycontrol-cluster-clusterendpoint-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClusterEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_endpoints": "clusterEndpoints",
        "name": "name",
        "tags": "tags",
    },
)
class CfnClusterProps:
    def __init__(
        self,
        *,
        cluster_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnCluster.ClusterEndpointProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCluster``.

        :param cluster_endpoints: ``AWS::Route53RecoveryControl::Cluster.ClusterEndpoints``.
        :param name: Name of the cluster. You can use any non-white space character in the name.
        :param tags: The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
            
            cfn_cluster_props = route53recoverycontrol.CfnClusterProps(
                cluster_endpoints=[route53recoverycontrol.CfnCluster.ClusterEndpointProperty(
                    endpoint="endpoint",
                    region="region"
                )],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bffa22753179417dc3e08f4b1d4b92bad5ba1fd54697710af4382185eb512c16)
            check_type(argname="argument cluster_endpoints", value=cluster_endpoints, expected_type=type_hints["cluster_endpoints"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_endpoints is not None:
            self._values["cluster_endpoints"] = cluster_endpoints
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cluster_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnCluster.ClusterEndpointProperty, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''``AWS::Route53RecoveryControl::Cluster.ClusterEndpoints``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html#cfn-route53recoverycontrol-cluster-clusterendpoints
        '''
        result = self._values.get("cluster_endpoints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnCluster.ClusterEndpointProperty, _aws_cdk_core_f4b25747.IResolvable]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the cluster.

        You can use any non-white space character in the name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html#cfn-route53recoverycontrol-cluster-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html#cfn-route53recoverycontrol-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnControlPanel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnControlPanel",
):
    '''A CloudFormation ``AWS::Route53RecoveryControl::ControlPanel``.

    Creates a new control panel. A control panel represents a group of routing controls that can be changed together in a single transaction. You can use a control panel to centrally view the operational status of applications across your organization, and trigger multi-app failovers in a single transaction, for example, to fail over an Availability Zone or AWS Region .

    :cloudformationResource: AWS::Route53RecoveryControl::ControlPanel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-controlpanel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
        
        cfn_control_panel = route53recoverycontrol.CfnControlPanel(self, "MyCfnControlPanel",
            name="name",
        
            # the properties below are optional
            cluster_arn="clusterArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        cluster_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryControl::ControlPanel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the control panel. You can use any non-white space character in the name.
        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster for the control panel.
        :param tags: The value for a tag.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc903ab94203a44c3b7d1969e21b723c14ae1263489e63d0b6f0cdf50074b075)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnControlPanelProps(name=name, cluster_arn=cluster_arn, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5f35c38a208a577e5bac7a5ccf944c54263dabcf0e80ff5b590ddd3bd3629a)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2c4f1843476d9001a3fde6e919baaf6bc72d6ea053d1c66cba46fb63e2f39b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrControlPanelArn")
    def attr_control_panel_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the control panel.

        :cloudformationAttribute: ControlPanelArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrControlPanelArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDefaultControlPanel")
    def attr_default_control_panel(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''The boolean flag that is set to true for the default control panel in the cluster.

        :cloudformationAttribute: DefaultControlPanel
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrDefaultControlPanel"))

    @builtins.property
    @jsii.member(jsii_name="attrRoutingControlCount")
    def attr_routing_control_count(self) -> jsii.Number:
        '''The number of routing controls in the control panel.

        :cloudformationAttribute: RoutingControlCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrRoutingControlCount"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The deployment status of control panel.

        Status can be one of the following: PENDING, DEPLOYED, PENDING_DELETION.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-controlpanel.html#cfn-route53recoverycontrol-controlpanel-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the control panel.

        You can use any non-white space character in the name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-controlpanel.html#cfn-route53recoverycontrol-controlpanel-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e5515b4d95d4d1f301760f1cbd82681423d4e78fc4f9c62982f2a343eea74c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the cluster for the control panel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-controlpanel.html#cfn-route53recoverycontrol-controlpanel-clusterarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterArn"))

    @cluster_arn.setter
    def cluster_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8896ae1e262b7522faeff4f2767e3d21e93ae2272dbf7c81d3230f6bf11b656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnControlPanelProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "cluster_arn": "clusterArn", "tags": "tags"},
)
class CfnControlPanelProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        cluster_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnControlPanel``.

        :param name: The name of the control panel. You can use any non-white space character in the name.
        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster for the control panel.
        :param tags: The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-controlpanel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
            
            cfn_control_panel_props = route53recoverycontrol.CfnControlPanelProps(
                name="name",
            
                # the properties below are optional
                cluster_arn="clusterArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67145e27b3d63359f442179e63bb2720fdba3a846f3d0ead17004de1c2eaee30)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if cluster_arn is not None:
            self._values["cluster_arn"] = cluster_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the control panel.

        You can use any non-white space character in the name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-controlpanel.html#cfn-route53recoverycontrol-controlpanel-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the cluster for the control panel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-controlpanel.html#cfn-route53recoverycontrol-controlpanel-clusterarn
        '''
        result = self._values.get("cluster_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-controlpanel.html#cfn-route53recoverycontrol-controlpanel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnControlPanelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRoutingControl(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnRoutingControl",
):
    '''A CloudFormation ``AWS::Route53RecoveryControl::RoutingControl``.

    Defines a routing control. To get or update the routing control state, see the Recovery Cluster (data plane) API actions for Amazon Route 53 Application Recovery Controller.

    :cloudformationResource: AWS::Route53RecoveryControl::RoutingControl
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-routingcontrol.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
        
        cfn_routing_control = route53recoverycontrol.CfnRoutingControl(self, "MyCfnRoutingControl",
            name="name",
        
            # the properties below are optional
            cluster_arn="clusterArn",
            control_panel_arn="controlPanelArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        cluster_arn: typing.Optional[builtins.str] = None,
        control_panel_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryControl::RoutingControl``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the routing control. You can use any non-white space character in the name.
        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster that includes the routing control.
        :param control_panel_arn: The Amazon Resource Name (ARN) of the control panel that includes the routing control.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6f7020ab2002b6006666264a5b3414ebd6f6a10dbe0e59ce6a1d5d717a517f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRoutingControlProps(
            name=name, cluster_arn=cluster_arn, control_panel_arn=control_panel_arn
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba95efc41cd53b3f35081c3b3a31d6dcb0008e5a8a5f72fa21d7a27466a4f4a)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ae631f2b3950535658b83d0e8f727abe68886b6e605729d9838a46a631d4a9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrRoutingControlArn")
    def attr_routing_control_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the routing control.

        :cloudformationAttribute: RoutingControlArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRoutingControlArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The deployment status of the routing control.

        Status can be one of the following: PENDING, DEPLOYED, PENDING_DELETION.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the routing control.

        You can use any non-white space character in the name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-routingcontrol.html#cfn-route53recoverycontrol-routingcontrol-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0492331b2882b1c2254c26e64fb370c80338bb3db4911b7be1484ef72f463c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the cluster that includes the routing control.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-routingcontrol.html#cfn-route53recoverycontrol-routingcontrol-clusterarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterArn"))

    @cluster_arn.setter
    def cluster_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abe8e890a08f84881f63be6edc6f80b2c46ad077bc0baf3cf3a8dd94f444d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterArn", value)

    @builtins.property
    @jsii.member(jsii_name="controlPanelArn")
    def control_panel_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the control panel that includes the routing control.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-routingcontrol.html#cfn-route53recoverycontrol-routingcontrol-controlpanelarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPanelArn"))

    @control_panel_arn.setter
    def control_panel_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db775bed261704da54810f4add6edff185e7a29bc46bee5ba3ef86664ce9ab49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPanelArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnRoutingControlProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "cluster_arn": "clusterArn",
        "control_panel_arn": "controlPanelArn",
    },
)
class CfnRoutingControlProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        cluster_arn: typing.Optional[builtins.str] = None,
        control_panel_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnRoutingControl``.

        :param name: The name of the routing control. You can use any non-white space character in the name.
        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster that includes the routing control.
        :param control_panel_arn: The Amazon Resource Name (ARN) of the control panel that includes the routing control.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-routingcontrol.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
            
            cfn_routing_control_props = route53recoverycontrol.CfnRoutingControlProps(
                name="name",
            
                # the properties below are optional
                cluster_arn="clusterArn",
                control_panel_arn="controlPanelArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c657e353937e6878dd64fbaf8a098120810ef7e403787e0b032b41f39770e9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
            check_type(argname="argument control_panel_arn", value=control_panel_arn, expected_type=type_hints["control_panel_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if cluster_arn is not None:
            self._values["cluster_arn"] = cluster_arn
        if control_panel_arn is not None:
            self._values["control_panel_arn"] = control_panel_arn

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the routing control.

        You can use any non-white space character in the name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-routingcontrol.html#cfn-route53recoverycontrol-routingcontrol-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the cluster that includes the routing control.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-routingcontrol.html#cfn-route53recoverycontrol-routingcontrol-clusterarn
        '''
        result = self._values.get("cluster_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def control_panel_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the control panel that includes the routing control.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-routingcontrol.html#cfn-route53recoverycontrol-routingcontrol-controlpanelarn
        '''
        result = self._values.get("control_panel_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRoutingControlProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSafetyRule(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnSafetyRule",
):
    '''A CloudFormation ``AWS::Route53RecoveryControl::SafetyRule``.

    List the safety rules (the assertion rules and gating rules) that you've defined for the routing controls in a control panel.

    :cloudformationResource: AWS::Route53RecoveryControl::SafetyRule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
        
        cfn_safety_rule = route53recoverycontrol.CfnSafetyRule(self, "MyCfnSafetyRule",
            control_panel_arn="controlPanelArn",
            name="name",
            rule_config=route53recoverycontrol.CfnSafetyRule.RuleConfigProperty(
                inverted=False,
                threshold=123,
                type="type"
            ),
        
            # the properties below are optional
            assertion_rule=route53recoverycontrol.CfnSafetyRule.AssertionRuleProperty(
                asserted_controls=["assertedControls"],
                wait_period_ms=123
            ),
            gating_rule=route53recoverycontrol.CfnSafetyRule.GatingRuleProperty(
                gating_controls=["gatingControls"],
                target_controls=["targetControls"],
                wait_period_ms=123
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        control_panel_arn: builtins.str,
        name: builtins.str,
        rule_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSafetyRule.RuleConfigProperty", typing.Dict[builtins.str, typing.Any]]],
        assertion_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSafetyRule.AssertionRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        gating_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSafetyRule.GatingRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryControl::SafetyRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param control_panel_arn: The Amazon Resource Name (ARN) for the control panel.
        :param name: The name of the assertion rule. The name must be unique within a control panel. You can use any non-white space character in the name except the following: & > < ' (single quote) " (double quote) ; (semicolon)
        :param rule_config: The criteria that you set for specific assertion controls (routing controls) that designate how many control states must be ``ON`` as the result of a transaction. For example, if you have three assertion controls, you might specify ``ATLEAST 2`` for your rule configuration. This means that at least two assertion controls must be ``ON`` , so that at least two AWS Regions have traffic flowing to them.
        :param assertion_rule: An assertion rule enforces that, when you change a routing control state, that the criteria that you set in the rule configuration is met. Otherwise, the change to the routing control is not accepted. For example, the criteria might be that at least one routing control state is ``On`` after the transaction so that traffic continues to flow to at least one cell for the application. This ensures that you avoid a fail-open scenario.
        :param gating_rule: A gating rule verifies that a gating routing control or set of gating routing controls, evaluates as true, based on a rule configuration that you specify, which allows a set of routing control state changes to complete. For example, if you specify one gating routing control and you set the ``Type`` in the rule configuration to ``OR`` , that indicates that you must set the gating routing control to ``On`` for the rule to evaluate as true; that is, for the gating control "switch" to be "On". When you do that, then you can update the routing control states for the target routing controls that you specify in the gating rule.
        :param tags: The value for a tag.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2792f792194e27d36ea49b91eda5776a0fac531015579f4921fe12d1ebb7ad63)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSafetyRuleProps(
            control_panel_arn=control_panel_arn,
            name=name,
            rule_config=rule_config,
            assertion_rule=assertion_rule,
            gating_rule=gating_rule,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5296b5f1381f956fe5fd55d13243531279f35ffac70c16855865dbcc59b2eb)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d64dbac25402c8f6b932df4d4bea31b4e759a0baba5bab6bb87e4c8090e5231)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSafetyRuleArn")
    def attr_safety_rule_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the safety rule.

        :cloudformationAttribute: SafetyRuleArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSafetyRuleArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The deployment status of the safety rule.

        Status can be one of the following: PENDING, DEPLOYED, PENDING_DELETION.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="controlPanelArn")
    def control_panel_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the control panel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-controlpanelarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "controlPanelArn"))

    @control_panel_arn.setter
    def control_panel_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021112255b2eb5f23472ac8a7863bc6ad9ef6a09a4647ebe461e4e47618e7fd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPanelArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the assertion rule.

        The name must be unique within a control panel. You can use any non-white space character in the name except the following: & > < ' (single quote) " (double quote) ; (semicolon)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102b2bd96811a2784aa4b270e49f5d51a978dadb1e821a82e8540f5ec7c943d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="ruleConfig")
    def rule_config(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSafetyRule.RuleConfigProperty"]:
        '''The criteria that you set for specific assertion controls (routing controls) that designate how many control states must be ``ON`` as the result of a transaction.

        For example, if you have three assertion controls, you might specify ``ATLEAST 2`` for your rule configuration. This means that at least two assertion controls must be ``ON`` , so that at least two AWS Regions have traffic flowing to them.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-ruleconfig
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSafetyRule.RuleConfigProperty"], jsii.get(self, "ruleConfig"))

    @rule_config.setter
    def rule_config(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSafetyRule.RuleConfigProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45d80c0accfd58a6907744ca155e22eb25fafbc81de2f577c77b705f3fd5e976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleConfig", value)

    @builtins.property
    @jsii.member(jsii_name="assertionRule")
    def assertion_rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSafetyRule.AssertionRuleProperty"]]:
        '''An assertion rule enforces that, when you change a routing control state, that the criteria that you set in the rule configuration is met.

        Otherwise, the change to the routing control is not accepted. For example, the criteria might be that at least one routing control state is ``On`` after the transaction so that traffic continues to flow to at least one cell for the application. This ensures that you avoid a fail-open scenario.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-assertionrule
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSafetyRule.AssertionRuleProperty"]], jsii.get(self, "assertionRule"))

    @assertion_rule.setter
    def assertion_rule(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSafetyRule.AssertionRuleProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb255b85104de6fe5973752bd0d1ba7beb03f9516c7b70b8072fb1b68ff5453a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assertionRule", value)

    @builtins.property
    @jsii.member(jsii_name="gatingRule")
    def gating_rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSafetyRule.GatingRuleProperty"]]:
        '''A gating rule verifies that a gating routing control or set of gating routing controls, evaluates as true, based on a rule configuration that you specify, which allows a set of routing control state changes to complete.

        For example, if you specify one gating routing control and you set the ``Type`` in the rule configuration to ``OR`` , that indicates that you must set the gating routing control to ``On`` for the rule to evaluate as true; that is, for the gating control "switch" to be "On". When you do that, then you can update the routing control states for the target routing controls that you specify in the gating rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-gatingrule
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSafetyRule.GatingRuleProperty"]], jsii.get(self, "gatingRule"))

    @gating_rule.setter
    def gating_rule(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSafetyRule.GatingRuleProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327654f653d06a4f01bd68a010e441946e0dd837ef21487df2d91ded205439ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatingRule", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnSafetyRule.AssertionRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "asserted_controls": "assertedControls",
            "wait_period_ms": "waitPeriodMs",
        },
    )
    class AssertionRuleProperty:
        def __init__(
            self,
            *,
            asserted_controls: typing.Sequence[builtins.str],
            wait_period_ms: jsii.Number,
        ) -> None:
            '''An assertion rule enforces that, when you change a routing control state, that the criteria that you set in the rule configuration is met.

            Otherwise, the change to the routing control is not accepted. For example, the criteria might be that at least one routing control state is ``On`` after the transaction so that traffic continues to flow to at least one cell for the application. This ensures that you avoid a fail-open scenario.

            :param asserted_controls: The routing controls that are part of transactions that are evaluated to determine if a request to change a routing control state is allowed. For example, you might include three routing controls, one for each of three AWS Regions.
            :param wait_period_ms: An evaluation period, in milliseconds (ms), during which any request against the target routing controls will fail. This helps prevent "flapping" of state. The wait period is 5000 ms by default, but you can choose a custom value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-assertionrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
                
                assertion_rule_property = route53recoverycontrol.CfnSafetyRule.AssertionRuleProperty(
                    asserted_controls=["assertedControls"],
                    wait_period_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2437035b18cce7df78f73cc1f677703d9dd5b8ebf668d41e82f1b8aadabe87e)
                check_type(argname="argument asserted_controls", value=asserted_controls, expected_type=type_hints["asserted_controls"])
                check_type(argname="argument wait_period_ms", value=wait_period_ms, expected_type=type_hints["wait_period_ms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "asserted_controls": asserted_controls,
                "wait_period_ms": wait_period_ms,
            }

        @builtins.property
        def asserted_controls(self) -> typing.List[builtins.str]:
            '''The routing controls that are part of transactions that are evaluated to determine if a request to change a routing control state is allowed.

            For example, you might include three routing controls, one for each of three AWS Regions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-assertionrule.html#cfn-route53recoverycontrol-safetyrule-assertionrule-assertedcontrols
            '''
            result = self._values.get("asserted_controls")
            assert result is not None, "Required property 'asserted_controls' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def wait_period_ms(self) -> jsii.Number:
            '''An evaluation period, in milliseconds (ms), during which any request against the target routing controls will fail.

            This helps prevent "flapping" of state. The wait period is 5000 ms by default, but you can choose a custom value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-assertionrule.html#cfn-route53recoverycontrol-safetyrule-assertionrule-waitperiodms
            '''
            result = self._values.get("wait_period_ms")
            assert result is not None, "Required property 'wait_period_ms' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssertionRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnSafetyRule.GatingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "gating_controls": "gatingControls",
            "target_controls": "targetControls",
            "wait_period_ms": "waitPeriodMs",
        },
    )
    class GatingRuleProperty:
        def __init__(
            self,
            *,
            gating_controls: typing.Sequence[builtins.str],
            target_controls: typing.Sequence[builtins.str],
            wait_period_ms: jsii.Number,
        ) -> None:
            '''A gating rule verifies that a gating routing control or set of gating routing controls, evaluates as true, based on a rule configuration that you specify, which allows a set of routing control state changes to complete.

            For example, if you specify one gating routing control and you set the ``Type`` in the rule configuration to ``OR`` , that indicates that you must set the gating routing control to ``On`` for the rule to evaluate as true; that is, for the gating control "switch" to be "On". When you do that, then you can update the routing control states for the target routing controls that you specify in the gating rule.

            :param gating_controls: An array of gating routing control Amazon Resource Names (ARNs). For a simple "on/off" switch, specify the ARN for one routing control. The gating routing controls are evaluated by the rule configuration that you specify to determine if the target routing control states can be changed.
            :param target_controls: An array of target routing control Amazon Resource Names (ARNs) for which the states can only be updated if the rule configuration that you specify evaluates to true for the gating routing control. As a simple example, if you have a single gating control, it acts as an overall "on/off" switch for a set of target routing controls. You can use this to manually override automated failover, for example.
            :param wait_period_ms: An evaluation period, in milliseconds (ms), during which any request against the target routing controls will fail. This helps prevent "flapping" of state. The wait period is 5000 ms by default, but you can choose a custom value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-gatingrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
                
                gating_rule_property = route53recoverycontrol.CfnSafetyRule.GatingRuleProperty(
                    gating_controls=["gatingControls"],
                    target_controls=["targetControls"],
                    wait_period_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__508e6e999879d01a88a16f3d13a03524280b9052591c96ebdc9499600c3b6283)
                check_type(argname="argument gating_controls", value=gating_controls, expected_type=type_hints["gating_controls"])
                check_type(argname="argument target_controls", value=target_controls, expected_type=type_hints["target_controls"])
                check_type(argname="argument wait_period_ms", value=wait_period_ms, expected_type=type_hints["wait_period_ms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "gating_controls": gating_controls,
                "target_controls": target_controls,
                "wait_period_ms": wait_period_ms,
            }

        @builtins.property
        def gating_controls(self) -> typing.List[builtins.str]:
            '''An array of gating routing control Amazon Resource Names (ARNs).

            For a simple "on/off" switch, specify the ARN for one routing control. The gating routing controls are evaluated by the rule configuration that you specify to determine if the target routing control states can be changed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-gatingrule.html#cfn-route53recoverycontrol-safetyrule-gatingrule-gatingcontrols
            '''
            result = self._values.get("gating_controls")
            assert result is not None, "Required property 'gating_controls' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def target_controls(self) -> typing.List[builtins.str]:
            '''An array of target routing control Amazon Resource Names (ARNs) for which the states can only be updated if the rule configuration that you specify evaluates to true for the gating routing control.

            As a simple example, if you have a single gating control, it acts as an overall "on/off" switch for a set of target routing controls. You can use this to manually override automated failover, for example.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-gatingrule.html#cfn-route53recoverycontrol-safetyrule-gatingrule-targetcontrols
            '''
            result = self._values.get("target_controls")
            assert result is not None, "Required property 'target_controls' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def wait_period_ms(self) -> jsii.Number:
            '''An evaluation period, in milliseconds (ms), during which any request against the target routing controls will fail.

            This helps prevent "flapping" of state. The wait period is 5000 ms by default, but you can choose a custom value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-gatingrule.html#cfn-route53recoverycontrol-safetyrule-gatingrule-waitperiodms
            '''
            result = self._values.get("wait_period_ms")
            assert result is not None, "Required property 'wait_period_ms' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatingRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnSafetyRule.RuleConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "inverted": "inverted",
            "threshold": "threshold",
            "type": "type",
        },
    )
    class RuleConfigProperty:
        def __init__(
            self,
            *,
            inverted: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            threshold: jsii.Number,
            type: builtins.str,
        ) -> None:
            '''The rule configuration for an assertion rule.

            That is, the criteria that you set for specific assertion controls (routing controls) that specify how many control states must be ``ON`` after a transaction completes.

            :param inverted: Logical negation of the rule. If the rule would usually evaluate true, it's evaluated as false, and vice versa.
            :param threshold: The value of N, when you specify an ``ATLEAST`` rule type. That is, ``Threshold`` is the number of controls that must be set when you specify an ``ATLEAST`` type.
            :param type: A rule can be one of the following: ``ATLEAST`` , ``AND`` , or ``OR`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-ruleconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
                
                rule_config_property = route53recoverycontrol.CfnSafetyRule.RuleConfigProperty(
                    inverted=False,
                    threshold=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbc5781970d348a40215c56f7959c522d20fdf716cf0cf0e33968826ecc440e5)
                check_type(argname="argument inverted", value=inverted, expected_type=type_hints["inverted"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "inverted": inverted,
                "threshold": threshold,
                "type": type,
            }

        @builtins.property
        def inverted(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Logical negation of the rule.

            If the rule would usually evaluate true, it's evaluated as false, and vice versa.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-ruleconfig.html#cfn-route53recoverycontrol-safetyrule-ruleconfig-inverted
            '''
            result = self._values.get("inverted")
            assert result is not None, "Required property 'inverted' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def threshold(self) -> jsii.Number:
            '''The value of N, when you specify an ``ATLEAST`` rule type.

            That is, ``Threshold`` is the number of controls that must be set when you specify an ``ATLEAST`` type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-ruleconfig.html#cfn-route53recoverycontrol-safetyrule-ruleconfig-threshold
            '''
            result = self._values.get("threshold")
            assert result is not None, "Required property 'threshold' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''A rule can be one of the following: ``ATLEAST`` , ``AND`` , or ``OR`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-ruleconfig.html#cfn-route53recoverycontrol-safetyrule-ruleconfig-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53recoverycontrol.CfnSafetyRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "control_panel_arn": "controlPanelArn",
        "name": "name",
        "rule_config": "ruleConfig",
        "assertion_rule": "assertionRule",
        "gating_rule": "gatingRule",
        "tags": "tags",
    },
)
class CfnSafetyRuleProps:
    def __init__(
        self,
        *,
        control_panel_arn: builtins.str,
        name: builtins.str,
        rule_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSafetyRule.RuleConfigProperty, typing.Dict[builtins.str, typing.Any]]],
        assertion_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSafetyRule.AssertionRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        gating_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSafetyRule.GatingRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSafetyRule``.

        :param control_panel_arn: The Amazon Resource Name (ARN) for the control panel.
        :param name: The name of the assertion rule. The name must be unique within a control panel. You can use any non-white space character in the name except the following: & > < ' (single quote) " (double quote) ; (semicolon)
        :param rule_config: The criteria that you set for specific assertion controls (routing controls) that designate how many control states must be ``ON`` as the result of a transaction. For example, if you have three assertion controls, you might specify ``ATLEAST 2`` for your rule configuration. This means that at least two assertion controls must be ``ON`` , so that at least two AWS Regions have traffic flowing to them.
        :param assertion_rule: An assertion rule enforces that, when you change a routing control state, that the criteria that you set in the rule configuration is met. Otherwise, the change to the routing control is not accepted. For example, the criteria might be that at least one routing control state is ``On`` after the transaction so that traffic continues to flow to at least one cell for the application. This ensures that you avoid a fail-open scenario.
        :param gating_rule: A gating rule verifies that a gating routing control or set of gating routing controls, evaluates as true, based on a rule configuration that you specify, which allows a set of routing control state changes to complete. For example, if you specify one gating routing control and you set the ``Type`` in the rule configuration to ``OR`` , that indicates that you must set the gating routing control to ``On`` for the rule to evaluate as true; that is, for the gating control "switch" to be "On". When you do that, then you can update the routing control states for the target routing controls that you specify in the gating rule.
        :param tags: The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_route53recoverycontrol as route53recoverycontrol
            
            cfn_safety_rule_props = route53recoverycontrol.CfnSafetyRuleProps(
                control_panel_arn="controlPanelArn",
                name="name",
                rule_config=route53recoverycontrol.CfnSafetyRule.RuleConfigProperty(
                    inverted=False,
                    threshold=123,
                    type="type"
                ),
            
                # the properties below are optional
                assertion_rule=route53recoverycontrol.CfnSafetyRule.AssertionRuleProperty(
                    asserted_controls=["assertedControls"],
                    wait_period_ms=123
                ),
                gating_rule=route53recoverycontrol.CfnSafetyRule.GatingRuleProperty(
                    gating_controls=["gatingControls"],
                    target_controls=["targetControls"],
                    wait_period_ms=123
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ed7406d28fb41d649c050113dc241f9b1cee3b0ab925b89d3e1ccb4084ca01)
            check_type(argname="argument control_panel_arn", value=control_panel_arn, expected_type=type_hints["control_panel_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rule_config", value=rule_config, expected_type=type_hints["rule_config"])
            check_type(argname="argument assertion_rule", value=assertion_rule, expected_type=type_hints["assertion_rule"])
            check_type(argname="argument gating_rule", value=gating_rule, expected_type=type_hints["gating_rule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_panel_arn": control_panel_arn,
            "name": name,
            "rule_config": rule_config,
        }
        if assertion_rule is not None:
            self._values["assertion_rule"] = assertion_rule
        if gating_rule is not None:
            self._values["gating_rule"] = gating_rule
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def control_panel_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the control panel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-controlpanelarn
        '''
        result = self._values.get("control_panel_arn")
        assert result is not None, "Required property 'control_panel_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the assertion rule.

        The name must be unique within a control panel. You can use any non-white space character in the name except the following: & > < ' (single quote) " (double quote) ; (semicolon)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_config(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSafetyRule.RuleConfigProperty]:
        '''The criteria that you set for specific assertion controls (routing controls) that designate how many control states must be ``ON`` as the result of a transaction.

        For example, if you have three assertion controls, you might specify ``ATLEAST 2`` for your rule configuration. This means that at least two assertion controls must be ``ON`` , so that at least two AWS Regions have traffic flowing to them.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-ruleconfig
        '''
        result = self._values.get("rule_config")
        assert result is not None, "Required property 'rule_config' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSafetyRule.RuleConfigProperty], result)

    @builtins.property
    def assertion_rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSafetyRule.AssertionRuleProperty]]:
        '''An assertion rule enforces that, when you change a routing control state, that the criteria that you set in the rule configuration is met.

        Otherwise, the change to the routing control is not accepted. For example, the criteria might be that at least one routing control state is ``On`` after the transaction so that traffic continues to flow to at least one cell for the application. This ensures that you avoid a fail-open scenario.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-assertionrule
        '''
        result = self._values.get("assertion_rule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSafetyRule.AssertionRuleProperty]], result)

    @builtins.property
    def gating_rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSafetyRule.GatingRuleProperty]]:
        '''A gating rule verifies that a gating routing control or set of gating routing controls, evaluates as true, based on a rule configuration that you specify, which allows a set of routing control state changes to complete.

        For example, if you specify one gating routing control and you set the ``Type`` in the rule configuration to ``OR`` , that indicates that you must set the gating routing control to ``On`` for the rule to evaluate as true; that is, for the gating control "switch" to be "On". When you do that, then you can update the routing control states for the target routing controls that you specify in the gating rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-gatingrule
        '''
        result = self._values.get("gating_rule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSafetyRule.GatingRuleProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSafetyRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCluster",
    "CfnClusterProps",
    "CfnControlPanel",
    "CfnControlPanelProps",
    "CfnRoutingControl",
    "CfnRoutingControlProps",
    "CfnSafetyRule",
    "CfnSafetyRuleProps",
]

publication.publish()

def _typecheckingstub__4d41dfe645334ead300abc5a285bc74cb9134e11a757d1862ae8b874d1bbdf5e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    cluster_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnCluster.ClusterEndpointProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3b3ab44594c0393df1cd3695fd7d56988e7781e1dce09a861fad6eac938fd1(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a335bdfa86babdd8dce2f447f06bd098edc3d356c97fd0c26062020814c2212d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1536579d807b43a9677de858e54e0bc5ecee68e1ecf47d640fe7535b31e33ec(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnCluster.ClusterEndpointProperty, _aws_cdk_core_f4b25747.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97350e787b2f12863d7abe1387aa6089336ea03e7e0348c7051a08aea4371e6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1596b12cf4bea6d59f07a3f028e502e3b10c184f6015358541657920042a220d(
    *,
    endpoint: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bffa22753179417dc3e08f4b1d4b92bad5ba1fd54697710af4382185eb512c16(
    *,
    cluster_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnCluster.ClusterEndpointProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc903ab94203a44c3b7d1969e21b723c14ae1263489e63d0b6f0cdf50074b075(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    cluster_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5f35c38a208a577e5bac7a5ccf944c54263dabcf0e80ff5b590ddd3bd3629a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2c4f1843476d9001a3fde6e919baaf6bc72d6ea053d1c66cba46fb63e2f39b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e5515b4d95d4d1f301760f1cbd82681423d4e78fc4f9c62982f2a343eea74c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8896ae1e262b7522faeff4f2767e3d21e93ae2272dbf7c81d3230f6bf11b656(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67145e27b3d63359f442179e63bb2720fdba3a846f3d0ead17004de1c2eaee30(
    *,
    name: builtins.str,
    cluster_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6f7020ab2002b6006666264a5b3414ebd6f6a10dbe0e59ce6a1d5d717a517f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    cluster_arn: typing.Optional[builtins.str] = None,
    control_panel_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba95efc41cd53b3f35081c3b3a31d6dcb0008e5a8a5f72fa21d7a27466a4f4a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ae631f2b3950535658b83d0e8f727abe68886b6e605729d9838a46a631d4a9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0492331b2882b1c2254c26e64fb370c80338bb3db4911b7be1484ef72f463c2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abe8e890a08f84881f63be6edc6f80b2c46ad077bc0baf3cf3a8dd94f444d57(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db775bed261704da54810f4add6edff185e7a29bc46bee5ba3ef86664ce9ab49(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c657e353937e6878dd64fbaf8a098120810ef7e403787e0b032b41f39770e9(
    *,
    name: builtins.str,
    cluster_arn: typing.Optional[builtins.str] = None,
    control_panel_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2792f792194e27d36ea49b91eda5776a0fac531015579f4921fe12d1ebb7ad63(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    control_panel_arn: builtins.str,
    name: builtins.str,
    rule_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSafetyRule.RuleConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    assertion_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSafetyRule.AssertionRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gating_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSafetyRule.GatingRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5296b5f1381f956fe5fd55d13243531279f35ffac70c16855865dbcc59b2eb(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d64dbac25402c8f6b932df4d4bea31b4e759a0baba5bab6bb87e4c8090e5231(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021112255b2eb5f23472ac8a7863bc6ad9ef6a09a4647ebe461e4e47618e7fd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102b2bd96811a2784aa4b270e49f5d51a978dadb1e821a82e8540f5ec7c943d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d80c0accfd58a6907744ca155e22eb25fafbc81de2f577c77b705f3fd5e976(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSafetyRule.RuleConfigProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb255b85104de6fe5973752bd0d1ba7beb03f9516c7b70b8072fb1b68ff5453a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSafetyRule.AssertionRuleProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327654f653d06a4f01bd68a010e441946e0dd837ef21487df2d91ded205439ec(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSafetyRule.GatingRuleProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2437035b18cce7df78f73cc1f677703d9dd5b8ebf668d41e82f1b8aadabe87e(
    *,
    asserted_controls: typing.Sequence[builtins.str],
    wait_period_ms: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508e6e999879d01a88a16f3d13a03524280b9052591c96ebdc9499600c3b6283(
    *,
    gating_controls: typing.Sequence[builtins.str],
    target_controls: typing.Sequence[builtins.str],
    wait_period_ms: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc5781970d348a40215c56f7959c522d20fdf716cf0cf0e33968826ecc440e5(
    *,
    inverted: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    threshold: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ed7406d28fb41d649c050113dc241f9b1cee3b0ab925b89d3e1ccb4084ca01(
    *,
    control_panel_arn: builtins.str,
    name: builtins.str,
    rule_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSafetyRule.RuleConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    assertion_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSafetyRule.AssertionRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gating_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSafetyRule.GatingRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
