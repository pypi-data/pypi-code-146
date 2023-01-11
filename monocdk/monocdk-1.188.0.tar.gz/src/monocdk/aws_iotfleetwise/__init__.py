'''
# AWS::IoTFleetWise Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as iotfleetwise
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for IoTFleetWise construct libraries](https://constructs.dev/search?q=iotfleetwise)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::IoTFleetWise resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTFleetWise.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::IoTFleetWise](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTFleetWise.html).

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
class CfnCampaign(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotfleetwise.CfnCampaign",
):
    '''A CloudFormation ``AWS::IoTFleetWise::Campaign``.

    Creates an orchestration of data collection rules. The AWS IoT FleetWise Edge Agent software running in vehicles uses campaigns to decide how to collect and transfer data to the cloud. You create campaigns in the cloud. After you or your team approve campaigns, AWS IoT FleetWise automatically deploys them to vehicles.

    For more information, see `Collect and transfer data with campaigns <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/campaigns.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :cloudformationResource: AWS::IoTFleetWise::Campaign
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotfleetwise as iotfleetwise
        
        cfn_campaign = iotfleetwise.CfnCampaign(self, "MyCfnCampaign",
            action="action",
            collection_scheme=iotfleetwise.CfnCampaign.CollectionSchemeProperty(
                condition_based_collection_scheme=iotfleetwise.CfnCampaign.ConditionBasedCollectionSchemeProperty(
                    expression="expression",
        
                    # the properties below are optional
                    condition_language_version=123,
                    minimum_trigger_interval_ms=123,
                    trigger_mode="triggerMode"
                ),
                time_based_collection_scheme=iotfleetwise.CfnCampaign.TimeBasedCollectionSchemeProperty(
                    period_ms=123
                )
            ),
            name="name",
            signal_catalog_arn="signalCatalogArn",
            target_arn="targetArn",
        
            # the properties below are optional
            compression="compression",
            data_extra_dimensions=["dataExtraDimensions"],
            description="description",
            diagnostics_mode="diagnosticsMode",
            expiry_time="expiryTime",
            post_trigger_collection_duration=123,
            priority=123,
            signals_to_collect=[iotfleetwise.CfnCampaign.SignalInformationProperty(
                name="name",
        
                # the properties below are optional
                max_sample_count=123,
                minimum_sampling_interval_ms=123
            )],
            spooling_mode="spoolingMode",
            start_time="startTime",
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
        action: builtins.str,
        collection_scheme: typing.Union[typing.Union["CfnCampaign.CollectionSchemeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        name: builtins.str,
        signal_catalog_arn: builtins.str,
        target_arn: builtins.str,
        compression: typing.Optional[builtins.str] = None,
        data_extra_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        diagnostics_mode: typing.Optional[builtins.str] = None,
        expiry_time: typing.Optional[builtins.str] = None,
        post_trigger_collection_duration: typing.Optional[jsii.Number] = None,
        priority: typing.Optional[jsii.Number] = None,
        signals_to_collect: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnCampaign.SignalInformationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        spooling_mode: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTFleetWise::Campaign``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param action: ``AWS::IoTFleetWise::Campaign.Action``.
        :param collection_scheme: ``AWS::IoTFleetWise::Campaign.CollectionScheme``.
        :param name: The name of a campaign.
        :param signal_catalog_arn: The ARN of the signal catalog associated with the campaign.
        :param target_arn: The ARN of a vehicle or fleet to which the campaign is deployed.
        :param compression: ``AWS::IoTFleetWise::Campaign.Compression``.
        :param data_extra_dimensions: ``AWS::IoTFleetWise::Campaign.DataExtraDimensions``.
        :param description: The description of the campaign.
        :param diagnostics_mode: ``AWS::IoTFleetWise::Campaign.DiagnosticsMode``.
        :param expiry_time: ``AWS::IoTFleetWise::Campaign.ExpiryTime``.
        :param post_trigger_collection_duration: ``AWS::IoTFleetWise::Campaign.PostTriggerCollectionDuration``.
        :param priority: ``AWS::IoTFleetWise::Campaign.Priority``.
        :param signals_to_collect: ``AWS::IoTFleetWise::Campaign.SignalsToCollect``.
        :param spooling_mode: ``AWS::IoTFleetWise::Campaign.SpoolingMode``.
        :param start_time: ``AWS::IoTFleetWise::Campaign.StartTime``.
        :param tags: ``AWS::IoTFleetWise::Campaign.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23fb5b8b308cea60def7e8ab524ba9ce7d68b68dc228aaabed8e56c49e440e32)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCampaignProps(
            action=action,
            collection_scheme=collection_scheme,
            name=name,
            signal_catalog_arn=signal_catalog_arn,
            target_arn=target_arn,
            compression=compression,
            data_extra_dimensions=data_extra_dimensions,
            description=description,
            diagnostics_mode=diagnostics_mode,
            expiry_time=expiry_time,
            post_trigger_collection_duration=post_trigger_collection_duration,
            priority=priority,
            signals_to_collect=signals_to_collect,
            spooling_mode=spooling_mode,
            start_time=start_time,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2b5b87334c7d8908c366b7fd5bcb53ad8b6a4d360beefb0721f54aa1eae376)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a341fbbf10ee78bbb6df8a89129093fd4e68b826f8eb9b4cf6ac256cbcdf3d74)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModificationTime")
    def attr_last_modification_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: LastModificationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''
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
        '''``AWS::IoTFleetWise::Campaign.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        '''``AWS::IoTFleetWise::Campaign.Action``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-action
        '''
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8069aecac51432040b50d2f942c1e9ca693651d326ba63cb1c2099f5ab4de6c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="collectionScheme")
    def collection_scheme(
        self,
    ) -> typing.Union["CfnCampaign.CollectionSchemeProperty", _IResolvable_a771d0ef]:
        '''``AWS::IoTFleetWise::Campaign.CollectionScheme``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-collectionscheme
        '''
        return typing.cast(typing.Union["CfnCampaign.CollectionSchemeProperty", _IResolvable_a771d0ef], jsii.get(self, "collectionScheme"))

    @collection_scheme.setter
    def collection_scheme(
        self,
        value: typing.Union["CfnCampaign.CollectionSchemeProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d3d042366d3968155052e581b0e1fef6462d55212dac2c6db452696d285ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionScheme", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of a campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4568ff1b08bb4e6acfd7c7117b90cd8c1057ff8c429d8dee80d980d6ba2abac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="signalCatalogArn")
    def signal_catalog_arn(self) -> builtins.str:
        '''The ARN of the signal catalog associated with the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-signalcatalogarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "signalCatalogArn"))

    @signal_catalog_arn.setter
    def signal_catalog_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051e5978f1fa221d2e6d45370c92e40024163f2be063bfb881d2a87edce51d7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signalCatalogArn", value)

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''The ARN of a vehicle or fleet to which the campaign is deployed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-targetarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc20a3f1c4a0f787b36e5cc11d85f4d6fa0f621ae191fd1e8101247a1df26921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetArn", value)

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::Campaign.Compression``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-compression
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3adf71168f42588adb1d327751271901791b601390b349666a3cc3b19fe99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value)

    @builtins.property
    @jsii.member(jsii_name="dataExtraDimensions")
    def data_extra_dimensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::IoTFleetWise::Campaign.DataExtraDimensions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-dataextradimensions
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dataExtraDimensions"))

    @data_extra_dimensions.setter
    def data_extra_dimensions(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa9be0e7b5a1584ebe0567fc40f45eaca67b8e9f59188e2b88f9d0c32f8fda4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataExtraDimensions", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad977b5d83868394a340be235c962dcd4901c6a0b4debca793cb01befbf19c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="diagnosticsMode")
    def diagnostics_mode(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::Campaign.DiagnosticsMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-diagnosticsmode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diagnosticsMode"))

    @diagnostics_mode.setter
    def diagnostics_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f48fe4cd6504918fefbddd9f256fa6198500c95c8b6a7b25e533ea68e5b8577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diagnosticsMode", value)

    @builtins.property
    @jsii.member(jsii_name="expiryTime")
    def expiry_time(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::Campaign.ExpiryTime``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-expirytime
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expiryTime"))

    @expiry_time.setter
    def expiry_time(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdc3ea623979aef49baa7df521355733011783f0d1614c94372bd5fd1795ab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiryTime", value)

    @builtins.property
    @jsii.member(jsii_name="postTriggerCollectionDuration")
    def post_trigger_collection_duration(self) -> typing.Optional[jsii.Number]:
        '''``AWS::IoTFleetWise::Campaign.PostTriggerCollectionDuration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-posttriggercollectionduration
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "postTriggerCollectionDuration"))

    @post_trigger_collection_duration.setter
    def post_trigger_collection_duration(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f80d4c4545451dafc1e756c63e48891d753b5c0656015573c1bcb9befc47f53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postTriggerCollectionDuration", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> typing.Optional[jsii.Number]:
        '''``AWS::IoTFleetWise::Campaign.Priority``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-priority
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409a484a01fe8caf68feee528a572a31da781fb397ba3251b42fa8bcbe40ded0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="signalsToCollect")
    def signals_to_collect(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCampaign.SignalInformationProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::IoTFleetWise::Campaign.SignalsToCollect``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-signalstocollect
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCampaign.SignalInformationProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "signalsToCollect"))

    @signals_to_collect.setter
    def signals_to_collect(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCampaign.SignalInformationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa37b449763b5d51c7c3c884317240d1cfc64b697b350f38a1bc40b40ad1889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signalsToCollect", value)

    @builtins.property
    @jsii.member(jsii_name="spoolingMode")
    def spooling_mode(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::Campaign.SpoolingMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-spoolingmode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spoolingMode"))

    @spooling_mode.setter
    def spooling_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa48a59fd3cce9f9f3faf148063f7f16c9867c9a3b29ed31c7ddb2d67f3ed7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spoolingMode", value)

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::Campaign.StartTime``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-starttime
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e1018486d554c86b80477ccdeafaa196370d881b5cf78eb0b8b01a67571912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnCampaign.CollectionSchemeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition_based_collection_scheme": "conditionBasedCollectionScheme",
            "time_based_collection_scheme": "timeBasedCollectionScheme",
        },
    )
    class CollectionSchemeProperty:
        def __init__(
            self,
            *,
            condition_based_collection_scheme: typing.Optional[typing.Union[typing.Union["CfnCampaign.ConditionBasedCollectionSchemeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            time_based_collection_scheme: typing.Optional[typing.Union[typing.Union["CfnCampaign.TimeBasedCollectionSchemeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies what data to collect and how often or when to collect it.

            :param condition_based_collection_scheme: Information about a collection scheme that uses a simple logical expression to recognize what data to collect.
            :param time_based_collection_scheme: Information about a collection scheme that uses a time period to decide how often to collect data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-collectionscheme.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                collection_scheme_property = iotfleetwise.CfnCampaign.CollectionSchemeProperty(
                    condition_based_collection_scheme=iotfleetwise.CfnCampaign.ConditionBasedCollectionSchemeProperty(
                        expression="expression",
                
                        # the properties below are optional
                        condition_language_version=123,
                        minimum_trigger_interval_ms=123,
                        trigger_mode="triggerMode"
                    ),
                    time_based_collection_scheme=iotfleetwise.CfnCampaign.TimeBasedCollectionSchemeProperty(
                        period_ms=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0b56c9bb346ba87ddc3e19d1af22b043dc61283010aab82dc4a2c616c6c4518)
                check_type(argname="argument condition_based_collection_scheme", value=condition_based_collection_scheme, expected_type=type_hints["condition_based_collection_scheme"])
                check_type(argname="argument time_based_collection_scheme", value=time_based_collection_scheme, expected_type=type_hints["time_based_collection_scheme"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition_based_collection_scheme is not None:
                self._values["condition_based_collection_scheme"] = condition_based_collection_scheme
            if time_based_collection_scheme is not None:
                self._values["time_based_collection_scheme"] = time_based_collection_scheme

        @builtins.property
        def condition_based_collection_scheme(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.ConditionBasedCollectionSchemeProperty", _IResolvable_a771d0ef]]:
            '''Information about a collection scheme that uses a simple logical expression to recognize what data to collect.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-collectionscheme.html#cfn-iotfleetwise-campaign-collectionscheme-conditionbasedcollectionscheme
            '''
            result = self._values.get("condition_based_collection_scheme")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.ConditionBasedCollectionSchemeProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def time_based_collection_scheme(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.TimeBasedCollectionSchemeProperty", _IResolvable_a771d0ef]]:
            '''Information about a collection scheme that uses a time period to decide how often to collect data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-collectionscheme.html#cfn-iotfleetwise-campaign-collectionscheme-timebasedcollectionscheme
            '''
            result = self._values.get("time_based_collection_scheme")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.TimeBasedCollectionSchemeProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CollectionSchemeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnCampaign.ConditionBasedCollectionSchemeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "condition_language_version": "conditionLanguageVersion",
            "minimum_trigger_interval_ms": "minimumTriggerIntervalMs",
            "trigger_mode": "triggerMode",
        },
    )
    class ConditionBasedCollectionSchemeProperty:
        def __init__(
            self,
            *,
            expression: builtins.str,
            condition_language_version: typing.Optional[jsii.Number] = None,
            minimum_trigger_interval_ms: typing.Optional[jsii.Number] = None,
            trigger_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a collection scheme that uses a simple logical expression to recognize what data to collect.

            :param expression: The logical expression used to recognize what data to collect. For example, ``$variable.Vehicle.OutsideAirTemperature >= 105.0`` .
            :param condition_language_version: Specifies the version of the conditional expression language.
            :param minimum_trigger_interval_ms: The minimum duration of time between two triggering events to collect data, in milliseconds. .. epigraph:: If a signal changes often, you might want to collect data at a slower rate.
            :param trigger_mode: Whether to collect data for all triggering events ( ``ALWAYS`` ). Specify ( ``RISING_EDGE`` ), or specify only when the condition first evaluates to false. For example, triggering on "AirbagDeployed"; Users aren't interested on triggering when the airbag is already exploded; they only care about the change from not deployed => deployed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedcollectionscheme.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                condition_based_collection_scheme_property = iotfleetwise.CfnCampaign.ConditionBasedCollectionSchemeProperty(
                    expression="expression",
                
                    # the properties below are optional
                    condition_language_version=123,
                    minimum_trigger_interval_ms=123,
                    trigger_mode="triggerMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2dd0fa2589ce7eec396519a2434c76197a9ed96e8d72967dbb4efaa1b1b3d62c)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument condition_language_version", value=condition_language_version, expected_type=type_hints["condition_language_version"])
                check_type(argname="argument minimum_trigger_interval_ms", value=minimum_trigger_interval_ms, expected_type=type_hints["minimum_trigger_interval_ms"])
                check_type(argname="argument trigger_mode", value=trigger_mode, expected_type=type_hints["trigger_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "expression": expression,
            }
            if condition_language_version is not None:
                self._values["condition_language_version"] = condition_language_version
            if minimum_trigger_interval_ms is not None:
                self._values["minimum_trigger_interval_ms"] = minimum_trigger_interval_ms
            if trigger_mode is not None:
                self._values["trigger_mode"] = trigger_mode

        @builtins.property
        def expression(self) -> builtins.str:
            '''The logical expression used to recognize what data to collect.

            For example, ``$variable.Vehicle.OutsideAirTemperature >= 105.0`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedcollectionscheme.html#cfn-iotfleetwise-campaign-conditionbasedcollectionscheme-expression
            '''
            result = self._values.get("expression")
            assert result is not None, "Required property 'expression' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def condition_language_version(self) -> typing.Optional[jsii.Number]:
            '''Specifies the version of the conditional expression language.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedcollectionscheme.html#cfn-iotfleetwise-campaign-conditionbasedcollectionscheme-conditionlanguageversion
            '''
            result = self._values.get("condition_language_version")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum_trigger_interval_ms(self) -> typing.Optional[jsii.Number]:
            '''The minimum duration of time between two triggering events to collect data, in milliseconds.

            .. epigraph::

               If a signal changes often, you might want to collect data at a slower rate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedcollectionscheme.html#cfn-iotfleetwise-campaign-conditionbasedcollectionscheme-minimumtriggerintervalms
            '''
            result = self._values.get("minimum_trigger_interval_ms")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def trigger_mode(self) -> typing.Optional[builtins.str]:
            '''Whether to collect data for all triggering events ( ``ALWAYS`` ).

            Specify ( ``RISING_EDGE`` ), or specify only when the condition first evaluates to false. For example, triggering on "AirbagDeployed"; Users aren't interested on triggering when the airbag is already exploded; they only care about the change from not deployed => deployed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedcollectionscheme.html#cfn-iotfleetwise-campaign-conditionbasedcollectionscheme-triggermode
            '''
            result = self._values.get("trigger_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionBasedCollectionSchemeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnCampaign.SignalInformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "max_sample_count": "maxSampleCount",
            "minimum_sampling_interval_ms": "minimumSamplingIntervalMs",
        },
    )
    class SignalInformationProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            max_sample_count: typing.Optional[jsii.Number] = None,
            minimum_sampling_interval_ms: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about a signal.

            :param name: The name of the signal.
            :param max_sample_count: The maximum number of samples to collect.
            :param minimum_sampling_interval_ms: The minimum duration of time (in milliseconds) between two triggering events to collect data. .. epigraph:: If a signal changes often, you might want to collect data at a slower rate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalinformation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                signal_information_property = iotfleetwise.CfnCampaign.SignalInformationProperty(
                    name="name",
                
                    # the properties below are optional
                    max_sample_count=123,
                    minimum_sampling_interval_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8cf093984560e2a6848a9799e8e77c9616ab738b681d9e926d0bfe402fd1f944)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument max_sample_count", value=max_sample_count, expected_type=type_hints["max_sample_count"])
                check_type(argname="argument minimum_sampling_interval_ms", value=minimum_sampling_interval_ms, expected_type=type_hints["minimum_sampling_interval_ms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if max_sample_count is not None:
                self._values["max_sample_count"] = max_sample_count
            if minimum_sampling_interval_ms is not None:
                self._values["minimum_sampling_interval_ms"] = minimum_sampling_interval_ms

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the signal.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalinformation.html#cfn-iotfleetwise-campaign-signalinformation-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def max_sample_count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of samples to collect.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalinformation.html#cfn-iotfleetwise-campaign-signalinformation-maxsamplecount
            '''
            result = self._values.get("max_sample_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum_sampling_interval_ms(self) -> typing.Optional[jsii.Number]:
            '''The minimum duration of time (in milliseconds) between two triggering events to collect data.

            .. epigraph::

               If a signal changes often, you might want to collect data at a slower rate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalinformation.html#cfn-iotfleetwise-campaign-signalinformation-minimumsamplingintervalms
            '''
            result = self._values.get("minimum_sampling_interval_ms")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SignalInformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnCampaign.TimeBasedCollectionSchemeProperty",
        jsii_struct_bases=[],
        name_mapping={"period_ms": "periodMs"},
    )
    class TimeBasedCollectionSchemeProperty:
        def __init__(self, *, period_ms: jsii.Number) -> None:
            '''Information about a collection scheme that uses a time period to decide how often to collect data.

            :param period_ms: The time period (in milliseconds) to decide how often to collect data. For example, if the time period is ``60000`` , the Edge Agent software collects data once every minute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-timebasedcollectionscheme.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                time_based_collection_scheme_property = iotfleetwise.CfnCampaign.TimeBasedCollectionSchemeProperty(
                    period_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57942af51326d4694e6ca7673d698b49c973b85ea417cc0a8637a76aa8cc1f55)
                check_type(argname="argument period_ms", value=period_ms, expected_type=type_hints["period_ms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "period_ms": period_ms,
            }

        @builtins.property
        def period_ms(self) -> jsii.Number:
            '''The time period (in milliseconds) to decide how often to collect data.

            For example, if the time period is ``60000`` , the Edge Agent software collects data once every minute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-timebasedcollectionscheme.html#cfn-iotfleetwise-campaign-timebasedcollectionscheme-periodms
            '''
            result = self._values.get("period_ms")
            assert result is not None, "Required property 'period_ms' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeBasedCollectionSchemeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotfleetwise.CfnCampaignProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "collection_scheme": "collectionScheme",
        "name": "name",
        "signal_catalog_arn": "signalCatalogArn",
        "target_arn": "targetArn",
        "compression": "compression",
        "data_extra_dimensions": "dataExtraDimensions",
        "description": "description",
        "diagnostics_mode": "diagnosticsMode",
        "expiry_time": "expiryTime",
        "post_trigger_collection_duration": "postTriggerCollectionDuration",
        "priority": "priority",
        "signals_to_collect": "signalsToCollect",
        "spooling_mode": "spoolingMode",
        "start_time": "startTime",
        "tags": "tags",
    },
)
class CfnCampaignProps:
    def __init__(
        self,
        *,
        action: builtins.str,
        collection_scheme: typing.Union[typing.Union[CfnCampaign.CollectionSchemeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        name: builtins.str,
        signal_catalog_arn: builtins.str,
        target_arn: builtins.str,
        compression: typing.Optional[builtins.str] = None,
        data_extra_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        diagnostics_mode: typing.Optional[builtins.str] = None,
        expiry_time: typing.Optional[builtins.str] = None,
        post_trigger_collection_duration: typing.Optional[jsii.Number] = None,
        priority: typing.Optional[jsii.Number] = None,
        signals_to_collect: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCampaign.SignalInformationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        spooling_mode: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCampaign``.

        :param action: ``AWS::IoTFleetWise::Campaign.Action``.
        :param collection_scheme: ``AWS::IoTFleetWise::Campaign.CollectionScheme``.
        :param name: The name of a campaign.
        :param signal_catalog_arn: The ARN of the signal catalog associated with the campaign.
        :param target_arn: The ARN of a vehicle or fleet to which the campaign is deployed.
        :param compression: ``AWS::IoTFleetWise::Campaign.Compression``.
        :param data_extra_dimensions: ``AWS::IoTFleetWise::Campaign.DataExtraDimensions``.
        :param description: The description of the campaign.
        :param diagnostics_mode: ``AWS::IoTFleetWise::Campaign.DiagnosticsMode``.
        :param expiry_time: ``AWS::IoTFleetWise::Campaign.ExpiryTime``.
        :param post_trigger_collection_duration: ``AWS::IoTFleetWise::Campaign.PostTriggerCollectionDuration``.
        :param priority: ``AWS::IoTFleetWise::Campaign.Priority``.
        :param signals_to_collect: ``AWS::IoTFleetWise::Campaign.SignalsToCollect``.
        :param spooling_mode: ``AWS::IoTFleetWise::Campaign.SpoolingMode``.
        :param start_time: ``AWS::IoTFleetWise::Campaign.StartTime``.
        :param tags: ``AWS::IoTFleetWise::Campaign.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotfleetwise as iotfleetwise
            
            cfn_campaign_props = iotfleetwise.CfnCampaignProps(
                action="action",
                collection_scheme=iotfleetwise.CfnCampaign.CollectionSchemeProperty(
                    condition_based_collection_scheme=iotfleetwise.CfnCampaign.ConditionBasedCollectionSchemeProperty(
                        expression="expression",
            
                        # the properties below are optional
                        condition_language_version=123,
                        minimum_trigger_interval_ms=123,
                        trigger_mode="triggerMode"
                    ),
                    time_based_collection_scheme=iotfleetwise.CfnCampaign.TimeBasedCollectionSchemeProperty(
                        period_ms=123
                    )
                ),
                name="name",
                signal_catalog_arn="signalCatalogArn",
                target_arn="targetArn",
            
                # the properties below are optional
                compression="compression",
                data_extra_dimensions=["dataExtraDimensions"],
                description="description",
                diagnostics_mode="diagnosticsMode",
                expiry_time="expiryTime",
                post_trigger_collection_duration=123,
                priority=123,
                signals_to_collect=[iotfleetwise.CfnCampaign.SignalInformationProperty(
                    name="name",
            
                    # the properties below are optional
                    max_sample_count=123,
                    minimum_sampling_interval_ms=123
                )],
                spooling_mode="spoolingMode",
                start_time="startTime",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3664a47dbea9aaeff9dd1e4d284f16659bd0deb9998412e7c7d3a778b2201c)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument collection_scheme", value=collection_scheme, expected_type=type_hints["collection_scheme"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument signal_catalog_arn", value=signal_catalog_arn, expected_type=type_hints["signal_catalog_arn"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument data_extra_dimensions", value=data_extra_dimensions, expected_type=type_hints["data_extra_dimensions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument diagnostics_mode", value=diagnostics_mode, expected_type=type_hints["diagnostics_mode"])
            check_type(argname="argument expiry_time", value=expiry_time, expected_type=type_hints["expiry_time"])
            check_type(argname="argument post_trigger_collection_duration", value=post_trigger_collection_duration, expected_type=type_hints["post_trigger_collection_duration"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument signals_to_collect", value=signals_to_collect, expected_type=type_hints["signals_to_collect"])
            check_type(argname="argument spooling_mode", value=spooling_mode, expected_type=type_hints["spooling_mode"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "collection_scheme": collection_scheme,
            "name": name,
            "signal_catalog_arn": signal_catalog_arn,
            "target_arn": target_arn,
        }
        if compression is not None:
            self._values["compression"] = compression
        if data_extra_dimensions is not None:
            self._values["data_extra_dimensions"] = data_extra_dimensions
        if description is not None:
            self._values["description"] = description
        if diagnostics_mode is not None:
            self._values["diagnostics_mode"] = diagnostics_mode
        if expiry_time is not None:
            self._values["expiry_time"] = expiry_time
        if post_trigger_collection_duration is not None:
            self._values["post_trigger_collection_duration"] = post_trigger_collection_duration
        if priority is not None:
            self._values["priority"] = priority
        if signals_to_collect is not None:
            self._values["signals_to_collect"] = signals_to_collect
        if spooling_mode is not None:
            self._values["spooling_mode"] = spooling_mode
        if start_time is not None:
            self._values["start_time"] = start_time
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def action(self) -> builtins.str:
        '''``AWS::IoTFleetWise::Campaign.Action``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-action
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def collection_scheme(
        self,
    ) -> typing.Union[CfnCampaign.CollectionSchemeProperty, _IResolvable_a771d0ef]:
        '''``AWS::IoTFleetWise::Campaign.CollectionScheme``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-collectionscheme
        '''
        result = self._values.get("collection_scheme")
        assert result is not None, "Required property 'collection_scheme' is missing"
        return typing.cast(typing.Union[CfnCampaign.CollectionSchemeProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of a campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signal_catalog_arn(self) -> builtins.str:
        '''The ARN of the signal catalog associated with the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-signalcatalogarn
        '''
        result = self._values.get("signal_catalog_arn")
        assert result is not None, "Required property 'signal_catalog_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''The ARN of a vehicle or fleet to which the campaign is deployed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-targetarn
        '''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::Campaign.Compression``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-compression
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_extra_dimensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::IoTFleetWise::Campaign.DataExtraDimensions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-dataextradimensions
        '''
        result = self._values.get("data_extra_dimensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def diagnostics_mode(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::Campaign.DiagnosticsMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-diagnosticsmode
        '''
        result = self._values.get("diagnostics_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiry_time(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::Campaign.ExpiryTime``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-expirytime
        '''
        result = self._values.get("expiry_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_trigger_collection_duration(self) -> typing.Optional[jsii.Number]:
        '''``AWS::IoTFleetWise::Campaign.PostTriggerCollectionDuration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-posttriggercollectionduration
        '''
        result = self._values.get("post_trigger_collection_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''``AWS::IoTFleetWise::Campaign.Priority``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def signals_to_collect(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCampaign.SignalInformationProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::IoTFleetWise::Campaign.SignalsToCollect``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-signalstocollect
        '''
        result = self._values.get("signals_to_collect")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCampaign.SignalInformationProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def spooling_mode(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::Campaign.SpoolingMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-spoolingmode
        '''
        result = self._values.get("spooling_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::Campaign.StartTime``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-starttime
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::IoTFleetWise::Campaign.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCampaignProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDecoderManifest(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotfleetwise.CfnDecoderManifest",
):
    '''A CloudFormation ``AWS::IoTFleetWise::DecoderManifest``.

    Creates the decoder manifest associated with a model manifest. To create a decoder manifest, the following must be true:

    - Every signal decoder has a unique name.
    - Each signal decoder is associated with a network interface.
    - Each network interface has a unique ID.
    - The signal decoders are specified in the model manifest.

    :cloudformationResource: AWS::IoTFleetWise::DecoderManifest
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotfleetwise as iotfleetwise
        
        cfn_decoder_manifest = iotfleetwise.CfnDecoderManifest(self, "MyCfnDecoderManifest",
            model_manifest_arn="modelManifestArn",
            name="name",
        
            # the properties below are optional
            description="description",
            network_interfaces=[iotfleetwise.CfnDecoderManifest.NetworkInterfacesItemsProperty(
                interface_id="interfaceId",
                type="type",
        
                # the properties below are optional
                can_interface=iotfleetwise.CfnDecoderManifest.CanInterfaceProperty(
                    name="name",
        
                    # the properties below are optional
                    protocol_name="protocolName",
                    protocol_version="protocolVersion"
                ),
                obd_interface=iotfleetwise.CfnDecoderManifest.ObdInterfaceProperty(
                    name="name",
                    request_message_id="requestMessageId",
        
                    # the properties below are optional
                    dtc_request_interval_seconds="dtcRequestIntervalSeconds",
                    has_transmission_ecu="hasTransmissionEcu",
                    obd_standard="obdStandard",
                    pid_request_interval_seconds="pidRequestIntervalSeconds",
                    use_extended_ids="useExtendedIds"
                )
            )],
            signal_decoders=[iotfleetwise.CfnDecoderManifest.SignalDecodersItemsProperty(
                fully_qualified_name="fullyQualifiedName",
                interface_id="interfaceId",
                type="type",
        
                # the properties below are optional
                can_signal=iotfleetwise.CfnDecoderManifest.CanSignalProperty(
                    factor="factor",
                    is_big_endian="isBigEndian",
                    is_signed="isSigned",
                    length="length",
                    message_id="messageId",
                    offset="offset",
                    start_bit="startBit",
        
                    # the properties below are optional
                    name="name"
                ),
                obd_signal=iotfleetwise.CfnDecoderManifest.ObdSignalProperty(
                    byte_length="byteLength",
                    offset="offset",
                    pid="pid",
                    pid_response_length="pidResponseLength",
                    scaling="scaling",
                    service_mode="serviceMode",
                    start_byte="startByte",
        
                    # the properties below are optional
                    bit_mask_length="bitMaskLength",
                    bit_right_shift="bitRightShift"
                )
            )],
            status="status",
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
        model_manifest_arn: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDecoderManifest.NetworkInterfacesItemsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        signal_decoders: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDecoderManifest.SignalDecodersItemsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTFleetWise::DecoderManifest``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param model_manifest_arn: The ARN of a vehicle model (model manifest) associated with the decoder manifest.
        :param name: The name of the decoder manifest.
        :param description: A brief description of the decoder manifest.
        :param network_interfaces: ``AWS::IoTFleetWise::DecoderManifest.NetworkInterfaces``.
        :param signal_decoders: ``AWS::IoTFleetWise::DecoderManifest.SignalDecoders``.
        :param status: The state of the decoder manifest. If the status is ``ACTIVE`` , the decoder manifest can't be edited. If the status is marked ``DRAFT`` , you can edit the decoder manifest.
        :param tags: ``AWS::IoTFleetWise::DecoderManifest.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65eedd006d93da34fc3cf09875b1f01a065dbaf025b1990760b62aaf8ed1d36c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDecoderManifestProps(
            model_manifest_arn=model_manifest_arn,
            name=name,
            description=description,
            network_interfaces=network_interfaces,
            signal_decoders=signal_decoders,
            status=status,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f7ea38fd2de65fe6d0eb61eaddaa019a8eb99f9256d4f6ea66b2e22e047907b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ebae224fab3d79a355d7bfc627c5fe1b03871e25d1e6c4ab54657a50b0e622f)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModificationTime")
    def attr_last_modification_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: LastModificationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::IoTFleetWise::DecoderManifest.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="modelManifestArn")
    def model_manifest_arn(self) -> builtins.str:
        '''The ARN of a vehicle model (model manifest) associated with the decoder manifest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-modelmanifestarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "modelManifestArn"))

    @model_manifest_arn.setter
    def model_manifest_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fdb67ee57f7e65bff1dfd07a47d9dcc70dea640ee3ad1f04f134c709c0d1948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelManifestArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the decoder manifest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fabe8a7f451a2ea9f9aad901ee8e25c3d9deabe4d1745fac24ace65db1299cc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the decoder manifest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b08751fb43386f0c1cfec714d2857b0823eff2345b77c5383f43edf9cd26ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="networkInterfaces")
    def network_interfaces(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDecoderManifest.NetworkInterfacesItemsProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::IoTFleetWise::DecoderManifest.NetworkInterfaces``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-networkinterfaces
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDecoderManifest.NetworkInterfacesItemsProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "networkInterfaces"))

    @network_interfaces.setter
    def network_interfaces(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDecoderManifest.NetworkInterfacesItemsProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad474a55a88a68be702bd6e73a517b2c1f93ff4046aaefd058db5b6c01f5481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkInterfaces", value)

    @builtins.property
    @jsii.member(jsii_name="signalDecoders")
    def signal_decoders(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDecoderManifest.SignalDecodersItemsProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::IoTFleetWise::DecoderManifest.SignalDecoders``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-signaldecoders
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDecoderManifest.SignalDecodersItemsProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "signalDecoders"))

    @signal_decoders.setter
    def signal_decoders(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDecoderManifest.SignalDecodersItemsProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd7961b3f92b2eb03740b49a3f30d6d39716bdc118d6ba066f430d142b87a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signalDecoders", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''The state of the decoder manifest.

        If the status is ``ACTIVE`` , the decoder manifest can't be edited. If the status is marked ``DRAFT`` , you can edit the decoder manifest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02bcaa42a4f4cb65c3031fea856238019ce3f51a316186ff29073827d3938ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnDecoderManifest.CanInterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "protocol_name": "protocolName",
            "protocol_version": "protocolVersion",
        },
    )
    class CanInterfaceProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            protocol_name: typing.Optional[builtins.str] = None,
            protocol_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A single controller area network (CAN) device interface.

            :param name: The unique name of the interface.
            :param protocol_name: The name of the communication protocol for the interface.
            :param protocol_version: The version of the communication protocol for the interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-caninterface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                can_interface_property = iotfleetwise.CfnDecoderManifest.CanInterfaceProperty(
                    name="name",
                
                    # the properties below are optional
                    protocol_name="protocolName",
                    protocol_version="protocolVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0129222cfd471bc80e18a5b14c99c724f83445e97e1dafd4c53bd63e4ca28bfa)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument protocol_name", value=protocol_name, expected_type=type_hints["protocol_name"])
                check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if protocol_name is not None:
                self._values["protocol_name"] = protocol_name
            if protocol_version is not None:
                self._values["protocol_version"] = protocol_version

        @builtins.property
        def name(self) -> builtins.str:
            '''The unique name of the interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-caninterface.html#cfn-iotfleetwise-decodermanifest-caninterface-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def protocol_name(self) -> typing.Optional[builtins.str]:
            '''The name of the communication protocol for the interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-caninterface.html#cfn-iotfleetwise-decodermanifest-caninterface-protocolname
            '''
            result = self._values.get("protocol_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol_version(self) -> typing.Optional[builtins.str]:
            '''The version of the communication protocol for the interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-caninterface.html#cfn-iotfleetwise-decodermanifest-caninterface-protocolversion
            '''
            result = self._values.get("protocol_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CanInterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnDecoderManifest.CanSignalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "factor": "factor",
            "is_big_endian": "isBigEndian",
            "is_signed": "isSigned",
            "length": "length",
            "message_id": "messageId",
            "offset": "offset",
            "start_bit": "startBit",
            "name": "name",
        },
    )
    class CanSignalProperty:
        def __init__(
            self,
            *,
            factor: builtins.str,
            is_big_endian: builtins.str,
            is_signed: builtins.str,
            length: builtins.str,
            message_id: builtins.str,
            offset: builtins.str,
            start_bit: builtins.str,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a single controller area network (CAN) signal and the messages it receives and transmits.

            :param factor: A multiplier used to decode the CAN message.
            :param is_big_endian: Whether the byte ordering of a CAN message is big-endian.
            :param is_signed: Whether the message data is specified as a signed value.
            :param length: How many bytes of data are in the message.
            :param message_id: The ID of the message.
            :param offset: Indicates where data appears in the CAN message.
            :param start_bit: Indicates the beginning of the CAN message.
            :param name: The name of the signal.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                can_signal_property = iotfleetwise.CfnDecoderManifest.CanSignalProperty(
                    factor="factor",
                    is_big_endian="isBigEndian",
                    is_signed="isSigned",
                    length="length",
                    message_id="messageId",
                    offset="offset",
                    start_bit="startBit",
                
                    # the properties below are optional
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed145af79f1c2da4094c58342eb40f268c984f336a565ceb7692c2373c41b02e)
                check_type(argname="argument factor", value=factor, expected_type=type_hints["factor"])
                check_type(argname="argument is_big_endian", value=is_big_endian, expected_type=type_hints["is_big_endian"])
                check_type(argname="argument is_signed", value=is_signed, expected_type=type_hints["is_signed"])
                check_type(argname="argument length", value=length, expected_type=type_hints["length"])
                check_type(argname="argument message_id", value=message_id, expected_type=type_hints["message_id"])
                check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
                check_type(argname="argument start_bit", value=start_bit, expected_type=type_hints["start_bit"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "factor": factor,
                "is_big_endian": is_big_endian,
                "is_signed": is_signed,
                "length": length,
                "message_id": message_id,
                "offset": offset,
                "start_bit": start_bit,
            }
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def factor(self) -> builtins.str:
            '''A multiplier used to decode the CAN message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-factor
            '''
            result = self._values.get("factor")
            assert result is not None, "Required property 'factor' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def is_big_endian(self) -> builtins.str:
            '''Whether the byte ordering of a CAN message is big-endian.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-isbigendian
            '''
            result = self._values.get("is_big_endian")
            assert result is not None, "Required property 'is_big_endian' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def is_signed(self) -> builtins.str:
            '''Whether the message data is specified as a signed value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-issigned
            '''
            result = self._values.get("is_signed")
            assert result is not None, "Required property 'is_signed' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def length(self) -> builtins.str:
            '''How many bytes of data are in the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-length
            '''
            result = self._values.get("length")
            assert result is not None, "Required property 'length' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def message_id(self) -> builtins.str:
            '''The ID of the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-messageid
            '''
            result = self._values.get("message_id")
            assert result is not None, "Required property 'message_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def offset(self) -> builtins.str:
            '''Indicates where data appears in the CAN message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-offset
            '''
            result = self._values.get("offset")
            assert result is not None, "Required property 'offset' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def start_bit(self) -> builtins.str:
            '''Indicates the beginning of the CAN message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-startbit
            '''
            result = self._values.get("start_bit")
            assert result is not None, "Required property 'start_bit' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the signal.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CanSignalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnDecoderManifest.NetworkInterfacesItemsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "interface_id": "interfaceId",
            "type": "type",
            "can_interface": "canInterface",
            "obd_interface": "obdInterface",
        },
    )
    class NetworkInterfacesItemsProperty:
        def __init__(
            self,
            *,
            interface_id: builtins.str,
            type: builtins.str,
            can_interface: typing.Optional[typing.Union[typing.Union["CfnDecoderManifest.CanInterfaceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            obd_interface: typing.Optional[typing.Union[typing.Union["CfnDecoderManifest.ObdInterfaceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param interface_id: ``CfnDecoderManifest.NetworkInterfacesItemsProperty.InterfaceId``.
            :param type: ``CfnDecoderManifest.NetworkInterfacesItemsProperty.Type``.
            :param can_interface: ``CfnDecoderManifest.NetworkInterfacesItemsProperty.CanInterface``.
            :param obd_interface: ``CfnDecoderManifest.NetworkInterfacesItemsProperty.ObdInterface``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-networkinterfacesitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                network_interfaces_items_property = iotfleetwise.CfnDecoderManifest.NetworkInterfacesItemsProperty(
                    interface_id="interfaceId",
                    type="type",
                
                    # the properties below are optional
                    can_interface=iotfleetwise.CfnDecoderManifest.CanInterfaceProperty(
                        name="name",
                
                        # the properties below are optional
                        protocol_name="protocolName",
                        protocol_version="protocolVersion"
                    ),
                    obd_interface=iotfleetwise.CfnDecoderManifest.ObdInterfaceProperty(
                        name="name",
                        request_message_id="requestMessageId",
                
                        # the properties below are optional
                        dtc_request_interval_seconds="dtcRequestIntervalSeconds",
                        has_transmission_ecu="hasTransmissionEcu",
                        obd_standard="obdStandard",
                        pid_request_interval_seconds="pidRequestIntervalSeconds",
                        use_extended_ids="useExtendedIds"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5164929065d606d8e2dc0dacc4ac433535c723e64a0977419b7b5cdcc6e7bce3)
                check_type(argname="argument interface_id", value=interface_id, expected_type=type_hints["interface_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument can_interface", value=can_interface, expected_type=type_hints["can_interface"])
                check_type(argname="argument obd_interface", value=obd_interface, expected_type=type_hints["obd_interface"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "interface_id": interface_id,
                "type": type,
            }
            if can_interface is not None:
                self._values["can_interface"] = can_interface
            if obd_interface is not None:
                self._values["obd_interface"] = obd_interface

        @builtins.property
        def interface_id(self) -> builtins.str:
            '''``CfnDecoderManifest.NetworkInterfacesItemsProperty.InterfaceId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-networkinterfacesitems.html#cfn-iotfleetwise-decodermanifest-networkinterfacesitems-interfaceid
            '''
            result = self._values.get("interface_id")
            assert result is not None, "Required property 'interface_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnDecoderManifest.NetworkInterfacesItemsProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-networkinterfacesitems.html#cfn-iotfleetwise-decodermanifest-networkinterfacesitems-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def can_interface(
            self,
        ) -> typing.Optional[typing.Union["CfnDecoderManifest.CanInterfaceProperty", _IResolvable_a771d0ef]]:
            '''``CfnDecoderManifest.NetworkInterfacesItemsProperty.CanInterface``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-networkinterfacesitems.html#cfn-iotfleetwise-decodermanifest-networkinterfacesitems-caninterface
            '''
            result = self._values.get("can_interface")
            return typing.cast(typing.Optional[typing.Union["CfnDecoderManifest.CanInterfaceProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def obd_interface(
            self,
        ) -> typing.Optional[typing.Union["CfnDecoderManifest.ObdInterfaceProperty", _IResolvable_a771d0ef]]:
            '''``CfnDecoderManifest.NetworkInterfacesItemsProperty.ObdInterface``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-networkinterfacesitems.html#cfn-iotfleetwise-decodermanifest-networkinterfacesitems-obdinterface
            '''
            result = self._values.get("obd_interface")
            return typing.cast(typing.Optional[typing.Union["CfnDecoderManifest.ObdInterfaceProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkInterfacesItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnDecoderManifest.ObdInterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "request_message_id": "requestMessageId",
            "dtc_request_interval_seconds": "dtcRequestIntervalSeconds",
            "has_transmission_ecu": "hasTransmissionEcu",
            "obd_standard": "obdStandard",
            "pid_request_interval_seconds": "pidRequestIntervalSeconds",
            "use_extended_ids": "useExtendedIds",
        },
    )
    class ObdInterfaceProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            request_message_id: builtins.str,
            dtc_request_interval_seconds: typing.Optional[builtins.str] = None,
            has_transmission_ecu: typing.Optional[builtins.str] = None,
            obd_standard: typing.Optional[builtins.str] = None,
            pid_request_interval_seconds: typing.Optional[builtins.str] = None,
            use_extended_ids: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A network interface that specifies the On-board diagnostic (OBD) II network protocol.

            :param name: The name of the interface.
            :param request_message_id: The ID of the message requesting vehicle data.
            :param dtc_request_interval_seconds: The maximum number message requests per diagnostic trouble code per second.
            :param has_transmission_ecu: Whether the vehicle has a transmission control module (TCM).
            :param obd_standard: The standard OBD II PID.
            :param pid_request_interval_seconds: The maximum number message requests per second.
            :param use_extended_ids: Whether to use extended IDs in the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                obd_interface_property = iotfleetwise.CfnDecoderManifest.ObdInterfaceProperty(
                    name="name",
                    request_message_id="requestMessageId",
                
                    # the properties below are optional
                    dtc_request_interval_seconds="dtcRequestIntervalSeconds",
                    has_transmission_ecu="hasTransmissionEcu",
                    obd_standard="obdStandard",
                    pid_request_interval_seconds="pidRequestIntervalSeconds",
                    use_extended_ids="useExtendedIds"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36035124d92aa491d26f7f3badad12234749ce5287196e39297302730919ddfd)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument request_message_id", value=request_message_id, expected_type=type_hints["request_message_id"])
                check_type(argname="argument dtc_request_interval_seconds", value=dtc_request_interval_seconds, expected_type=type_hints["dtc_request_interval_seconds"])
                check_type(argname="argument has_transmission_ecu", value=has_transmission_ecu, expected_type=type_hints["has_transmission_ecu"])
                check_type(argname="argument obd_standard", value=obd_standard, expected_type=type_hints["obd_standard"])
                check_type(argname="argument pid_request_interval_seconds", value=pid_request_interval_seconds, expected_type=type_hints["pid_request_interval_seconds"])
                check_type(argname="argument use_extended_ids", value=use_extended_ids, expected_type=type_hints["use_extended_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "request_message_id": request_message_id,
            }
            if dtc_request_interval_seconds is not None:
                self._values["dtc_request_interval_seconds"] = dtc_request_interval_seconds
            if has_transmission_ecu is not None:
                self._values["has_transmission_ecu"] = has_transmission_ecu
            if obd_standard is not None:
                self._values["obd_standard"] = obd_standard
            if pid_request_interval_seconds is not None:
                self._values["pid_request_interval_seconds"] = pid_request_interval_seconds
            if use_extended_ids is not None:
                self._values["use_extended_ids"] = use_extended_ids

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def request_message_id(self) -> builtins.str:
            '''The ID of the message requesting vehicle data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-requestmessageid
            '''
            result = self._values.get("request_message_id")
            assert result is not None, "Required property 'request_message_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def dtc_request_interval_seconds(self) -> typing.Optional[builtins.str]:
            '''The maximum number message requests per diagnostic trouble code per second.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-dtcrequestintervalseconds
            '''
            result = self._values.get("dtc_request_interval_seconds")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def has_transmission_ecu(self) -> typing.Optional[builtins.str]:
            '''Whether the vehicle has a transmission control module (TCM).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-hastransmissionecu
            '''
            result = self._values.get("has_transmission_ecu")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def obd_standard(self) -> typing.Optional[builtins.str]:
            '''The standard OBD II PID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-obdstandard
            '''
            result = self._values.get("obd_standard")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pid_request_interval_seconds(self) -> typing.Optional[builtins.str]:
            '''The maximum number message requests per second.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-pidrequestintervalseconds
            '''
            result = self._values.get("pid_request_interval_seconds")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_extended_ids(self) -> typing.Optional[builtins.str]:
            '''Whether to use extended IDs in the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-useextendedids
            '''
            result = self._values.get("use_extended_ids")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObdInterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnDecoderManifest.ObdSignalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "byte_length": "byteLength",
            "offset": "offset",
            "pid": "pid",
            "pid_response_length": "pidResponseLength",
            "scaling": "scaling",
            "service_mode": "serviceMode",
            "start_byte": "startByte",
            "bit_mask_length": "bitMaskLength",
            "bit_right_shift": "bitRightShift",
        },
    )
    class ObdSignalProperty:
        def __init__(
            self,
            *,
            byte_length: builtins.str,
            offset: builtins.str,
            pid: builtins.str,
            pid_response_length: builtins.str,
            scaling: builtins.str,
            service_mode: builtins.str,
            start_byte: builtins.str,
            bit_mask_length: typing.Optional[builtins.str] = None,
            bit_right_shift: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about signal messages using the on-board diagnostics (OBD) II protocol in a vehicle.

            :param byte_length: The length of a message.
            :param offset: Indicates where data appears in the message.
            :param pid: The diagnostic code used to request data from a vehicle for this signal.
            :param pid_response_length: The length of the requested data.
            :param scaling: A multiplier used to decode the message.
            :param service_mode: The mode of operation (diagnostic service) in a message.
            :param start_byte: Indicates the beginning of the message.
            :param bit_mask_length: The number of bits to mask in a message.
            :param bit_right_shift: The number of positions to shift bits in the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                obd_signal_property = iotfleetwise.CfnDecoderManifest.ObdSignalProperty(
                    byte_length="byteLength",
                    offset="offset",
                    pid="pid",
                    pid_response_length="pidResponseLength",
                    scaling="scaling",
                    service_mode="serviceMode",
                    start_byte="startByte",
                
                    # the properties below are optional
                    bit_mask_length="bitMaskLength",
                    bit_right_shift="bitRightShift"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__701af2c9ec258d82f07b58404b5f34be536d73fe08eac2a1004d856673d9669a)
                check_type(argname="argument byte_length", value=byte_length, expected_type=type_hints["byte_length"])
                check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
                check_type(argname="argument pid", value=pid, expected_type=type_hints["pid"])
                check_type(argname="argument pid_response_length", value=pid_response_length, expected_type=type_hints["pid_response_length"])
                check_type(argname="argument scaling", value=scaling, expected_type=type_hints["scaling"])
                check_type(argname="argument service_mode", value=service_mode, expected_type=type_hints["service_mode"])
                check_type(argname="argument start_byte", value=start_byte, expected_type=type_hints["start_byte"])
                check_type(argname="argument bit_mask_length", value=bit_mask_length, expected_type=type_hints["bit_mask_length"])
                check_type(argname="argument bit_right_shift", value=bit_right_shift, expected_type=type_hints["bit_right_shift"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "byte_length": byte_length,
                "offset": offset,
                "pid": pid,
                "pid_response_length": pid_response_length,
                "scaling": scaling,
                "service_mode": service_mode,
                "start_byte": start_byte,
            }
            if bit_mask_length is not None:
                self._values["bit_mask_length"] = bit_mask_length
            if bit_right_shift is not None:
                self._values["bit_right_shift"] = bit_right_shift

        @builtins.property
        def byte_length(self) -> builtins.str:
            '''The length of a message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-bytelength
            '''
            result = self._values.get("byte_length")
            assert result is not None, "Required property 'byte_length' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def offset(self) -> builtins.str:
            '''Indicates where data appears in the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-offset
            '''
            result = self._values.get("offset")
            assert result is not None, "Required property 'offset' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def pid(self) -> builtins.str:
            '''The diagnostic code used to request data from a vehicle for this signal.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-pid
            '''
            result = self._values.get("pid")
            assert result is not None, "Required property 'pid' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def pid_response_length(self) -> builtins.str:
            '''The length of the requested data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-pidresponselength
            '''
            result = self._values.get("pid_response_length")
            assert result is not None, "Required property 'pid_response_length' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def scaling(self) -> builtins.str:
            '''A multiplier used to decode the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-scaling
            '''
            result = self._values.get("scaling")
            assert result is not None, "Required property 'scaling' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def service_mode(self) -> builtins.str:
            '''The mode of operation (diagnostic service) in a message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-servicemode
            '''
            result = self._values.get("service_mode")
            assert result is not None, "Required property 'service_mode' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def start_byte(self) -> builtins.str:
            '''Indicates the beginning of the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-startbyte
            '''
            result = self._values.get("start_byte")
            assert result is not None, "Required property 'start_byte' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bit_mask_length(self) -> typing.Optional[builtins.str]:
            '''The number of bits to mask in a message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-bitmasklength
            '''
            result = self._values.get("bit_mask_length")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bit_right_shift(self) -> typing.Optional[builtins.str]:
            '''The number of positions to shift bits in the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-bitrightshift
            '''
            result = self._values.get("bit_right_shift")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObdSignalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnDecoderManifest.SignalDecodersItemsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "fully_qualified_name": "fullyQualifiedName",
            "interface_id": "interfaceId",
            "type": "type",
            "can_signal": "canSignal",
            "obd_signal": "obdSignal",
        },
    )
    class SignalDecodersItemsProperty:
        def __init__(
            self,
            *,
            fully_qualified_name: builtins.str,
            interface_id: builtins.str,
            type: builtins.str,
            can_signal: typing.Optional[typing.Union[typing.Union["CfnDecoderManifest.CanSignalProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            obd_signal: typing.Optional[typing.Union[typing.Union["CfnDecoderManifest.ObdSignalProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param fully_qualified_name: ``CfnDecoderManifest.SignalDecodersItemsProperty.FullyQualifiedName``.
            :param interface_id: ``CfnDecoderManifest.SignalDecodersItemsProperty.InterfaceId``.
            :param type: ``CfnDecoderManifest.SignalDecodersItemsProperty.Type``.
            :param can_signal: ``CfnDecoderManifest.SignalDecodersItemsProperty.CanSignal``.
            :param obd_signal: ``CfnDecoderManifest.SignalDecodersItemsProperty.ObdSignal``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                signal_decoders_items_property = iotfleetwise.CfnDecoderManifest.SignalDecodersItemsProperty(
                    fully_qualified_name="fullyQualifiedName",
                    interface_id="interfaceId",
                    type="type",
                
                    # the properties below are optional
                    can_signal=iotfleetwise.CfnDecoderManifest.CanSignalProperty(
                        factor="factor",
                        is_big_endian="isBigEndian",
                        is_signed="isSigned",
                        length="length",
                        message_id="messageId",
                        offset="offset",
                        start_bit="startBit",
                
                        # the properties below are optional
                        name="name"
                    ),
                    obd_signal=iotfleetwise.CfnDecoderManifest.ObdSignalProperty(
                        byte_length="byteLength",
                        offset="offset",
                        pid="pid",
                        pid_response_length="pidResponseLength",
                        scaling="scaling",
                        service_mode="serviceMode",
                        start_byte="startByte",
                
                        # the properties below are optional
                        bit_mask_length="bitMaskLength",
                        bit_right_shift="bitRightShift"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e9c41d005beeec9830cf27750c5a3fb6af1317338d2cded80dd0a0881034aa2)
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument interface_id", value=interface_id, expected_type=type_hints["interface_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument can_signal", value=can_signal, expected_type=type_hints["can_signal"])
                check_type(argname="argument obd_signal", value=obd_signal, expected_type=type_hints["obd_signal"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "fully_qualified_name": fully_qualified_name,
                "interface_id": interface_id,
                "type": type,
            }
            if can_signal is not None:
                self._values["can_signal"] = can_signal
            if obd_signal is not None:
                self._values["obd_signal"] = obd_signal

        @builtins.property
        def fully_qualified_name(self) -> builtins.str:
            '''``CfnDecoderManifest.SignalDecodersItemsProperty.FullyQualifiedName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html#cfn-iotfleetwise-decodermanifest-signaldecodersitems-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            assert result is not None, "Required property 'fully_qualified_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def interface_id(self) -> builtins.str:
            '''``CfnDecoderManifest.SignalDecodersItemsProperty.InterfaceId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html#cfn-iotfleetwise-decodermanifest-signaldecodersitems-interfaceid
            '''
            result = self._values.get("interface_id")
            assert result is not None, "Required property 'interface_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnDecoderManifest.SignalDecodersItemsProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html#cfn-iotfleetwise-decodermanifest-signaldecodersitems-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def can_signal(
            self,
        ) -> typing.Optional[typing.Union["CfnDecoderManifest.CanSignalProperty", _IResolvable_a771d0ef]]:
            '''``CfnDecoderManifest.SignalDecodersItemsProperty.CanSignal``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html#cfn-iotfleetwise-decodermanifest-signaldecodersitems-cansignal
            '''
            result = self._values.get("can_signal")
            return typing.cast(typing.Optional[typing.Union["CfnDecoderManifest.CanSignalProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def obd_signal(
            self,
        ) -> typing.Optional[typing.Union["CfnDecoderManifest.ObdSignalProperty", _IResolvable_a771d0ef]]:
            '''``CfnDecoderManifest.SignalDecodersItemsProperty.ObdSignal``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html#cfn-iotfleetwise-decodermanifest-signaldecodersitems-obdsignal
            '''
            result = self._values.get("obd_signal")
            return typing.cast(typing.Optional[typing.Union["CfnDecoderManifest.ObdSignalProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SignalDecodersItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotfleetwise.CfnDecoderManifestProps",
    jsii_struct_bases=[],
    name_mapping={
        "model_manifest_arn": "modelManifestArn",
        "name": "name",
        "description": "description",
        "network_interfaces": "networkInterfaces",
        "signal_decoders": "signalDecoders",
        "status": "status",
        "tags": "tags",
    },
)
class CfnDecoderManifestProps:
    def __init__(
        self,
        *,
        model_manifest_arn: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDecoderManifest.NetworkInterfacesItemsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        signal_decoders: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDecoderManifest.SignalDecodersItemsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDecoderManifest``.

        :param model_manifest_arn: The ARN of a vehicle model (model manifest) associated with the decoder manifest.
        :param name: The name of the decoder manifest.
        :param description: A brief description of the decoder manifest.
        :param network_interfaces: ``AWS::IoTFleetWise::DecoderManifest.NetworkInterfaces``.
        :param signal_decoders: ``AWS::IoTFleetWise::DecoderManifest.SignalDecoders``.
        :param status: The state of the decoder manifest. If the status is ``ACTIVE`` , the decoder manifest can't be edited. If the status is marked ``DRAFT`` , you can edit the decoder manifest.
        :param tags: ``AWS::IoTFleetWise::DecoderManifest.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotfleetwise as iotfleetwise
            
            cfn_decoder_manifest_props = iotfleetwise.CfnDecoderManifestProps(
                model_manifest_arn="modelManifestArn",
                name="name",
            
                # the properties below are optional
                description="description",
                network_interfaces=[iotfleetwise.CfnDecoderManifest.NetworkInterfacesItemsProperty(
                    interface_id="interfaceId",
                    type="type",
            
                    # the properties below are optional
                    can_interface=iotfleetwise.CfnDecoderManifest.CanInterfaceProperty(
                        name="name",
            
                        # the properties below are optional
                        protocol_name="protocolName",
                        protocol_version="protocolVersion"
                    ),
                    obd_interface=iotfleetwise.CfnDecoderManifest.ObdInterfaceProperty(
                        name="name",
                        request_message_id="requestMessageId",
            
                        # the properties below are optional
                        dtc_request_interval_seconds="dtcRequestIntervalSeconds",
                        has_transmission_ecu="hasTransmissionEcu",
                        obd_standard="obdStandard",
                        pid_request_interval_seconds="pidRequestIntervalSeconds",
                        use_extended_ids="useExtendedIds"
                    )
                )],
                signal_decoders=[iotfleetwise.CfnDecoderManifest.SignalDecodersItemsProperty(
                    fully_qualified_name="fullyQualifiedName",
                    interface_id="interfaceId",
                    type="type",
            
                    # the properties below are optional
                    can_signal=iotfleetwise.CfnDecoderManifest.CanSignalProperty(
                        factor="factor",
                        is_big_endian="isBigEndian",
                        is_signed="isSigned",
                        length="length",
                        message_id="messageId",
                        offset="offset",
                        start_bit="startBit",
            
                        # the properties below are optional
                        name="name"
                    ),
                    obd_signal=iotfleetwise.CfnDecoderManifest.ObdSignalProperty(
                        byte_length="byteLength",
                        offset="offset",
                        pid="pid",
                        pid_response_length="pidResponseLength",
                        scaling="scaling",
                        service_mode="serviceMode",
                        start_byte="startByte",
            
                        # the properties below are optional
                        bit_mask_length="bitMaskLength",
                        bit_right_shift="bitRightShift"
                    )
                )],
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__569ec6ea44200ea874b020dc44809eea72eee555b50cdc8656e558ed1653bb26)
            check_type(argname="argument model_manifest_arn", value=model_manifest_arn, expected_type=type_hints["model_manifest_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
            check_type(argname="argument signal_decoders", value=signal_decoders, expected_type=type_hints["signal_decoders"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "model_manifest_arn": model_manifest_arn,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if network_interfaces is not None:
            self._values["network_interfaces"] = network_interfaces
        if signal_decoders is not None:
            self._values["signal_decoders"] = signal_decoders
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def model_manifest_arn(self) -> builtins.str:
        '''The ARN of a vehicle model (model manifest) associated with the decoder manifest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-modelmanifestarn
        '''
        result = self._values.get("model_manifest_arn")
        assert result is not None, "Required property 'model_manifest_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the decoder manifest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the decoder manifest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interfaces(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDecoderManifest.NetworkInterfacesItemsProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::IoTFleetWise::DecoderManifest.NetworkInterfaces``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-networkinterfaces
        '''
        result = self._values.get("network_interfaces")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDecoderManifest.NetworkInterfacesItemsProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def signal_decoders(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDecoderManifest.SignalDecodersItemsProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::IoTFleetWise::DecoderManifest.SignalDecoders``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-signaldecoders
        '''
        result = self._values.get("signal_decoders")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDecoderManifest.SignalDecodersItemsProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The state of the decoder manifest.

        If the status is ``ACTIVE`` , the decoder manifest can't be edited. If the status is marked ``DRAFT`` , you can edit the decoder manifest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::IoTFleetWise::DecoderManifest.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDecoderManifestProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFleet(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotfleetwise.CfnFleet",
):
    '''A CloudFormation ``AWS::IoTFleetWise::Fleet``.

    Creates a fleet that represents a group of vehicles.
    .. epigraph::

       You must create both a signal catalog and vehicles before you can create a fleet.

    For more information, see `Fleets <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleets.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :cloudformationResource: AWS::IoTFleetWise::Fleet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotfleetwise as iotfleetwise
        
        cfn_fleet = iotfleetwise.CfnFleet(self, "MyCfnFleet",
            id="id",
            signal_catalog_arn="signalCatalogArn",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id_: builtins.str,
        *,
        id: builtins.str,
        signal_catalog_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTFleetWise::Fleet``.

        :param scope: - scope in which this resource is defined.
        :param id_: - scoped id of the resource.
        :param id: The unique ID of the fleet.
        :param signal_catalog_arn: The ARN of the signal catalog associated with the fleet.
        :param description: A brief description of the fleet.
        :param tags: ``AWS::IoTFleetWise::Fleet.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc4563792e7e71428d90b3f55210f042ac37b415f11f16298d546516dc7ffce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = CfnFleetProps(
            id=id,
            signal_catalog_arn=signal_catalog_arn,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb7b647abcb966caa125db58cd283f8214b8b14f0ad51b664a7dd05cd844336a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b4ae548a116a9b3278778dcc4bc58544ed45682bf1f75fea6a840777e28d45e)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModificationTime")
    def attr_last_modification_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: LastModificationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::IoTFleetWise::Fleet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''The unique ID of the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-id
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975249f522e00e0d641c388a14fd235fefdc0e23d0cbeb2c5f70f57067a13507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="signalCatalogArn")
    def signal_catalog_arn(self) -> builtins.str:
        '''The ARN of the signal catalog associated with the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-signalcatalogarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "signalCatalogArn"))

    @signal_catalog_arn.setter
    def signal_catalog_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b2c1322d2ab01a5b6375b016bfb042f680fae9ca4695d5e027ca9878a6d162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signalCatalogArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a28dd550208ea25556d35fd847cda8a66419064e36594b1e931f6b5a6426b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iotfleetwise.CfnFleetProps",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "signal_catalog_arn": "signalCatalogArn",
        "description": "description",
        "tags": "tags",
    },
)
class CfnFleetProps:
    def __init__(
        self,
        *,
        id: builtins.str,
        signal_catalog_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFleet``.

        :param id: The unique ID of the fleet.
        :param signal_catalog_arn: The ARN of the signal catalog associated with the fleet.
        :param description: A brief description of the fleet.
        :param tags: ``AWS::IoTFleetWise::Fleet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotfleetwise as iotfleetwise
            
            cfn_fleet_props = iotfleetwise.CfnFleetProps(
                id="id",
                signal_catalog_arn="signalCatalogArn",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4413fb47b0df2de3acde09efd3170fa1fe100d90b4b61c6c27c330fe6aab04e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument signal_catalog_arn", value=signal_catalog_arn, expected_type=type_hints["signal_catalog_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "signal_catalog_arn": signal_catalog_arn,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique ID of the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-id
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signal_catalog_arn(self) -> builtins.str:
        '''The ARN of the signal catalog associated with the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-signalcatalogarn
        '''
        result = self._values.get("signal_catalog_arn")
        assert result is not None, "Required property 'signal_catalog_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::IoTFleetWise::Fleet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnModelManifest(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotfleetwise.CfnModelManifest",
):
    '''A CloudFormation ``AWS::IoTFleetWise::ModelManifest``.

    Creates a vehicle model (model manifest) that specifies signals (attributes, branches, sensors, and actuators).

    For more information, see `Vehicle models <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/vehicle-models.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :cloudformationResource: AWS::IoTFleetWise::ModelManifest
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotfleetwise as iotfleetwise
        
        cfn_model_manifest = iotfleetwise.CfnModelManifest(self, "MyCfnModelManifest",
            name="name",
            signal_catalog_arn="signalCatalogArn",
        
            # the properties below are optional
            description="description",
            nodes=["nodes"],
            status="status",
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
        signal_catalog_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTFleetWise::ModelManifest``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the vehicle model.
        :param signal_catalog_arn: The ARN of the signal catalog associated with the vehicle model.
        :param description: A brief description of the vehicle model.
        :param nodes: ``AWS::IoTFleetWise::ModelManifest.Nodes``.
        :param status: The state of the vehicle model. If the status is ``ACTIVE`` , the vehicle model can't be edited. If the status is ``DRAFT`` , you can edit the vehicle model.
        :param tags: ``AWS::IoTFleetWise::ModelManifest.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b02ae0a75a63feb3c136d2c3fcc6f81ba3de65a78516a82ff8a47ed81cd4b2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnModelManifestProps(
            name=name,
            signal_catalog_arn=signal_catalog_arn,
            description=description,
            nodes=nodes,
            status=status,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ab04b0c662d6db90a024896f69ec2fddd3c88fe78396b70b90e055b6ba01ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6594bab2cfd9ade3c46534e72f2854f862af6125953803f728abcb63ee7c930e)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModificationTime")
    def attr_last_modification_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: LastModificationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::IoTFleetWise::ModelManifest.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the vehicle model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f1fa793afa08970b3266638d9c5d57c01f9dd28faa5ae232aae60279aa1879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="signalCatalogArn")
    def signal_catalog_arn(self) -> builtins.str:
        '''The ARN of the signal catalog associated with the vehicle model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-signalcatalogarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "signalCatalogArn"))

    @signal_catalog_arn.setter
    def signal_catalog_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad0bb5470e1b5f921c4b28b0e0d44bf056cd3debbb573e274cd821ab45a2da8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signalCatalogArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the vehicle model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af8bb0014f22d61b377aabfd02963589b4ba86b52b635f105e4484640d9f7ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::IoTFleetWise::ModelManifest.Nodes``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-nodes
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nodes"))

    @nodes.setter
    def nodes(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b02781d0161075eac6cf06659c9f6fc35a33c1b36c414ab22296742a42286b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodes", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''The state of the vehicle model.

        If the status is ``ACTIVE`` , the vehicle model can't be edited. If the status is ``DRAFT`` , you can edit the vehicle model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966d704da02de7c15769615345fded070f4efe479cbb37999efc10e0d07f9801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iotfleetwise.CfnModelManifestProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "signal_catalog_arn": "signalCatalogArn",
        "description": "description",
        "nodes": "nodes",
        "status": "status",
        "tags": "tags",
    },
)
class CfnModelManifestProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        signal_catalog_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnModelManifest``.

        :param name: The name of the vehicle model.
        :param signal_catalog_arn: The ARN of the signal catalog associated with the vehicle model.
        :param description: A brief description of the vehicle model.
        :param nodes: ``AWS::IoTFleetWise::ModelManifest.Nodes``.
        :param status: The state of the vehicle model. If the status is ``ACTIVE`` , the vehicle model can't be edited. If the status is ``DRAFT`` , you can edit the vehicle model.
        :param tags: ``AWS::IoTFleetWise::ModelManifest.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotfleetwise as iotfleetwise
            
            cfn_model_manifest_props = iotfleetwise.CfnModelManifestProps(
                name="name",
                signal_catalog_arn="signalCatalogArn",
            
                # the properties below are optional
                description="description",
                nodes=["nodes"],
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a219d5d487efed80061e39daa712d94004ac9331120b13748d5dd6eb5455b425)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument signal_catalog_arn", value=signal_catalog_arn, expected_type=type_hints["signal_catalog_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument nodes", value=nodes, expected_type=type_hints["nodes"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "signal_catalog_arn": signal_catalog_arn,
        }
        if description is not None:
            self._values["description"] = description
        if nodes is not None:
            self._values["nodes"] = nodes
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the vehicle model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signal_catalog_arn(self) -> builtins.str:
        '''The ARN of the signal catalog associated with the vehicle model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-signalcatalogarn
        '''
        result = self._values.get("signal_catalog_arn")
        assert result is not None, "Required property 'signal_catalog_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the vehicle model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nodes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::IoTFleetWise::ModelManifest.Nodes``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-nodes
        '''
        result = self._values.get("nodes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The state of the vehicle model.

        If the status is ``ACTIVE`` , the vehicle model can't be edited. If the status is ``DRAFT`` , you can edit the vehicle model.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::IoTFleetWise::ModelManifest.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnModelManifestProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSignalCatalog(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotfleetwise.CfnSignalCatalog",
):
    '''A CloudFormation ``AWS::IoTFleetWise::SignalCatalog``.

    Creates a collection of standardized signals that can be reused to create vehicle models.

    :cloudformationResource: AWS::IoTFleetWise::SignalCatalog
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotfleetwise as iotfleetwise
        
        cfn_signal_catalog = iotfleetwise.CfnSignalCatalog(self, "MyCfnSignalCatalog",
            description="description",
            name="name",
            node_counts=iotfleetwise.CfnSignalCatalog.NodeCountsProperty(
                total_actuators=123,
                total_attributes=123,
                total_branches=123,
                total_nodes=123,
                total_sensors=123
            ),
            nodes=[iotfleetwise.CfnSignalCatalog.NodeProperty(
                actuator=iotfleetwise.CfnSignalCatalog.ActuatorProperty(
                    data_type="dataType",
                    fully_qualified_name="fullyQualifiedName",
        
                    # the properties below are optional
                    allowed_values=["allowedValues"],
                    assigned_value="assignedValue",
                    description="description",
                    max=123,
                    min=123,
                    unit="unit"
                ),
                attribute=iotfleetwise.CfnSignalCatalog.AttributeProperty(
                    data_type="dataType",
                    fully_qualified_name="fullyQualifiedName",
        
                    # the properties below are optional
                    allowed_values=["allowedValues"],
                    assigned_value="assignedValue",
                    default_value="defaultValue",
                    description="description",
                    max=123,
                    min=123,
                    unit="unit"
                ),
                branch=iotfleetwise.CfnSignalCatalog.BranchProperty(
                    fully_qualified_name="fullyQualifiedName",
        
                    # the properties below are optional
                    description="description"
                ),
                sensor=iotfleetwise.CfnSignalCatalog.SensorProperty(
                    data_type="dataType",
                    fully_qualified_name="fullyQualifiedName",
        
                    # the properties below are optional
                    allowed_values=["allowedValues"],
                    description="description",
                    max=123,
                    min=123,
                    unit="unit"
                )
            )],
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
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        node_counts: typing.Optional[typing.Union[typing.Union["CfnSignalCatalog.NodeCountsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        nodes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnSignalCatalog.NodeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTFleetWise::SignalCatalog``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::IoTFleetWise::SignalCatalog.Description``.
        :param name: The name of the signal catalog.
        :param node_counts: ``AWS::IoTFleetWise::SignalCatalog.NodeCounts``.
        :param nodes: ``AWS::IoTFleetWise::SignalCatalog.Nodes``.
        :param tags: ``AWS::IoTFleetWise::SignalCatalog.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b893f0439f4cca922b1ab6f883b6aef8edab3157de46d42f1b00071c314a27a2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSignalCatalogProps(
            description=description,
            name=name,
            node_counts=node_counts,
            nodes=nodes,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74221350fadd4443f89253fc71451a5ce131773fa492abb43a3519f4506f83ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__225a5f02eba21fabadfa34ebaa51b61ac0a6569088763e7833123395dc273b42)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModificationTime")
    def attr_last_modification_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: LastModificationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrNodeCountsTotalActuators")
    def attr_node_counts_total_actuators(self) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: NodeCounts.TotalActuators
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrNodeCountsTotalActuators"))

    @builtins.property
    @jsii.member(jsii_name="attrNodeCountsTotalAttributes")
    def attr_node_counts_total_attributes(self) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: NodeCounts.TotalAttributes
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrNodeCountsTotalAttributes"))

    @builtins.property
    @jsii.member(jsii_name="attrNodeCountsTotalBranches")
    def attr_node_counts_total_branches(self) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: NodeCounts.TotalBranches
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrNodeCountsTotalBranches"))

    @builtins.property
    @jsii.member(jsii_name="attrNodeCountsTotalNodes")
    def attr_node_counts_total_nodes(self) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: NodeCounts.TotalNodes
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrNodeCountsTotalNodes"))

    @builtins.property
    @jsii.member(jsii_name="attrNodeCountsTotalSensors")
    def attr_node_counts_total_sensors(self) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: NodeCounts.TotalSensors
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrNodeCountsTotalSensors"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::IoTFleetWise::SignalCatalog.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::SignalCatalog.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5f0fa3eab22d8c57599c90df05b68a5911c564de701f9a2c43ae389005c42e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the signal catalog.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e28223c7175931ac8a27cda4dc362d0ec7b18f03a0694f1d29c53744148985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nodeCounts")
    def node_counts(
        self,
    ) -> typing.Optional[typing.Union["CfnSignalCatalog.NodeCountsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::IoTFleetWise::SignalCatalog.NodeCounts``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-nodecounts
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSignalCatalog.NodeCountsProperty", _IResolvable_a771d0ef]], jsii.get(self, "nodeCounts"))

    @node_counts.setter
    def node_counts(
        self,
        value: typing.Optional[typing.Union["CfnSignalCatalog.NodeCountsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020a82e341463b102ac595a8ddfdb0cd2492faf08e68c7ae43d554f1397e9880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCounts", value)

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSignalCatalog.NodeProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::IoTFleetWise::SignalCatalog.Nodes``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-nodes
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSignalCatalog.NodeProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "nodes"))

    @nodes.setter
    def nodes(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSignalCatalog.NodeProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5275b6c2afac9469e5e3052457a1fb7cdbba14ad2116191344b81ec573a5053e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodes", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnSignalCatalog.ActuatorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_type": "dataType",
            "fully_qualified_name": "fullyQualifiedName",
            "allowed_values": "allowedValues",
            "assigned_value": "assignedValue",
            "description": "description",
            "max": "max",
            "min": "min",
            "unit": "unit",
        },
    )
    class ActuatorProperty:
        def __init__(
            self,
            *,
            data_type: builtins.str,
            fully_qualified_name: builtins.str,
            allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            assigned_value: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A signal that represents a vehicle device such as the engine, heater, and door locks.

            Data from an actuator reports the state of a certain vehicle device.
            .. epigraph::

               Updating actuator data can change the state of a device. For example, you can turn on or off the heater by updating its actuator data.

            :param data_type: The specified data type of the actuator.
            :param fully_qualified_name: The fully qualified name of the actuator. For example, the fully qualified name of an actuator might be ``Vehicle.Front.Left.Door.Lock`` .
            :param allowed_values: A list of possible values an actuator can take.
            :param assigned_value: A specified value for the actuator.
            :param description: A brief description of the actuator.
            :param max: The specified possible maximum value of an actuator.
            :param min: The specified possible minimum value of an actuator.
            :param unit: The scientific unit for the actuator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                actuator_property = iotfleetwise.CfnSignalCatalog.ActuatorProperty(
                    data_type="dataType",
                    fully_qualified_name="fullyQualifiedName",
                
                    # the properties below are optional
                    allowed_values=["allowedValues"],
                    assigned_value="assignedValue",
                    description="description",
                    max=123,
                    min=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__29779cd7804fa9caba59eda5f2576e5448f5a95423003aa9cff3d76393f2b471)
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument assigned_value", value=assigned_value, expected_type=type_hints["assigned_value"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_type": data_type,
                "fully_qualified_name": fully_qualified_name,
            }
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if assigned_value is not None:
                self._values["assigned_value"] = assigned_value
            if description is not None:
                self._values["description"] = description
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def data_type(self) -> builtins.str:
            '''The specified data type of the actuator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-datatype
            '''
            result = self._values.get("data_type")
            assert result is not None, "Required property 'data_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def fully_qualified_name(self) -> builtins.str:
            '''The fully qualified name of the actuator.

            For example, the fully qualified name of an actuator might be ``Vehicle.Front.Left.Door.Lock`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            assert result is not None, "Required property 'fully_qualified_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of possible values an actuator can take.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def assigned_value(self) -> typing.Optional[builtins.str]:
            '''A specified value for the actuator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-assignedvalue
            '''
            result = self._values.get("assigned_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A brief description of the actuator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The specified possible maximum value of an actuator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The specified possible minimum value of an actuator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The scientific unit for the actuator.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActuatorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnSignalCatalog.AttributeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_type": "dataType",
            "fully_qualified_name": "fullyQualifiedName",
            "allowed_values": "allowedValues",
            "assigned_value": "assignedValue",
            "default_value": "defaultValue",
            "description": "description",
            "max": "max",
            "min": "min",
            "unit": "unit",
        },
    )
    class AttributeProperty:
        def __init__(
            self,
            *,
            data_type: builtins.str,
            fully_qualified_name: builtins.str,
            allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            assigned_value: typing.Optional[builtins.str] = None,
            default_value: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A signal that represents static information about the vehicle, such as engine type or manufacturing date.

            :param data_type: The specified data type of the attribute.
            :param fully_qualified_name: The fully qualified name of the attribute. For example, the fully qualified name of an attribute might be ``Vehicle.Body.Engine.Type`` .
            :param allowed_values: A list of possible values an attribute can be assigned.
            :param assigned_value: A specified value for the attribute.
            :param default_value: The default value of the attribute.
            :param description: A brief description of the attribute.
            :param max: The specified possible maximum value of the attribute.
            :param min: The specified possible minimum value of the attribute.
            :param unit: The scientific unit for the attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                attribute_property = iotfleetwise.CfnSignalCatalog.AttributeProperty(
                    data_type="dataType",
                    fully_qualified_name="fullyQualifiedName",
                
                    # the properties below are optional
                    allowed_values=["allowedValues"],
                    assigned_value="assignedValue",
                    default_value="defaultValue",
                    description="description",
                    max=123,
                    min=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51bb5dfd4926d4570aa227b8747fb0b557bc00076095551123b5f63568152634)
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument assigned_value", value=assigned_value, expected_type=type_hints["assigned_value"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_type": data_type,
                "fully_qualified_name": fully_qualified_name,
            }
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if assigned_value is not None:
                self._values["assigned_value"] = assigned_value
            if default_value is not None:
                self._values["default_value"] = default_value
            if description is not None:
                self._values["description"] = description
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def data_type(self) -> builtins.str:
            '''The specified data type of the attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-datatype
            '''
            result = self._values.get("data_type")
            assert result is not None, "Required property 'data_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def fully_qualified_name(self) -> builtins.str:
            '''The fully qualified name of the attribute.

            For example, the fully qualified name of an attribute might be ``Vehicle.Body.Engine.Type`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            assert result is not None, "Required property 'fully_qualified_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of possible values an attribute can be assigned.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def assigned_value(self) -> typing.Optional[builtins.str]:
            '''A specified value for the attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-assignedvalue
            '''
            result = self._values.get("assigned_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value of the attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A brief description of the attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The specified possible maximum value of the attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The specified possible minimum value of the attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The scientific unit for the attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnSignalCatalog.BranchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "fully_qualified_name": "fullyQualifiedName",
            "description": "description",
        },
    )
    class BranchProperty:
        def __init__(
            self,
            *,
            fully_qualified_name: builtins.str,
            description: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A group of signals that are defined in a hierarchical structure.

            :param fully_qualified_name: The fully qualified name of the branch. For example, the fully qualified name of a branch might be ``Vehicle.Body.Engine`` .
            :param description: A brief description of the branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-branch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                branch_property = iotfleetwise.CfnSignalCatalog.BranchProperty(
                    fully_qualified_name="fullyQualifiedName",
                
                    # the properties below are optional
                    description="description"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea8d3abd4726d0f0da78f1ca34fc36314c43533f8410cadee62b0b91d3e452c1)
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "fully_qualified_name": fully_qualified_name,
            }
            if description is not None:
                self._values["description"] = description

        @builtins.property
        def fully_qualified_name(self) -> builtins.str:
            '''The fully qualified name of the branch.

            For example, the fully qualified name of a branch might be ``Vehicle.Body.Engine`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-branch.html#cfn-iotfleetwise-signalcatalog-branch-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            assert result is not None, "Required property 'fully_qualified_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A brief description of the branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-branch.html#cfn-iotfleetwise-signalcatalog-branch-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BranchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnSignalCatalog.NodeCountsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "total_actuators": "totalActuators",
            "total_attributes": "totalAttributes",
            "total_branches": "totalBranches",
            "total_nodes": "totalNodes",
            "total_sensors": "totalSensors",
        },
    )
    class NodeCountsProperty:
        def __init__(
            self,
            *,
            total_actuators: typing.Optional[jsii.Number] = None,
            total_attributes: typing.Optional[jsii.Number] = None,
            total_branches: typing.Optional[jsii.Number] = None,
            total_nodes: typing.Optional[jsii.Number] = None,
            total_sensors: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about the number of nodes and node types in a vehicle network.

            :param total_actuators: The total number of nodes in a vehicle network that represent actuators.
            :param total_attributes: The total number of nodes in a vehicle network that represent attributes.
            :param total_branches: The total number of nodes in a vehicle network that represent branches.
            :param total_nodes: The total number of nodes in a vehicle network.
            :param total_sensors: The total number of nodes in a vehicle network that represent sensors.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                node_counts_property = iotfleetwise.CfnSignalCatalog.NodeCountsProperty(
                    total_actuators=123,
                    total_attributes=123,
                    total_branches=123,
                    total_nodes=123,
                    total_sensors=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2b361fd2dd1ad9193e312728642ac284acbf701ee00b5c4a2abab449713be46)
                check_type(argname="argument total_actuators", value=total_actuators, expected_type=type_hints["total_actuators"])
                check_type(argname="argument total_attributes", value=total_attributes, expected_type=type_hints["total_attributes"])
                check_type(argname="argument total_branches", value=total_branches, expected_type=type_hints["total_branches"])
                check_type(argname="argument total_nodes", value=total_nodes, expected_type=type_hints["total_nodes"])
                check_type(argname="argument total_sensors", value=total_sensors, expected_type=type_hints["total_sensors"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if total_actuators is not None:
                self._values["total_actuators"] = total_actuators
            if total_attributes is not None:
                self._values["total_attributes"] = total_attributes
            if total_branches is not None:
                self._values["total_branches"] = total_branches
            if total_nodes is not None:
                self._values["total_nodes"] = total_nodes
            if total_sensors is not None:
                self._values["total_sensors"] = total_sensors

        @builtins.property
        def total_actuators(self) -> typing.Optional[jsii.Number]:
            '''The total number of nodes in a vehicle network that represent actuators.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html#cfn-iotfleetwise-signalcatalog-nodecounts-totalactuators
            '''
            result = self._values.get("total_actuators")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total_attributes(self) -> typing.Optional[jsii.Number]:
            '''The total number of nodes in a vehicle network that represent attributes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html#cfn-iotfleetwise-signalcatalog-nodecounts-totalattributes
            '''
            result = self._values.get("total_attributes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total_branches(self) -> typing.Optional[jsii.Number]:
            '''The total number of nodes in a vehicle network that represent branches.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html#cfn-iotfleetwise-signalcatalog-nodecounts-totalbranches
            '''
            result = self._values.get("total_branches")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total_nodes(self) -> typing.Optional[jsii.Number]:
            '''The total number of nodes in a vehicle network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html#cfn-iotfleetwise-signalcatalog-nodecounts-totalnodes
            '''
            result = self._values.get("total_nodes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total_sensors(self) -> typing.Optional[jsii.Number]:
            '''The total number of nodes in a vehicle network that represent sensors.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html#cfn-iotfleetwise-signalcatalog-nodecounts-totalsensors
            '''
            result = self._values.get("total_sensors")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeCountsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnSignalCatalog.NodeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actuator": "actuator",
            "attribute": "attribute",
            "branch": "branch",
            "sensor": "sensor",
        },
    )
    class NodeProperty:
        def __init__(
            self,
            *,
            actuator: typing.Optional[typing.Union[typing.Union["CfnSignalCatalog.ActuatorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            attribute: typing.Optional[typing.Union[typing.Union["CfnSignalCatalog.AttributeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            branch: typing.Optional[typing.Union[typing.Union["CfnSignalCatalog.BranchProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sensor: typing.Optional[typing.Union[typing.Union["CfnSignalCatalog.SensorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''A general abstraction of a signal.

            A node can be specified as an actuator, attribute, branch, or sensor.

            :param actuator: Information about a node specified as an actuator. .. epigraph:: An actuator is a digital representation of a vehicle device.
            :param attribute: Information about a node specified as an attribute. .. epigraph:: An attribute represents static information about a vehicle.
            :param branch: Information about a node specified as a branch. .. epigraph:: A group of signals that are defined in a hierarchical structure.
            :param sensor: ``CfnSignalCatalog.NodeProperty.Sensor``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-node.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                node_property = iotfleetwise.CfnSignalCatalog.NodeProperty(
                    actuator=iotfleetwise.CfnSignalCatalog.ActuatorProperty(
                        data_type="dataType",
                        fully_qualified_name="fullyQualifiedName",
                
                        # the properties below are optional
                        allowed_values=["allowedValues"],
                        assigned_value="assignedValue",
                        description="description",
                        max=123,
                        min=123,
                        unit="unit"
                    ),
                    attribute=iotfleetwise.CfnSignalCatalog.AttributeProperty(
                        data_type="dataType",
                        fully_qualified_name="fullyQualifiedName",
                
                        # the properties below are optional
                        allowed_values=["allowedValues"],
                        assigned_value="assignedValue",
                        default_value="defaultValue",
                        description="description",
                        max=123,
                        min=123,
                        unit="unit"
                    ),
                    branch=iotfleetwise.CfnSignalCatalog.BranchProperty(
                        fully_qualified_name="fullyQualifiedName",
                
                        # the properties below are optional
                        description="description"
                    ),
                    sensor=iotfleetwise.CfnSignalCatalog.SensorProperty(
                        data_type="dataType",
                        fully_qualified_name="fullyQualifiedName",
                
                        # the properties below are optional
                        allowed_values=["allowedValues"],
                        description="description",
                        max=123,
                        min=123,
                        unit="unit"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27d6bed217354b0750bcb825302cab5c857c527abc610fd0a00970db0663415d)
                check_type(argname="argument actuator", value=actuator, expected_type=type_hints["actuator"])
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
                check_type(argname="argument sensor", value=sensor, expected_type=type_hints["sensor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actuator is not None:
                self._values["actuator"] = actuator
            if attribute is not None:
                self._values["attribute"] = attribute
            if branch is not None:
                self._values["branch"] = branch
            if sensor is not None:
                self._values["sensor"] = sensor

        @builtins.property
        def actuator(
            self,
        ) -> typing.Optional[typing.Union["CfnSignalCatalog.ActuatorProperty", _IResolvable_a771d0ef]]:
            '''Information about a node specified as an actuator.

            .. epigraph::

               An actuator is a digital representation of a vehicle device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-node.html#cfn-iotfleetwise-signalcatalog-node-actuator
            '''
            result = self._values.get("actuator")
            return typing.cast(typing.Optional[typing.Union["CfnSignalCatalog.ActuatorProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def attribute(
            self,
        ) -> typing.Optional[typing.Union["CfnSignalCatalog.AttributeProperty", _IResolvable_a771d0ef]]:
            '''Information about a node specified as an attribute.

            .. epigraph::

               An attribute represents static information about a vehicle.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-node.html#cfn-iotfleetwise-signalcatalog-node-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[typing.Union["CfnSignalCatalog.AttributeProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def branch(
            self,
        ) -> typing.Optional[typing.Union["CfnSignalCatalog.BranchProperty", _IResolvable_a771d0ef]]:
            '''Information about a node specified as a branch.

            .. epigraph::

               A group of signals that are defined in a hierarchical structure.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-node.html#cfn-iotfleetwise-signalcatalog-node-branch
            '''
            result = self._values.get("branch")
            return typing.cast(typing.Optional[typing.Union["CfnSignalCatalog.BranchProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sensor(
            self,
        ) -> typing.Optional[typing.Union["CfnSignalCatalog.SensorProperty", _IResolvable_a771d0ef]]:
            '''``CfnSignalCatalog.NodeProperty.Sensor``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-node.html#cfn-iotfleetwise-signalcatalog-node-sensor
            '''
            result = self._values.get("sensor")
            return typing.cast(typing.Optional[typing.Union["CfnSignalCatalog.SensorProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotfleetwise.CfnSignalCatalog.SensorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_type": "dataType",
            "fully_qualified_name": "fullyQualifiedName",
            "allowed_values": "allowedValues",
            "description": "description",
            "max": "max",
            "min": "min",
            "unit": "unit",
        },
    )
    class SensorProperty:
        def __init__(
            self,
            *,
            data_type: builtins.str,
            fully_qualified_name: builtins.str,
            allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            description: typing.Optional[builtins.str] = None,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An input component that reports the environmental condition of a vehicle.

            .. epigraph::

               You can collect data about fluid levels, temperatures, vibrations, or battery voltage from sensors.

            :param data_type: The specified data type of the sensor.
            :param fully_qualified_name: The fully qualified name of the sensor. For example, the fully qualified name of a sensor might be ``Vehicle.Body.Engine.Battery`` .
            :param allowed_values: A list of possible values a sensor can take.
            :param description: A brief description of a sensor.
            :param max: The specified possible maximum value of the sensor.
            :param min: The specified possible minimum value of the sensor.
            :param unit: The scientific unit of measurement for data collected by the sensor.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iotfleetwise as iotfleetwise
                
                sensor_property = iotfleetwise.CfnSignalCatalog.SensorProperty(
                    data_type="dataType",
                    fully_qualified_name="fullyQualifiedName",
                
                    # the properties below are optional
                    allowed_values=["allowedValues"],
                    description="description",
                    max=123,
                    min=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8e19129731b60998cba6035a76a71fe0f793308a5d216698040cda099db7edf)
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_type": data_type,
                "fully_qualified_name": fully_qualified_name,
            }
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if description is not None:
                self._values["description"] = description
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def data_type(self) -> builtins.str:
            '''The specified data type of the sensor.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-datatype
            '''
            result = self._values.get("data_type")
            assert result is not None, "Required property 'data_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def fully_qualified_name(self) -> builtins.str:
            '''The fully qualified name of the sensor.

            For example, the fully qualified name of a sensor might be ``Vehicle.Body.Engine.Battery`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            assert result is not None, "Required property 'fully_qualified_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of possible values a sensor can take.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A brief description of a sensor.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The specified possible maximum value of the sensor.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The specified possible minimum value of the sensor.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The scientific unit of measurement for data collected by the sensor.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SensorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotfleetwise.CfnSignalCatalogProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "node_counts": "nodeCounts",
        "nodes": "nodes",
        "tags": "tags",
    },
)
class CfnSignalCatalogProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        node_counts: typing.Optional[typing.Union[typing.Union[CfnSignalCatalog.NodeCountsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        nodes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSignalCatalog.NodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSignalCatalog``.

        :param description: ``AWS::IoTFleetWise::SignalCatalog.Description``.
        :param name: The name of the signal catalog.
        :param node_counts: ``AWS::IoTFleetWise::SignalCatalog.NodeCounts``.
        :param nodes: ``AWS::IoTFleetWise::SignalCatalog.Nodes``.
        :param tags: ``AWS::IoTFleetWise::SignalCatalog.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotfleetwise as iotfleetwise
            
            cfn_signal_catalog_props = iotfleetwise.CfnSignalCatalogProps(
                description="description",
                name="name",
                node_counts=iotfleetwise.CfnSignalCatalog.NodeCountsProperty(
                    total_actuators=123,
                    total_attributes=123,
                    total_branches=123,
                    total_nodes=123,
                    total_sensors=123
                ),
                nodes=[iotfleetwise.CfnSignalCatalog.NodeProperty(
                    actuator=iotfleetwise.CfnSignalCatalog.ActuatorProperty(
                        data_type="dataType",
                        fully_qualified_name="fullyQualifiedName",
            
                        # the properties below are optional
                        allowed_values=["allowedValues"],
                        assigned_value="assignedValue",
                        description="description",
                        max=123,
                        min=123,
                        unit="unit"
                    ),
                    attribute=iotfleetwise.CfnSignalCatalog.AttributeProperty(
                        data_type="dataType",
                        fully_qualified_name="fullyQualifiedName",
            
                        # the properties below are optional
                        allowed_values=["allowedValues"],
                        assigned_value="assignedValue",
                        default_value="defaultValue",
                        description="description",
                        max=123,
                        min=123,
                        unit="unit"
                    ),
                    branch=iotfleetwise.CfnSignalCatalog.BranchProperty(
                        fully_qualified_name="fullyQualifiedName",
            
                        # the properties below are optional
                        description="description"
                    ),
                    sensor=iotfleetwise.CfnSignalCatalog.SensorProperty(
                        data_type="dataType",
                        fully_qualified_name="fullyQualifiedName",
            
                        # the properties below are optional
                        allowed_values=["allowedValues"],
                        description="description",
                        max=123,
                        min=123,
                        unit="unit"
                    )
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8576e6ed9a3eab7ee1395e3e3fe2c07fa13c4c413b5752eb36572559dc5cc1c1)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_counts", value=node_counts, expected_type=type_hints["node_counts"])
            check_type(argname="argument nodes", value=nodes, expected_type=type_hints["nodes"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if node_counts is not None:
            self._values["node_counts"] = node_counts
        if nodes is not None:
            self._values["nodes"] = nodes
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::IoTFleetWise::SignalCatalog.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the signal catalog.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_counts(
        self,
    ) -> typing.Optional[typing.Union[CfnSignalCatalog.NodeCountsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::IoTFleetWise::SignalCatalog.NodeCounts``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-nodecounts
        '''
        result = self._values.get("node_counts")
        return typing.cast(typing.Optional[typing.Union[CfnSignalCatalog.NodeCountsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def nodes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSignalCatalog.NodeProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::IoTFleetWise::SignalCatalog.Nodes``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-nodes
        '''
        result = self._values.get("nodes")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSignalCatalog.NodeProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::IoTFleetWise::SignalCatalog.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSignalCatalogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnVehicle(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotfleetwise.CfnVehicle",
):
    '''A CloudFormation ``AWS::IoTFleetWise::Vehicle``.

    Creates a vehicle, which is an instance of a vehicle model (model manifest). Vehicles created from the same vehicle model consist of the same signals inherited from the vehicle model.
    .. epigraph::

       If you have an existing AWS IoT Thing, you can use AWS IoT FleetWise to create a vehicle and collect data from your thing.

    For more information, see `Create a vehicle (CLI) <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/create-vehicle-cli.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :cloudformationResource: AWS::IoTFleetWise::Vehicle
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iotfleetwise as iotfleetwise
        
        cfn_vehicle = iotfleetwise.CfnVehicle(self, "MyCfnVehicle",
            decoder_manifest_arn="decoderManifestArn",
            model_manifest_arn="modelManifestArn",
            name="name",
        
            # the properties below are optional
            association_behavior="associationBehavior",
            attributes={
                "attributes_key": "attributes"
            },
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
        decoder_manifest_arn: builtins.str,
        model_manifest_arn: builtins.str,
        name: builtins.str,
        association_behavior: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTFleetWise::Vehicle``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param decoder_manifest_arn: The Amazon Resource Name (ARN) of a decoder manifest associated with the vehicle to create.
        :param model_manifest_arn: The ARN of the vehicle model (model manifest) to create the vehicle from.
        :param name: ``AWS::IoTFleetWise::Vehicle.Name``.
        :param association_behavior: An option to create a new AWS IoT thing when creating a vehicle, or to validate an existing thing as a vehicle.
        :param attributes: Static information about a vehicle in a key-value pair. For example: ``"engine Type"`` : ``"v6"``
        :param tags: Metadata which can be used to manage the vehicle.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34d549696e1dd2eb7ccd43d3c740231cc42ab6102bd1b5376caff9393bebdc3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVehicleProps(
            decoder_manifest_arn=decoder_manifest_arn,
            model_manifest_arn=model_manifest_arn,
            name=name,
            association_behavior=association_behavior,
            attributes=attributes,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984c32b24cb897cf030bc2fe52cac8e0f379c4994fdc681ffc171c6407e36240)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db65b94faaf42495a81b8e28f38c9c540099cc6b32385ad3d22228b433741ea8)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModificationTime")
    def attr_last_modification_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: LastModificationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Metadata which can be used to manage the vehicle.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="decoderManifestArn")
    def decoder_manifest_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of a decoder manifest associated with the vehicle to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-decodermanifestarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "decoderManifestArn"))

    @decoder_manifest_arn.setter
    def decoder_manifest_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ddd8147ec8acbc59d4059a06ee514a730acc169424ee4b4f89145a154736859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "decoderManifestArn", value)

    @builtins.property
    @jsii.member(jsii_name="modelManifestArn")
    def model_manifest_arn(self) -> builtins.str:
        '''The ARN of the vehicle model (model manifest) to create the vehicle from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-modelmanifestarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "modelManifestArn"))

    @model_manifest_arn.setter
    def model_manifest_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a781a90b6626efdd6fd70d7ff7960a2fb2d5f09ab1ebbdac3affba0e0bb3fa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelManifestArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::IoTFleetWise::Vehicle.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2fcd4279d56b9dc300a41f30d0bb6d66d7dd6a5a6d9d78ca83a3ec28a0e2c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="associationBehavior")
    def association_behavior(self) -> typing.Optional[builtins.str]:
        '''An option to create a new AWS IoT thing when creating a vehicle, or to validate an existing thing as a vehicle.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-associationbehavior
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "associationBehavior"))

    @association_behavior.setter
    def association_behavior(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2cdd2821a0cdd669268bc40715d9ac5c762681bf1d5b5727f8aae8b114a8a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associationBehavior", value)

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''Static information about a vehicle in a key-value pair.

        For example: ``"engine Type"`` : ``"v6"``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-attributes
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33bf674fae93670fcc31ed144370b884508fcb231e2ff4264b6bb12b5cf2f8e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iotfleetwise.CfnVehicleProps",
    jsii_struct_bases=[],
    name_mapping={
        "decoder_manifest_arn": "decoderManifestArn",
        "model_manifest_arn": "modelManifestArn",
        "name": "name",
        "association_behavior": "associationBehavior",
        "attributes": "attributes",
        "tags": "tags",
    },
)
class CfnVehicleProps:
    def __init__(
        self,
        *,
        decoder_manifest_arn: builtins.str,
        model_manifest_arn: builtins.str,
        name: builtins.str,
        association_behavior: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnVehicle``.

        :param decoder_manifest_arn: The Amazon Resource Name (ARN) of a decoder manifest associated with the vehicle to create.
        :param model_manifest_arn: The ARN of the vehicle model (model manifest) to create the vehicle from.
        :param name: ``AWS::IoTFleetWise::Vehicle.Name``.
        :param association_behavior: An option to create a new AWS IoT thing when creating a vehicle, or to validate an existing thing as a vehicle.
        :param attributes: Static information about a vehicle in a key-value pair. For example: ``"engine Type"`` : ``"v6"``
        :param tags: Metadata which can be used to manage the vehicle.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iotfleetwise as iotfleetwise
            
            cfn_vehicle_props = iotfleetwise.CfnVehicleProps(
                decoder_manifest_arn="decoderManifestArn",
                model_manifest_arn="modelManifestArn",
                name="name",
            
                # the properties below are optional
                association_behavior="associationBehavior",
                attributes={
                    "attributes_key": "attributes"
                },
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58443223259b53f3d81b68c4dccfca6763b4be9f67f9d05c4be63ebcf99db4c8)
            check_type(argname="argument decoder_manifest_arn", value=decoder_manifest_arn, expected_type=type_hints["decoder_manifest_arn"])
            check_type(argname="argument model_manifest_arn", value=model_manifest_arn, expected_type=type_hints["model_manifest_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument association_behavior", value=association_behavior, expected_type=type_hints["association_behavior"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "decoder_manifest_arn": decoder_manifest_arn,
            "model_manifest_arn": model_manifest_arn,
            "name": name,
        }
        if association_behavior is not None:
            self._values["association_behavior"] = association_behavior
        if attributes is not None:
            self._values["attributes"] = attributes
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def decoder_manifest_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of a decoder manifest associated with the vehicle to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-decodermanifestarn
        '''
        result = self._values.get("decoder_manifest_arn")
        assert result is not None, "Required property 'decoder_manifest_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def model_manifest_arn(self) -> builtins.str:
        '''The ARN of the vehicle model (model manifest) to create the vehicle from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-modelmanifestarn
        '''
        result = self._values.get("model_manifest_arn")
        assert result is not None, "Required property 'model_manifest_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::IoTFleetWise::Vehicle.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def association_behavior(self) -> typing.Optional[builtins.str]:
        '''An option to create a new AWS IoT thing when creating a vehicle, or to validate an existing thing as a vehicle.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-associationbehavior
        '''
        result = self._values.get("association_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''Static information about a vehicle in a key-value pair.

        For example: ``"engine Type"`` : ``"v6"``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Metadata which can be used to manage the vehicle.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVehicleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCampaign",
    "CfnCampaignProps",
    "CfnDecoderManifest",
    "CfnDecoderManifestProps",
    "CfnFleet",
    "CfnFleetProps",
    "CfnModelManifest",
    "CfnModelManifestProps",
    "CfnSignalCatalog",
    "CfnSignalCatalogProps",
    "CfnVehicle",
    "CfnVehicleProps",
]

publication.publish()

def _typecheckingstub__23fb5b8b308cea60def7e8ab524ba9ce7d68b68dc228aaabed8e56c49e440e32(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    action: builtins.str,
    collection_scheme: typing.Union[typing.Union[CfnCampaign.CollectionSchemeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    name: builtins.str,
    signal_catalog_arn: builtins.str,
    target_arn: builtins.str,
    compression: typing.Optional[builtins.str] = None,
    data_extra_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    diagnostics_mode: typing.Optional[builtins.str] = None,
    expiry_time: typing.Optional[builtins.str] = None,
    post_trigger_collection_duration: typing.Optional[jsii.Number] = None,
    priority: typing.Optional[jsii.Number] = None,
    signals_to_collect: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCampaign.SignalInformationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    spooling_mode: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2b5b87334c7d8908c366b7fd5bcb53ad8b6a4d360beefb0721f54aa1eae376(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a341fbbf10ee78bbb6df8a89129093fd4e68b826f8eb9b4cf6ac256cbcdf3d74(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8069aecac51432040b50d2f942c1e9ca693651d326ba63cb1c2099f5ab4de6c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d3d042366d3968155052e581b0e1fef6462d55212dac2c6db452696d285ff5(
    value: typing.Union[CfnCampaign.CollectionSchemeProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4568ff1b08bb4e6acfd7c7117b90cd8c1057ff8c429d8dee80d980d6ba2abac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051e5978f1fa221d2e6d45370c92e40024163f2be063bfb881d2a87edce51d7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc20a3f1c4a0f787b36e5cc11d85f4d6fa0f621ae191fd1e8101247a1df26921(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3adf71168f42588adb1d327751271901791b601390b349666a3cc3b19fe99c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa9be0e7b5a1584ebe0567fc40f45eaca67b8e9f59188e2b88f9d0c32f8fda4(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad977b5d83868394a340be235c962dcd4901c6a0b4debca793cb01befbf19c7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f48fe4cd6504918fefbddd9f256fa6198500c95c8b6a7b25e533ea68e5b8577(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdc3ea623979aef49baa7df521355733011783f0d1614c94372bd5fd1795ab2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f80d4c4545451dafc1e756c63e48891d753b5c0656015573c1bcb9befc47f53(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409a484a01fe8caf68feee528a572a31da781fb397ba3251b42fa8bcbe40ded0(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa37b449763b5d51c7c3c884317240d1cfc64b697b350f38a1bc40b40ad1889(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCampaign.SignalInformationProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa48a59fd3cce9f9f3faf148063f7f16c9867c9a3b29ed31c7ddb2d67f3ed7e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e1018486d554c86b80477ccdeafaa196370d881b5cf78eb0b8b01a67571912(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b56c9bb346ba87ddc3e19d1af22b043dc61283010aab82dc4a2c616c6c4518(
    *,
    condition_based_collection_scheme: typing.Optional[typing.Union[typing.Union[CfnCampaign.ConditionBasedCollectionSchemeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    time_based_collection_scheme: typing.Optional[typing.Union[typing.Union[CfnCampaign.TimeBasedCollectionSchemeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd0fa2589ce7eec396519a2434c76197a9ed96e8d72967dbb4efaa1b1b3d62c(
    *,
    expression: builtins.str,
    condition_language_version: typing.Optional[jsii.Number] = None,
    minimum_trigger_interval_ms: typing.Optional[jsii.Number] = None,
    trigger_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf093984560e2a6848a9799e8e77c9616ab738b681d9e926d0bfe402fd1f944(
    *,
    name: builtins.str,
    max_sample_count: typing.Optional[jsii.Number] = None,
    minimum_sampling_interval_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57942af51326d4694e6ca7673d698b49c973b85ea417cc0a8637a76aa8cc1f55(
    *,
    period_ms: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3664a47dbea9aaeff9dd1e4d284f16659bd0deb9998412e7c7d3a778b2201c(
    *,
    action: builtins.str,
    collection_scheme: typing.Union[typing.Union[CfnCampaign.CollectionSchemeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    name: builtins.str,
    signal_catalog_arn: builtins.str,
    target_arn: builtins.str,
    compression: typing.Optional[builtins.str] = None,
    data_extra_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    diagnostics_mode: typing.Optional[builtins.str] = None,
    expiry_time: typing.Optional[builtins.str] = None,
    post_trigger_collection_duration: typing.Optional[jsii.Number] = None,
    priority: typing.Optional[jsii.Number] = None,
    signals_to_collect: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCampaign.SignalInformationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    spooling_mode: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65eedd006d93da34fc3cf09875b1f01a065dbaf025b1990760b62aaf8ed1d36c(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    model_manifest_arn: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    network_interfaces: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDecoderManifest.NetworkInterfacesItemsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    signal_decoders: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDecoderManifest.SignalDecodersItemsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7ea38fd2de65fe6d0eb61eaddaa019a8eb99f9256d4f6ea66b2e22e047907b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ebae224fab3d79a355d7bfc627c5fe1b03871e25d1e6c4ab54657a50b0e622f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fdb67ee57f7e65bff1dfd07a47d9dcc70dea640ee3ad1f04f134c709c0d1948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabe8a7f451a2ea9f9aad901ee8e25c3d9deabe4d1745fac24ace65db1299cc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b08751fb43386f0c1cfec714d2857b0823eff2345b77c5383f43edf9cd26ac(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad474a55a88a68be702bd6e73a517b2c1f93ff4046aaefd058db5b6c01f5481(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDecoderManifest.NetworkInterfacesItemsProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd7961b3f92b2eb03740b49a3f30d6d39716bdc118d6ba066f430d142b87a69(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDecoderManifest.SignalDecodersItemsProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02bcaa42a4f4cb65c3031fea856238019ce3f51a316186ff29073827d3938ef(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0129222cfd471bc80e18a5b14c99c724f83445e97e1dafd4c53bd63e4ca28bfa(
    *,
    name: builtins.str,
    protocol_name: typing.Optional[builtins.str] = None,
    protocol_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed145af79f1c2da4094c58342eb40f268c984f336a565ceb7692c2373c41b02e(
    *,
    factor: builtins.str,
    is_big_endian: builtins.str,
    is_signed: builtins.str,
    length: builtins.str,
    message_id: builtins.str,
    offset: builtins.str,
    start_bit: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5164929065d606d8e2dc0dacc4ac433535c723e64a0977419b7b5cdcc6e7bce3(
    *,
    interface_id: builtins.str,
    type: builtins.str,
    can_interface: typing.Optional[typing.Union[typing.Union[CfnDecoderManifest.CanInterfaceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    obd_interface: typing.Optional[typing.Union[typing.Union[CfnDecoderManifest.ObdInterfaceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36035124d92aa491d26f7f3badad12234749ce5287196e39297302730919ddfd(
    *,
    name: builtins.str,
    request_message_id: builtins.str,
    dtc_request_interval_seconds: typing.Optional[builtins.str] = None,
    has_transmission_ecu: typing.Optional[builtins.str] = None,
    obd_standard: typing.Optional[builtins.str] = None,
    pid_request_interval_seconds: typing.Optional[builtins.str] = None,
    use_extended_ids: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701af2c9ec258d82f07b58404b5f34be536d73fe08eac2a1004d856673d9669a(
    *,
    byte_length: builtins.str,
    offset: builtins.str,
    pid: builtins.str,
    pid_response_length: builtins.str,
    scaling: builtins.str,
    service_mode: builtins.str,
    start_byte: builtins.str,
    bit_mask_length: typing.Optional[builtins.str] = None,
    bit_right_shift: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9c41d005beeec9830cf27750c5a3fb6af1317338d2cded80dd0a0881034aa2(
    *,
    fully_qualified_name: builtins.str,
    interface_id: builtins.str,
    type: builtins.str,
    can_signal: typing.Optional[typing.Union[typing.Union[CfnDecoderManifest.CanSignalProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    obd_signal: typing.Optional[typing.Union[typing.Union[CfnDecoderManifest.ObdSignalProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569ec6ea44200ea874b020dc44809eea72eee555b50cdc8656e558ed1653bb26(
    *,
    model_manifest_arn: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    network_interfaces: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDecoderManifest.NetworkInterfacesItemsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    signal_decoders: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDecoderManifest.SignalDecodersItemsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc4563792e7e71428d90b3f55210f042ac37b415f11f16298d546516dc7ffce(
    scope: _Construct_e78e779f,
    id_: builtins.str,
    *,
    id: builtins.str,
    signal_catalog_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7b647abcb966caa125db58cd283f8214b8b14f0ad51b664a7dd05cd844336a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4ae548a116a9b3278778dcc4bc58544ed45682bf1f75fea6a840777e28d45e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975249f522e00e0d641c388a14fd235fefdc0e23d0cbeb2c5f70f57067a13507(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b2c1322d2ab01a5b6375b016bfb042f680fae9ca4695d5e027ca9878a6d162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a28dd550208ea25556d35fd847cda8a66419064e36594b1e931f6b5a6426b1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4413fb47b0df2de3acde09efd3170fa1fe100d90b4b61c6c27c330fe6aab04e(
    *,
    id: builtins.str,
    signal_catalog_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b02ae0a75a63feb3c136d2c3fcc6f81ba3de65a78516a82ff8a47ed81cd4b2(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    signal_catalog_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ab04b0c662d6db90a024896f69ec2fddd3c88fe78396b70b90e055b6ba01ce(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6594bab2cfd9ade3c46534e72f2854f862af6125953803f728abcb63ee7c930e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f1fa793afa08970b3266638d9c5d57c01f9dd28faa5ae232aae60279aa1879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad0bb5470e1b5f921c4b28b0e0d44bf056cd3debbb573e274cd821ab45a2da8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8bb0014f22d61b377aabfd02963589b4ba86b52b635f105e4484640d9f7ef0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b02781d0161075eac6cf06659c9f6fc35a33c1b36c414ab22296742a42286b2(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966d704da02de7c15769615345fded070f4efe479cbb37999efc10e0d07f9801(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a219d5d487efed80061e39daa712d94004ac9331120b13748d5dd6eb5455b425(
    *,
    name: builtins.str,
    signal_catalog_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b893f0439f4cca922b1ab6f883b6aef8edab3157de46d42f1b00071c314a27a2(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    node_counts: typing.Optional[typing.Union[typing.Union[CfnSignalCatalog.NodeCountsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    nodes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSignalCatalog.NodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74221350fadd4443f89253fc71451a5ce131773fa492abb43a3519f4506f83ef(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225a5f02eba21fabadfa34ebaa51b61ac0a6569088763e7833123395dc273b42(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5f0fa3eab22d8c57599c90df05b68a5911c564de701f9a2c43ae389005c42e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e28223c7175931ac8a27cda4dc362d0ec7b18f03a0694f1d29c53744148985(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020a82e341463b102ac595a8ddfdb0cd2492faf08e68c7ae43d554f1397e9880(
    value: typing.Optional[typing.Union[CfnSignalCatalog.NodeCountsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5275b6c2afac9469e5e3052457a1fb7cdbba14ad2116191344b81ec573a5053e(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSignalCatalog.NodeProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29779cd7804fa9caba59eda5f2576e5448f5a95423003aa9cff3d76393f2b471(
    *,
    data_type: builtins.str,
    fully_qualified_name: builtins.str,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    assigned_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bb5dfd4926d4570aa227b8747fb0b557bc00076095551123b5f63568152634(
    *,
    data_type: builtins.str,
    fully_qualified_name: builtins.str,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    assigned_value: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8d3abd4726d0f0da78f1ca34fc36314c43533f8410cadee62b0b91d3e452c1(
    *,
    fully_qualified_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b361fd2dd1ad9193e312728642ac284acbf701ee00b5c4a2abab449713be46(
    *,
    total_actuators: typing.Optional[jsii.Number] = None,
    total_attributes: typing.Optional[jsii.Number] = None,
    total_branches: typing.Optional[jsii.Number] = None,
    total_nodes: typing.Optional[jsii.Number] = None,
    total_sensors: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d6bed217354b0750bcb825302cab5c857c527abc610fd0a00970db0663415d(
    *,
    actuator: typing.Optional[typing.Union[typing.Union[CfnSignalCatalog.ActuatorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    attribute: typing.Optional[typing.Union[typing.Union[CfnSignalCatalog.AttributeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    branch: typing.Optional[typing.Union[typing.Union[CfnSignalCatalog.BranchProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sensor: typing.Optional[typing.Union[typing.Union[CfnSignalCatalog.SensorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e19129731b60998cba6035a76a71fe0f793308a5d216698040cda099db7edf(
    *,
    data_type: builtins.str,
    fully_qualified_name: builtins.str,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8576e6ed9a3eab7ee1395e3e3fe2c07fa13c4c413b5752eb36572559dc5cc1c1(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    node_counts: typing.Optional[typing.Union[typing.Union[CfnSignalCatalog.NodeCountsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    nodes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSignalCatalog.NodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34d549696e1dd2eb7ccd43d3c740231cc42ab6102bd1b5376caff9393bebdc3(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    decoder_manifest_arn: builtins.str,
    model_manifest_arn: builtins.str,
    name: builtins.str,
    association_behavior: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984c32b24cb897cf030bc2fe52cac8e0f379c4994fdc681ffc171c6407e36240(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db65b94faaf42495a81b8e28f38c9c540099cc6b32385ad3d22228b433741ea8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ddd8147ec8acbc59d4059a06ee514a730acc169424ee4b4f89145a154736859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a781a90b6626efdd6fd70d7ff7960a2fb2d5f09ab1ebbdac3affba0e0bb3fa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2fcd4279d56b9dc300a41f30d0bb6d66d7dd6a5a6d9d78ca83a3ec28a0e2c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2cdd2821a0cdd669268bc40715d9ac5c762681bf1d5b5727f8aae8b114a8a02(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33bf674fae93670fcc31ed144370b884508fcb231e2ff4264b6bb12b5cf2f8e0(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58443223259b53f3d81b68c4dccfca6763b4be9f67f9d05c4be63ebcf99db4c8(
    *,
    decoder_manifest_arn: builtins.str,
    model_manifest_arn: builtins.str,
    name: builtins.str,
    association_behavior: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
