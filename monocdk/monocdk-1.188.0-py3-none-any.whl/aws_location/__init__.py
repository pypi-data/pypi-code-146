'''
# AWS::Location Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as location
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Location construct libraries](https://constructs.dev/search?q=location)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Location resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Location.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Location](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Location.html).

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
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnGeofenceCollection(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_location.CfnGeofenceCollection",
):
    '''A CloudFormation ``AWS::Location::GeofenceCollection``.

    The ``AWS::Location::GeofenceCollection`` resource specifies the ability to detect and act when a tracked device enters or exits a defined geographical boundary known as a geofence.

    :cloudformationResource: AWS::Location::GeofenceCollection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_location as location
        
        cfn_geofence_collection = location.CfnGeofenceCollection(self, "MyCfnGeofenceCollection",
            collection_name="collectionName",
        
            # the properties below are optional
            description="description",
            kms_key_id="kmsKeyId",
            pricing_plan="pricingPlan",
            pricing_plan_data_source="pricingPlanDataSource"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        collection_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        pricing_plan_data_source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Location::GeofenceCollection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param collection_name: A custom name for the geofence collection. Requirements: - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_). - Must be a unique geofence collection name. - No spaces allowed. For example, ``ExampleGeofenceCollection`` .
        :param description: An optional description for the geofence collection.
        :param kms_key_id: A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` . *Allowed Values* : ``RequestBasedUsage``
        :param pricing_plan_data_source: This parameter is no longer used.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5194b718a761e2b36865b4979514eec5430e887673fd5fb8b65a467b614b0cc8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGeofenceCollectionProps(
            collection_name=collection_name,
            description=description,
            kms_key_id=kms_key_id,
            pricing_plan=pricing_plan,
            pricing_plan_data_source=pricing_plan_data_source,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1ce456452e864b417cf1348369129c6571486a1445ef322a2a75ba837ff481)
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
            type_hints = typing.get_type_hints(_typecheckingstub__749a20a6ae3eb2a3e3d61e081c3d83b54f12ad55d76fc322ef59ffb5c7a13308)
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
        '''The Amazon Resource Name (ARN) for the geofence collection resource.

        Used when you need to specify a resource across all AWS .

        - Format example: ``arn:aws:geo:region:account-id:geofence-collection/ExampleGeofenceCollection``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCollectionArn")
    def attr_collection_arn(self) -> builtins.str:
        '''Synonym for ``Arn`` .

        The Amazon Resource Name (ARN) for the geofence collection resource. Used when you need to specify a resource across all AWS .

        - Format example: ``arn:aws:geo:region:account-id:geofence-collection/ExampleGeofenceCollection``

        :cloudformationAttribute: CollectionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCollectionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreateTime")
    def attr_create_time(self) -> builtins.str:
        '''The timestamp for when the geofence collection resource was created in `ISO 8601 <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ format: ``YYYY-MM-DDThh:mm:ss.sssZ`` .

        :cloudformationAttribute: CreateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateTime")
    def attr_update_time(self) -> builtins.str:
        '''The timestamp for when the geofence collection resource was last updated in `ISO 8601 <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ format: ``YYYY-MM-DDThh:mm:ss.sssZ`` .

        :cloudformationAttribute: UpdateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="collectionName")
    def collection_name(self) -> builtins.str:
        '''A custom name for the geofence collection.

        Requirements:

        - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
        - Must be a unique geofence collection name.
        - No spaces allowed. For example, ``ExampleGeofenceCollection`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-collectionname
        '''
        return typing.cast(builtins.str, jsii.get(self, "collectionName"))

    @collection_name.setter
    def collection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de53f70a92eb84956f1293a9ee089b06b924b0a4fd4587936724ac67fc14b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the geofence collection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3be9b5d8201beefc5dea6f911fca1e0a901089e10c2e49da964033f70cd6f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28afa53b421338172e3fe4d4839c8934b83f99514679ae1dd770e49a03dd15f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="pricingPlan")
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used. If included, the only allowed value is ``RequestBasedUsage`` .

        *Allowed Values* : ``RequestBasedUsage``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-pricingplan
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingPlan"))

    @pricing_plan.setter
    def pricing_plan(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf83a895634a31d5222f816f637a7d5213aad8cd37647688fb2b1e598c9e7e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlan", value)

    @builtins.property
    @jsii.member(jsii_name="pricingPlanDataSource")
    def pricing_plan_data_source(self) -> typing.Optional[builtins.str]:
        '''This parameter is no longer used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-pricingplandatasource
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingPlanDataSource"))

    @pricing_plan_data_source.setter
    def pricing_plan_data_source(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7e85ed033c7a1a16266ff13d38f242cbe6c03ddae95a08030da025d47a7e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlanDataSource", value)


@jsii.data_type(
    jsii_type="monocdk.aws_location.CfnGeofenceCollectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "collection_name": "collectionName",
        "description": "description",
        "kms_key_id": "kmsKeyId",
        "pricing_plan": "pricingPlan",
        "pricing_plan_data_source": "pricingPlanDataSource",
    },
)
class CfnGeofenceCollectionProps:
    def __init__(
        self,
        *,
        collection_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        pricing_plan_data_source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnGeofenceCollection``.

        :param collection_name: A custom name for the geofence collection. Requirements: - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_). - Must be a unique geofence collection name. - No spaces allowed. For example, ``ExampleGeofenceCollection`` .
        :param description: An optional description for the geofence collection.
        :param kms_key_id: A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` . *Allowed Values* : ``RequestBasedUsage``
        :param pricing_plan_data_source: This parameter is no longer used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_location as location
            
            cfn_geofence_collection_props = location.CfnGeofenceCollectionProps(
                collection_name="collectionName",
            
                # the properties below are optional
                description="description",
                kms_key_id="kmsKeyId",
                pricing_plan="pricingPlan",
                pricing_plan_data_source="pricingPlanDataSource"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faaf80475179505a24d76442b7d124aeabf8f4f4061fcea03e506768a4a4ca4f)
            check_type(argname="argument collection_name", value=collection_name, expected_type=type_hints["collection_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument pricing_plan", value=pricing_plan, expected_type=type_hints["pricing_plan"])
            check_type(argname="argument pricing_plan_data_source", value=pricing_plan_data_source, expected_type=type_hints["pricing_plan_data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "collection_name": collection_name,
        }
        if description is not None:
            self._values["description"] = description
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if pricing_plan is not None:
            self._values["pricing_plan"] = pricing_plan
        if pricing_plan_data_source is not None:
            self._values["pricing_plan_data_source"] = pricing_plan_data_source

    @builtins.property
    def collection_name(self) -> builtins.str:
        '''A custom name for the geofence collection.

        Requirements:

        - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
        - Must be a unique geofence collection name.
        - No spaces allowed. For example, ``ExampleGeofenceCollection`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-collectionname
        '''
        result = self._values.get("collection_name")
        assert result is not None, "Required property 'collection_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the geofence collection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used. If included, the only allowed value is ``RequestBasedUsage`` .

        *Allowed Values* : ``RequestBasedUsage``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-pricingplan
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan_data_source(self) -> typing.Optional[builtins.str]:
        '''This parameter is no longer used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-pricingplandatasource
        '''
        result = self._values.get("pricing_plan_data_source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGeofenceCollectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnMap(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_location.CfnMap",
):
    '''A CloudFormation ``AWS::Location::Map``.

    The ``AWS::Location::Map`` resource specifies a map resource in your AWS account, which provides map tiles of different styles sourced from global location data providers.

    :cloudformationResource: AWS::Location::Map
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_location as location
        
        cfn_map = location.CfnMap(self, "MyCfnMap",
            configuration=location.CfnMap.MapConfigurationProperty(
                style="style"
            ),
            map_name="mapName",
        
            # the properties below are optional
            description="description",
            pricing_plan="pricingPlan"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        configuration: typing.Union[typing.Union["CfnMap.MapConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        map_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Location::Map``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param configuration: Specifies the ``MapConfiguration`` , including the map style, for the map resource that you create. The map style defines the look of maps and the data provider for your map resource.
        :param map_name: The name for the map resource. Requirements: - Must contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_). - Must be a unique map resource name. - No spaces allowed. For example, ``ExampleMap`` .
        :param description: An optional description for the map resource.
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` . *Allowed Values* : ``RequestBasedUsage``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61965e15228b6b61ae0eb24ea9f6c7ea50e056d3b3ab26113607d8c981469a2d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMapProps(
            configuration=configuration,
            map_name=map_name,
            description=description,
            pricing_plan=pricing_plan,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b207b93d25b9810a09ed802c59af6addc11d91ce3c8e8e9d1a4badfec90f5592)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6122a4fddd5898c78a765b3c0840c3ef0298cc675cbc6adffc612fa3fbb93258)
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
        '''The Amazon Resource Name (ARN) for the map resource. Used to specify a resource across all AWS .

        - Format example: ``arn:aws:geo:region:account-id:maps/ExampleMap``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreateTime")
    def attr_create_time(self) -> builtins.str:
        '''The timestamp for when the map resource was created in `ISO 8601 <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ format: ``YYYY-MM-DDThh:mm:ss.sssZ`` .

        :cloudformationAttribute: CreateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrDataSource")
    def attr_data_source(self) -> builtins.str:
        '''The data provider for the associated map tiles.

        :cloudformationAttribute: DataSource
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDataSource"))

    @builtins.property
    @jsii.member(jsii_name="attrMapArn")
    def attr_map_arn(self) -> builtins.str:
        '''Synonym for ``Arn`` .

        The Amazon Resource Name (ARN) for the map resource. Used to specify a resource across all AWS .

        - Format example: ``arn:aws:geo:region:account-id:maps/ExampleMap``

        :cloudformationAttribute: MapArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMapArn"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateTime")
    def attr_update_time(self) -> builtins.str:
        '''The timestamp for when the map resource was last updated in `ISO 8601 <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ format: ``YYYY-MM-DDThh:mm:ss.sssZ`` .

        :cloudformationAttribute: UpdateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Union["CfnMap.MapConfigurationProperty", _IResolvable_a771d0ef]:
        '''Specifies the ``MapConfiguration`` , including the map style, for the map resource that you create.

        The map style defines the look of maps and the data provider for your map resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-configuration
        '''
        return typing.cast(typing.Union["CfnMap.MapConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: typing.Union["CfnMap.MapConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ba85181ef6e4287c2a126c75e1dd8071fba27e3971ee250e9a3cf6702c631b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="mapName")
    def map_name(self) -> builtins.str:
        '''The name for the map resource.

        Requirements:

        - Must contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
        - Must be a unique map resource name.
        - No spaces allowed. For example, ``ExampleMap`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-mapname
        '''
        return typing.cast(builtins.str, jsii.get(self, "mapName"))

    @map_name.setter
    def map_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbed74f27c87010d98ebeb923c76a78034f3daa544774ed562793d8a97ffdd24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the map resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743ecea26a102d8a65235b8c8e0f73ee595ba2c99da9bfe9853415afe2f22840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="pricingPlan")
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used. If included, the only allowed value is ``RequestBasedUsage`` .

        *Allowed Values* : ``RequestBasedUsage``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-pricingplan
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingPlan"))

    @pricing_plan.setter
    def pricing_plan(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a476d79ecb23c52997ac7ed300d81e7a2bf1e4c3cd4d072724b4e4f25cabda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlan", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_location.CfnMap.MapConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"style": "style"},
    )
    class MapConfigurationProperty:
        def __init__(self, *, style: builtins.str) -> None:
            '''Specifies the map tile style selected from an available provider.

            :param style: Specifies the map style selected from an available data provider. Valid `Esri map styles <https://docs.aws.amazon.com/location/latest/developerguide/esri.html>`_ : - ``VectorEsriDarkGrayCanvas`` – The Esri Dark Gray Canvas map style. A vector basemap with a dark gray, neutral background with minimal colors, labels, and features that's designed to draw attention to your thematic content. - ``RasterEsriImagery`` – The Esri Imagery map style. A raster basemap that provides one meter or better satellite and aerial imagery in many parts of the world and lower resolution satellite imagery worldwide. - ``VectorEsriLightGrayCanvas`` – The Esri Light Gray Canvas map style, which provides a detailed vector basemap with a light gray, neutral background style with minimal colors, labels, and features that's designed to draw attention to your thematic content. - ``VectorEsriTopographic`` – The Esri Light map style, which provides a detailed vector basemap with a classic Esri map style. - ``VectorEsriStreets`` – The Esri World Streets map style, which provides a detailed vector basemap for the world symbolized with a classic Esri street map style. The vector tile layer is similar in content and style to the World Street Map raster map. - ``VectorEsriNavigation`` – The Esri World Navigation map style, which provides a detailed basemap for the world symbolized with a custom navigation map style that's designed for use during the day in mobile devices. Valid `HERE Technologies map styles <https://docs.aws.amazon.com/location/latest/developerguide/HERE.html>`_ : - ``VectorHereContrast`` – The HERE Contrast (Berlin) map style is a high contrast detailed base map of the world that blends 3D and 2D rendering. .. epigraph:: The ``VectorHereContrast`` style has been renamed from ``VectorHereBerlin`` . ``VectorHereBerlin`` has been deprecated, but will continue to work in applications that use it. - ``VectorHereExplore`` – A default HERE map style containing a neutral, global map and its features including roads, buildings, landmarks, and water features. It also now includes a fully designed map of Japan. - ``VectorHereExploreTruck`` – A global map containing truck restrictions and attributes (e.g. width / height / HAZMAT) symbolized with highlighted segments and icons on top of HERE Explore to support use cases within transport and logistics. - ``RasterHereExploreSatellite`` – A global map containing high resolution satellite imagery. - ``HybridHereExploreSatellite`` – A global map displaying the road network, street names, and city labels over satellite imagery. This style will automatically retrieve both raster and vector tiles, and your charges will be based on total tiles retrieved. .. epigraph:: Hybrid styles use both vector and raster tiles when rendering the map that you see. This means that more tiles are retrieved than when using either vector or raster tiles alone. Your charges will include all tiles retrieved. Valid `GrabMaps map styles <https://docs.aws.amazon.com/location/latest/developerguide/grab.html>`_ : - ``VectorGrabStandardLight`` – The Grab Standard Light map style provides a basemap with detailed land use coloring, area names, roads, landmarks, and points of interest covering Southeast Asia. - ``VectorGrabStandardDark`` – The Grab Standard Dark map style provides a dark variation of the standard basemap covering Southeast Asia. .. epigraph:: Grab provides maps only for countries in Southeast Asia, and is only available in the Asia Pacific (Singapore) Region ( ``ap-southeast-1`` ). For more information, see `GrabMaps countries and area covered <https://docs.aws.amazon.com/location/latest/developerguide/grab.html#grab-coverage-area>`_ . Valid `Open Data (Preview) map styles <https://docs.aws.amazon.com/location/latest/developerguide/open-data.html>`_ : - ``VectorOpenDataStandardLight`` – The Open Data Standard Light (preview) map style provides a detailed basemap for the world suitable for website and mobile application use. The map includes highways major roads, minor roads, railways, water features, cities, parks, landmarks, building footprints, and administrative boundaries. .. epigraph:: Open Data maps is in preview. We may add, change, or remove features before announcing general availability. For more information, see `Open Data is in preview release <https://docs.aws.amazon.com/location/latest/developerguide/open-data.html#open-data-preview>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-map-mapconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_location as location
                
                map_configuration_property = location.CfnMap.MapConfigurationProperty(
                    style="style"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b15d01b8c829e58006cf4fc762fb3ec80a23357f9e9c7a2dc16473010b99361c)
                check_type(argname="argument style", value=style, expected_type=type_hints["style"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "style": style,
            }

        @builtins.property
        def style(self) -> builtins.str:
            '''Specifies the map style selected from an available data provider.

            Valid `Esri map styles <https://docs.aws.amazon.com/location/latest/developerguide/esri.html>`_ :

            - ``VectorEsriDarkGrayCanvas`` – The Esri Dark Gray Canvas map style. A vector basemap with a dark gray, neutral background with minimal colors, labels, and features that's designed to draw attention to your thematic content.
            - ``RasterEsriImagery`` – The Esri Imagery map style. A raster basemap that provides one meter or better satellite and aerial imagery in many parts of the world and lower resolution satellite imagery worldwide.
            - ``VectorEsriLightGrayCanvas`` – The Esri Light Gray Canvas map style, which provides a detailed vector basemap with a light gray, neutral background style with minimal colors, labels, and features that's designed to draw attention to your thematic content.
            - ``VectorEsriTopographic`` – The Esri Light map style, which provides a detailed vector basemap with a classic Esri map style.
            - ``VectorEsriStreets`` – The Esri World Streets map style, which provides a detailed vector basemap for the world symbolized with a classic Esri street map style. The vector tile layer is similar in content and style to the World Street Map raster map.
            - ``VectorEsriNavigation`` – The Esri World Navigation map style, which provides a detailed basemap for the world symbolized with a custom navigation map style that's designed for use during the day in mobile devices.

            Valid `HERE Technologies map styles <https://docs.aws.amazon.com/location/latest/developerguide/HERE.html>`_ :

            - ``VectorHereContrast`` – The HERE Contrast (Berlin) map style is a high contrast detailed base map of the world that blends 3D and 2D rendering.

            .. epigraph::

               The ``VectorHereContrast`` style has been renamed from ``VectorHereBerlin`` . ``VectorHereBerlin`` has been deprecated, but will continue to work in applications that use it.

            - ``VectorHereExplore`` – A default HERE map style containing a neutral, global map and its features including roads, buildings, landmarks, and water features. It also now includes a fully designed map of Japan.
            - ``VectorHereExploreTruck`` – A global map containing truck restrictions and attributes (e.g. width / height / HAZMAT) symbolized with highlighted segments and icons on top of HERE Explore to support use cases within transport and logistics.
            - ``RasterHereExploreSatellite`` – A global map containing high resolution satellite imagery.
            - ``HybridHereExploreSatellite`` – A global map displaying the road network, street names, and city labels over satellite imagery. This style will automatically retrieve both raster and vector tiles, and your charges will be based on total tiles retrieved.

            .. epigraph::

               Hybrid styles use both vector and raster tiles when rendering the map that you see. This means that more tiles are retrieved than when using either vector or raster tiles alone. Your charges will include all tiles retrieved.

            Valid `GrabMaps map styles <https://docs.aws.amazon.com/location/latest/developerguide/grab.html>`_ :

            - ``VectorGrabStandardLight`` – The Grab Standard Light map style provides a basemap with detailed land use coloring, area names, roads, landmarks, and points of interest covering Southeast Asia.
            - ``VectorGrabStandardDark`` – The Grab Standard Dark map style provides a dark variation of the standard basemap covering Southeast Asia.

            .. epigraph::

               Grab provides maps only for countries in Southeast Asia, and is only available in the Asia Pacific (Singapore) Region ( ``ap-southeast-1`` ). For more information, see `GrabMaps countries and area covered <https://docs.aws.amazon.com/location/latest/developerguide/grab.html#grab-coverage-area>`_ .

            Valid `Open Data (Preview) map styles <https://docs.aws.amazon.com/location/latest/developerguide/open-data.html>`_ :

            - ``VectorOpenDataStandardLight`` – The Open Data Standard Light (preview) map style provides a detailed basemap for the world suitable for website and mobile application use. The map includes highways major roads, minor roads, railways, water features, cities, parks, landmarks, building footprints, and administrative boundaries.

            .. epigraph::

               Open Data maps is in preview. We may add, change, or remove features before announcing general availability. For more information, see `Open Data is in preview release <https://docs.aws.amazon.com/location/latest/developerguide/open-data.html#open-data-preview>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-map-mapconfiguration.html#cfn-location-map-mapconfiguration-style
            '''
            result = self._values.get("style")
            assert result is not None, "Required property 'style' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MapConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_location.CfnMapProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "map_name": "mapName",
        "description": "description",
        "pricing_plan": "pricingPlan",
    },
)
class CfnMapProps:
    def __init__(
        self,
        *,
        configuration: typing.Union[typing.Union[CfnMap.MapConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        map_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnMap``.

        :param configuration: Specifies the ``MapConfiguration`` , including the map style, for the map resource that you create. The map style defines the look of maps and the data provider for your map resource.
        :param map_name: The name for the map resource. Requirements: - Must contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_). - Must be a unique map resource name. - No spaces allowed. For example, ``ExampleMap`` .
        :param description: An optional description for the map resource.
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` . *Allowed Values* : ``RequestBasedUsage``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_location as location
            
            cfn_map_props = location.CfnMapProps(
                configuration=location.CfnMap.MapConfigurationProperty(
                    style="style"
                ),
                map_name="mapName",
            
                # the properties below are optional
                description="description",
                pricing_plan="pricingPlan"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71782980c56d8598397d541f96858d65ca8843083651a16589fcfa7cc31f4f1)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument map_name", value=map_name, expected_type=type_hints["map_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument pricing_plan", value=pricing_plan, expected_type=type_hints["pricing_plan"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration": configuration,
            "map_name": map_name,
        }
        if description is not None:
            self._values["description"] = description
        if pricing_plan is not None:
            self._values["pricing_plan"] = pricing_plan

    @builtins.property
    def configuration(
        self,
    ) -> typing.Union[CfnMap.MapConfigurationProperty, _IResolvable_a771d0ef]:
        '''Specifies the ``MapConfiguration`` , including the map style, for the map resource that you create.

        The map style defines the look of maps and the data provider for your map resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-configuration
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast(typing.Union[CfnMap.MapConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def map_name(self) -> builtins.str:
        '''The name for the map resource.

        Requirements:

        - Must contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
        - Must be a unique map resource name.
        - No spaces allowed. For example, ``ExampleMap`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-mapname
        '''
        result = self._values.get("map_name")
        assert result is not None, "Required property 'map_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the map resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used. If included, the only allowed value is ``RequestBasedUsage`` .

        *Allowed Values* : ``RequestBasedUsage``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-pricingplan
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMapProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPlaceIndex(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_location.CfnPlaceIndex",
):
    '''A CloudFormation ``AWS::Location::PlaceIndex``.

    Creates a place index resource in your AWS account. Use a place index resource to geocode addresses and other text queries by using the ``SearchPlaceIndexForText`` operation, and reverse geocode coordinates by using the ``SearchPlaceIndexForPosition`` operation, and enable autosuggestions by using the ``SearchPlaceIndexForSuggestions`` operation.
    .. epigraph::

       If your application is tracking or routing assets you use in your business, such as delivery vehicles or employees, you must not use Esri as your geolocation provider. See section 82 of the `AWS service terms <https://docs.aws.amazon.com/service-terms>`_ for more details.

    :cloudformationResource: AWS::Location::PlaceIndex
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_location as location
        
        cfn_place_index = location.CfnPlaceIndex(self, "MyCfnPlaceIndex",
            data_source="dataSource",
            index_name="indexName",
        
            # the properties below are optional
            data_source_configuration=location.CfnPlaceIndex.DataSourceConfigurationProperty(
                intended_use="intendedUse"
            ),
            description="description",
            pricing_plan="pricingPlan"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        data_source: builtins.str,
        index_name: builtins.str,
        data_source_configuration: typing.Optional[typing.Union[typing.Union["CfnPlaceIndex.DataSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Location::PlaceIndex``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data_source: Specifies the geospatial data provider for the new place index. .. epigraph:: This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error. Valid values include: - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/latest/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on geocoding coverage <https://docs.aws.amazon.com/https://developers.arcgis.com/rest/geocode/api-reference/geocode-coverage.htm>`_ . - ``Grab`` – Grab provides place index functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/latest/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/latest/developerguide/grab.html#grab-coverage-area>`_ . - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/latest/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE details on goecoding coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/geocoder/dev_guide/topics/coverage-geocoder.html>`_ . .. epigraph:: If you specify HERE Technologies ( ``Here`` ) as the data provider, you may not `store results <https://docs.aws.amazon.com//location-places/latest/APIReference/API_DataSourceConfiguration.html>`_ for locations in Japan. For more information, see the `AWS Service Terms <https://docs.aws.amazon.com/service-terms/>`_ for Amazon Location Service. For additional information , see `Data providers <https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service Developer Guide* .
        :param index_name: The name of the place index resource. Requirements: - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_). - Must be a unique place index resource name. - No spaces allowed. For example, ``ExamplePlaceIndex`` .
        :param data_source_configuration: Specifies the data storage option for requesting Places.
        :param description: The optional description for the place index resource.
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` . *Allowed Values* : ``RequestBasedUsage``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ff36650fade187b3a3ee9372c417724bb11f64a2ec8f29ffbca93c9cb1cb24)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPlaceIndexProps(
            data_source=data_source,
            index_name=index_name,
            data_source_configuration=data_source_configuration,
            description=description,
            pricing_plan=pricing_plan,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63fb52c6b80eeeb0881d035743d2e9025a1eeee41377c9dc4dd1e9061991f99d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe7832de0a0526c94809b6e360ef4480c69a2d0c7c93ae4b3c36cde4064df9a8)
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
        '''The Amazon Resource Name (ARN) for the place index resource. Used to specify a resource across AWS .

        - Format example: ``arn:aws:geo:region:account-id:place-index/ExamplePlaceIndex``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreateTime")
    def attr_create_time(self) -> builtins.str:
        '''The timestamp for when the place index resource was created in `ISO 8601 <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ format: ``YYYY-MM-DDThh:mm:ss.sssZ`` .

        :cloudformationAttribute: CreateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrIndexArn")
    def attr_index_arn(self) -> builtins.str:
        '''Synonym for ``Arn`` .

        The Amazon Resource Name (ARN) for the place index resource. Used to specify a resource across AWS .

        - Format example: ``arn:aws:geo:region:account-id:place-index/ExamplePlaceIndex``

        :cloudformationAttribute: IndexArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrIndexArn"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateTime")
    def attr_update_time(self) -> builtins.str:
        '''The timestamp for when the place index resource was last updated in `ISO 8601 <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ format: ``YYYY-MM-DDThh:mm:ss.sssZ`` .

        :cloudformationAttribute: UpdateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="dataSource")
    def data_source(self) -> builtins.str:
        '''Specifies the geospatial data provider for the new place index.

        .. epigraph::

           This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error.

        Valid values include:

        - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/latest/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on geocoding coverage <https://docs.aws.amazon.com/https://developers.arcgis.com/rest/geocode/api-reference/geocode-coverage.htm>`_ .
        - ``Grab`` – Grab provides place index functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/latest/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/latest/developerguide/grab.html#grab-coverage-area>`_ .
        - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/latest/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE details on goecoding coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/geocoder/dev_guide/topics/coverage-geocoder.html>`_ .

        .. epigraph::

           If you specify HERE Technologies ( ``Here`` ) as the data provider, you may not `store results <https://docs.aws.amazon.com//location-places/latest/APIReference/API_DataSourceConfiguration.html>`_ for locations in Japan. For more information, see the `AWS Service Terms <https://docs.aws.amazon.com/service-terms/>`_ for Amazon Location Service.

        For additional information , see `Data providers <https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-datasource
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSource"))

    @data_source.setter
    def data_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514f314f7e6c3a8fdb93e617fbf9e60ee6214c4c089f6a7dd9dbb98c1ef3c788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSource", value)

    @builtins.property
    @jsii.member(jsii_name="indexName")
    def index_name(self) -> builtins.str:
        '''The name of the place index resource.

        Requirements:

        - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
        - Must be a unique place index resource name.
        - No spaces allowed. For example, ``ExamplePlaceIndex`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-indexname
        '''
        return typing.cast(builtins.str, jsii.get(self, "indexName"))

    @index_name.setter
    def index_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc7984259ca6fc773117bbe828fcc6ca1571cbee9afe86914d6d99b817ae9d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexName", value)

    @builtins.property
    @jsii.member(jsii_name="dataSourceConfiguration")
    def data_source_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnPlaceIndex.DataSourceConfigurationProperty", _IResolvable_a771d0ef]]:
        '''Specifies the data storage option for requesting Places.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-datasourceconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPlaceIndex.DataSourceConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "dataSourceConfiguration"))

    @data_source_configuration.setter
    def data_source_configuration(
        self,
        value: typing.Optional[typing.Union["CfnPlaceIndex.DataSourceConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864b8aa3447a5f044fa4b5e4c2cef33c3bd2c9aad9ede4edba55b9aeb961408b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The optional description for the place index resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02cede97e4545e30674fee6009a369662f3f05adfb1c97bafa9979e1b215bf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="pricingPlan")
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used. If included, the only allowed value is ``RequestBasedUsage`` .

        *Allowed Values* : ``RequestBasedUsage``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-pricingplan
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingPlan"))

    @pricing_plan.setter
    def pricing_plan(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73198f8d173265a14f5d8b3d295f01bb3231141ab4d29d21f75b92e4e3abf6e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlan", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_location.CfnPlaceIndex.DataSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"intended_use": "intendedUse"},
    )
    class DataSourceConfigurationProperty:
        def __init__(
            self,
            *,
            intended_use: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the data storage option for requesting Places.

            :param intended_use: Specifies how the results of an operation will be stored by the caller. Valid values include: - ``SingleUse`` specifies that the results won't be stored. - ``Storage`` specifies that the result can be cached or stored in a database. .. epigraph:: Place index resources using HERE as a data provider can't be configured to store results for locations in Japan when choosing ``Storage`` for the ``IntendedUse`` parameter. Default value: ``SingleUse``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-placeindex-datasourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_location as location
                
                data_source_configuration_property = location.CfnPlaceIndex.DataSourceConfigurationProperty(
                    intended_use="intendedUse"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02d177c8cf697b24a9984386d2ef7284a635d33f044b02706eb3f86afc212e48)
                check_type(argname="argument intended_use", value=intended_use, expected_type=type_hints["intended_use"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if intended_use is not None:
                self._values["intended_use"] = intended_use

        @builtins.property
        def intended_use(self) -> typing.Optional[builtins.str]:
            '''Specifies how the results of an operation will be stored by the caller.

            Valid values include:

            - ``SingleUse`` specifies that the results won't be stored.
            - ``Storage`` specifies that the result can be cached or stored in a database.

            .. epigraph::

               Place index resources using HERE as a data provider can't be configured to store results for locations in Japan when choosing ``Storage`` for the ``IntendedUse`` parameter.

            Default value: ``SingleUse``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-placeindex-datasourceconfiguration.html#cfn-location-placeindex-datasourceconfiguration-intendeduse
            '''
            result = self._values.get("intended_use")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_location.CfnPlaceIndexProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_source": "dataSource",
        "index_name": "indexName",
        "data_source_configuration": "dataSourceConfiguration",
        "description": "description",
        "pricing_plan": "pricingPlan",
    },
)
class CfnPlaceIndexProps:
    def __init__(
        self,
        *,
        data_source: builtins.str,
        index_name: builtins.str,
        data_source_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaceIndex.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPlaceIndex``.

        :param data_source: Specifies the geospatial data provider for the new place index. .. epigraph:: This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error. Valid values include: - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/latest/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on geocoding coverage <https://docs.aws.amazon.com/https://developers.arcgis.com/rest/geocode/api-reference/geocode-coverage.htm>`_ . - ``Grab`` – Grab provides place index functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/latest/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/latest/developerguide/grab.html#grab-coverage-area>`_ . - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/latest/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE details on goecoding coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/geocoder/dev_guide/topics/coverage-geocoder.html>`_ . .. epigraph:: If you specify HERE Technologies ( ``Here`` ) as the data provider, you may not `store results <https://docs.aws.amazon.com//location-places/latest/APIReference/API_DataSourceConfiguration.html>`_ for locations in Japan. For more information, see the `AWS Service Terms <https://docs.aws.amazon.com/service-terms/>`_ for Amazon Location Service. For additional information , see `Data providers <https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service Developer Guide* .
        :param index_name: The name of the place index resource. Requirements: - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_). - Must be a unique place index resource name. - No spaces allowed. For example, ``ExamplePlaceIndex`` .
        :param data_source_configuration: Specifies the data storage option for requesting Places.
        :param description: The optional description for the place index resource.
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` . *Allowed Values* : ``RequestBasedUsage``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_location as location
            
            cfn_place_index_props = location.CfnPlaceIndexProps(
                data_source="dataSource",
                index_name="indexName",
            
                # the properties below are optional
                data_source_configuration=location.CfnPlaceIndex.DataSourceConfigurationProperty(
                    intended_use="intendedUse"
                ),
                description="description",
                pricing_plan="pricingPlan"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa3d95cae2a4e33e7a1b5a0725a1d0fddd2491893da78b8a750f2381e910a93)
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument data_source_configuration", value=data_source_configuration, expected_type=type_hints["data_source_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument pricing_plan", value=pricing_plan, expected_type=type_hints["pricing_plan"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source": data_source,
            "index_name": index_name,
        }
        if data_source_configuration is not None:
            self._values["data_source_configuration"] = data_source_configuration
        if description is not None:
            self._values["description"] = description
        if pricing_plan is not None:
            self._values["pricing_plan"] = pricing_plan

    @builtins.property
    def data_source(self) -> builtins.str:
        '''Specifies the geospatial data provider for the new place index.

        .. epigraph::

           This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error.

        Valid values include:

        - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/latest/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on geocoding coverage <https://docs.aws.amazon.com/https://developers.arcgis.com/rest/geocode/api-reference/geocode-coverage.htm>`_ .
        - ``Grab`` – Grab provides place index functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/latest/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/latest/developerguide/grab.html#grab-coverage-area>`_ .
        - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/latest/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE details on goecoding coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/geocoder/dev_guide/topics/coverage-geocoder.html>`_ .

        .. epigraph::

           If you specify HERE Technologies ( ``Here`` ) as the data provider, you may not `store results <https://docs.aws.amazon.com//location-places/latest/APIReference/API_DataSourceConfiguration.html>`_ for locations in Japan. For more information, see the `AWS Service Terms <https://docs.aws.amazon.com/service-terms/>`_ for Amazon Location Service.

        For additional information , see `Data providers <https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-datasource
        '''
        result = self._values.get("data_source")
        assert result is not None, "Required property 'data_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index_name(self) -> builtins.str:
        '''The name of the place index resource.

        Requirements:

        - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
        - Must be a unique place index resource name.
        - No spaces allowed. For example, ``ExamplePlaceIndex`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-indexname
        '''
        result = self._values.get("index_name")
        assert result is not None, "Required property 'index_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnPlaceIndex.DataSourceConfigurationProperty, _IResolvable_a771d0ef]]:
        '''Specifies the data storage option for requesting Places.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-datasourceconfiguration
        '''
        result = self._values.get("data_source_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnPlaceIndex.DataSourceConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The optional description for the place index resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used. If included, the only allowed value is ``RequestBasedUsage`` .

        *Allowed Values* : ``RequestBasedUsage``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-pricingplan
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlaceIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRouteCalculator(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_location.CfnRouteCalculator",
):
    '''A CloudFormation ``AWS::Location::RouteCalculator``.

    Creates a route calculator resource in your AWS account.

    You can send requests to a route calculator resource to estimate travel time, distance, and get directions. A route calculator sources traffic and road network data from your chosen data provider.
    .. epigraph::

       If your application is tracking or routing assets you use in your business, such as delivery vehicles or employees, you must not use Esri as your geolocation provider. See section 82 of the `AWS service terms <https://docs.aws.amazon.com/service-terms>`_ for more details.

    :cloudformationResource: AWS::Location::RouteCalculator
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_location as location
        
        cfn_route_calculator = location.CfnRouteCalculator(self, "MyCfnRouteCalculator",
            calculator_name="calculatorName",
            data_source="dataSource",
        
            # the properties below are optional
            description="description",
            pricing_plan="pricingPlan"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        calculator_name: builtins.str,
        data_source: builtins.str,
        description: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Location::RouteCalculator``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param calculator_name: The name of the route calculator resource. Requirements: - Can use alphanumeric characters (A–Z, a–z, 0–9) , hyphens (-), periods (.), and underscores (_). - Must be a unique route calculator resource name. - No spaces allowed. For example, ``ExampleRouteCalculator`` .
        :param data_source: Specifies the data provider of traffic and road network data. .. epigraph:: This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error. Valid values include: - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/latest/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on street networks and traffic coverage <https://docs.aws.amazon.com/https://doc.arcgis.com/en/arcgis-online/reference/network-coverage.htm>`_ . Route calculators that use Esri as a data source only calculate routes that are shorter than 400 km. - ``Grab`` – Grab provides routing functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/latest/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/latest/developerguide/grab.html#grab-coverage-area>`_ . - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/latest/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE car routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/car-routing.html>`_ and `HERE truck routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/truck-routing.html>`_ . For additional information , see `Data providers <https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service Developer Guide* .
        :param description: The optional description for the route calculator resource.
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` . *Allowed Values* : ``RequestBasedUsage``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e580485e8d9f0c8889272d20975130827a5c497cd42b373c64897a63f62b1fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRouteCalculatorProps(
            calculator_name=calculator_name,
            data_source=data_source,
            description=description,
            pricing_plan=pricing_plan,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e5b7bb5b55b5365afc92501e3aa721ede4fb35f7ab3e413df5b476f697f48c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5864cc3ee387760b5cf09b6ba6f23fc5f7b4896bb391ea5858275e02934a2e1)
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
        '''The Amazon Resource Name (ARN) for the route calculator resource.

        Use the ARN when you specify a resource across all AWS .

        - Format example: ``arn:aws:geo:region:account-id:route-calculator/ExampleCalculator``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCalculatorArn")
    def attr_calculator_arn(self) -> builtins.str:
        '''Synonym for ``Arn`` .

        The Amazon Resource Name (ARN) for the route calculator resource. Use the ARN when you specify a resource across all AWS .

        - Format example: ``arn:aws:geo:region:account-id:route-calculator/ExampleCalculator``

        :cloudformationAttribute: CalculatorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCalculatorArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreateTime")
    def attr_create_time(self) -> builtins.str:
        '''The timestamp for when the route calculator resource was created in `ISO 8601 <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ format: ``YYYY-MM-DDThh:mm:ss.sssZ`` .

        :cloudformationAttribute: CreateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateTime")
    def attr_update_time(self) -> builtins.str:
        '''The timestamp for when the route calculator resource was last updated in `ISO 8601 <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ format: ``YYYY-MM-DDThh:mm:ss.sssZ`` .

        :cloudformationAttribute: UpdateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="calculatorName")
    def calculator_name(self) -> builtins.str:
        '''The name of the route calculator resource.

        Requirements:

        - Can use alphanumeric characters (A–Z, a–z, 0–9) , hyphens (-), periods (.), and underscores (_).
        - Must be a unique route calculator resource name.
        - No spaces allowed. For example, ``ExampleRouteCalculator`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-calculatorname
        '''
        return typing.cast(builtins.str, jsii.get(self, "calculatorName"))

    @calculator_name.setter
    def calculator_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c94b7f23c5fdc791a98d493da8e854f3dfa72de2e59ff1314c87012134e836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "calculatorName", value)

    @builtins.property
    @jsii.member(jsii_name="dataSource")
    def data_source(self) -> builtins.str:
        '''Specifies the data provider of traffic and road network data.

        .. epigraph::

           This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error.

        Valid values include:

        - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/latest/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on street networks and traffic coverage <https://docs.aws.amazon.com/https://doc.arcgis.com/en/arcgis-online/reference/network-coverage.htm>`_ .

        Route calculators that use Esri as a data source only calculate routes that are shorter than 400 km.

        - ``Grab`` – Grab provides routing functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/latest/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/latest/developerguide/grab.html#grab-coverage-area>`_ .
        - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/latest/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE car routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/car-routing.html>`_ and `HERE truck routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/truck-routing.html>`_ .

        For additional information , see `Data providers <https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-datasource
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSource"))

    @data_source.setter
    def data_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23fc677ee1a40fbc79c91d4a2c938353601aa6c711caf506c392f6b7db29adf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSource", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The optional description for the route calculator resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e54214a89f84f0a269228439f7d40e622bbf08ee32311b7ac8ebb4d93b61d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="pricingPlan")
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used. If included, the only allowed value is ``RequestBasedUsage`` .

        *Allowed Values* : ``RequestBasedUsage``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-pricingplan
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingPlan"))

    @pricing_plan.setter
    def pricing_plan(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc6de3ebe6a59b918827c3d3812c40134d6769104527a87a3c83979880fec91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlan", value)


@jsii.data_type(
    jsii_type="monocdk.aws_location.CfnRouteCalculatorProps",
    jsii_struct_bases=[],
    name_mapping={
        "calculator_name": "calculatorName",
        "data_source": "dataSource",
        "description": "description",
        "pricing_plan": "pricingPlan",
    },
)
class CfnRouteCalculatorProps:
    def __init__(
        self,
        *,
        calculator_name: builtins.str,
        data_source: builtins.str,
        description: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnRouteCalculator``.

        :param calculator_name: The name of the route calculator resource. Requirements: - Can use alphanumeric characters (A–Z, a–z, 0–9) , hyphens (-), periods (.), and underscores (_). - Must be a unique route calculator resource name. - No spaces allowed. For example, ``ExampleRouteCalculator`` .
        :param data_source: Specifies the data provider of traffic and road network data. .. epigraph:: This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error. Valid values include: - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/latest/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on street networks and traffic coverage <https://docs.aws.amazon.com/https://doc.arcgis.com/en/arcgis-online/reference/network-coverage.htm>`_ . Route calculators that use Esri as a data source only calculate routes that are shorter than 400 km. - ``Grab`` – Grab provides routing functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/latest/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/latest/developerguide/grab.html#grab-coverage-area>`_ . - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/latest/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE car routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/car-routing.html>`_ and `HERE truck routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/truck-routing.html>`_ . For additional information , see `Data providers <https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service Developer Guide* .
        :param description: The optional description for the route calculator resource.
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` . *Allowed Values* : ``RequestBasedUsage``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_location as location
            
            cfn_route_calculator_props = location.CfnRouteCalculatorProps(
                calculator_name="calculatorName",
                data_source="dataSource",
            
                # the properties below are optional
                description="description",
                pricing_plan="pricingPlan"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c323cac48642073bb54784bec03d7f4957e1bf800640b05fdeb536280c253b14)
            check_type(argname="argument calculator_name", value=calculator_name, expected_type=type_hints["calculator_name"])
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument pricing_plan", value=pricing_plan, expected_type=type_hints["pricing_plan"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "calculator_name": calculator_name,
            "data_source": data_source,
        }
        if description is not None:
            self._values["description"] = description
        if pricing_plan is not None:
            self._values["pricing_plan"] = pricing_plan

    @builtins.property
    def calculator_name(self) -> builtins.str:
        '''The name of the route calculator resource.

        Requirements:

        - Can use alphanumeric characters (A–Z, a–z, 0–9) , hyphens (-), periods (.), and underscores (_).
        - Must be a unique route calculator resource name.
        - No spaces allowed. For example, ``ExampleRouteCalculator`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-calculatorname
        '''
        result = self._values.get("calculator_name")
        assert result is not None, "Required property 'calculator_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_source(self) -> builtins.str:
        '''Specifies the data provider of traffic and road network data.

        .. epigraph::

           This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error.

        Valid values include:

        - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/latest/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on street networks and traffic coverage <https://docs.aws.amazon.com/https://doc.arcgis.com/en/arcgis-online/reference/network-coverage.htm>`_ .

        Route calculators that use Esri as a data source only calculate routes that are shorter than 400 km.

        - ``Grab`` – Grab provides routing functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/latest/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/latest/developerguide/grab.html#grab-coverage-area>`_ .
        - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/latest/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE car routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/car-routing.html>`_ and `HERE truck routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/truck-routing.html>`_ .

        For additional information , see `Data providers <https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-datasource
        '''
        result = self._values.get("data_source")
        assert result is not None, "Required property 'data_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The optional description for the route calculator resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used. If included, the only allowed value is ``RequestBasedUsage`` .

        *Allowed Values* : ``RequestBasedUsage``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-pricingplan
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouteCalculatorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTracker(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_location.CfnTracker",
):
    '''A CloudFormation ``AWS::Location::Tracker``.

    The ``AWS::Location::Tracker`` resource specifies a tracker resource in your AWS account , which lets you receive current and historical location of devices.

    :cloudformationResource: AWS::Location::Tracker
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_location as location
        
        cfn_tracker = location.CfnTracker(self, "MyCfnTracker",
            tracker_name="trackerName",
        
            # the properties below are optional
            description="description",
            kms_key_id="kmsKeyId",
            position_filtering="positionFiltering",
            pricing_plan="pricingPlan",
            pricing_plan_data_source="pricingPlanDataSource"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        tracker_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        position_filtering: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        pricing_plan_data_source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Location::Tracker``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param tracker_name: The name for the tracker resource. Requirements: - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_). - Must be a unique tracker resource name. - No spaces allowed. For example, ``ExampleTracker`` .
        :param description: An optional description for the tracker resource.
        :param kms_key_id: A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.
        :param position_filtering: Specifies the position filtering for the tracker resource. Valid values: - ``TimeBased`` - Location updates are evaluated against linked geofence collections, but not every location update is stored. If your update frequency is more often than 30 seconds, only one update per 30 seconds is stored for each unique device ID. - ``DistanceBased`` - If the device has moved less than 30 m (98.4 ft), location updates are ignored. Location updates within this area are neither evaluated against linked geofence collections, nor stored. This helps control costs by reducing the number of geofence evaluations and historical device positions to paginate through. Distance-based filtering can also reduce the effects of GPS noise when displaying device trajectories on a map. - ``AccuracyBased`` - If the device has moved less than the measured accuracy, location updates are ignored. For example, if two consecutive updates from a device have a horizontal accuracy of 5 m and 10 m, the second update is ignored if the device has moved less than 15 m. Ignored location updates are neither evaluated against linked geofence collections, nor stored. This can reduce the effects of GPS noise when displaying device trajectories on a map, and can help control your costs by reducing the number of geofence evaluations. This field is optional. If not specified, the default value is ``TimeBased`` .
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` .
        :param pricing_plan_data_source: This parameter is no longer used.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ecd41f1c16620e6bae2b577e3fe00217597e7af45fa1455b9158f7fd99295fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTrackerProps(
            tracker_name=tracker_name,
            description=description,
            kms_key_id=kms_key_id,
            position_filtering=position_filtering,
            pricing_plan=pricing_plan,
            pricing_plan_data_source=pricing_plan_data_source,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c93c04d3e7642920785a1bea4debb95e54808ce0e758915a08435eb48d83ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0096d7d02efb38b33a6d0c07b5022226757bb282cacbbb396a58842be239cf07)
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
        '''The Amazon Resource Name (ARN) for the tracker resource.

        Used when you need to specify a resource across all AWS .

        - Format example: ``arn:aws:geo:region:account-id:tracker/ExampleTracker``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreateTime")
    def attr_create_time(self) -> builtins.str:
        '''The timestamp for when the tracker resource was created in `ISO 8601 <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ format: ``YYYY-MM-DDThh:mm:ss.sssZ`` .

        :cloudformationAttribute: CreateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrTrackerArn")
    def attr_tracker_arn(self) -> builtins.str:
        '''Synonym for ``Arn`` .

        The Amazon Resource Name (ARN) for the tracker resource. Used when you need to specify a resource across all AWS .

        - Format example: ``arn:aws:geo:region:account-id:tracker/ExampleTracker``

        :cloudformationAttribute: TrackerArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTrackerArn"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateTime")
    def attr_update_time(self) -> builtins.str:
        '''The timestamp for when the tracker resource was last updated in `ISO 8601 <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ format: ``YYYY-MM-DDThh:mm:ss.sssZ`` .

        :cloudformationAttribute: UpdateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="trackerName")
    def tracker_name(self) -> builtins.str:
        '''The name for the tracker resource.

        Requirements:

        - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_).
        - Must be a unique tracker resource name.
        - No spaces allowed. For example, ``ExampleTracker`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-trackername
        '''
        return typing.cast(builtins.str, jsii.get(self, "trackerName"))

    @tracker_name.setter
    def tracker_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec36c0884769d2e75530c5d7cb80b654c93c14cc2d250c5eed0c95b9ccf8f14e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackerName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the tracker resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c060149c5f809ca120ad6f5172402a335f95ebe078f034279752070f1bb3d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3645cb89b15efa537fa64739a061978464dc838d82e005ac0c62f277c382f630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="positionFiltering")
    def position_filtering(self) -> typing.Optional[builtins.str]:
        '''Specifies the position filtering for the tracker resource.

        Valid values:

        - ``TimeBased`` - Location updates are evaluated against linked geofence collections, but not every location update is stored. If your update frequency is more often than 30 seconds, only one update per 30 seconds is stored for each unique device ID.
        - ``DistanceBased`` - If the device has moved less than 30 m (98.4 ft), location updates are ignored. Location updates within this area are neither evaluated against linked geofence collections, nor stored. This helps control costs by reducing the number of geofence evaluations and historical device positions to paginate through. Distance-based filtering can also reduce the effects of GPS noise when displaying device trajectories on a map.
        - ``AccuracyBased`` - If the device has moved less than the measured accuracy, location updates are ignored. For example, if two consecutive updates from a device have a horizontal accuracy of 5 m and 10 m, the second update is ignored if the device has moved less than 15 m. Ignored location updates are neither evaluated against linked geofence collections, nor stored. This can reduce the effects of GPS noise when displaying device trajectories on a map, and can help control your costs by reducing the number of geofence evaluations.

        This field is optional. If not specified, the default value is ``TimeBased`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-positionfiltering
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "positionFiltering"))

    @position_filtering.setter
    def position_filtering(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1937d3e22915966b69e613cb230c8f2ff86d979805195ecd55353644c7f62b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "positionFiltering", value)

    @builtins.property
    @jsii.member(jsii_name="pricingPlan")
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used.

        If included, the only allowed value is ``RequestBasedUsage`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-pricingplan
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingPlan"))

    @pricing_plan.setter
    def pricing_plan(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a30501d9eda9d8c6663b768a5c15dd4560305dfeb95d29eb078a1f3000ffb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlan", value)

    @builtins.property
    @jsii.member(jsii_name="pricingPlanDataSource")
    def pricing_plan_data_source(self) -> typing.Optional[builtins.str]:
        '''This parameter is no longer used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-pricingplandatasource
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingPlanDataSource"))

    @pricing_plan_data_source.setter
    def pricing_plan_data_source(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea82443681d1d587fcad9c9e8089aeb06151f4608cec5ebe37331dbba6eeff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlanDataSource", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnTrackerConsumer(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_location.CfnTrackerConsumer",
):
    '''A CloudFormation ``AWS::Location::TrackerConsumer``.

    The ``AWS::Location::TrackerConsumer`` resource specifies an association between a geofence collection and a tracker resource. The geofence collection is referred to as the *consumer* of the tracker. This allows the tracker resource to communicate location data to the linked geofence collection.
    .. epigraph::

       Currently not supported — Cross-account configurations, such as creating associations between a tracker resource in one account and a geofence collection in another account.

    :cloudformationResource: AWS::Location::TrackerConsumer
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-trackerconsumer.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_location as location
        
        cfn_tracker_consumer = location.CfnTrackerConsumer(self, "MyCfnTrackerConsumer",
            consumer_arn="consumerArn",
            tracker_name="trackerName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        consumer_arn: builtins.str,
        tracker_name: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Location::TrackerConsumer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param consumer_arn: The Amazon Resource Name (ARN) for the geofence collection that consumes the tracker resource updates. - Format example: ``arn:aws:geo:region:account-id:geofence-collection/ExampleGeofenceCollectionConsumer``
        :param tracker_name: The name for the tracker resource. Requirements: - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_). - Must be a unique tracker resource name. - No spaces allowed. For example, ``ExampleTracker`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54427b9c73dc6ad386fdf5895c45f94875cb0dfa20cabc1ccdd44df44625c8fe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTrackerConsumerProps(
            consumer_arn=consumer_arn, tracker_name=tracker_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45cbdd8471e5e9b3b0c497ee310663b6c16259e9b16df3a91e08b00daa10ead)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14970ebcf8c27a4a5c47e5fe0c454487a3d2d584961db597a3bae359239b2bdd)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="consumerArn")
    def consumer_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the geofence collection that consumes the tracker resource updates.

        - Format example: ``arn:aws:geo:region:account-id:geofence-collection/ExampleGeofenceCollectionConsumer``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-trackerconsumer.html#cfn-location-trackerconsumer-consumerarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "consumerArn"))

    @consumer_arn.setter
    def consumer_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eaf3024190aee2ffd756a5b571f1d4bfd77f6851ed4eb597cc6ff78df0e4b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerArn", value)

    @builtins.property
    @jsii.member(jsii_name="trackerName")
    def tracker_name(self) -> builtins.str:
        '''The name for the tracker resource.

        Requirements:

        - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_).
        - Must be a unique tracker resource name.
        - No spaces allowed. For example, ``ExampleTracker`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-trackerconsumer.html#cfn-location-trackerconsumer-trackername
        '''
        return typing.cast(builtins.str, jsii.get(self, "trackerName"))

    @tracker_name.setter
    def tracker_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39aa33427cc4e7e6a1fd104e75b608c720c464079ddfd9ebf1041ffe8804c04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackerName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_location.CfnTrackerConsumerProps",
    jsii_struct_bases=[],
    name_mapping={"consumer_arn": "consumerArn", "tracker_name": "trackerName"},
)
class CfnTrackerConsumerProps:
    def __init__(
        self,
        *,
        consumer_arn: builtins.str,
        tracker_name: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnTrackerConsumer``.

        :param consumer_arn: The Amazon Resource Name (ARN) for the geofence collection that consumes the tracker resource updates. - Format example: ``arn:aws:geo:region:account-id:geofence-collection/ExampleGeofenceCollectionConsumer``
        :param tracker_name: The name for the tracker resource. Requirements: - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_). - Must be a unique tracker resource name. - No spaces allowed. For example, ``ExampleTracker`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-trackerconsumer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_location as location
            
            cfn_tracker_consumer_props = location.CfnTrackerConsumerProps(
                consumer_arn="consumerArn",
                tracker_name="trackerName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9812e18f4cd5c73f7eb6b51975a9b41a8bc80fe2ecebb3c643f131d3ed88d2c3)
            check_type(argname="argument consumer_arn", value=consumer_arn, expected_type=type_hints["consumer_arn"])
            check_type(argname="argument tracker_name", value=tracker_name, expected_type=type_hints["tracker_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_arn": consumer_arn,
            "tracker_name": tracker_name,
        }

    @builtins.property
    def consumer_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the geofence collection that consumes the tracker resource updates.

        - Format example: ``arn:aws:geo:region:account-id:geofence-collection/ExampleGeofenceCollectionConsumer``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-trackerconsumer.html#cfn-location-trackerconsumer-consumerarn
        '''
        result = self._values.get("consumer_arn")
        assert result is not None, "Required property 'consumer_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tracker_name(self) -> builtins.str:
        '''The name for the tracker resource.

        Requirements:

        - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_).
        - Must be a unique tracker resource name.
        - No spaces allowed. For example, ``ExampleTracker`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-trackerconsumer.html#cfn-location-trackerconsumer-trackername
        '''
        result = self._values.get("tracker_name")
        assert result is not None, "Required property 'tracker_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrackerConsumerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_location.CfnTrackerProps",
    jsii_struct_bases=[],
    name_mapping={
        "tracker_name": "trackerName",
        "description": "description",
        "kms_key_id": "kmsKeyId",
        "position_filtering": "positionFiltering",
        "pricing_plan": "pricingPlan",
        "pricing_plan_data_source": "pricingPlanDataSource",
    },
)
class CfnTrackerProps:
    def __init__(
        self,
        *,
        tracker_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        position_filtering: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        pricing_plan_data_source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnTracker``.

        :param tracker_name: The name for the tracker resource. Requirements: - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_). - Must be a unique tracker resource name. - No spaces allowed. For example, ``ExampleTracker`` .
        :param description: An optional description for the tracker resource.
        :param kms_key_id: A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.
        :param position_filtering: Specifies the position filtering for the tracker resource. Valid values: - ``TimeBased`` - Location updates are evaluated against linked geofence collections, but not every location update is stored. If your update frequency is more often than 30 seconds, only one update per 30 seconds is stored for each unique device ID. - ``DistanceBased`` - If the device has moved less than 30 m (98.4 ft), location updates are ignored. Location updates within this area are neither evaluated against linked geofence collections, nor stored. This helps control costs by reducing the number of geofence evaluations and historical device positions to paginate through. Distance-based filtering can also reduce the effects of GPS noise when displaying device trajectories on a map. - ``AccuracyBased`` - If the device has moved less than the measured accuracy, location updates are ignored. For example, if two consecutive updates from a device have a horizontal accuracy of 5 m and 10 m, the second update is ignored if the device has moved less than 15 m. Ignored location updates are neither evaluated against linked geofence collections, nor stored. This can reduce the effects of GPS noise when displaying device trajectories on a map, and can help control your costs by reducing the number of geofence evaluations. This field is optional. If not specified, the default value is ``TimeBased`` .
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` .
        :param pricing_plan_data_source: This parameter is no longer used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_location as location
            
            cfn_tracker_props = location.CfnTrackerProps(
                tracker_name="trackerName",
            
                # the properties below are optional
                description="description",
                kms_key_id="kmsKeyId",
                position_filtering="positionFiltering",
                pricing_plan="pricingPlan",
                pricing_plan_data_source="pricingPlanDataSource"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855e80956d6dd901f94f697174044276ff57baa3f3ed443560f2e2e9e63dbd04)
            check_type(argname="argument tracker_name", value=tracker_name, expected_type=type_hints["tracker_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument position_filtering", value=position_filtering, expected_type=type_hints["position_filtering"])
            check_type(argname="argument pricing_plan", value=pricing_plan, expected_type=type_hints["pricing_plan"])
            check_type(argname="argument pricing_plan_data_source", value=pricing_plan_data_source, expected_type=type_hints["pricing_plan_data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tracker_name": tracker_name,
        }
        if description is not None:
            self._values["description"] = description
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if position_filtering is not None:
            self._values["position_filtering"] = position_filtering
        if pricing_plan is not None:
            self._values["pricing_plan"] = pricing_plan
        if pricing_plan_data_source is not None:
            self._values["pricing_plan_data_source"] = pricing_plan_data_source

    @builtins.property
    def tracker_name(self) -> builtins.str:
        '''The name for the tracker resource.

        Requirements:

        - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_).
        - Must be a unique tracker resource name.
        - No spaces allowed. For example, ``ExampleTracker`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-trackername
        '''
        result = self._values.get("tracker_name")
        assert result is not None, "Required property 'tracker_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the tracker resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def position_filtering(self) -> typing.Optional[builtins.str]:
        '''Specifies the position filtering for the tracker resource.

        Valid values:

        - ``TimeBased`` - Location updates are evaluated against linked geofence collections, but not every location update is stored. If your update frequency is more often than 30 seconds, only one update per 30 seconds is stored for each unique device ID.
        - ``DistanceBased`` - If the device has moved less than 30 m (98.4 ft), location updates are ignored. Location updates within this area are neither evaluated against linked geofence collections, nor stored. This helps control costs by reducing the number of geofence evaluations and historical device positions to paginate through. Distance-based filtering can also reduce the effects of GPS noise when displaying device trajectories on a map.
        - ``AccuracyBased`` - If the device has moved less than the measured accuracy, location updates are ignored. For example, if two consecutive updates from a device have a horizontal accuracy of 5 m and 10 m, the second update is ignored if the device has moved less than 15 m. Ignored location updates are neither evaluated against linked geofence collections, nor stored. This can reduce the effects of GPS noise when displaying device trajectories on a map, and can help control your costs by reducing the number of geofence evaluations.

        This field is optional. If not specified, the default value is ``TimeBased`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-positionfiltering
        '''
        result = self._values.get("position_filtering")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used.

        If included, the only allowed value is ``RequestBasedUsage`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-pricingplan
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan_data_source(self) -> typing.Optional[builtins.str]:
        '''This parameter is no longer used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-pricingplandatasource
        '''
        result = self._values.get("pricing_plan_data_source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrackerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnGeofenceCollection",
    "CfnGeofenceCollectionProps",
    "CfnMap",
    "CfnMapProps",
    "CfnPlaceIndex",
    "CfnPlaceIndexProps",
    "CfnRouteCalculator",
    "CfnRouteCalculatorProps",
    "CfnTracker",
    "CfnTrackerConsumer",
    "CfnTrackerConsumerProps",
    "CfnTrackerProps",
]

publication.publish()

def _typecheckingstub__5194b718a761e2b36865b4979514eec5430e887673fd5fb8b65a467b614b0cc8(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    collection_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    pricing_plan_data_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1ce456452e864b417cf1348369129c6571486a1445ef322a2a75ba837ff481(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749a20a6ae3eb2a3e3d61e081c3d83b54f12ad55d76fc322ef59ffb5c7a13308(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de53f70a92eb84956f1293a9ee089b06b924b0a4fd4587936724ac67fc14b8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3be9b5d8201beefc5dea6f911fca1e0a901089e10c2e49da964033f70cd6f97(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28afa53b421338172e3fe4d4839c8934b83f99514679ae1dd770e49a03dd15f1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf83a895634a31d5222f816f637a7d5213aad8cd37647688fb2b1e598c9e7e1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7e85ed033c7a1a16266ff13d38f242cbe6c03ddae95a08030da025d47a7e1e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faaf80475179505a24d76442b7d124aeabf8f4f4061fcea03e506768a4a4ca4f(
    *,
    collection_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    pricing_plan_data_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61965e15228b6b61ae0eb24ea9f6c7ea50e056d3b3ab26113607d8c981469a2d(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    configuration: typing.Union[typing.Union[CfnMap.MapConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    map_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b207b93d25b9810a09ed802c59af6addc11d91ce3c8e8e9d1a4badfec90f5592(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6122a4fddd5898c78a765b3c0840c3ef0298cc675cbc6adffc612fa3fbb93258(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba85181ef6e4287c2a126c75e1dd8071fba27e3971ee250e9a3cf6702c631b6(
    value: typing.Union[CfnMap.MapConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbed74f27c87010d98ebeb923c76a78034f3daa544774ed562793d8a97ffdd24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743ecea26a102d8a65235b8c8e0f73ee595ba2c99da9bfe9853415afe2f22840(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a476d79ecb23c52997ac7ed300d81e7a2bf1e4c3cd4d072724b4e4f25cabda(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15d01b8c829e58006cf4fc762fb3ec80a23357f9e9c7a2dc16473010b99361c(
    *,
    style: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71782980c56d8598397d541f96858d65ca8843083651a16589fcfa7cc31f4f1(
    *,
    configuration: typing.Union[typing.Union[CfnMap.MapConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    map_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ff36650fade187b3a3ee9372c417724bb11f64a2ec8f29ffbca93c9cb1cb24(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    data_source: builtins.str,
    index_name: builtins.str,
    data_source_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaceIndex.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63fb52c6b80eeeb0881d035743d2e9025a1eeee41377c9dc4dd1e9061991f99d(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7832de0a0526c94809b6e360ef4480c69a2d0c7c93ae4b3c36cde4064df9a8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514f314f7e6c3a8fdb93e617fbf9e60ee6214c4c089f6a7dd9dbb98c1ef3c788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc7984259ca6fc773117bbe828fcc6ca1571cbee9afe86914d6d99b817ae9d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864b8aa3447a5f044fa4b5e4c2cef33c3bd2c9aad9ede4edba55b9aeb961408b(
    value: typing.Optional[typing.Union[CfnPlaceIndex.DataSourceConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02cede97e4545e30674fee6009a369662f3f05adfb1c97bafa9979e1b215bf1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73198f8d173265a14f5d8b3d295f01bb3231141ab4d29d21f75b92e4e3abf6e6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d177c8cf697b24a9984386d2ef7284a635d33f044b02706eb3f86afc212e48(
    *,
    intended_use: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa3d95cae2a4e33e7a1b5a0725a1d0fddd2491893da78b8a750f2381e910a93(
    *,
    data_source: builtins.str,
    index_name: builtins.str,
    data_source_configuration: typing.Optional[typing.Union[typing.Union[CfnPlaceIndex.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e580485e8d9f0c8889272d20975130827a5c497cd42b373c64897a63f62b1fc(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    calculator_name: builtins.str,
    data_source: builtins.str,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e5b7bb5b55b5365afc92501e3aa721ede4fb35f7ab3e413df5b476f697f48c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5864cc3ee387760b5cf09b6ba6f23fc5f7b4896bb391ea5858275e02934a2e1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c94b7f23c5fdc791a98d493da8e854f3dfa72de2e59ff1314c87012134e836(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23fc677ee1a40fbc79c91d4a2c938353601aa6c711caf506c392f6b7db29adf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e54214a89f84f0a269228439f7d40e622bbf08ee32311b7ac8ebb4d93b61d8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc6de3ebe6a59b918827c3d3812c40134d6769104527a87a3c83979880fec91(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c323cac48642073bb54784bec03d7f4957e1bf800640b05fdeb536280c253b14(
    *,
    calculator_name: builtins.str,
    data_source: builtins.str,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecd41f1c16620e6bae2b577e3fe00217597e7af45fa1455b9158f7fd99295fc(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    tracker_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    position_filtering: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    pricing_plan_data_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c93c04d3e7642920785a1bea4debb95e54808ce0e758915a08435eb48d83ab(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0096d7d02efb38b33a6d0c07b5022226757bb282cacbbb396a58842be239cf07(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec36c0884769d2e75530c5d7cb80b654c93c14cc2d250c5eed0c95b9ccf8f14e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c060149c5f809ca120ad6f5172402a335f95ebe078f034279752070f1bb3d7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3645cb89b15efa537fa64739a061978464dc838d82e005ac0c62f277c382f630(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1937d3e22915966b69e613cb230c8f2ff86d979805195ecd55353644c7f62b1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a30501d9eda9d8c6663b768a5c15dd4560305dfeb95d29eb078a1f3000ffb7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea82443681d1d587fcad9c9e8089aeb06151f4608cec5ebe37331dbba6eeff4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54427b9c73dc6ad386fdf5895c45f94875cb0dfa20cabc1ccdd44df44625c8fe(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    consumer_arn: builtins.str,
    tracker_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45cbdd8471e5e9b3b0c497ee310663b6c16259e9b16df3a91e08b00daa10ead(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14970ebcf8c27a4a5c47e5fe0c454487a3d2d584961db597a3bae359239b2bdd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eaf3024190aee2ffd756a5b571f1d4bfd77f6851ed4eb597cc6ff78df0e4b6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39aa33427cc4e7e6a1fd104e75b608c720c464079ddfd9ebf1041ffe8804c04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9812e18f4cd5c73f7eb6b51975a9b41a8bc80fe2ecebb3c643f131d3ed88d2c3(
    *,
    consumer_arn: builtins.str,
    tracker_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855e80956d6dd901f94f697174044276ff57baa3f3ed443560f2e2e9e63dbd04(
    *,
    tracker_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    position_filtering: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    pricing_plan_data_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
