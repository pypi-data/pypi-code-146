'''
# AWS::LookoutEquipment Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as lookoutequipment
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for LookoutEquipment construct libraries](https://constructs.dev/search?q=lookoutequipment)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::LookoutEquipment resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LookoutEquipment.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::LookoutEquipment](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LookoutEquipment.html).

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
class CfnInferenceScheduler(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lookoutequipment.CfnInferenceScheduler",
):
    '''A CloudFormation ``AWS::LookoutEquipment::InferenceScheduler``.

    Creates a scheduled inference. Scheduling an inference is setting up a continuous real-time inference plan to analyze new measurement data. When setting up the schedule, you provide an Amazon S3 bucket location for the input data, assign it a delimiter between separate entries in the data, set an offset delay if desired, and set the frequency of inferencing. You must also provide an Amazon S3 bucket location for the output data.
    .. epigraph::

       Updating some properties below (for example, InferenceSchedulerName and ServerSideKmsKeyId) triggers a resource replacement, which requires a new model. To replace such a property using AWS CloudFormation , but without creating a completely new stack, you must replace ModelName. If you need to replace the property, but want to use the same model, delete the current stack and create a new one with the updated properties.

    :cloudformationResource: AWS::LookoutEquipment::InferenceScheduler
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_lookoutequipment as lookoutequipment
        
        # data_input_configuration: Any
        # data_output_configuration: Any
        
        cfn_inference_scheduler = lookoutequipment.CfnInferenceScheduler(self, "MyCfnInferenceScheduler",
            data_input_configuration=data_input_configuration,
            data_output_configuration=data_output_configuration,
            data_upload_frequency="dataUploadFrequency",
            model_name="modelName",
            role_arn="roleArn",
        
            # the properties below are optional
            data_delay_offset_in_minutes=123,
            inference_scheduler_name="inferenceSchedulerName",
            server_side_kms_key_id="serverSideKmsKeyId",
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
        data_input_configuration: typing.Any,
        data_output_configuration: typing.Any,
        data_upload_frequency: builtins.str,
        model_name: builtins.str,
        role_arn: builtins.str,
        data_delay_offset_in_minutes: typing.Optional[jsii.Number] = None,
        inference_scheduler_name: typing.Optional[builtins.str] = None,
        server_side_kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::LookoutEquipment::InferenceScheduler``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data_input_configuration: Specifies configuration information for the input data for the inference scheduler, including delimiter, format, and dataset location.
        :param data_output_configuration: Specifies configuration information for the output results for the inference scheduler, including the Amazon S3 location for the output.
        :param data_upload_frequency: How often data is uploaded to the source S3 bucket for the input data. This value is the length of time between data uploads. For instance, if you select 5 minutes, Amazon Lookout for Equipment will upload the real-time data to the source bucket once every 5 minutes. This frequency also determines how often Amazon Lookout for Equipment starts a scheduled inference on your data. In this example, it starts once every 5 minutes.
        :param model_name: The name of the ML model used for the inference scheduler.
        :param role_arn: The Amazon Resource Name (ARN) of a role with permission to access the data source being used for the inference.
        :param data_delay_offset_in_minutes: A period of time (in minutes) by which inference on the data is delayed after the data starts. For instance, if an offset delay time of five minutes was selected, inference will not begin on the data until the first data measurement after the five minute mark. For example, if five minutes is selected, the inference scheduler will wake up at the configured frequency with the additional five minute delay time to check the customer S3 bucket. The customer can upload data at the same frequency and they don't need to stop and restart the scheduler when uploading new data.
        :param inference_scheduler_name: The name of the inference scheduler.
        :param server_side_kms_key_id: Provides the identifier of the AWS KMS key used to encrypt inference scheduler data by Amazon Lookout for Equipment .
        :param tags: Any tags associated with the inference scheduler. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d179f57a47ea8b7e7abdc5f7ee2d9853d1f772079603b2204b611fc13af99f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInferenceSchedulerProps(
            data_input_configuration=data_input_configuration,
            data_output_configuration=data_output_configuration,
            data_upload_frequency=data_upload_frequency,
            model_name=model_name,
            role_arn=role_arn,
            data_delay_offset_in_minutes=data_delay_offset_in_minutes,
            inference_scheduler_name=inference_scheduler_name,
            server_side_kms_key_id=server_side_kms_key_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f093f195f780459045a3ea1cb4a8d5a3864c618e79e1d9906d50c443710ff7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bc235164c845e2db63991c756df45389f7e76779cfa21070095cb88425a58f9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrInferenceSchedulerArn")
    def attr_inference_scheduler_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the inference scheduler being created.

        :cloudformationAttribute: InferenceSchedulerArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrInferenceSchedulerArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Any tags associated with the inference scheduler.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dataInputConfiguration")
    def data_input_configuration(self) -> typing.Any:
        '''Specifies configuration information for the input data for the inference scheduler, including delimiter, format, and dataset location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-datainputconfiguration
        '''
        return typing.cast(typing.Any, jsii.get(self, "dataInputConfiguration"))

    @data_input_configuration.setter
    def data_input_configuration(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5520c6f70b7c458ceb4ed590c09deed7440f970be2436a2f923afbb1ea902c71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataInputConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="dataOutputConfiguration")
    def data_output_configuration(self) -> typing.Any:
        '''Specifies configuration information for the output results for the inference scheduler, including the Amazon S3 location for the output.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-dataoutputconfiguration
        '''
        return typing.cast(typing.Any, jsii.get(self, "dataOutputConfiguration"))

    @data_output_configuration.setter
    def data_output_configuration(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a6e6ade1cf3aa6a6321f08ffb57975ce3b048ba01a5964bdcf2bd220b68598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataOutputConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="dataUploadFrequency")
    def data_upload_frequency(self) -> builtins.str:
        '''How often data is uploaded to the source S3 bucket for the input data.

        This value is the length of time between data uploads. For instance, if you select 5 minutes, Amazon Lookout for Equipment will upload the real-time data to the source bucket once every 5 minutes. This frequency also determines how often Amazon Lookout for Equipment starts a scheduled inference on your data. In this example, it starts once every 5 minutes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-datauploadfrequency
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataUploadFrequency"))

    @data_upload_frequency.setter
    def data_upload_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af496eef06199c5aa712544dbaaa9a946caf2f162c2ec834cb45ce2cd9d8cfe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataUploadFrequency", value)

    @builtins.property
    @jsii.member(jsii_name="modelName")
    def model_name(self) -> builtins.str:
        '''The name of the ML model used for the inference scheduler.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-modelname
        '''
        return typing.cast(builtins.str, jsii.get(self, "modelName"))

    @model_name.setter
    def model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0830d7761610c3cb18f98df35cb68f0d05114b0bc089758503b1255ff0532391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of a role with permission to access the data source being used for the inference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42e7966f7a2e5a67d4f9bda3bd0c3ad0586064822129b72cc9ab593b89e9635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="dataDelayOffsetInMinutes")
    def data_delay_offset_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''A period of time (in minutes) by which inference on the data is delayed after the data starts.

        For instance, if an offset delay time of five minutes was selected, inference will not begin on the data until the first data measurement after the five minute mark. For example, if five minutes is selected, the inference scheduler will wake up at the configured frequency with the additional five minute delay time to check the customer S3 bucket. The customer can upload data at the same frequency and they don't need to stop and restart the scheduler when uploading new data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-datadelayoffsetinminutes
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataDelayOffsetInMinutes"))

    @data_delay_offset_in_minutes.setter
    def data_delay_offset_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436a440c5c478f55bd6bae6bd9f463881aee969c984278afc00330266b98b2e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDelayOffsetInMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="inferenceSchedulerName")
    def inference_scheduler_name(self) -> typing.Optional[builtins.str]:
        '''The name of the inference scheduler.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-inferenceschedulername
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inferenceSchedulerName"))

    @inference_scheduler_name.setter
    def inference_scheduler_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47767f32dcf4efb4760fa42c1c3468f5b832a5ee7f455c2407365bc2d54397d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inferenceSchedulerName", value)

    @builtins.property
    @jsii.member(jsii_name="serverSideKmsKeyId")
    def server_side_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Provides the identifier of the AWS KMS key used to encrypt inference scheduler data by Amazon Lookout for Equipment .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-serversidekmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverSideKmsKeyId"))

    @server_side_kms_key_id.setter
    def server_side_kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__412f49d750a9ec4e1c2f02dbec52093ad8bc99aa552a5e9c3526f4717c268979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverSideKmsKeyId", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_lookoutequipment.CfnInferenceScheduler.DataInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_input_configuration": "s3InputConfiguration",
            "inference_input_name_configuration": "inferenceInputNameConfiguration",
            "input_time_zone_offset": "inputTimeZoneOffset",
        },
    )
    class DataInputConfigurationProperty:
        def __init__(
            self,
            *,
            s3_input_configuration: typing.Union[typing.Union["CfnInferenceScheduler.S3InputConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            inference_input_name_configuration: typing.Optional[typing.Union[typing.Union["CfnInferenceScheduler.InputNameConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            input_time_zone_offset: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param s3_input_configuration: ``CfnInferenceScheduler.DataInputConfigurationProperty.S3InputConfiguration``.
            :param inference_input_name_configuration: ``CfnInferenceScheduler.DataInputConfigurationProperty.InferenceInputNameConfiguration``.
            :param input_time_zone_offset: ``CfnInferenceScheduler.DataInputConfigurationProperty.InputTimeZoneOffset``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-datainputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lookoutequipment as lookoutequipment
                
                data_input_configuration_property = lookoutequipment.CfnInferenceScheduler.DataInputConfigurationProperty(
                    s3_input_configuration=lookoutequipment.CfnInferenceScheduler.S3InputConfigurationProperty(
                        bucket="bucket",
                
                        # the properties below are optional
                        prefix="prefix"
                    ),
                
                    # the properties below are optional
                    inference_input_name_configuration=lookoutequipment.CfnInferenceScheduler.InputNameConfigurationProperty(
                        component_timestamp_delimiter="componentTimestampDelimiter",
                        timestamp_format="timestampFormat"
                    ),
                    input_time_zone_offset="inputTimeZoneOffset"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea857136c1fa50e42e912d012a4f91459f6aa4b6bb6420491a2e5ab5c94717cf)
                check_type(argname="argument s3_input_configuration", value=s3_input_configuration, expected_type=type_hints["s3_input_configuration"])
                check_type(argname="argument inference_input_name_configuration", value=inference_input_name_configuration, expected_type=type_hints["inference_input_name_configuration"])
                check_type(argname="argument input_time_zone_offset", value=input_time_zone_offset, expected_type=type_hints["input_time_zone_offset"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_input_configuration": s3_input_configuration,
            }
            if inference_input_name_configuration is not None:
                self._values["inference_input_name_configuration"] = inference_input_name_configuration
            if input_time_zone_offset is not None:
                self._values["input_time_zone_offset"] = input_time_zone_offset

        @builtins.property
        def s3_input_configuration(
            self,
        ) -> typing.Union["CfnInferenceScheduler.S3InputConfigurationProperty", _IResolvable_a771d0ef]:
            '''``CfnInferenceScheduler.DataInputConfigurationProperty.S3InputConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-datainputconfiguration.html#cfn-lookoutequipment-inferencescheduler-datainputconfiguration-s3inputconfiguration
            '''
            result = self._values.get("s3_input_configuration")
            assert result is not None, "Required property 's3_input_configuration' is missing"
            return typing.cast(typing.Union["CfnInferenceScheduler.S3InputConfigurationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def inference_input_name_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnInferenceScheduler.InputNameConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnInferenceScheduler.DataInputConfigurationProperty.InferenceInputNameConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-datainputconfiguration.html#cfn-lookoutequipment-inferencescheduler-datainputconfiguration-inferenceinputnameconfiguration
            '''
            result = self._values.get("inference_input_name_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnInferenceScheduler.InputNameConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def input_time_zone_offset(self) -> typing.Optional[builtins.str]:
            '''``CfnInferenceScheduler.DataInputConfigurationProperty.InputTimeZoneOffset``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-datainputconfiguration.html#cfn-lookoutequipment-inferencescheduler-datainputconfiguration-inputtimezoneoffset
            '''
            result = self._values.get("input_time_zone_offset")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lookoutequipment.CfnInferenceScheduler.DataOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_output_configuration": "s3OutputConfiguration",
            "kms_key_id": "kmsKeyId",
        },
    )
    class DataOutputConfigurationProperty:
        def __init__(
            self,
            *,
            s3_output_configuration: typing.Union[typing.Union["CfnInferenceScheduler.S3OutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param s3_output_configuration: ``CfnInferenceScheduler.DataOutputConfigurationProperty.S3OutputConfiguration``.
            :param kms_key_id: ``CfnInferenceScheduler.DataOutputConfigurationProperty.KmsKeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-dataoutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lookoutequipment as lookoutequipment
                
                data_output_configuration_property = lookoutequipment.CfnInferenceScheduler.DataOutputConfigurationProperty(
                    s3_output_configuration=lookoutequipment.CfnInferenceScheduler.S3OutputConfigurationProperty(
                        bucket="bucket",
                
                        # the properties below are optional
                        prefix="prefix"
                    ),
                
                    # the properties below are optional
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__98af3ad87b6d6b63c4b450a4593c9e7495e8ef966d6b6acd341335dae389346d)
                check_type(argname="argument s3_output_configuration", value=s3_output_configuration, expected_type=type_hints["s3_output_configuration"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_output_configuration": s3_output_configuration,
            }
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def s3_output_configuration(
            self,
        ) -> typing.Union["CfnInferenceScheduler.S3OutputConfigurationProperty", _IResolvable_a771d0ef]:
            '''``CfnInferenceScheduler.DataOutputConfigurationProperty.S3OutputConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-dataoutputconfiguration.html#cfn-lookoutequipment-inferencescheduler-dataoutputconfiguration-s3outputconfiguration
            '''
            result = self._values.get("s3_output_configuration")
            assert result is not None, "Required property 's3_output_configuration' is missing"
            return typing.cast(typing.Union["CfnInferenceScheduler.S3OutputConfigurationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''``CfnInferenceScheduler.DataOutputConfigurationProperty.KmsKeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-dataoutputconfiguration.html#cfn-lookoutequipment-inferencescheduler-dataoutputconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lookoutequipment.CfnInferenceScheduler.InputNameConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_timestamp_delimiter": "componentTimestampDelimiter",
            "timestamp_format": "timestampFormat",
        },
    )
    class InputNameConfigurationProperty:
        def __init__(
            self,
            *,
            component_timestamp_delimiter: typing.Optional[builtins.str] = None,
            timestamp_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param component_timestamp_delimiter: ``CfnInferenceScheduler.InputNameConfigurationProperty.ComponentTimestampDelimiter``.
            :param timestamp_format: ``CfnInferenceScheduler.InputNameConfigurationProperty.TimestampFormat``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-inputnameconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lookoutequipment as lookoutequipment
                
                input_name_configuration_property = lookoutequipment.CfnInferenceScheduler.InputNameConfigurationProperty(
                    component_timestamp_delimiter="componentTimestampDelimiter",
                    timestamp_format="timestampFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__011188cc1bf2e689fefeb800f089d8b024046b2cb28351471dbec7aedad9e7e0)
                check_type(argname="argument component_timestamp_delimiter", value=component_timestamp_delimiter, expected_type=type_hints["component_timestamp_delimiter"])
                check_type(argname="argument timestamp_format", value=timestamp_format, expected_type=type_hints["timestamp_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_timestamp_delimiter is not None:
                self._values["component_timestamp_delimiter"] = component_timestamp_delimiter
            if timestamp_format is not None:
                self._values["timestamp_format"] = timestamp_format

        @builtins.property
        def component_timestamp_delimiter(self) -> typing.Optional[builtins.str]:
            '''``CfnInferenceScheduler.InputNameConfigurationProperty.ComponentTimestampDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-inputnameconfiguration.html#cfn-lookoutequipment-inferencescheduler-inputnameconfiguration-componenttimestampdelimiter
            '''
            result = self._values.get("component_timestamp_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp_format(self) -> typing.Optional[builtins.str]:
            '''``CfnInferenceScheduler.InputNameConfigurationProperty.TimestampFormat``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-inputnameconfiguration.html#cfn-lookoutequipment-inferencescheduler-inputnameconfiguration-timestampformat
            '''
            result = self._values.get("timestamp_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputNameConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lookoutequipment.CfnInferenceScheduler.S3InputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "prefix": "prefix"},
    )
    class S3InputConfigurationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket: ``CfnInferenceScheduler.S3InputConfigurationProperty.Bucket``.
            :param prefix: ``CfnInferenceScheduler.S3InputConfigurationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3inputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lookoutequipment as lookoutequipment
                
                s3_input_configuration_property = lookoutequipment.CfnInferenceScheduler.S3InputConfigurationProperty(
                    bucket="bucket",
                
                    # the properties below are optional
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__796bb79ff0260201e97de1c20f0d4e5d1ca6a5e32cd6d62138d0ffa6ca00230a)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
            }
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnInferenceScheduler.S3InputConfigurationProperty.Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3inputconfiguration.html#cfn-lookoutequipment-inferencescheduler-s3inputconfiguration-bucket
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnInferenceScheduler.S3InputConfigurationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3inputconfiguration.html#cfn-lookoutequipment-inferencescheduler-s3inputconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3InputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lookoutequipment.CfnInferenceScheduler.S3OutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "prefix": "prefix"},
    )
    class S3OutputConfigurationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket: ``CfnInferenceScheduler.S3OutputConfigurationProperty.Bucket``.
            :param prefix: ``CfnInferenceScheduler.S3OutputConfigurationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3outputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lookoutequipment as lookoutequipment
                
                s3_output_configuration_property = lookoutequipment.CfnInferenceScheduler.S3OutputConfigurationProperty(
                    bucket="bucket",
                
                    # the properties below are optional
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04a3693e0621dcbe66da313961a67d45158db254952ff2bb94bedd87381719bd)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
            }
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnInferenceScheduler.S3OutputConfigurationProperty.Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3outputconfiguration.html#cfn-lookoutequipment-inferencescheduler-s3outputconfiguration-bucket
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnInferenceScheduler.S3OutputConfigurationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3outputconfiguration.html#cfn-lookoutequipment-inferencescheduler-s3outputconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3OutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_lookoutequipment.CfnInferenceSchedulerProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_input_configuration": "dataInputConfiguration",
        "data_output_configuration": "dataOutputConfiguration",
        "data_upload_frequency": "dataUploadFrequency",
        "model_name": "modelName",
        "role_arn": "roleArn",
        "data_delay_offset_in_minutes": "dataDelayOffsetInMinutes",
        "inference_scheduler_name": "inferenceSchedulerName",
        "server_side_kms_key_id": "serverSideKmsKeyId",
        "tags": "tags",
    },
)
class CfnInferenceSchedulerProps:
    def __init__(
        self,
        *,
        data_input_configuration: typing.Any,
        data_output_configuration: typing.Any,
        data_upload_frequency: builtins.str,
        model_name: builtins.str,
        role_arn: builtins.str,
        data_delay_offset_in_minutes: typing.Optional[jsii.Number] = None,
        inference_scheduler_name: typing.Optional[builtins.str] = None,
        server_side_kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnInferenceScheduler``.

        :param data_input_configuration: Specifies configuration information for the input data for the inference scheduler, including delimiter, format, and dataset location.
        :param data_output_configuration: Specifies configuration information for the output results for the inference scheduler, including the Amazon S3 location for the output.
        :param data_upload_frequency: How often data is uploaded to the source S3 bucket for the input data. This value is the length of time between data uploads. For instance, if you select 5 minutes, Amazon Lookout for Equipment will upload the real-time data to the source bucket once every 5 minutes. This frequency also determines how often Amazon Lookout for Equipment starts a scheduled inference on your data. In this example, it starts once every 5 minutes.
        :param model_name: The name of the ML model used for the inference scheduler.
        :param role_arn: The Amazon Resource Name (ARN) of a role with permission to access the data source being used for the inference.
        :param data_delay_offset_in_minutes: A period of time (in minutes) by which inference on the data is delayed after the data starts. For instance, if an offset delay time of five minutes was selected, inference will not begin on the data until the first data measurement after the five minute mark. For example, if five minutes is selected, the inference scheduler will wake up at the configured frequency with the additional five minute delay time to check the customer S3 bucket. The customer can upload data at the same frequency and they don't need to stop and restart the scheduler when uploading new data.
        :param inference_scheduler_name: The name of the inference scheduler.
        :param server_side_kms_key_id: Provides the identifier of the AWS KMS key used to encrypt inference scheduler data by Amazon Lookout for Equipment .
        :param tags: Any tags associated with the inference scheduler. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_lookoutequipment as lookoutequipment
            
            # data_input_configuration: Any
            # data_output_configuration: Any
            
            cfn_inference_scheduler_props = lookoutequipment.CfnInferenceSchedulerProps(
                data_input_configuration=data_input_configuration,
                data_output_configuration=data_output_configuration,
                data_upload_frequency="dataUploadFrequency",
                model_name="modelName",
                role_arn="roleArn",
            
                # the properties below are optional
                data_delay_offset_in_minutes=123,
                inference_scheduler_name="inferenceSchedulerName",
                server_side_kms_key_id="serverSideKmsKeyId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36c5c24bc04e70adaeae244c60627f947dc310862ac82b97f35845b676b4c6d)
            check_type(argname="argument data_input_configuration", value=data_input_configuration, expected_type=type_hints["data_input_configuration"])
            check_type(argname="argument data_output_configuration", value=data_output_configuration, expected_type=type_hints["data_output_configuration"])
            check_type(argname="argument data_upload_frequency", value=data_upload_frequency, expected_type=type_hints["data_upload_frequency"])
            check_type(argname="argument model_name", value=model_name, expected_type=type_hints["model_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument data_delay_offset_in_minutes", value=data_delay_offset_in_minutes, expected_type=type_hints["data_delay_offset_in_minutes"])
            check_type(argname="argument inference_scheduler_name", value=inference_scheduler_name, expected_type=type_hints["inference_scheduler_name"])
            check_type(argname="argument server_side_kms_key_id", value=server_side_kms_key_id, expected_type=type_hints["server_side_kms_key_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_input_configuration": data_input_configuration,
            "data_output_configuration": data_output_configuration,
            "data_upload_frequency": data_upload_frequency,
            "model_name": model_name,
            "role_arn": role_arn,
        }
        if data_delay_offset_in_minutes is not None:
            self._values["data_delay_offset_in_minutes"] = data_delay_offset_in_minutes
        if inference_scheduler_name is not None:
            self._values["inference_scheduler_name"] = inference_scheduler_name
        if server_side_kms_key_id is not None:
            self._values["server_side_kms_key_id"] = server_side_kms_key_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_input_configuration(self) -> typing.Any:
        '''Specifies configuration information for the input data for the inference scheduler, including delimiter, format, and dataset location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-datainputconfiguration
        '''
        result = self._values.get("data_input_configuration")
        assert result is not None, "Required property 'data_input_configuration' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def data_output_configuration(self) -> typing.Any:
        '''Specifies configuration information for the output results for the inference scheduler, including the Amazon S3 location for the output.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-dataoutputconfiguration
        '''
        result = self._values.get("data_output_configuration")
        assert result is not None, "Required property 'data_output_configuration' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def data_upload_frequency(self) -> builtins.str:
        '''How often data is uploaded to the source S3 bucket for the input data.

        This value is the length of time between data uploads. For instance, if you select 5 minutes, Amazon Lookout for Equipment will upload the real-time data to the source bucket once every 5 minutes. This frequency also determines how often Amazon Lookout for Equipment starts a scheduled inference on your data. In this example, it starts once every 5 minutes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-datauploadfrequency
        '''
        result = self._values.get("data_upload_frequency")
        assert result is not None, "Required property 'data_upload_frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def model_name(self) -> builtins.str:
        '''The name of the ML model used for the inference scheduler.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-modelname
        '''
        result = self._values.get("model_name")
        assert result is not None, "Required property 'model_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of a role with permission to access the data source being used for the inference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_delay_offset_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''A period of time (in minutes) by which inference on the data is delayed after the data starts.

        For instance, if an offset delay time of five minutes was selected, inference will not begin on the data until the first data measurement after the five minute mark. For example, if five minutes is selected, the inference scheduler will wake up at the configured frequency with the additional five minute delay time to check the customer S3 bucket. The customer can upload data at the same frequency and they don't need to stop and restart the scheduler when uploading new data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-datadelayoffsetinminutes
        '''
        result = self._values.get("data_delay_offset_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def inference_scheduler_name(self) -> typing.Optional[builtins.str]:
        '''The name of the inference scheduler.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-inferenceschedulername
        '''
        result = self._values.get("inference_scheduler_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Provides the identifier of the AWS KMS key used to encrypt inference scheduler data by Amazon Lookout for Equipment .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-serversidekmskeyid
        '''
        result = self._values.get("server_side_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Any tags associated with the inference scheduler.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInferenceSchedulerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnInferenceScheduler",
    "CfnInferenceSchedulerProps",
]

publication.publish()

def _typecheckingstub__7d179f57a47ea8b7e7abdc5f7ee2d9853d1f772079603b2204b611fc13af99f0(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    data_input_configuration: typing.Any,
    data_output_configuration: typing.Any,
    data_upload_frequency: builtins.str,
    model_name: builtins.str,
    role_arn: builtins.str,
    data_delay_offset_in_minutes: typing.Optional[jsii.Number] = None,
    inference_scheduler_name: typing.Optional[builtins.str] = None,
    server_side_kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f093f195f780459045a3ea1cb4a8d5a3864c618e79e1d9906d50c443710ff7f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc235164c845e2db63991c756df45389f7e76779cfa21070095cb88425a58f9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5520c6f70b7c458ceb4ed590c09deed7440f970be2436a2f923afbb1ea902c71(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a6e6ade1cf3aa6a6321f08ffb57975ce3b048ba01a5964bdcf2bd220b68598(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af496eef06199c5aa712544dbaaa9a946caf2f162c2ec834cb45ce2cd9d8cfe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0830d7761610c3cb18f98df35cb68f0d05114b0bc089758503b1255ff0532391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42e7966f7a2e5a67d4f9bda3bd0c3ad0586064822129b72cc9ab593b89e9635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436a440c5c478f55bd6bae6bd9f463881aee969c984278afc00330266b98b2e8(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47767f32dcf4efb4760fa42c1c3468f5b832a5ee7f455c2407365bc2d54397d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412f49d750a9ec4e1c2f02dbec52093ad8bc99aa552a5e9c3526f4717c268979(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea857136c1fa50e42e912d012a4f91459f6aa4b6bb6420491a2e5ab5c94717cf(
    *,
    s3_input_configuration: typing.Union[typing.Union[CfnInferenceScheduler.S3InputConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    inference_input_name_configuration: typing.Optional[typing.Union[typing.Union[CfnInferenceScheduler.InputNameConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    input_time_zone_offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98af3ad87b6d6b63c4b450a4593c9e7495e8ef966d6b6acd341335dae389346d(
    *,
    s3_output_configuration: typing.Union[typing.Union[CfnInferenceScheduler.S3OutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011188cc1bf2e689fefeb800f089d8b024046b2cb28351471dbec7aedad9e7e0(
    *,
    component_timestamp_delimiter: typing.Optional[builtins.str] = None,
    timestamp_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796bb79ff0260201e97de1c20f0d4e5d1ca6a5e32cd6d62138d0ffa6ca00230a(
    *,
    bucket: builtins.str,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a3693e0621dcbe66da313961a67d45158db254952ff2bb94bedd87381719bd(
    *,
    bucket: builtins.str,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36c5c24bc04e70adaeae244c60627f947dc310862ac82b97f35845b676b4c6d(
    *,
    data_input_configuration: typing.Any,
    data_output_configuration: typing.Any,
    data_upload_frequency: builtins.str,
    model_name: builtins.str,
    role_arn: builtins.str,
    data_delay_offset_in_minutes: typing.Optional[jsii.Number] = None,
    inference_scheduler_name: typing.Optional[builtins.str] = None,
    server_side_kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
