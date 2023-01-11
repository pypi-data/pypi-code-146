'''
# AWS::CE Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_ce as ce
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for CE construct libraries](https://constructs.dev/search?q=ce)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::CE resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CE.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::CE](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CE.html).

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
class CfnAnomalyMonitor(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ce.CfnAnomalyMonitor",
):
    '''A CloudFormation ``AWS::CE::AnomalyMonitor``.

    The ``AWS::CE::AnomalyMonitor`` resource is a Cost Explorer resource type that continuously inspects your account's cost data for anomalies, based on ``MonitorType`` and ``MonitorSpecification`` . The content consists of detailed metadata and the current status of the monitor object.

    :cloudformationResource: AWS::CE::AnomalyMonitor
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ce as ce
        
        cfn_anomaly_monitor = ce.CfnAnomalyMonitor(self, "MyCfnAnomalyMonitor",
            monitor_name="monitorName",
            monitor_type="monitorType",
        
            # the properties below are optional
            monitor_dimension="monitorDimension",
            monitor_specification="monitorSpecification",
            resource_tags=[ce.CfnAnomalyMonitor.ResourceTagProperty(
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
        monitor_name: builtins.str,
        monitor_type: builtins.str,
        monitor_dimension: typing.Optional[builtins.str] = None,
        monitor_specification: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnAnomalyMonitor.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CE::AnomalyMonitor``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param monitor_name: The name of the monitor.
        :param monitor_type: The possible type values.
        :param monitor_dimension: The dimensions to evaluate.
        :param monitor_specification: The array of ``MonitorSpecification`` in JSON array format. For instance, you can use ``MonitorSpecification`` to specify a tag, Cost Category, or linked account for your custom anomaly monitor. For further information, see the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#aws-resource-ce-anomalymonitor--examples>`_ section of this page.
        :param resource_tags: ``AWS::CE::AnomalyMonitor.ResourceTags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f53317433755ca5b4636716c3a33228f79704406037a9d362081e936156090)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAnomalyMonitorProps(
            monitor_name=monitor_name,
            monitor_type=monitor_type,
            monitor_dimension=monitor_dimension,
            monitor_specification=monitor_specification,
            resource_tags=resource_tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7910f5202051e9857c176fb6e796fd30daa32e4d3009569527e143c25728e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20bcd972f71eb76cebcb46e8a787d3a4d3f06e49e7f6476245bc3a5f41618692)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDate")
    def attr_creation_date(self) -> builtins.str:
        '''The date when the monitor was created.

        :cloudformationAttribute: CreationDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDate"))

    @builtins.property
    @jsii.member(jsii_name="attrDimensionalValueCount")
    def attr_dimensional_value_count(self) -> jsii.Number:
        '''The value for evaluated dimensions.

        :cloudformationAttribute: DimensionalValueCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrDimensionalValueCount"))

    @builtins.property
    @jsii.member(jsii_name="attrLastEvaluatedDate")
    def attr_last_evaluated_date(self) -> builtins.str:
        '''The date when the monitor last evaluated for anomalies.

        :cloudformationAttribute: LastEvaluatedDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastEvaluatedDate"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedDate")
    def attr_last_updated_date(self) -> builtins.str:
        '''The date when the monitor was last updated.

        :cloudformationAttribute: LastUpdatedDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedDate"))

    @builtins.property
    @jsii.member(jsii_name="attrMonitorArn")
    def attr_monitor_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) value for the monitor.

        :cloudformationAttribute: MonitorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMonitorArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="monitorName")
    def monitor_name(self) -> builtins.str:
        '''The name of the monitor.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitorname
        '''
        return typing.cast(builtins.str, jsii.get(self, "monitorName"))

    @monitor_name.setter
    def monitor_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cbde7a7bb043805da5df3b9478d315e92fcdbd58e74209ae325e371a7255b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorName", value)

    @builtins.property
    @jsii.member(jsii_name="monitorType")
    def monitor_type(self) -> builtins.str:
        '''The possible type values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitortype
        '''
        return typing.cast(builtins.str, jsii.get(self, "monitorType"))

    @monitor_type.setter
    def monitor_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0543f46498df833238e235679c5d5a047e6a1fea42dbdf29bae8763e20cb62ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorType", value)

    @builtins.property
    @jsii.member(jsii_name="monitorDimension")
    def monitor_dimension(self) -> typing.Optional[builtins.str]:
        '''The dimensions to evaluate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitordimension
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorDimension"))

    @monitor_dimension.setter
    def monitor_dimension(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff79309b9fb6b6e81e1cef9c2f05e756e614cb69a9df633252f918737b3b6acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorDimension", value)

    @builtins.property
    @jsii.member(jsii_name="monitorSpecification")
    def monitor_specification(self) -> typing.Optional[builtins.str]:
        '''The array of ``MonitorSpecification`` in JSON array format.

        For instance, you can use ``MonitorSpecification`` to specify a tag, Cost Category, or linked account for your custom anomaly monitor. For further information, see the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#aws-resource-ce-anomalymonitor--examples>`_ section of this page.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitorspecification
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorSpecification"))

    @monitor_specification.setter
    def monitor_specification(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a14c2af48924fe63344517cb1aca26d5a773c40aa3d27b8d876b25f7f58d12e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnAnomalyMonitor.ResourceTagProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''``AWS::CE::AnomalyMonitor.ResourceTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-resourcetags
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnAnomalyMonitor.ResourceTagProperty", _aws_cdk_core_f4b25747.IResolvable]]]], jsii.get(self, "resourceTags"))

    @resource_tags.setter
    def resource_tags(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnAnomalyMonitor.ResourceTagProperty", _aws_cdk_core_f4b25747.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dda64289d8b76f3867cd1d74f3d49813928e5d2782ae187eb671b9c72208b562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTags", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ce.CfnAnomalyMonitor.ResourceTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ResourceTagProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''The tag structure that contains a tag key and value.

            .. epigraph::

               Tagging is supported only for the following Cost Explorer resource types: ```AnomalyMonitor`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalyMonitor.html>`_ , ```AnomalySubscription`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalySubscription.html>`_ , ```CostCategory`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_CostCategory.html>`_ .

            :param key: The key that's associated with the tag.
            :param value: The value that's associated with the tag.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalymonitor-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ce as ce
                
                resource_tag_property = ce.CfnAnomalyMonitor.ResourceTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d67b8063ac428384e77769e71adbffee848cc2a9f580eb0e6e4499e90e822d24)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The key that's associated with the tag.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalymonitor-resourcetag.html#cfn-ce-anomalymonitor-resourcetag-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value that's associated with the tag.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalymonitor-resourcetag.html#cfn-ce-anomalymonitor-resourcetag-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ce.CfnAnomalyMonitorProps",
    jsii_struct_bases=[],
    name_mapping={
        "monitor_name": "monitorName",
        "monitor_type": "monitorType",
        "monitor_dimension": "monitorDimension",
        "monitor_specification": "monitorSpecification",
        "resource_tags": "resourceTags",
    },
)
class CfnAnomalyMonitorProps:
    def __init__(
        self,
        *,
        monitor_name: builtins.str,
        monitor_type: builtins.str,
        monitor_dimension: typing.Optional[builtins.str] = None,
        monitor_specification: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnAnomalyMonitor.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAnomalyMonitor``.

        :param monitor_name: The name of the monitor.
        :param monitor_type: The possible type values.
        :param monitor_dimension: The dimensions to evaluate.
        :param monitor_specification: The array of ``MonitorSpecification`` in JSON array format. For instance, you can use ``MonitorSpecification`` to specify a tag, Cost Category, or linked account for your custom anomaly monitor. For further information, see the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#aws-resource-ce-anomalymonitor--examples>`_ section of this page.
        :param resource_tags: ``AWS::CE::AnomalyMonitor.ResourceTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ce as ce
            
            cfn_anomaly_monitor_props = ce.CfnAnomalyMonitorProps(
                monitor_name="monitorName",
                monitor_type="monitorType",
            
                # the properties below are optional
                monitor_dimension="monitorDimension",
                monitor_specification="monitorSpecification",
                resource_tags=[ce.CfnAnomalyMonitor.ResourceTagProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09743b43a68e2cab7b28ba5c62a3dad9b55e741f161771af3d08889e3ea16a0)
            check_type(argname="argument monitor_name", value=monitor_name, expected_type=type_hints["monitor_name"])
            check_type(argname="argument monitor_type", value=monitor_type, expected_type=type_hints["monitor_type"])
            check_type(argname="argument monitor_dimension", value=monitor_dimension, expected_type=type_hints["monitor_dimension"])
            check_type(argname="argument monitor_specification", value=monitor_specification, expected_type=type_hints["monitor_specification"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "monitor_name": monitor_name,
            "monitor_type": monitor_type,
        }
        if monitor_dimension is not None:
            self._values["monitor_dimension"] = monitor_dimension
        if monitor_specification is not None:
            self._values["monitor_specification"] = monitor_specification
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags

    @builtins.property
    def monitor_name(self) -> builtins.str:
        '''The name of the monitor.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitorname
        '''
        result = self._values.get("monitor_name")
        assert result is not None, "Required property 'monitor_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def monitor_type(self) -> builtins.str:
        '''The possible type values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitortype
        '''
        result = self._values.get("monitor_type")
        assert result is not None, "Required property 'monitor_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def monitor_dimension(self) -> typing.Optional[builtins.str]:
        '''The dimensions to evaluate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitordimension
        '''
        result = self._values.get("monitor_dimension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_specification(self) -> typing.Optional[builtins.str]:
        '''The array of ``MonitorSpecification`` in JSON array format.

        For instance, you can use ``MonitorSpecification`` to specify a tag, Cost Category, or linked account for your custom anomaly monitor. For further information, see the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#aws-resource-ce-anomalymonitor--examples>`_ section of this page.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitorspecification
        '''
        result = self._values.get("monitor_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnAnomalyMonitor.ResourceTagProperty, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''``AWS::CE::AnomalyMonitor.ResourceTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnAnomalyMonitor.ResourceTagProperty, _aws_cdk_core_f4b25747.IResolvable]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnomalyMonitorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAnomalySubscription(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ce.CfnAnomalySubscription",
):
    '''A CloudFormation ``AWS::CE::AnomalySubscription``.

    The ``AWS::CE::AnomalySubscription`` resource is a Cost Explorer resource type that associates a monitor, threshold, and list of subscribers. It delivers notifications about anomalies detected by a monitor that exceeds a threshold. The content consists of the detailed metadata and the current status of the ``AnomalySubscription`` object.

    :cloudformationResource: AWS::CE::AnomalySubscription
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ce as ce
        
        cfn_anomaly_subscription = ce.CfnAnomalySubscription(self, "MyCfnAnomalySubscription",
            frequency="frequency",
            monitor_arn_list=["monitorArnList"],
            subscribers=[ce.CfnAnomalySubscription.SubscriberProperty(
                address="address",
                type="type",
        
                # the properties below are optional
                status="status"
            )],
            subscription_name="subscriptionName",
            threshold=123,
        
            # the properties below are optional
            resource_tags=[ce.CfnAnomalySubscription.ResourceTagProperty(
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
        frequency: builtins.str,
        monitor_arn_list: typing.Sequence[builtins.str],
        subscribers: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAnomalySubscription.SubscriberProperty", typing.Dict[builtins.str, typing.Any]]]]],
        subscription_name: builtins.str,
        threshold: jsii.Number,
        resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAnomalySubscription.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CE::AnomalySubscription``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param frequency: The frequency that anomaly reports are sent over email.
        :param monitor_arn_list: A list of cost anomaly monitors.
        :param subscribers: A list of subscribers to notify.
        :param subscription_name: The name for the subscription.
        :param threshold: (deprecated). The dollar value that triggers a notification if the threshold is exceeded. This field has been deprecated. To specify a threshold, use ThresholdExpression. Continued use of Threshold will be treated as shorthand syntax for a ThresholdExpression. One of Threshold or ThresholdExpression is required for this resource.
        :param resource_tags: ``AWS::CE::AnomalySubscription.ResourceTags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedc01e7792d6d1498fe2f105ec543963b5444c017f1be06bef64762e522f1e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAnomalySubscriptionProps(
            frequency=frequency,
            monitor_arn_list=monitor_arn_list,
            subscribers=subscribers,
            subscription_name=subscription_name,
            threshold=threshold,
            resource_tags=resource_tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__011542380e1ec8495031c1b60071a75cc16cb1364db958554ea4b33d36ff2c51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b238cdeb2e921780cf02bc9e1e4848128ec4aaf0cac0bdf2d8e02fb176e35a7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAccountId")
    def attr_account_id(self) -> builtins.str:
        '''Your unique account identifier.

        :cloudformationAttribute: AccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAccountId"))

    @builtins.property
    @jsii.member(jsii_name="attrSubscriptionArn")
    def attr_subscription_arn(self) -> builtins.str:
        '''The ``AnomalySubscription`` Amazon Resource Name (ARN).

        :cloudformationAttribute: SubscriptionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSubscriptionArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        '''The frequency that anomaly reports are sent over email.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-frequency
        '''
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa69eea3257bddf7ec67a097e09014053417e5705d1c1248dee639816403cb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value)

    @builtins.property
    @jsii.member(jsii_name="monitorArnList")
    def monitor_arn_list(self) -> typing.List[builtins.str]:
        '''A list of cost anomaly monitors.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-monitorarnlist
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "monitorArnList"))

    @monitor_arn_list.setter
    def monitor_arn_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d507359ed995b6443578e4aca51bddab936c70022966f54ae3af067bf8f92aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorArnList", value)

    @builtins.property
    @jsii.member(jsii_name="subscribers")
    def subscribers(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnomalySubscription.SubscriberProperty"]]]:
        '''A list of subscribers to notify.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-subscribers
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnomalySubscription.SubscriberProperty"]]], jsii.get(self, "subscribers"))

    @subscribers.setter
    def subscribers(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnomalySubscription.SubscriberProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f237b182ed81799205e44385fb9cc494f8105b1210c56c629e8c1d055cacb89c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscribers", value)

    @builtins.property
    @jsii.member(jsii_name="subscriptionName")
    def subscription_name(self) -> builtins.str:
        '''The name for the subscription.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-subscriptionname
        '''
        return typing.cast(builtins.str, jsii.get(self, "subscriptionName"))

    @subscription_name.setter
    def subscription_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a83a2436827ff2bf11d2cf02c74184b55ae0ebfa6fb43b9f7864bb584813adb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionName", value)

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        '''(deprecated).

        The dollar value that triggers a notification if the threshold is exceeded.

        This field has been deprecated. To specify a threshold, use ThresholdExpression. Continued use of Threshold will be treated as shorthand syntax for a ThresholdExpression.

        One of Threshold or ThresholdExpression is required for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-threshold
        '''
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77c34ad116d25cd3751d74642da82cdb7dc0a60cc93828fd0983cd91b424a59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnomalySubscription.ResourceTagProperty"]]]]:
        '''``AWS::CE::AnomalySubscription.ResourceTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-resourcetags
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnomalySubscription.ResourceTagProperty"]]]], jsii.get(self, "resourceTags"))

    @resource_tags.setter
    def resource_tags(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnomalySubscription.ResourceTagProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae8c61c7ab624a357b20407935404b665b683140ca1d042f2fbab8665694d68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTags", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ce.CfnAnomalySubscription.ResourceTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ResourceTagProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''The tag structure that contains a tag key and value.

            .. epigraph::

               Tagging is supported only for the following Cost Explorer resource types: ```AnomalyMonitor`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalyMonitor.html>`_ , ```AnomalySubscription`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalySubscription.html>`_ , ```CostCategory`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_CostCategory.html>`_ .

            :param key: The key that's associated with the tag.
            :param value: The value that's associated with the tag.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ce as ce
                
                resource_tag_property = ce.CfnAnomalySubscription.ResourceTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b3dfb4ac75bab59fe15f3c3f2c916db714ba50ab0987700ed9c5f08b5bf243b)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The key that's associated with the tag.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-resourcetag.html#cfn-ce-anomalysubscription-resourcetag-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value that's associated with the tag.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-resourcetag.html#cfn-ce-anomalysubscription-resourcetag-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ce.CfnAnomalySubscription.SubscriberProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address", "type": "type", "status": "status"},
    )
    class SubscriberProperty:
        def __init__(
            self,
            *,
            address: builtins.str,
            type: builtins.str,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The recipient of ``AnomalySubscription`` notifications.

            :param address: The email address or SNS Topic Amazon Resource Name (ARN), depending on the ``Type`` .
            :param type: The notification delivery channel.
            :param status: Indicates if the subscriber accepts the notifications.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-subscriber.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ce as ce
                
                subscriber_property = ce.CfnAnomalySubscription.SubscriberProperty(
                    address="address",
                    type="type",
                
                    # the properties below are optional
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f53815c92956ca4bf3e235db1c48951d2cbd9258b5a1151d7ca9d8a64cd49952)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "address": address,
                "type": type,
            }
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def address(self) -> builtins.str:
            '''The email address or SNS Topic Amazon Resource Name (ARN), depending on the ``Type`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-subscriber.html#cfn-ce-anomalysubscription-subscriber-address
            '''
            result = self._values.get("address")
            assert result is not None, "Required property 'address' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The notification delivery channel.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-subscriber.html#cfn-ce-anomalysubscription-subscriber-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Indicates if the subscriber accepts the notifications.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-subscriber.html#cfn-ce-anomalysubscription-subscriber-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriberProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ce.CfnAnomalySubscriptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "frequency": "frequency",
        "monitor_arn_list": "monitorArnList",
        "subscribers": "subscribers",
        "subscription_name": "subscriptionName",
        "threshold": "threshold",
        "resource_tags": "resourceTags",
    },
)
class CfnAnomalySubscriptionProps:
    def __init__(
        self,
        *,
        frequency: builtins.str,
        monitor_arn_list: typing.Sequence[builtins.str],
        subscribers: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnomalySubscription.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]]]],
        subscription_name: builtins.str,
        threshold: jsii.Number,
        resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnomalySubscription.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAnomalySubscription``.

        :param frequency: The frequency that anomaly reports are sent over email.
        :param monitor_arn_list: A list of cost anomaly monitors.
        :param subscribers: A list of subscribers to notify.
        :param subscription_name: The name for the subscription.
        :param threshold: (deprecated). The dollar value that triggers a notification if the threshold is exceeded. This field has been deprecated. To specify a threshold, use ThresholdExpression. Continued use of Threshold will be treated as shorthand syntax for a ThresholdExpression. One of Threshold or ThresholdExpression is required for this resource.
        :param resource_tags: ``AWS::CE::AnomalySubscription.ResourceTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ce as ce
            
            cfn_anomaly_subscription_props = ce.CfnAnomalySubscriptionProps(
                frequency="frequency",
                monitor_arn_list=["monitorArnList"],
                subscribers=[ce.CfnAnomalySubscription.SubscriberProperty(
                    address="address",
                    type="type",
            
                    # the properties below are optional
                    status="status"
                )],
                subscription_name="subscriptionName",
                threshold=123,
            
                # the properties below are optional
                resource_tags=[ce.CfnAnomalySubscription.ResourceTagProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba55057a9beaf430c797c5608244ba6d42d040d01cea76a9358a99318a069a7)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument monitor_arn_list", value=monitor_arn_list, expected_type=type_hints["monitor_arn_list"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
            check_type(argname="argument subscription_name", value=subscription_name, expected_type=type_hints["subscription_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency": frequency,
            "monitor_arn_list": monitor_arn_list,
            "subscribers": subscribers,
            "subscription_name": subscription_name,
            "threshold": threshold,
        }
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags

    @builtins.property
    def frequency(self) -> builtins.str:
        '''The frequency that anomaly reports are sent over email.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-frequency
        '''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def monitor_arn_list(self) -> typing.List[builtins.str]:
        '''A list of cost anomaly monitors.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-monitorarnlist
        '''
        result = self._values.get("monitor_arn_list")
        assert result is not None, "Required property 'monitor_arn_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subscribers(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnomalySubscription.SubscriberProperty]]]:
        '''A list of subscribers to notify.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-subscribers
        '''
        result = self._values.get("subscribers")
        assert result is not None, "Required property 'subscribers' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnomalySubscription.SubscriberProperty]]], result)

    @builtins.property
    def subscription_name(self) -> builtins.str:
        '''The name for the subscription.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-subscriptionname
        '''
        result = self._values.get("subscription_name")
        assert result is not None, "Required property 'subscription_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''(deprecated).

        The dollar value that triggers a notification if the threshold is exceeded.

        This field has been deprecated. To specify a threshold, use ThresholdExpression. Continued use of Threshold will be treated as shorthand syntax for a ThresholdExpression.

        One of Threshold or ThresholdExpression is required for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-threshold
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnomalySubscription.ResourceTagProperty]]]]:
        '''``AWS::CE::AnomalySubscription.ResourceTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnomalySubscription.ResourceTagProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnomalySubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCostCategory(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ce.CfnCostCategory",
):
    '''A CloudFormation ``AWS::CE::CostCategory``.

    The ``AWS::CE::CostCategory`` resource creates groupings of cost that you can use across products in the AWS Billing and Cost Management console, such as Cost Explorer and AWS Budgets. For more information, see `Managing Your Costs with Cost Categories <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-cost-categories.html>`_ in the *AWS Billing and Cost Management User Guide* .

    :cloudformationResource: AWS::CE::CostCategory
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ce as ce
        
        cfn_cost_category = ce.CfnCostCategory(self, "MyCfnCostCategory",
            name="name",
            rules="rules",
            rule_version="ruleVersion",
        
            # the properties below are optional
            default_value="defaultValue",
            split_charge_rules="splitChargeRules"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        rules: builtins.str,
        rule_version: builtins.str,
        default_value: typing.Optional[builtins.str] = None,
        split_charge_rules: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CE::CostCategory``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The unique name of the Cost Category.
        :param rules: The array of CostCategoryRule in JSON array format. .. epigraph:: Rules are processed in order. If there are multiple rules that match the line item, then the first rule to match is used to determine that Cost Category value.
        :param rule_version: The rule schema version in this particular Cost Category.
        :param default_value: The default value for the cost category.
        :param split_charge_rules: The split charge rules that are used to allocate your charges between your Cost Category values.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480729d0715b30f4da893bcd6b67c77a13dc582290aae0f30fe2c5599f77057a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCostCategoryProps(
            name=name,
            rules=rules,
            rule_version=rule_version,
            default_value=default_value,
            split_charge_rules=split_charge_rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67de86b19a0838cabea36db69601374529f1d24b9c7504c55881d89c1e6d0a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17475e3bb4db75ff64d2134598ebc80f574aaadf9a565859372cd02ebd79c23a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The unique identifier for your Cost Category.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrEffectiveStart")
    def attr_effective_start(self) -> builtins.str:
        '''The Cost Category's effective start date.

        :cloudformationAttribute: EffectiveStart
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEffectiveStart"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The unique name of the Cost Category.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5957f467efb2adbac34a8fbceb11bf99b3a87789f577d7fb93b982f751574da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> builtins.str:
        '''The array of CostCategoryRule in JSON array format.

        .. epigraph::

           Rules are processed in order. If there are multiple rules that match the line item, then the first rule to match is used to determine that Cost Category value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-rules
        '''
        return typing.cast(builtins.str, jsii.get(self, "rules"))

    @rules.setter
    def rules(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62eb206078c0d1d56968bec995ec4930240c810606cd54e4d9082be4819bc977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rules", value)

    @builtins.property
    @jsii.member(jsii_name="ruleVersion")
    def rule_version(self) -> builtins.str:
        '''The rule schema version in this particular Cost Category.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-ruleversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleVersion"))

    @rule_version.setter
    def rule_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e6c80b688ac944da315e9285a9544cc66fe62b2dfa27f1c9e14e26bc89b047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleVersion", value)

    @builtins.property
    @jsii.member(jsii_name="defaultValue")
    def default_value(self) -> typing.Optional[builtins.str]:
        '''The default value for the cost category.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-defaultvalue
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultValue"))

    @default_value.setter
    def default_value(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da960ec231dcaa17d51fb749c63f55f415a18f18d5b5929e80377389c83b489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultValue", value)

    @builtins.property
    @jsii.member(jsii_name="splitChargeRules")
    def split_charge_rules(self) -> typing.Optional[builtins.str]:
        '''The split charge rules that are used to allocate your charges between your Cost Category values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-splitchargerules
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "splitChargeRules"))

    @split_charge_rules.setter
    def split_charge_rules(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfca03e47575ee4590488cc83caeb10e15ebf584435d201ca07c7d63a9e92507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "splitChargeRules", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ce.CfnCostCategoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "rules": "rules",
        "rule_version": "ruleVersion",
        "default_value": "defaultValue",
        "split_charge_rules": "splitChargeRules",
    },
)
class CfnCostCategoryProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        rules: builtins.str,
        rule_version: builtins.str,
        default_value: typing.Optional[builtins.str] = None,
        split_charge_rules: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnCostCategory``.

        :param name: The unique name of the Cost Category.
        :param rules: The array of CostCategoryRule in JSON array format. .. epigraph:: Rules are processed in order. If there are multiple rules that match the line item, then the first rule to match is used to determine that Cost Category value.
        :param rule_version: The rule schema version in this particular Cost Category.
        :param default_value: The default value for the cost category.
        :param split_charge_rules: The split charge rules that are used to allocate your charges between your Cost Category values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ce as ce
            
            cfn_cost_category_props = ce.CfnCostCategoryProps(
                name="name",
                rules="rules",
                rule_version="ruleVersion",
            
                # the properties below are optional
                default_value="defaultValue",
                split_charge_rules="splitChargeRules"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b5415e9594ca52dd194407ed742b054e5bc917e1085ca5225394168b99610a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument rule_version", value=rule_version, expected_type=type_hints["rule_version"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            check_type(argname="argument split_charge_rules", value=split_charge_rules, expected_type=type_hints["split_charge_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "rules": rules,
            "rule_version": rule_version,
        }
        if default_value is not None:
            self._values["default_value"] = default_value
        if split_charge_rules is not None:
            self._values["split_charge_rules"] = split_charge_rules

    @builtins.property
    def name(self) -> builtins.str:
        '''The unique name of the Cost Category.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(self) -> builtins.str:
        '''The array of CostCategoryRule in JSON array format.

        .. epigraph::

           Rules are processed in order. If there are multiple rules that match the line item, then the first rule to match is used to determine that Cost Category value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-rules
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_version(self) -> builtins.str:
        '''The rule schema version in this particular Cost Category.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-ruleversion
        '''
        result = self._values.get("rule_version")
        assert result is not None, "Required property 'rule_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_value(self) -> typing.Optional[builtins.str]:
        '''The default value for the cost category.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-defaultvalue
        '''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def split_charge_rules(self) -> typing.Optional[builtins.str]:
        '''The split charge rules that are used to allocate your charges between your Cost Category values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-splitchargerules
        '''
        result = self._values.get("split_charge_rules")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCostCategoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAnomalyMonitor",
    "CfnAnomalyMonitorProps",
    "CfnAnomalySubscription",
    "CfnAnomalySubscriptionProps",
    "CfnCostCategory",
    "CfnCostCategoryProps",
]

publication.publish()

def _typecheckingstub__32f53317433755ca5b4636716c3a33228f79704406037a9d362081e936156090(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    monitor_name: builtins.str,
    monitor_type: builtins.str,
    monitor_dimension: typing.Optional[builtins.str] = None,
    monitor_specification: typing.Optional[builtins.str] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnAnomalyMonitor.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7910f5202051e9857c176fb6e796fd30daa32e4d3009569527e143c25728e7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bcd972f71eb76cebcb46e8a787d3a4d3f06e49e7f6476245bc3a5f41618692(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cbde7a7bb043805da5df3b9478d315e92fcdbd58e74209ae325e371a7255b75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0543f46498df833238e235679c5d5a047e6a1fea42dbdf29bae8763e20cb62ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff79309b9fb6b6e81e1cef9c2f05e756e614cb69a9df633252f918737b3b6acd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a14c2af48924fe63344517cb1aca26d5a773c40aa3d27b8d876b25f7f58d12e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda64289d8b76f3867cd1d74f3d49813928e5d2782ae187eb671b9c72208b562(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnAnomalyMonitor.ResourceTagProperty, _aws_cdk_core_f4b25747.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67b8063ac428384e77769e71adbffee848cc2a9f580eb0e6e4499e90e822d24(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09743b43a68e2cab7b28ba5c62a3dad9b55e741f161771af3d08889e3ea16a0(
    *,
    monitor_name: builtins.str,
    monitor_type: builtins.str,
    monitor_dimension: typing.Optional[builtins.str] = None,
    monitor_specification: typing.Optional[builtins.str] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnAnomalyMonitor.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedc01e7792d6d1498fe2f105ec543963b5444c017f1be06bef64762e522f1e8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    frequency: builtins.str,
    monitor_arn_list: typing.Sequence[builtins.str],
    subscribers: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnomalySubscription.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]]]],
    subscription_name: builtins.str,
    threshold: jsii.Number,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnomalySubscription.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011542380e1ec8495031c1b60071a75cc16cb1364db958554ea4b33d36ff2c51(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b238cdeb2e921780cf02bc9e1e4848128ec4aaf0cac0bdf2d8e02fb176e35a7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa69eea3257bddf7ec67a097e09014053417e5705d1c1248dee639816403cb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d507359ed995b6443578e4aca51bddab936c70022966f54ae3af067bf8f92aa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f237b182ed81799205e44385fb9cc494f8105b1210c56c629e8c1d055cacb89c(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnomalySubscription.SubscriberProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a83a2436827ff2bf11d2cf02c74184b55ae0ebfa6fb43b9f7864bb584813adb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77c34ad116d25cd3751d74642da82cdb7dc0a60cc93828fd0983cd91b424a59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae8c61c7ab624a357b20407935404b665b683140ca1d042f2fbab8665694d68(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnomalySubscription.ResourceTagProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3dfb4ac75bab59fe15f3c3f2c916db714ba50ab0987700ed9c5f08b5bf243b(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53815c92956ca4bf3e235db1c48951d2cbd9258b5a1151d7ca9d8a64cd49952(
    *,
    address: builtins.str,
    type: builtins.str,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba55057a9beaf430c797c5608244ba6d42d040d01cea76a9358a99318a069a7(
    *,
    frequency: builtins.str,
    monitor_arn_list: typing.Sequence[builtins.str],
    subscribers: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnomalySubscription.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]]]],
    subscription_name: builtins.str,
    threshold: jsii.Number,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnomalySubscription.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480729d0715b30f4da893bcd6b67c77a13dc582290aae0f30fe2c5599f77057a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    rules: builtins.str,
    rule_version: builtins.str,
    default_value: typing.Optional[builtins.str] = None,
    split_charge_rules: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67de86b19a0838cabea36db69601374529f1d24b9c7504c55881d89c1e6d0a6(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17475e3bb4db75ff64d2134598ebc80f574aaadf9a565859372cd02ebd79c23a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5957f467efb2adbac34a8fbceb11bf99b3a87789f577d7fb93b982f751574da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62eb206078c0d1d56968bec995ec4930240c810606cd54e4d9082be4819bc977(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e6c80b688ac944da315e9285a9544cc66fe62b2dfa27f1c9e14e26bc89b047(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da960ec231dcaa17d51fb749c63f55f415a18f18d5b5929e80377389c83b489(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfca03e47575ee4590488cc83caeb10e15ebf584435d201ca07c7d63a9e92507(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b5415e9594ca52dd194407ed742b054e5bc917e1085ca5225394168b99610a(
    *,
    name: builtins.str,
    rules: builtins.str,
    rule_version: builtins.str,
    default_value: typing.Optional[builtins.str] = None,
    split_charge_rules: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
