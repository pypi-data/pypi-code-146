'''
# AWS::Panorama Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as panorama
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Panorama construct libraries](https://constructs.dev/search?q=panorama)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Panorama resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Panorama.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Panorama](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Panorama.html).

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
class CfnApplicationInstance(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_panorama.CfnApplicationInstance",
):
    '''A CloudFormation ``AWS::Panorama::ApplicationInstance``.

    Creates an application instance and deploys it to a device.

    :cloudformationResource: AWS::Panorama::ApplicationInstance
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_panorama as panorama
        
        cfn_application_instance = panorama.CfnApplicationInstance(self, "MyCfnApplicationInstance",
            default_runtime_context_device="defaultRuntimeContextDevice",
            manifest_payload=panorama.CfnApplicationInstance.ManifestPayloadProperty(
                payload_data="payloadData"
            ),
        
            # the properties below are optional
            application_instance_id_to_replace="applicationInstanceIdToReplace",
            description="description",
            device_id="deviceId",
            manifest_overrides_payload=panorama.CfnApplicationInstance.ManifestOverridesPayloadProperty(
                payload_data="payloadData"
            ),
            name="name",
            runtime_role_arn="runtimeRoleArn",
            status_filter="statusFilter",
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
        default_runtime_context_device: builtins.str,
        manifest_payload: typing.Union[typing.Union["CfnApplicationInstance.ManifestPayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        application_instance_id_to_replace: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        device_id: typing.Optional[builtins.str] = None,
        manifest_overrides_payload: typing.Optional[typing.Union[typing.Union["CfnApplicationInstance.ManifestOverridesPayloadProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        runtime_role_arn: typing.Optional[builtins.str] = None,
        status_filter: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Panorama::ApplicationInstance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_runtime_context_device: The device's ID.
        :param manifest_payload: The application's manifest document.
        :param application_instance_id_to_replace: The ID of an application instance to replace with the new instance.
        :param description: A description for the application instance.
        :param device_id: A device's ID.
        :param manifest_overrides_payload: Setting overrides for the application manifest.
        :param name: A name for the application instance.
        :param runtime_role_arn: The ARN of a runtime role for the application instance.
        :param status_filter: Only include instances with a specific status.
        :param tags: Tags for the application instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58844ecd20408ee621fe4618ad942892da770259acc25102774445e7c4bd2141)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationInstanceProps(
            default_runtime_context_device=default_runtime_context_device,
            manifest_payload=manifest_payload,
            application_instance_id_to_replace=application_instance_id_to_replace,
            description=description,
            device_id=device_id,
            manifest_overrides_payload=manifest_overrides_payload,
            name=name,
            runtime_role_arn=runtime_role_arn,
            status_filter=status_filter,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b22ba9004f91c94d8e9a0f58bf3a86698bc4ea3fb67de0c51985226f10bbc4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2839f8fde36ba2af55175f64cc9c6aa2d69ff5e93ae0f82c86b0d09ffdbee697)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApplicationInstanceId")
    def attr_application_instance_id(self) -> builtins.str:
        '''The application instance's ID.

        :cloudformationAttribute: ApplicationInstanceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApplicationInstanceId"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The application instance's ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> jsii.Number:
        '''The application instance's created time.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrDefaultRuntimeContextDeviceName")
    def attr_default_runtime_context_device_name(self) -> builtins.str:
        '''The application instance's default runtime context device name.

        :cloudformationAttribute: DefaultRuntimeContextDeviceName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDefaultRuntimeContextDeviceName"))

    @builtins.property
    @jsii.member(jsii_name="attrHealthStatus")
    def attr_health_status(self) -> builtins.str:
        '''The application instance's health status.

        :cloudformationAttribute: HealthStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrHealthStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> jsii.Number:
        '''The application instance's last updated time.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The application instance's status.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusDescription")
    def attr_status_description(self) -> builtins.str:
        '''The application instance's status description.

        :cloudformationAttribute: StatusDescription
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusDescription"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Tags for the application instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="defaultRuntimeContextDevice")
    def default_runtime_context_device(self) -> builtins.str:
        '''The device's ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-defaultruntimecontextdevice
        '''
        return typing.cast(builtins.str, jsii.get(self, "defaultRuntimeContextDevice"))

    @default_runtime_context_device.setter
    def default_runtime_context_device(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3b330c7f6b81d693f426a17326c1a8630ded9cd2ac12e96cbcde14dfe25ec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRuntimeContextDevice", value)

    @builtins.property
    @jsii.member(jsii_name="manifestPayload")
    def manifest_payload(
        self,
    ) -> typing.Union["CfnApplicationInstance.ManifestPayloadProperty", _IResolvable_a771d0ef]:
        '''The application's manifest document.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-manifestpayload
        '''
        return typing.cast(typing.Union["CfnApplicationInstance.ManifestPayloadProperty", _IResolvable_a771d0ef], jsii.get(self, "manifestPayload"))

    @manifest_payload.setter
    def manifest_payload(
        self,
        value: typing.Union["CfnApplicationInstance.ManifestPayloadProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2c001c290943c2afd9889fef1ce95f1ccfa7ad7262285b3eda62ad4df4e5e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manifestPayload", value)

    @builtins.property
    @jsii.member(jsii_name="applicationInstanceIdToReplace")
    def application_instance_id_to_replace(self) -> typing.Optional[builtins.str]:
        '''The ID of an application instance to replace with the new instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-applicationinstanceidtoreplace
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationInstanceIdToReplace"))

    @application_instance_id_to_replace.setter
    def application_instance_id_to_replace(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d6ef8513cffa578445b5701e9f9795fce6ffc1497e33972aa3ed23c72bd9fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationInstanceIdToReplace", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the application instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f745e9cb986a459bea6c89da9a3e24270c3ab886725bf291a86d348747b7b570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> typing.Optional[builtins.str]:
        '''A device's ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-deviceid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceId"))

    @device_id.setter
    def device_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06c5f27bdbb06347d5ba893ffd8c09ff8833867b3112bc6c335352e34479a3ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceId", value)

    @builtins.property
    @jsii.member(jsii_name="manifestOverridesPayload")
    def manifest_overrides_payload(
        self,
    ) -> typing.Optional[typing.Union["CfnApplicationInstance.ManifestOverridesPayloadProperty", _IResolvable_a771d0ef]]:
        '''Setting overrides for the application manifest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-manifestoverridespayload
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApplicationInstance.ManifestOverridesPayloadProperty", _IResolvable_a771d0ef]], jsii.get(self, "manifestOverridesPayload"))

    @manifest_overrides_payload.setter
    def manifest_overrides_payload(
        self,
        value: typing.Optional[typing.Union["CfnApplicationInstance.ManifestOverridesPayloadProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5234bfb55c825f5d6488789088cadced331ffa851f3cf421fce8c7c21c26b14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manifestOverridesPayload", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the application instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d11edb6943b492b1fad88de0430c3372ab105b68f1188668147f3252f4b2cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="runtimeRoleArn")
    def runtime_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of a runtime role for the application instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-runtimerolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeRoleArn"))

    @runtime_role_arn.setter
    def runtime_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5b633e493b785fe265891df571e844db413311ef34b582102275c26df1e915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="statusFilter")
    def status_filter(self) -> typing.Optional[builtins.str]:
        '''Only include instances with a specific status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-statusfilter
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusFilter"))

    @status_filter.setter
    def status_filter(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14b10fe5a0c65758c13a0acbfd9316ff17bc8eeaa3ba84fbc0e003750b38c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusFilter", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_panorama.CfnApplicationInstance.ManifestOverridesPayloadProperty",
        jsii_struct_bases=[],
        name_mapping={"payload_data": "payloadData"},
    )
    class ManifestOverridesPayloadProperty:
        def __init__(
            self,
            *,
            payload_data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Parameter overrides for an application instance.

            This is a JSON document that has a single key ( ``PayloadData`` ) where the value is an escaped string representation of the overrides document.

            :param payload_data: The overrides document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-applicationinstance-manifestoverridespayload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_panorama as panorama
                
                manifest_overrides_payload_property = panorama.CfnApplicationInstance.ManifestOverridesPayloadProperty(
                    payload_data="payloadData"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0e16b9b0013af6622a65e3fd7793248e307ca446f8f188e365f5480e8f1166b)
                check_type(argname="argument payload_data", value=payload_data, expected_type=type_hints["payload_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload_data is not None:
                self._values["payload_data"] = payload_data

        @builtins.property
        def payload_data(self) -> typing.Optional[builtins.str]:
            '''The overrides document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-applicationinstance-manifestoverridespayload.html#cfn-panorama-applicationinstance-manifestoverridespayload-payloaddata
            '''
            result = self._values.get("payload_data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManifestOverridesPayloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_panorama.CfnApplicationInstance.ManifestPayloadProperty",
        jsii_struct_bases=[],
        name_mapping={"payload_data": "payloadData"},
    )
    class ManifestPayloadProperty:
        def __init__(
            self,
            *,
            payload_data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A application verion's manifest file.

            This is a JSON document that has a single key ( ``PayloadData`` ) where the value is an escaped string representation of the application manifest ( ``graph.json`` ). This file is located in the ``graphs`` folder in your application source.

            :param payload_data: The application manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-applicationinstance-manifestpayload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_panorama as panorama
                
                manifest_payload_property = panorama.CfnApplicationInstance.ManifestPayloadProperty(
                    payload_data="payloadData"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc7971eca2de16f3b3de3cdc8ec767666bca974b9fc9cc0cabc1a41a77e8cf58)
                check_type(argname="argument payload_data", value=payload_data, expected_type=type_hints["payload_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload_data is not None:
                self._values["payload_data"] = payload_data

        @builtins.property
        def payload_data(self) -> typing.Optional[builtins.str]:
            '''The application manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-applicationinstance-manifestpayload.html#cfn-panorama-applicationinstance-manifestpayload-payloaddata
            '''
            result = self._values.get("payload_data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManifestPayloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_panorama.CfnApplicationInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_runtime_context_device": "defaultRuntimeContextDevice",
        "manifest_payload": "manifestPayload",
        "application_instance_id_to_replace": "applicationInstanceIdToReplace",
        "description": "description",
        "device_id": "deviceId",
        "manifest_overrides_payload": "manifestOverridesPayload",
        "name": "name",
        "runtime_role_arn": "runtimeRoleArn",
        "status_filter": "statusFilter",
        "tags": "tags",
    },
)
class CfnApplicationInstanceProps:
    def __init__(
        self,
        *,
        default_runtime_context_device: builtins.str,
        manifest_payload: typing.Union[typing.Union[CfnApplicationInstance.ManifestPayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        application_instance_id_to_replace: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        device_id: typing.Optional[builtins.str] = None,
        manifest_overrides_payload: typing.Optional[typing.Union[typing.Union[CfnApplicationInstance.ManifestOverridesPayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        runtime_role_arn: typing.Optional[builtins.str] = None,
        status_filter: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplicationInstance``.

        :param default_runtime_context_device: The device's ID.
        :param manifest_payload: The application's manifest document.
        :param application_instance_id_to_replace: The ID of an application instance to replace with the new instance.
        :param description: A description for the application instance.
        :param device_id: A device's ID.
        :param manifest_overrides_payload: Setting overrides for the application manifest.
        :param name: A name for the application instance.
        :param runtime_role_arn: The ARN of a runtime role for the application instance.
        :param status_filter: Only include instances with a specific status.
        :param tags: Tags for the application instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_panorama as panorama
            
            cfn_application_instance_props = panorama.CfnApplicationInstanceProps(
                default_runtime_context_device="defaultRuntimeContextDevice",
                manifest_payload=panorama.CfnApplicationInstance.ManifestPayloadProperty(
                    payload_data="payloadData"
                ),
            
                # the properties below are optional
                application_instance_id_to_replace="applicationInstanceIdToReplace",
                description="description",
                device_id="deviceId",
                manifest_overrides_payload=panorama.CfnApplicationInstance.ManifestOverridesPayloadProperty(
                    payload_data="payloadData"
                ),
                name="name",
                runtime_role_arn="runtimeRoleArn",
                status_filter="statusFilter",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af982778120f2ede7767796d8ffc48de33bc5fbd64a5e175baaac57ba6995c9f)
            check_type(argname="argument default_runtime_context_device", value=default_runtime_context_device, expected_type=type_hints["default_runtime_context_device"])
            check_type(argname="argument manifest_payload", value=manifest_payload, expected_type=type_hints["manifest_payload"])
            check_type(argname="argument application_instance_id_to_replace", value=application_instance_id_to_replace, expected_type=type_hints["application_instance_id_to_replace"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
            check_type(argname="argument manifest_overrides_payload", value=manifest_overrides_payload, expected_type=type_hints["manifest_overrides_payload"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument runtime_role_arn", value=runtime_role_arn, expected_type=type_hints["runtime_role_arn"])
            check_type(argname="argument status_filter", value=status_filter, expected_type=type_hints["status_filter"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_runtime_context_device": default_runtime_context_device,
            "manifest_payload": manifest_payload,
        }
        if application_instance_id_to_replace is not None:
            self._values["application_instance_id_to_replace"] = application_instance_id_to_replace
        if description is not None:
            self._values["description"] = description
        if device_id is not None:
            self._values["device_id"] = device_id
        if manifest_overrides_payload is not None:
            self._values["manifest_overrides_payload"] = manifest_overrides_payload
        if name is not None:
            self._values["name"] = name
        if runtime_role_arn is not None:
            self._values["runtime_role_arn"] = runtime_role_arn
        if status_filter is not None:
            self._values["status_filter"] = status_filter
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def default_runtime_context_device(self) -> builtins.str:
        '''The device's ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-defaultruntimecontextdevice
        '''
        result = self._values.get("default_runtime_context_device")
        assert result is not None, "Required property 'default_runtime_context_device' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def manifest_payload(
        self,
    ) -> typing.Union[CfnApplicationInstance.ManifestPayloadProperty, _IResolvable_a771d0ef]:
        '''The application's manifest document.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-manifestpayload
        '''
        result = self._values.get("manifest_payload")
        assert result is not None, "Required property 'manifest_payload' is missing"
        return typing.cast(typing.Union[CfnApplicationInstance.ManifestPayloadProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def application_instance_id_to_replace(self) -> typing.Optional[builtins.str]:
        '''The ID of an application instance to replace with the new instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-applicationinstanceidtoreplace
        '''
        result = self._values.get("application_instance_id_to_replace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the application instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_id(self) -> typing.Optional[builtins.str]:
        '''A device's ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-deviceid
        '''
        result = self._values.get("device_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manifest_overrides_payload(
        self,
    ) -> typing.Optional[typing.Union[CfnApplicationInstance.ManifestOverridesPayloadProperty, _IResolvable_a771d0ef]]:
        '''Setting overrides for the application manifest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-manifestoverridespayload
        '''
        result = self._values.get("manifest_overrides_payload")
        return typing.cast(typing.Optional[typing.Union[CfnApplicationInstance.ManifestOverridesPayloadProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the application instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of a runtime role for the application instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-runtimerolearn
        '''
        result = self._values.get("runtime_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_filter(self) -> typing.Optional[builtins.str]:
        '''Only include instances with a specific status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-statusfilter
        '''
        result = self._values.get("status_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Tags for the application instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-applicationinstance.html#cfn-panorama-applicationinstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPackage(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_panorama.CfnPackage",
):
    '''A CloudFormation ``AWS::Panorama::Package``.

    Creates a package and storage location in an Amazon S3 access point.

    :cloudformationResource: AWS::Panorama::Package
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_panorama as panorama
        
        cfn_package = panorama.CfnPackage(self, "MyCfnPackage",
            package_name="packageName",
        
            # the properties below are optional
            storage_location=panorama.CfnPackage.StorageLocationProperty(
                binary_prefix_location="binaryPrefixLocation",
                bucket="bucket",
                generated_prefix_location="generatedPrefixLocation",
                manifest_prefix_location="manifestPrefixLocation",
                repo_prefix_location="repoPrefixLocation"
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
        package_name: builtins.str,
        storage_location: typing.Optional[typing.Union[typing.Union["CfnPackage.StorageLocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Panorama::Package``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param package_name: A name for the package.
        :param storage_location: ``AWS::Panorama::Package.StorageLocation``.
        :param tags: Tags for the package.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e920012df3013bb391769bac2b5e98320b7e7502914b48f8b05cce679dc825)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPackageProps(
            package_name=package_name, storage_location=storage_location, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24497f19f48f4bb9bc226398ab83a339b4d482ad5fbf02fec48c5189c2ccc5e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17c092468053c32a5c5ca3bb046bc8b089b19c1668e68bd0da81bedabc449325)
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
        '''The package's ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> jsii.Number:
        '''The item's created time.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrPackageId")
    def attr_package_id(self) -> builtins.str:
        '''The package's ID.

        :cloudformationAttribute: PackageId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPackageId"))

    @builtins.property
    @jsii.member(jsii_name="attrStorageLocationBinaryPrefixLocation")
    def attr_storage_location_binary_prefix_location(self) -> builtins.str:
        '''
        :cloudformationAttribute: StorageLocation.BinaryPrefixLocation
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStorageLocationBinaryPrefixLocation"))

    @builtins.property
    @jsii.member(jsii_name="attrStorageLocationBucket")
    def attr_storage_location_bucket(self) -> builtins.str:
        '''
        :cloudformationAttribute: StorageLocation.Bucket
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStorageLocationBucket"))

    @builtins.property
    @jsii.member(jsii_name="attrStorageLocationGeneratedPrefixLocation")
    def attr_storage_location_generated_prefix_location(self) -> builtins.str:
        '''
        :cloudformationAttribute: StorageLocation.GeneratedPrefixLocation
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStorageLocationGeneratedPrefixLocation"))

    @builtins.property
    @jsii.member(jsii_name="attrStorageLocationManifestPrefixLocation")
    def attr_storage_location_manifest_prefix_location(self) -> builtins.str:
        '''
        :cloudformationAttribute: StorageLocation.ManifestPrefixLocation
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStorageLocationManifestPrefixLocation"))

    @builtins.property
    @jsii.member(jsii_name="attrStorageLocationRepoPrefixLocation")
    def attr_storage_location_repo_prefix_location(self) -> builtins.str:
        '''
        :cloudformationAttribute: StorageLocation.RepoPrefixLocation
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStorageLocationRepoPrefixLocation"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Tags for the package.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html#cfn-panorama-package-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="packageName")
    def package_name(self) -> builtins.str:
        '''A name for the package.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html#cfn-panorama-package-packagename
        '''
        return typing.cast(builtins.str, jsii.get(self, "packageName"))

    @package_name.setter
    def package_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5565baf518d55a36a087b18c69db383209084d0bf614a5a68dfd40f9dba1a0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageName", value)

    @builtins.property
    @jsii.member(jsii_name="storageLocation")
    def storage_location(
        self,
    ) -> typing.Optional[typing.Union["CfnPackage.StorageLocationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Panorama::Package.StorageLocation``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html#cfn-panorama-package-storagelocation
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPackage.StorageLocationProperty", _IResolvable_a771d0ef]], jsii.get(self, "storageLocation"))

    @storage_location.setter
    def storage_location(
        self,
        value: typing.Optional[typing.Union["CfnPackage.StorageLocationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf909503030cb203fa18c2da175c56f4f7f913ec104da5bdb6155935567241b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageLocation", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_panorama.CfnPackage.StorageLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "binary_prefix_location": "binaryPrefixLocation",
            "bucket": "bucket",
            "generated_prefix_location": "generatedPrefixLocation",
            "manifest_prefix_location": "manifestPrefixLocation",
            "repo_prefix_location": "repoPrefixLocation",
        },
    )
    class StorageLocationProperty:
        def __init__(
            self,
            *,
            binary_prefix_location: typing.Optional[builtins.str] = None,
            bucket: typing.Optional[builtins.str] = None,
            generated_prefix_location: typing.Optional[builtins.str] = None,
            manifest_prefix_location: typing.Optional[builtins.str] = None,
            repo_prefix_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A storage location.

            :param binary_prefix_location: The location's binary prefix.
            :param bucket: The location's bucket.
            :param generated_prefix_location: The location's generated prefix.
            :param manifest_prefix_location: The location's manifest prefix.
            :param repo_prefix_location: The location's repo prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_panorama as panorama
                
                storage_location_property = panorama.CfnPackage.StorageLocationProperty(
                    binary_prefix_location="binaryPrefixLocation",
                    bucket="bucket",
                    generated_prefix_location="generatedPrefixLocation",
                    manifest_prefix_location="manifestPrefixLocation",
                    repo_prefix_location="repoPrefixLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3286a64cd538f8f19e491b45432ccd4a29b0293c63fa78201070b35cc800bd6b)
                check_type(argname="argument binary_prefix_location", value=binary_prefix_location, expected_type=type_hints["binary_prefix_location"])
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument generated_prefix_location", value=generated_prefix_location, expected_type=type_hints["generated_prefix_location"])
                check_type(argname="argument manifest_prefix_location", value=manifest_prefix_location, expected_type=type_hints["manifest_prefix_location"])
                check_type(argname="argument repo_prefix_location", value=repo_prefix_location, expected_type=type_hints["repo_prefix_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if binary_prefix_location is not None:
                self._values["binary_prefix_location"] = binary_prefix_location
            if bucket is not None:
                self._values["bucket"] = bucket
            if generated_prefix_location is not None:
                self._values["generated_prefix_location"] = generated_prefix_location
            if manifest_prefix_location is not None:
                self._values["manifest_prefix_location"] = manifest_prefix_location
            if repo_prefix_location is not None:
                self._values["repo_prefix_location"] = repo_prefix_location

        @builtins.property
        def binary_prefix_location(self) -> typing.Optional[builtins.str]:
            '''The location's binary prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html#cfn-panorama-package-storagelocation-binaryprefixlocation
            '''
            result = self._values.get("binary_prefix_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The location's bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html#cfn-panorama-package-storagelocation-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def generated_prefix_location(self) -> typing.Optional[builtins.str]:
            '''The location's generated prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html#cfn-panorama-package-storagelocation-generatedprefixlocation
            '''
            result = self._values.get("generated_prefix_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_prefix_location(self) -> typing.Optional[builtins.str]:
            '''The location's manifest prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html#cfn-panorama-package-storagelocation-manifestprefixlocation
            '''
            result = self._values.get("manifest_prefix_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def repo_prefix_location(self) -> typing.Optional[builtins.str]:
            '''The location's repo prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-panorama-package-storagelocation.html#cfn-panorama-package-storagelocation-repoprefixlocation
            '''
            result = self._values.get("repo_prefix_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_panorama.CfnPackageProps",
    jsii_struct_bases=[],
    name_mapping={
        "package_name": "packageName",
        "storage_location": "storageLocation",
        "tags": "tags",
    },
)
class CfnPackageProps:
    def __init__(
        self,
        *,
        package_name: builtins.str,
        storage_location: typing.Optional[typing.Union[typing.Union[CfnPackage.StorageLocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPackage``.

        :param package_name: A name for the package.
        :param storage_location: ``AWS::Panorama::Package.StorageLocation``.
        :param tags: Tags for the package.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_panorama as panorama
            
            cfn_package_props = panorama.CfnPackageProps(
                package_name="packageName",
            
                # the properties below are optional
                storage_location=panorama.CfnPackage.StorageLocationProperty(
                    binary_prefix_location="binaryPrefixLocation",
                    bucket="bucket",
                    generated_prefix_location="generatedPrefixLocation",
                    manifest_prefix_location="manifestPrefixLocation",
                    repo_prefix_location="repoPrefixLocation"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adfcbdba199c67d77c1c2cac7606414c9b7641e65322b294e97cdaa4f304a133)
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument storage_location", value=storage_location, expected_type=type_hints["storage_location"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "package_name": package_name,
        }
        if storage_location is not None:
            self._values["storage_location"] = storage_location
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def package_name(self) -> builtins.str:
        '''A name for the package.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html#cfn-panorama-package-packagename
        '''
        result = self._values.get("package_name")
        assert result is not None, "Required property 'package_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_location(
        self,
    ) -> typing.Optional[typing.Union[CfnPackage.StorageLocationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Panorama::Package.StorageLocation``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html#cfn-panorama-package-storagelocation
        '''
        result = self._values.get("storage_location")
        return typing.cast(typing.Optional[typing.Union[CfnPackage.StorageLocationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Tags for the package.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-package.html#cfn-panorama-package-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPackageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPackageVersion(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_panorama.CfnPackageVersion",
):
    '''A CloudFormation ``AWS::Panorama::PackageVersion``.

    Registers a package version.

    :cloudformationResource: AWS::Panorama::PackageVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_panorama as panorama
        
        cfn_package_version = panorama.CfnPackageVersion(self, "MyCfnPackageVersion",
            package_id="packageId",
            package_version="packageVersion",
            patch_version="patchVersion",
        
            # the properties below are optional
            mark_latest=False,
            owner_account="ownerAccount",
            updated_latest_patch_version="updatedLatestPatchVersion"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        package_id: builtins.str,
        package_version: builtins.str,
        patch_version: builtins.str,
        mark_latest: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        owner_account: typing.Optional[builtins.str] = None,
        updated_latest_patch_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Panorama::PackageVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param package_id: A package ID.
        :param package_version: A package version.
        :param patch_version: A patch version.
        :param mark_latest: Whether to mark the new version as the latest version.
        :param owner_account: An owner account.
        :param updated_latest_patch_version: If the version was marked latest, the new version to maker as latest.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845c2734be85531c84a59efcf3989b483ce5b17f5905360291f3d43388a6d841)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPackageVersionProps(
            package_id=package_id,
            package_version=package_version,
            patch_version=patch_version,
            mark_latest=mark_latest,
            owner_account=owner_account,
            updated_latest_patch_version=updated_latest_patch_version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6e4ad5b4667f633c7efcf9836dfa3dabe23dcacf5cf471c05e3c5fecd2f331)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c10fe87e00a9b633624875b7c1ccbdc920393881c991b44d6d5882eec100bc31)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrIsLatestPatch")
    def attr_is_latest_patch(self) -> _IResolvable_a771d0ef:
        '''Whether the package version is the latest version.

        :cloudformationAttribute: IsLatestPatch
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrIsLatestPatch"))

    @builtins.property
    @jsii.member(jsii_name="attrPackageArn")
    def attr_package_arn(self) -> builtins.str:
        '''The package version's ARN.

        :cloudformationAttribute: PackageArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPackageArn"))

    @builtins.property
    @jsii.member(jsii_name="attrPackageName")
    def attr_package_name(self) -> builtins.str:
        '''The package version's name.

        :cloudformationAttribute: PackageName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPackageName"))

    @builtins.property
    @jsii.member(jsii_name="attrRegisteredTime")
    def attr_registered_time(self) -> jsii.Number:
        '''The package version's registered time.

        :cloudformationAttribute: RegisteredTime
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrRegisteredTime"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The package version's status.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusDescription")
    def attr_status_description(self) -> builtins.str:
        '''The package version's status description.

        :cloudformationAttribute: StatusDescription
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusDescription"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="packageId")
    def package_id(self) -> builtins.str:
        '''A package ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-packageid
        '''
        return typing.cast(builtins.str, jsii.get(self, "packageId"))

    @package_id.setter
    def package_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4716b3745159dab59de4c1037dc292531819abda81c6464ebe90d7e58df126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageId", value)

    @builtins.property
    @jsii.member(jsii_name="packageVersion")
    def package_version(self) -> builtins.str:
        '''A package version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-packageversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "packageVersion"))

    @package_version.setter
    def package_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea9aa5e481fdd6494205260d393909d6b5c54464bb2c4dd5bb631e5ce62435c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageVersion", value)

    @builtins.property
    @jsii.member(jsii_name="patchVersion")
    def patch_version(self) -> builtins.str:
        '''A patch version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-patchversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "patchVersion"))

    @patch_version.setter
    def patch_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152b59085257ad7e59d46a8ab07baf1235f3bfe44104a57cb67964dbaada56ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patchVersion", value)

    @builtins.property
    @jsii.member(jsii_name="markLatest")
    def mark_latest(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Whether to mark the new version as the latest version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-marklatest
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "markLatest"))

    @mark_latest.setter
    def mark_latest(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc0a3981814cdb8aaa62d4d16315cde1ea2a1de85dd1c7b4239d851101bb642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "markLatest", value)

    @builtins.property
    @jsii.member(jsii_name="ownerAccount")
    def owner_account(self) -> typing.Optional[builtins.str]:
        '''An owner account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-owneraccount
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerAccount"))

    @owner_account.setter
    def owner_account(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2381373af77a5b70ec3721c786c51be50ea35ec5b3ebae792f025697a93fa3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownerAccount", value)

    @builtins.property
    @jsii.member(jsii_name="updatedLatestPatchVersion")
    def updated_latest_patch_version(self) -> typing.Optional[builtins.str]:
        '''If the version was marked latest, the new version to maker as latest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-updatedlatestpatchversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updatedLatestPatchVersion"))

    @updated_latest_patch_version.setter
    def updated_latest_patch_version(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f24584fd4145754212c9ccabfc0cd69c7c4034ec8cf4f86a94de7c1ce3d0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatedLatestPatchVersion", value)


@jsii.data_type(
    jsii_type="monocdk.aws_panorama.CfnPackageVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "package_id": "packageId",
        "package_version": "packageVersion",
        "patch_version": "patchVersion",
        "mark_latest": "markLatest",
        "owner_account": "ownerAccount",
        "updated_latest_patch_version": "updatedLatestPatchVersion",
    },
)
class CfnPackageVersionProps:
    def __init__(
        self,
        *,
        package_id: builtins.str,
        package_version: builtins.str,
        patch_version: builtins.str,
        mark_latest: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        owner_account: typing.Optional[builtins.str] = None,
        updated_latest_patch_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPackageVersion``.

        :param package_id: A package ID.
        :param package_version: A package version.
        :param patch_version: A patch version.
        :param mark_latest: Whether to mark the new version as the latest version.
        :param owner_account: An owner account.
        :param updated_latest_patch_version: If the version was marked latest, the new version to maker as latest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_panorama as panorama
            
            cfn_package_version_props = panorama.CfnPackageVersionProps(
                package_id="packageId",
                package_version="packageVersion",
                patch_version="patchVersion",
            
                # the properties below are optional
                mark_latest=False,
                owner_account="ownerAccount",
                updated_latest_patch_version="updatedLatestPatchVersion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ed6332aeee997b68f61bdc76f0b125f04db7d0f5a3c0bca5fcc578bdc2e4aa)
            check_type(argname="argument package_id", value=package_id, expected_type=type_hints["package_id"])
            check_type(argname="argument package_version", value=package_version, expected_type=type_hints["package_version"])
            check_type(argname="argument patch_version", value=patch_version, expected_type=type_hints["patch_version"])
            check_type(argname="argument mark_latest", value=mark_latest, expected_type=type_hints["mark_latest"])
            check_type(argname="argument owner_account", value=owner_account, expected_type=type_hints["owner_account"])
            check_type(argname="argument updated_latest_patch_version", value=updated_latest_patch_version, expected_type=type_hints["updated_latest_patch_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "package_id": package_id,
            "package_version": package_version,
            "patch_version": patch_version,
        }
        if mark_latest is not None:
            self._values["mark_latest"] = mark_latest
        if owner_account is not None:
            self._values["owner_account"] = owner_account
        if updated_latest_patch_version is not None:
            self._values["updated_latest_patch_version"] = updated_latest_patch_version

    @builtins.property
    def package_id(self) -> builtins.str:
        '''A package ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-packageid
        '''
        result = self._values.get("package_id")
        assert result is not None, "Required property 'package_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def package_version(self) -> builtins.str:
        '''A package version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-packageversion
        '''
        result = self._values.get("package_version")
        assert result is not None, "Required property 'package_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def patch_version(self) -> builtins.str:
        '''A patch version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-patchversion
        '''
        result = self._values.get("patch_version")
        assert result is not None, "Required property 'patch_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mark_latest(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Whether to mark the new version as the latest version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-marklatest
        '''
        result = self._values.get("mark_latest")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def owner_account(self) -> typing.Optional[builtins.str]:
        '''An owner account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-owneraccount
        '''
        result = self._values.get("owner_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updated_latest_patch_version(self) -> typing.Optional[builtins.str]:
        '''If the version was marked latest, the new version to maker as latest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-panorama-packageversion.html#cfn-panorama-packageversion-updatedlatestpatchversion
        '''
        result = self._values.get("updated_latest_patch_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPackageVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplicationInstance",
    "CfnApplicationInstanceProps",
    "CfnPackage",
    "CfnPackageProps",
    "CfnPackageVersion",
    "CfnPackageVersionProps",
]

publication.publish()

def _typecheckingstub__58844ecd20408ee621fe4618ad942892da770259acc25102774445e7c4bd2141(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    default_runtime_context_device: builtins.str,
    manifest_payload: typing.Union[typing.Union[CfnApplicationInstance.ManifestPayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    application_instance_id_to_replace: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    manifest_overrides_payload: typing.Optional[typing.Union[typing.Union[CfnApplicationInstance.ManifestOverridesPayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    runtime_role_arn: typing.Optional[builtins.str] = None,
    status_filter: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b22ba9004f91c94d8e9a0f58bf3a86698bc4ea3fb67de0c51985226f10bbc4b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2839f8fde36ba2af55175f64cc9c6aa2d69ff5e93ae0f82c86b0d09ffdbee697(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3b330c7f6b81d693f426a17326c1a8630ded9cd2ac12e96cbcde14dfe25ec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2c001c290943c2afd9889fef1ce95f1ccfa7ad7262285b3eda62ad4df4e5e8(
    value: typing.Union[CfnApplicationInstance.ManifestPayloadProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d6ef8513cffa578445b5701e9f9795fce6ffc1497e33972aa3ed23c72bd9fa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f745e9cb986a459bea6c89da9a3e24270c3ab886725bf291a86d348747b7b570(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c5f27bdbb06347d5ba893ffd8c09ff8833867b3112bc6c335352e34479a3ec(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5234bfb55c825f5d6488789088cadced331ffa851f3cf421fce8c7c21c26b14(
    value: typing.Optional[typing.Union[CfnApplicationInstance.ManifestOverridesPayloadProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d11edb6943b492b1fad88de0430c3372ab105b68f1188668147f3252f4b2cd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5b633e493b785fe265891df571e844db413311ef34b582102275c26df1e915(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14b10fe5a0c65758c13a0acbfd9316ff17bc8eeaa3ba84fbc0e003750b38c59(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e16b9b0013af6622a65e3fd7793248e307ca446f8f188e365f5480e8f1166b(
    *,
    payload_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7971eca2de16f3b3de3cdc8ec767666bca974b9fc9cc0cabc1a41a77e8cf58(
    *,
    payload_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af982778120f2ede7767796d8ffc48de33bc5fbd64a5e175baaac57ba6995c9f(
    *,
    default_runtime_context_device: builtins.str,
    manifest_payload: typing.Union[typing.Union[CfnApplicationInstance.ManifestPayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    application_instance_id_to_replace: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    manifest_overrides_payload: typing.Optional[typing.Union[typing.Union[CfnApplicationInstance.ManifestOverridesPayloadProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    runtime_role_arn: typing.Optional[builtins.str] = None,
    status_filter: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e920012df3013bb391769bac2b5e98320b7e7502914b48f8b05cce679dc825(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    package_name: builtins.str,
    storage_location: typing.Optional[typing.Union[typing.Union[CfnPackage.StorageLocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24497f19f48f4bb9bc226398ab83a339b4d482ad5fbf02fec48c5189c2ccc5e2(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c092468053c32a5c5ca3bb046bc8b089b19c1668e68bd0da81bedabc449325(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5565baf518d55a36a087b18c69db383209084d0bf614a5a68dfd40f9dba1a0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf909503030cb203fa18c2da175c56f4f7f913ec104da5bdb6155935567241b9(
    value: typing.Optional[typing.Union[CfnPackage.StorageLocationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3286a64cd538f8f19e491b45432ccd4a29b0293c63fa78201070b35cc800bd6b(
    *,
    binary_prefix_location: typing.Optional[builtins.str] = None,
    bucket: typing.Optional[builtins.str] = None,
    generated_prefix_location: typing.Optional[builtins.str] = None,
    manifest_prefix_location: typing.Optional[builtins.str] = None,
    repo_prefix_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adfcbdba199c67d77c1c2cac7606414c9b7641e65322b294e97cdaa4f304a133(
    *,
    package_name: builtins.str,
    storage_location: typing.Optional[typing.Union[typing.Union[CfnPackage.StorageLocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845c2734be85531c84a59efcf3989b483ce5b17f5905360291f3d43388a6d841(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    package_id: builtins.str,
    package_version: builtins.str,
    patch_version: builtins.str,
    mark_latest: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    owner_account: typing.Optional[builtins.str] = None,
    updated_latest_patch_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6e4ad5b4667f633c7efcf9836dfa3dabe23dcacf5cf471c05e3c5fecd2f331(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10fe87e00a9b633624875b7c1ccbdc920393881c991b44d6d5882eec100bc31(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4716b3745159dab59de4c1037dc292531819abda81c6464ebe90d7e58df126(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea9aa5e481fdd6494205260d393909d6b5c54464bb2c4dd5bb631e5ce62435c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152b59085257ad7e59d46a8ab07baf1235f3bfe44104a57cb67964dbaada56ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc0a3981814cdb8aaa62d4d16315cde1ea2a1de85dd1c7b4239d851101bb642(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2381373af77a5b70ec3721c786c51be50ea35ec5b3ebae792f025697a93fa3f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f24584fd4145754212c9ccabfc0cd69c7c4034ec8cf4f86a94de7c1ce3d0ff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ed6332aeee997b68f61bdc76f0b125f04db7d0f5a3c0bca5fcc578bdc2e4aa(
    *,
    package_id: builtins.str,
    package_version: builtins.str,
    patch_version: builtins.str,
    mark_latest: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    owner_account: typing.Optional[builtins.str] = None,
    updated_latest_patch_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
