'''
# AWS::Route53RecoveryControl Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as route53recoverycontrol
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

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnCluster(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53recoverycontrol.CfnCluster",
):
    '''A CloudFormation ``AWS::Route53RecoveryControl::Cluster``.

    Returns an array of all the clusters in an account.

    :cloudformationResource: AWS::Route53RecoveryControl::Cluster
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53recoverycontrol as route53recoverycontrol
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        cluster_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnCluster.ClusterEndpointProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryControl::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster_endpoints: ``AWS::Route53RecoveryControl::Cluster.ClusterEndpoints``.
        :param name: Name of the cluster. You can use any non-white space character in the name.
        :param tags: The value for a tag.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8194fc4bec4689429b364858a6051f88d75f12377a662b4a66fd6468f3244d60)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnClusterProps(
            cluster_endpoints=cluster_endpoints, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e7860b4bf4f46e7bc86f1449dda79cfea9935fb2bf1115471aab7041724f49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e62465f401c60247949cc54fbd7431f932427ddf713d0e70cbbfa5e00edf0b65)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html#cfn-route53recoverycontrol-cluster-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoints")
    def cluster_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCluster.ClusterEndpointProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Route53RecoveryControl::Cluster.ClusterEndpoints``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html#cfn-route53recoverycontrol-cluster-clusterendpoints
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCluster.ClusterEndpointProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "clusterEndpoints"))

    @cluster_endpoints.setter
    def cluster_endpoints(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCluster.ClusterEndpointProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87824c3d6a1b3dc81b2c5df001aeef9a92ec67c38f3a9aa38d106f68ca8fe46d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edcf07eddd3dcbea69ed3d54d5193daa5c99ba9fcb04fe003631c720571f0e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_route53recoverycontrol.CfnCluster.ClusterEndpointProperty",
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
                from monocdk import aws_route53recoverycontrol as route53recoverycontrol
                
                cluster_endpoint_property = route53recoverycontrol.CfnCluster.ClusterEndpointProperty(
                    endpoint="endpoint",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f046cc891ddf0914da1661444adc896915e54a7141e014931a70c8df2136aff)
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
    jsii_type="monocdk.aws_route53recoverycontrol.CfnClusterProps",
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
        cluster_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCluster.ClusterEndpointProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_route53recoverycontrol as route53recoverycontrol
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0518efe35e9137eec9f4d8b42e5562081438a9c07329fa09ca5891c91581b32)
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
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCluster.ClusterEndpointProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Route53RecoveryControl::Cluster.ClusterEndpoints``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html#cfn-route53recoverycontrol-cluster-clusterendpoints
        '''
        result = self._values.get("cluster_endpoints")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCluster.ClusterEndpointProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the cluster.

        You can use any non-white space character in the name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html#cfn-route53recoverycontrol-cluster-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-cluster.html#cfn-route53recoverycontrol-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnControlPanel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53recoverycontrol.CfnControlPanel",
):
    '''A CloudFormation ``AWS::Route53RecoveryControl::ControlPanel``.

    Creates a new control panel. A control panel represents a group of routing controls that can be changed together in a single transaction. You can use a control panel to centrally view the operational status of applications across your organization, and trigger multi-app failovers in a single transaction, for example, to fail over an Availability Zone or AWS Region .

    :cloudformationResource: AWS::Route53RecoveryControl::ControlPanel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-controlpanel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53recoverycontrol as route53recoverycontrol
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        cluster_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryControl::ControlPanel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the control panel. You can use any non-white space character in the name.
        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster for the control panel.
        :param tags: The value for a tag.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0a5fc7cfeef6c14a296c3d91e720490a1b09c49fa4c48cd164bf145e689ee9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnControlPanelProps(name=name, cluster_arn=cluster_arn, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31bdeea3a15fc334f618a55fbc691e28fd4b8dadbf043f947e6fe56d52ce1f73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b864cf80ba0ee78b416d23d940b7defb568b32a127e1b6772078575d157666b)
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
    def attr_default_control_panel(self) -> _IResolvable_a771d0ef:
        '''The boolean flag that is set to true for the default control panel in the cluster.

        :cloudformationAttribute: DefaultControlPanel
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrDefaultControlPanel"))

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
    def tags(self) -> _TagManager_0b7ab120:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-controlpanel.html#cfn-route53recoverycontrol-controlpanel-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e9582b562a0e674f84210cc6e630426825f6ba2fd39cb2c06f76b9783b20c59e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1217d07b2c4622a78e341f69dc4a0c618df2985d8f2138efc2c9591e772c41d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53recoverycontrol.CfnControlPanelProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "cluster_arn": "clusterArn", "tags": "tags"},
)
class CfnControlPanelProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        cluster_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_route53recoverycontrol as route53recoverycontrol
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__b89ba378f4b0eaf94516f6fc3568f75602d7c1ee963901e56c6259098e479efb)
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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-controlpanel.html#cfn-route53recoverycontrol-controlpanel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnControlPanelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRoutingControl(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53recoverycontrol.CfnRoutingControl",
):
    '''A CloudFormation ``AWS::Route53RecoveryControl::RoutingControl``.

    Defines a routing control. To get or update the routing control state, see the Recovery Cluster (data plane) API actions for Amazon Route 53 Application Recovery Controller.

    :cloudformationResource: AWS::Route53RecoveryControl::RoutingControl
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-routingcontrol.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53recoverycontrol as route53recoverycontrol
        
        cfn_routing_control = route53recoverycontrol.CfnRoutingControl(self, "MyCfnRoutingControl",
            name="name",
        
            # the properties below are optional
            cluster_arn="clusterArn",
            control_panel_arn="controlPanelArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
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
            type_hints = typing.get_type_hints(_typecheckingstub__0943d76165f42094a79eb2ed53e97650ca29dce7f26d895cb65d191ddc1b98f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRoutingControlProps(
            name=name, cluster_arn=cluster_arn, control_panel_arn=control_panel_arn
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229dc69acfa4b0c2e306f5e1edd9e4ee02e7a81b3b990358dfa188485446b0e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6aae9d87f66cbd1cd60a57335fdf0e47f1c5efa36d8ba9cef82267b0917878e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49167ffb7c50155fa9fbd947209485d92a1fb4e5abe88fd1660185616d6e6cf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__448ed62b1e99895869451ea04fcf1d7f3aa038d0d44563b385a6b3724f18ad7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ae0eacd1e1eb3b665f437166e4120e3f9abda6c79443a3c1743473aa29bacee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPanelArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53recoverycontrol.CfnRoutingControlProps",
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
            from monocdk import aws_route53recoverycontrol as route53recoverycontrol
            
            cfn_routing_control_props = route53recoverycontrol.CfnRoutingControlProps(
                name="name",
            
                # the properties below are optional
                cluster_arn="clusterArn",
                control_panel_arn="controlPanelArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43681b1d0ae625fab245899e4baaa9fc05007d9b0fd66aba23547084e97cd1a1)
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


@jsii.implements(_IInspectable_82c04a63)
class CfnSafetyRule(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53recoverycontrol.CfnSafetyRule",
):
    '''A CloudFormation ``AWS::Route53RecoveryControl::SafetyRule``.

    List the safety rules (the assertion rules and gating rules) that you've defined for the routing controls in a control panel.

    :cloudformationResource: AWS::Route53RecoveryControl::SafetyRule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53recoverycontrol as route53recoverycontrol
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        control_panel_arn: builtins.str,
        name: builtins.str,
        rule_config: typing.Union[typing.Union["CfnSafetyRule.RuleConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        assertion_rule: typing.Optional[typing.Union[typing.Union["CfnSafetyRule.AssertionRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        gating_rule: typing.Optional[typing.Union[typing.Union["CfnSafetyRule.GatingRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__54dc945af59e616d74b14c9d79dfd2e2427521a368a0320fee1f896a6df64371)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59fbc6026637632141fa59f54516f7fa43a2bec34d34f9a98fa615d62c883b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50cd39c284d083fe99669292c11f52e918ab1d7b2b8c639131076abaaba33c15)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__03baafd37bb00b7656049c97931770909dc50362db530378e93ce1f66fa7adb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8da3ac05c0affe081dc72b273259bde44a7e03d8378172a525dbb709b7b1f68d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="ruleConfig")
    def rule_config(
        self,
    ) -> typing.Union["CfnSafetyRule.RuleConfigProperty", _IResolvable_a771d0ef]:
        '''The criteria that you set for specific assertion controls (routing controls) that designate how many control states must be ``ON`` as the result of a transaction.

        For example, if you have three assertion controls, you might specify ``ATLEAST 2`` for your rule configuration. This means that at least two assertion controls must be ``ON`` , so that at least two AWS Regions have traffic flowing to them.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-ruleconfig
        '''
        return typing.cast(typing.Union["CfnSafetyRule.RuleConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "ruleConfig"))

    @rule_config.setter
    def rule_config(
        self,
        value: typing.Union["CfnSafetyRule.RuleConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce29abc0be560964b44cd8c690196df2e0c3579789d5b25f49a2d1e393cd689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleConfig", value)

    @builtins.property
    @jsii.member(jsii_name="assertionRule")
    def assertion_rule(
        self,
    ) -> typing.Optional[typing.Union["CfnSafetyRule.AssertionRuleProperty", _IResolvable_a771d0ef]]:
        '''An assertion rule enforces that, when you change a routing control state, that the criteria that you set in the rule configuration is met.

        Otherwise, the change to the routing control is not accepted. For example, the criteria might be that at least one routing control state is ``On`` after the transaction so that traffic continues to flow to at least one cell for the application. This ensures that you avoid a fail-open scenario.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-assertionrule
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSafetyRule.AssertionRuleProperty", _IResolvable_a771d0ef]], jsii.get(self, "assertionRule"))

    @assertion_rule.setter
    def assertion_rule(
        self,
        value: typing.Optional[typing.Union["CfnSafetyRule.AssertionRuleProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19096c3bd38249c13987acaca982b07671041d44e255a1cb758865dd657128a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assertionRule", value)

    @builtins.property
    @jsii.member(jsii_name="gatingRule")
    def gating_rule(
        self,
    ) -> typing.Optional[typing.Union["CfnSafetyRule.GatingRuleProperty", _IResolvable_a771d0ef]]:
        '''A gating rule verifies that a gating routing control or set of gating routing controls, evaluates as true, based on a rule configuration that you specify, which allows a set of routing control state changes to complete.

        For example, if you specify one gating routing control and you set the ``Type`` in the rule configuration to ``OR`` , that indicates that you must set the gating routing control to ``On`` for the rule to evaluate as true; that is, for the gating control "switch" to be "On". When you do that, then you can update the routing control states for the target routing controls that you specify in the gating rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-gatingrule
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSafetyRule.GatingRuleProperty", _IResolvable_a771d0ef]], jsii.get(self, "gatingRule"))

    @gating_rule.setter
    def gating_rule(
        self,
        value: typing.Optional[typing.Union["CfnSafetyRule.GatingRuleProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d94715ba919cbd7f641edd85e7e8564d4998b484ca66afdbacb2c4de7d5c3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatingRule", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_route53recoverycontrol.CfnSafetyRule.AssertionRuleProperty",
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
                from monocdk import aws_route53recoverycontrol as route53recoverycontrol
                
                assertion_rule_property = route53recoverycontrol.CfnSafetyRule.AssertionRuleProperty(
                    asserted_controls=["assertedControls"],
                    wait_period_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df831c5a594ab7e9f2b957bd66b497c43e2bd3199a16bfda82ad95bf39160844)
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
        jsii_type="monocdk.aws_route53recoverycontrol.CfnSafetyRule.GatingRuleProperty",
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
                from monocdk import aws_route53recoverycontrol as route53recoverycontrol
                
                gating_rule_property = route53recoverycontrol.CfnSafetyRule.GatingRuleProperty(
                    gating_controls=["gatingControls"],
                    target_controls=["targetControls"],
                    wait_period_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6dd2de1d95b96b2d276999e8947ae96b0e5c10c9ef8e1722e22634ab428b9b01)
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
        jsii_type="monocdk.aws_route53recoverycontrol.CfnSafetyRule.RuleConfigProperty",
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
            inverted: typing.Union[builtins.bool, _IResolvable_a771d0ef],
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
                from monocdk import aws_route53recoverycontrol as route53recoverycontrol
                
                rule_config_property = route53recoverycontrol.CfnSafetyRule.RuleConfigProperty(
                    inverted=False,
                    threshold=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b0315a027e6f21ec9ad2b34a5fef804f8ccaec457ac3dd09c71a4328ced6355)
                check_type(argname="argument inverted", value=inverted, expected_type=type_hints["inverted"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "inverted": inverted,
                "threshold": threshold,
                "type": type,
            }

        @builtins.property
        def inverted(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Logical negation of the rule.

            If the rule would usually evaluate true, it's evaluated as false, and vice versa.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoverycontrol-safetyrule-ruleconfig.html#cfn-route53recoverycontrol-safetyrule-ruleconfig-inverted
            '''
            result = self._values.get("inverted")
            assert result is not None, "Required property 'inverted' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

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
    jsii_type="monocdk.aws_route53recoverycontrol.CfnSafetyRuleProps",
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
        rule_config: typing.Union[typing.Union[CfnSafetyRule.RuleConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        assertion_rule: typing.Optional[typing.Union[typing.Union[CfnSafetyRule.AssertionRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        gating_rule: typing.Optional[typing.Union[typing.Union[CfnSafetyRule.GatingRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_route53recoverycontrol as route53recoverycontrol
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba84944287cff783920a4c2fe8172a3ebe4eb9b2e17e2f83c57ea25805c528c2)
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
    ) -> typing.Union[CfnSafetyRule.RuleConfigProperty, _IResolvable_a771d0ef]:
        '''The criteria that you set for specific assertion controls (routing controls) that designate how many control states must be ``ON`` as the result of a transaction.

        For example, if you have three assertion controls, you might specify ``ATLEAST 2`` for your rule configuration. This means that at least two assertion controls must be ``ON`` , so that at least two AWS Regions have traffic flowing to them.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-ruleconfig
        '''
        result = self._values.get("rule_config")
        assert result is not None, "Required property 'rule_config' is missing"
        return typing.cast(typing.Union[CfnSafetyRule.RuleConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def assertion_rule(
        self,
    ) -> typing.Optional[typing.Union[CfnSafetyRule.AssertionRuleProperty, _IResolvable_a771d0ef]]:
        '''An assertion rule enforces that, when you change a routing control state, that the criteria that you set in the rule configuration is met.

        Otherwise, the change to the routing control is not accepted. For example, the criteria might be that at least one routing control state is ``On`` after the transaction so that traffic continues to flow to at least one cell for the application. This ensures that you avoid a fail-open scenario.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-assertionrule
        '''
        result = self._values.get("assertion_rule")
        return typing.cast(typing.Optional[typing.Union[CfnSafetyRule.AssertionRuleProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def gating_rule(
        self,
    ) -> typing.Optional[typing.Union[CfnSafetyRule.GatingRuleProperty, _IResolvable_a771d0ef]]:
        '''A gating rule verifies that a gating routing control or set of gating routing controls, evaluates as true, based on a rule configuration that you specify, which allows a set of routing control state changes to complete.

        For example, if you specify one gating routing control and you set the ``Type`` in the rule configuration to ``OR`` , that indicates that you must set the gating routing control to ``On`` for the rule to evaluate as true; that is, for the gating control "switch" to be "On". When you do that, then you can update the routing control states for the target routing controls that you specify in the gating rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-gatingrule
        '''
        result = self._values.get("gating_rule")
        return typing.cast(typing.Optional[typing.Union[CfnSafetyRule.GatingRuleProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The value for a tag.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoverycontrol-safetyrule.html#cfn-route53recoverycontrol-safetyrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

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

def _typecheckingstub__8194fc4bec4689429b364858a6051f88d75f12377a662b4a66fd6468f3244d60(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    cluster_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCluster.ClusterEndpointProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e7860b4bf4f46e7bc86f1449dda79cfea9935fb2bf1115471aab7041724f49(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62465f401c60247949cc54fbd7431f932427ddf713d0e70cbbfa5e00edf0b65(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87824c3d6a1b3dc81b2c5df001aeef9a92ec67c38f3a9aa38d106f68ca8fe46d(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCluster.ClusterEndpointProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edcf07eddd3dcbea69ed3d54d5193daa5c99ba9fcb04fe003631c720571f0e8c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f046cc891ddf0914da1661444adc896915e54a7141e014931a70c8df2136aff(
    *,
    endpoint: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0518efe35e9137eec9f4d8b42e5562081438a9c07329fa09ca5891c91581b32(
    *,
    cluster_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCluster.ClusterEndpointProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0a5fc7cfeef6c14a296c3d91e720490a1b09c49fa4c48cd164bf145e689ee9(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    cluster_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bdeea3a15fc334f618a55fbc691e28fd4b8dadbf043f947e6fe56d52ce1f73(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b864cf80ba0ee78b416d23d940b7defb568b32a127e1b6772078575d157666b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9582b562a0e674f84210cc6e630426825f6ba2fd39cb2c06f76b9783b20c59e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1217d07b2c4622a78e341f69dc4a0c618df2985d8f2138efc2c9591e772c41d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89ba378f4b0eaf94516f6fc3568f75602d7c1ee963901e56c6259098e479efb(
    *,
    name: builtins.str,
    cluster_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0943d76165f42094a79eb2ed53e97650ca29dce7f26d895cb65d191ddc1b98f8(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    cluster_arn: typing.Optional[builtins.str] = None,
    control_panel_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229dc69acfa4b0c2e306f5e1edd9e4ee02e7a81b3b990358dfa188485446b0e7(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6aae9d87f66cbd1cd60a57335fdf0e47f1c5efa36d8ba9cef82267b0917878e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49167ffb7c50155fa9fbd947209485d92a1fb4e5abe88fd1660185616d6e6cf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448ed62b1e99895869451ea04fcf1d7f3aa038d0d44563b385a6b3724f18ad7b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae0eacd1e1eb3b665f437166e4120e3f9abda6c79443a3c1743473aa29bacee(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43681b1d0ae625fab245899e4baaa9fc05007d9b0fd66aba23547084e97cd1a1(
    *,
    name: builtins.str,
    cluster_arn: typing.Optional[builtins.str] = None,
    control_panel_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54dc945af59e616d74b14c9d79dfd2e2427521a368a0320fee1f896a6df64371(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    control_panel_arn: builtins.str,
    name: builtins.str,
    rule_config: typing.Union[typing.Union[CfnSafetyRule.RuleConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    assertion_rule: typing.Optional[typing.Union[typing.Union[CfnSafetyRule.AssertionRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    gating_rule: typing.Optional[typing.Union[typing.Union[CfnSafetyRule.GatingRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59fbc6026637632141fa59f54516f7fa43a2bec34d34f9a98fa615d62c883b2(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50cd39c284d083fe99669292c11f52e918ab1d7b2b8c639131076abaaba33c15(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03baafd37bb00b7656049c97931770909dc50362db530378e93ce1f66fa7adb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da3ac05c0affe081dc72b273259bde44a7e03d8378172a525dbb709b7b1f68d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce29abc0be560964b44cd8c690196df2e0c3579789d5b25f49a2d1e393cd689(
    value: typing.Union[CfnSafetyRule.RuleConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19096c3bd38249c13987acaca982b07671041d44e255a1cb758865dd657128a7(
    value: typing.Optional[typing.Union[CfnSafetyRule.AssertionRuleProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d94715ba919cbd7f641edd85e7e8564d4998b484ca66afdbacb2c4de7d5c3b4(
    value: typing.Optional[typing.Union[CfnSafetyRule.GatingRuleProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df831c5a594ab7e9f2b957bd66b497c43e2bd3199a16bfda82ad95bf39160844(
    *,
    asserted_controls: typing.Sequence[builtins.str],
    wait_period_ms: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd2de1d95b96b2d276999e8947ae96b0e5c10c9ef8e1722e22634ab428b9b01(
    *,
    gating_controls: typing.Sequence[builtins.str],
    target_controls: typing.Sequence[builtins.str],
    wait_period_ms: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0315a027e6f21ec9ad2b34a5fef804f8ccaec457ac3dd09c71a4328ced6355(
    *,
    inverted: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    threshold: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba84944287cff783920a4c2fe8172a3ebe4eb9b2e17e2f83c57ea25805c528c2(
    *,
    control_panel_arn: builtins.str,
    name: builtins.str,
    rule_config: typing.Union[typing.Union[CfnSafetyRule.RuleConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    assertion_rule: typing.Optional[typing.Union[typing.Union[CfnSafetyRule.AssertionRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    gating_rule: typing.Optional[typing.Union[typing.Union[CfnSafetyRule.GatingRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
