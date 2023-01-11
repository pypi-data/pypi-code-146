'''
# AWS::Location Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_location as location
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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnGeofenceCollection(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location.CfnGeofenceCollection",
):
    '''A CloudFormation ``AWS::Location::GeofenceCollection``.

    The ``AWS::Location::GeofenceCollection`` resource specifies the ability to detect and act when a tracked device enters or exits a defined geographical boundary known as a geofence.

    :cloudformationResource: AWS::Location::GeofenceCollection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_location as location
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__9018e3067e982702dd137eed30602c3c16f57469af16f3e88007344b0d71f636)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf58e35ab80de4cafa51c18945a1bd992c4aabc9c29571305e453c5099995a45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd8d6197317c030ff4082cbfb8e0ec0a61e1744f9cd43787f066cee88bd50149)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94a4af131504193fa0157d1672102f757a3a3923e0fb54131e57fff94d7dd46a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c8d208963b8e428bcd0eaf5df8e7f3973908cb93f150bbb51f70ee497ac1fe6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61fbad311498ae8daad067efa1f67ae18384a1df7ca3d855843dc2ddf5879e7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ffe49980cb6fbb220120b5dc6de081606d989146093327848a99d58f2b8364b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2984208444eda554a26111a094d9cf22d4ab3636df4a307b8632540a8e0e4fbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlanDataSource", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location.CfnGeofenceCollectionProps",
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
            import aws_cdk.aws_location as location
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e19173daebea0ce2822d79971aedca87ff8ac5fb357b869a28ddbe47ab68271)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnMap(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location.CfnMap",
):
    '''A CloudFormation ``AWS::Location::Map``.

    The ``AWS::Location::Map`` resource specifies a map resource in your AWS account, which provides map tiles of different styles sourced from global location data providers.

    :cloudformationResource: AWS::Location::Map
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_location as location
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        configuration: typing.Union[typing.Union["CfnMap.MapConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bdb5c873869954c69d2dd82191ce2270e7a1317d935b702600260ae38021288)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ae49b3363d795f0ca3240f7214ad9d4f9ee00b8b09e2f5f7c2824a7dcb926e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__775fc2311860d915bf26a6d39f5d9607574d2b5f4388cff14593fce721446925)
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
    ) -> typing.Union["CfnMap.MapConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''Specifies the ``MapConfiguration`` , including the map style, for the map resource that you create.

        The map style defines the look of maps and the data provider for your map resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-configuration
        '''
        return typing.cast(typing.Union["CfnMap.MapConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: typing.Union["CfnMap.MapConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d738cf296646e6c982f88680192635bb5830bef9f5336d9a79350d0e105ed95f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__719e492053fdffcb9f3137c5f0ecf505863787c289f6b7c041616069331dfe41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e24f2b555c4f5c97330264ec20de4c88967b805391caa2bebdf6bbe9ba417767)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90fc4a46cf3644eeadae3f92274fad61fdc9a5a1c3863724f625da63a948ce3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlan", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-location.CfnMap.MapConfigurationProperty",
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
                import aws_cdk.aws_location as location
                
                map_configuration_property = location.CfnMap.MapConfigurationProperty(
                    style="style"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59c1519f4209e0377a99ca00539a7e14b6219628829d4fba3c4f6b99871c8517)
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
    jsii_type="@aws-cdk/aws-location.CfnMapProps",
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
        configuration: typing.Union[typing.Union[CfnMap.MapConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
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
            import aws_cdk.aws_location as location
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9f641eb8c2a846b6f2e5a35f271e141d034281b3132051d67138f448e67282a)
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
    ) -> typing.Union[CfnMap.MapConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''Specifies the ``MapConfiguration`` , including the map style, for the map resource that you create.

        The map style defines the look of maps and the data provider for your map resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-configuration
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast(typing.Union[CfnMap.MapConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnPlaceIndex(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location.CfnPlaceIndex",
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
        import aws_cdk.aws_location as location
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        data_source: builtins.str,
        index_name: builtins.str,
        data_source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPlaceIndex.DataSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dd20bed6e20d53dfd9ff3fc3292e5084516a589fbfe6ed3ddc37ea1ba7efb9d)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94fc813ed7b46adc76145b0b067b288270602f240cfe6b692e73c48827dbb8c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d83743c9b85dfb2539c40f112b4a16f858cde370e031b54d0f5122880b083303)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c227c531d6cd18e70098a990b7e4c334d6466a4f4b9ab3f1e81ba6e3291471d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9795f73180db6e0c4e4d43d89945cf5f956a95c2562c6bac4b9ab4c0582b8483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexName", value)

    @builtins.property
    @jsii.member(jsii_name="dataSourceConfiguration")
    def data_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlaceIndex.DataSourceConfigurationProperty"]]:
        '''Specifies the data storage option for requesting Places.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-datasourceconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlaceIndex.DataSourceConfigurationProperty"]], jsii.get(self, "dataSourceConfiguration"))

    @data_source_configuration.setter
    def data_source_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPlaceIndex.DataSourceConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32072b4405d5e0b31e75af255be1248533a2dbe7ecf232201c66ef2832aae8e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__140b56081eb3215a5a411973bf0b5e4865cb9698b9b733e16c84626584a0b351)
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
            type_hints = typing.get_type_hints(_typecheckingstub__808b28eb263299d8db23ef87b5e1a88ed16d4db7bc7d80c5293c483eb56e44aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlan", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-location.CfnPlaceIndex.DataSourceConfigurationProperty",
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
                import aws_cdk.aws_location as location
                
                data_source_configuration_property = location.CfnPlaceIndex.DataSourceConfigurationProperty(
                    intended_use="intendedUse"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1985a524f87e62e806f794675c8f65b14bcc3bf281d46050731081df4b106b67)
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
    jsii_type="@aws-cdk/aws-location.CfnPlaceIndexProps",
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
        data_source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPlaceIndex.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_location as location
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceab054c8ff89653cd6ba7a8f3d3ef27f9247e11f0b3f60b2547b52522fdaff1)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPlaceIndex.DataSourceConfigurationProperty]]:
        '''Specifies the data storage option for requesting Places.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-datasourceconfiguration
        '''
        result = self._values.get("data_source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPlaceIndex.DataSourceConfigurationProperty]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRouteCalculator(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location.CfnRouteCalculator",
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
        import aws_cdk.aws_location as location
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3d9028ff2793448029d10b239f25678a21fe9b987ab8b219b9a2e73b048ed3e)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895701fe20b6c0b0ac00838c668cf7af7586dcbbd1304f671b3999fc440e61a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1c6da780324ef36bc23adc0ba266a9bc401196bccc9972f57be931ca7e10726)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b5cbb5f9fed6143ac5b50c8686d8664b9a7abc1b4f0ed4c2c40ae9aaf4863fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d77416ac74c4d045b51684bbece0996a4bf50d0f904fc02aa73afdd75fc66ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__153f01fc31ed7e9827c88b3c5e95428664df2167e025337ac009c822cd236179)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d91ffb5219412eacd7ec957777974d0c93ce6b8a4d7aa74b9e9ff76ce34028ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlan", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location.CfnRouteCalculatorProps",
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
            import aws_cdk.aws_location as location
            
            cfn_route_calculator_props = location.CfnRouteCalculatorProps(
                calculator_name="calculatorName",
                data_source="dataSource",
            
                # the properties below are optional
                description="description",
                pricing_plan="pricingPlan"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb6b6d083df9281d6bab06ffef9f52909de10c193a66ed254a792bc5e86cc85a)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnTracker(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location.CfnTracker",
):
    '''A CloudFormation ``AWS::Location::Tracker``.

    The ``AWS::Location::Tracker`` resource specifies a tracker resource in your AWS account , which lets you receive current and historical location of devices.

    :cloudformationResource: AWS::Location::Tracker
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_location as location
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__a94a6c651448f081f8948e75ce7fa269fa37de28637cfe33abfaac75b11fe39a)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff899dec37322290348b939445fc2e711b497bf5c39f3ddd3aff0f1781c7ade8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dad88ca3c497278a2ccb51ed1aa8168a2ffb8551f8c26af4e5dac033c46a06b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f785f9b282c92cd01909d0f22f6c3febd7f303adaedc6be90610e8fffa04f71a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3239485af5bfbeada71d74ccf59640c91fc382bae1904a954e8b4d5cc05d6c8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d449d6b74a580631d7d5353451ac52fd36fc918afff2ad73e520b9e2a971a15a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__052313fe4964c4c989fe3433c167a4d11af3fcdb6b5e7249bd966632fddc0374)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f988bf4966e2eaede6fbaad0729934f9fb4bfd590e2aeef8aa44bb0796d8f9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a9b214a5d59adddcfc71546d36034dfe5c657200d1475ff2b5ef103398c2e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlanDataSource", value)


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnTrackerConsumer(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location.CfnTrackerConsumer",
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
        import aws_cdk.aws_location as location
        
        cfn_tracker_consumer = location.CfnTrackerConsumer(self, "MyCfnTrackerConsumer",
            consumer_arn="consumerArn",
            tracker_name="trackerName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea3f31af1d925cae3576331a642ea4fb65a7fd8917c81e61d4dc6849d184f2bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTrackerConsumerProps(
            consumer_arn=consumer_arn, tracker_name=tracker_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be50a9abaea98579dab0ebc3a5c3da9882fe81c7bc2ee6057a4c26ccb1c8fa7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb756977d0d918e49715c6045141ac9c7a8590990445091cf67951c8486edee0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfb55ace552847145f99df2cefb00edcdfcfa405cfb500518a0b7f9e234f7eac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b904db1eed3f166944420043493b7ad5c191d383938140cd7c2358d9563a63e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackerName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location.CfnTrackerConsumerProps",
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
            import aws_cdk.aws_location as location
            
            cfn_tracker_consumer_props = location.CfnTrackerConsumerProps(
                consumer_arn="consumerArn",
                tracker_name="trackerName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb4f68fd640e843b901aa9fb7e24493f9296052066538561b14e6385f9d1499)
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
    jsii_type="@aws-cdk/aws-location.CfnTrackerProps",
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
            import aws_cdk.aws_location as location
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__117332148ca5a68ba9fe6edac80b31d6203a532b66d207e5bef0894d3e972b5b)
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

def _typecheckingstub__9018e3067e982702dd137eed30602c3c16f57469af16f3e88007344b0d71f636(
    scope: _aws_cdk_core_f4b25747.Construct,
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

def _typecheckingstub__bf58e35ab80de4cafa51c18945a1bd992c4aabc9c29571305e453c5099995a45(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8d6197317c030ff4082cbfb8e0ec0a61e1744f9cd43787f066cee88bd50149(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a4af131504193fa0157d1672102f757a3a3923e0fb54131e57fff94d7dd46a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8d208963b8e428bcd0eaf5df8e7f3973908cb93f150bbb51f70ee497ac1fe6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fbad311498ae8daad067efa1f67ae18384a1df7ca3d855843dc2ddf5879e7c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ffe49980cb6fbb220120b5dc6de081606d989146093327848a99d58f2b8364b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2984208444eda554a26111a094d9cf22d4ab3636df4a307b8632540a8e0e4fbd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e19173daebea0ce2822d79971aedca87ff8ac5fb357b869a28ddbe47ab68271(
    *,
    collection_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    pricing_plan_data_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bdb5c873869954c69d2dd82191ce2270e7a1317d935b702600260ae38021288(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    configuration: typing.Union[typing.Union[CfnMap.MapConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    map_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ae49b3363d795f0ca3240f7214ad9d4f9ee00b8b09e2f5f7c2824a7dcb926e(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775fc2311860d915bf26a6d39f5d9607574d2b5f4388cff14593fce721446925(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d738cf296646e6c982f88680192635bb5830bef9f5336d9a79350d0e105ed95f(
    value: typing.Union[CfnMap.MapConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719e492053fdffcb9f3137c5f0ecf505863787c289f6b7c041616069331dfe41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24f2b555c4f5c97330264ec20de4c88967b805391caa2bebdf6bbe9ba417767(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fc4a46cf3644eeadae3f92274fad61fdc9a5a1c3863724f625da63a948ce3f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c1519f4209e0377a99ca00539a7e14b6219628829d4fba3c4f6b99871c8517(
    *,
    style: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f641eb8c2a846b6f2e5a35f271e141d034281b3132051d67138f448e67282a(
    *,
    configuration: typing.Union[typing.Union[CfnMap.MapConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    map_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd20bed6e20d53dfd9ff3fc3292e5084516a589fbfe6ed3ddc37ea1ba7efb9d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    data_source: builtins.str,
    index_name: builtins.str,
    data_source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPlaceIndex.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fc813ed7b46adc76145b0b067b288270602f240cfe6b692e73c48827dbb8c9(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83743c9b85dfb2539c40f112b4a16f858cde370e031b54d0f5122880b083303(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c227c531d6cd18e70098a990b7e4c334d6466a4f4b9ab3f1e81ba6e3291471d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9795f73180db6e0c4e4d43d89945cf5f956a95c2562c6bac4b9ab4c0582b8483(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32072b4405d5e0b31e75af255be1248533a2dbe7ecf232201c66ef2832aae8e6(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPlaceIndex.DataSourceConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140b56081eb3215a5a411973bf0b5e4865cb9698b9b733e16c84626584a0b351(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808b28eb263299d8db23ef87b5e1a88ed16d4db7bc7d80c5293c483eb56e44aa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1985a524f87e62e806f794675c8f65b14bcc3bf281d46050731081df4b106b67(
    *,
    intended_use: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceab054c8ff89653cd6ba7a8f3d3ef27f9247e11f0b3f60b2547b52522fdaff1(
    *,
    data_source: builtins.str,
    index_name: builtins.str,
    data_source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPlaceIndex.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d9028ff2793448029d10b239f25678a21fe9b987ab8b219b9a2e73b048ed3e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    calculator_name: builtins.str,
    data_source: builtins.str,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895701fe20b6c0b0ac00838c668cf7af7586dcbbd1304f671b3999fc440e61a7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c6da780324ef36bc23adc0ba266a9bc401196bccc9972f57be931ca7e10726(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5cbb5f9fed6143ac5b50c8686d8664b9a7abc1b4f0ed4c2c40ae9aaf4863fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d77416ac74c4d045b51684bbece0996a4bf50d0f904fc02aa73afdd75fc66ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153f01fc31ed7e9827c88b3c5e95428664df2167e025337ac009c822cd236179(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91ffb5219412eacd7ec957777974d0c93ce6b8a4d7aa74b9e9ff76ce34028ff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6b6d083df9281d6bab06ffef9f52909de10c193a66ed254a792bc5e86cc85a(
    *,
    calculator_name: builtins.str,
    data_source: builtins.str,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94a6c651448f081f8948e75ce7fa269fa37de28637cfe33abfaac75b11fe39a(
    scope: _aws_cdk_core_f4b25747.Construct,
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

def _typecheckingstub__ff899dec37322290348b939445fc2e711b497bf5c39f3ddd3aff0f1781c7ade8(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad88ca3c497278a2ccb51ed1aa8168a2ffb8551f8c26af4e5dac033c46a06b8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f785f9b282c92cd01909d0f22f6c3febd7f303adaedc6be90610e8fffa04f71a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3239485af5bfbeada71d74ccf59640c91fc382bae1904a954e8b4d5cc05d6c8b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d449d6b74a580631d7d5353451ac52fd36fc918afff2ad73e520b9e2a971a15a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052313fe4964c4c989fe3433c167a4d11af3fcdb6b5e7249bd966632fddc0374(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f988bf4966e2eaede6fbaad0729934f9fb4bfd590e2aeef8aa44bb0796d8f9e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9b214a5d59adddcfc71546d36034dfe5c657200d1475ff2b5ef103398c2e41(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3f31af1d925cae3576331a642ea4fb65a7fd8917c81e61d4dc6849d184f2bb(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    consumer_arn: builtins.str,
    tracker_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be50a9abaea98579dab0ebc3a5c3da9882fe81c7bc2ee6057a4c26ccb1c8fa7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb756977d0d918e49715c6045141ac9c7a8590990445091cf67951c8486edee0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb55ace552847145f99df2cefb00edcdfcfa405cfb500518a0b7f9e234f7eac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b904db1eed3f166944420043493b7ad5c191d383938140cd7c2358d9563a63e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb4f68fd640e843b901aa9fb7e24493f9296052066538561b14e6385f9d1499(
    *,
    consumer_arn: builtins.str,
    tracker_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117332148ca5a68ba9fe6edac80b31d6203a532b66d207e5bef0894d3e972b5b(
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
