'''
# AWS::Location Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

Amazon Location Service lets you add location data and functionality to applications, which
includes capabilities such as maps, points of interest, geocoding, routing, geofences, and
tracking. Amazon Location provides location-based services (LBS) using high-quality data from
global, trusted providers Esri and HERE. With affordable data, tracking and geofencing
capabilities, and built-in metrics for health monitoring, you can build sophisticated
location-enabled applications.

## Place Index

A key function of Amazon Location Service is the ability to search the geolocation information.
Amazon Location provides this functionality via the Place index resource. The place index includes
which [data provider](https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html)
to use for the search.

To create a place index, define a `PlaceIndex`:

```python
location.PlaceIndex(self, "PlaceIndex",
    place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
    data_source=location.DataSource.HERE
)
```

Use the `grant()` or `grantSearch()` method to grant the given identity permissions to perform actions
on the place index:

```python
# role: iam.Role


place_index = location.PlaceIndex(self, "PlaceIndex")
place_index.grant_search(role)
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.DataSource")
class DataSource(enum.Enum):
    '''(experimental) Data source for a place index.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.PlaceIndex(self, "PlaceIndex",
            place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
            data_source=location.DataSource.HERE
        )
    '''

    ESRI = "ESRI"
    '''(experimental) Esri.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/esri.html
    :stability: experimental
    '''
    HERE = "HERE"
    '''(experimental) HERE.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/HERE.html
    :stability: experimental
    '''


@jsii.interface(jsii_type="@aws-cdk/aws-location-alpha.IPlaceIndex")
class IPlaceIndex(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A Place Index.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="placeIndexArn")
    def place_index_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the place index resource.

        :stability: experimental
        :attribute: Arn,IndexArn
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="placeIndexName")
    def place_index_name(self) -> builtins.str:
        '''(experimental) The name of the place index.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IPlaceIndexProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A Place Index.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-location-alpha.IPlaceIndex"

    @builtins.property
    @jsii.member(jsii_name="placeIndexArn")
    def place_index_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the place index resource.

        :stability: experimental
        :attribute: Arn,IndexArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexArn"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexName")
    def place_index_name(self) -> builtins.str:
        '''(experimental) The name of the place index.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPlaceIndex).__jsii_proxy_class__ = lambda : _IPlaceIndexProxy


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.IntendedUse")
class IntendedUse(enum.Enum):
    '''(experimental) Intend use for the results of an operation.

    :stability: experimental
    '''

    SINGLE_USE = "SINGLE_USE"
    '''(experimental) The results won't be stored.

    :stability: experimental
    '''
    STORAGE = "STORAGE"
    '''(experimental) The result can be cached or stored in a database.

    :stability: experimental
    '''


@jsii.implements(IPlaceIndex)
class PlaceIndex(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location-alpha.PlaceIndex",
):
    '''(experimental) A Place Index.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/places-concepts.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.PlaceIndex(self, "PlaceIndex",
            place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
            data_source=location.DataSource.HERE
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        data_source: typing.Optional[DataSource] = None,
        description: typing.Optional[builtins.str] = None,
        intended_use: typing.Optional[IntendedUse] = None,
        place_index_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param data_source: (experimental) Data source for the place index. Default: DataSource.ESRI
        :param description: (experimental) A description for the place index. Default: - no description
        :param intended_use: (experimental) Intend use for the results of an operation. Default: IntendedUse.SINGLE_USE
        :param place_index_name: (experimental) A name for the place index. Default: - A name is automatically generated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45352af3f6c713374f537c829e98f8db51c9684d0ccc55eedcc24f34b4115a7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PlaceIndexProps(
            data_source=data_source,
            description=description,
            intended_use=intended_use,
            place_index_name=place_index_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPlaceIndexArn")
    @builtins.classmethod
    def from_place_index_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        place_index_arn: builtins.str,
    ) -> IPlaceIndex:
        '''(experimental) Use an existing place index by ARN.

        :param scope: -
        :param id: -
        :param place_index_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248ee08bccad0771877a2fcc90a9b08d64668a1cf797c90deb8c53fec79af85d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument place_index_arn", value=place_index_arn, expected_type=type_hints["place_index_arn"])
        return typing.cast(IPlaceIndex, jsii.sinvoke(cls, "fromPlaceIndexArn", [scope, id, place_index_arn]))

    @jsii.member(jsii_name="fromPlaceIndexName")
    @builtins.classmethod
    def from_place_index_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        place_index_name: builtins.str,
    ) -> IPlaceIndex:
        '''(experimental) Use an existing place index by name.

        :param scope: -
        :param id: -
        :param place_index_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8d45231ce3a808cab553413e12ee6462eb276374dc71795aae0d1b4cbc7651)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument place_index_name", value=place_index_name, expected_type=type_hints["place_index_name"])
        return typing.cast(IPlaceIndex, jsii.sinvoke(cls, "fromPlaceIndexName", [scope, id, place_index_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform the actions on this place index.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f4422a489b304c7bbc9bfabd28b7282eb0ff8e5a625351b01c27528783eef2)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantSearch")
    def grant_search(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to search using this index.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d5a407a04ad6cfe5d7ad704c60c4485d954e37151f87d42b4a0f8aae3e8fcf)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantSearch", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="placeIndexArn")
    def place_index_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the place index resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexArn"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexCreateTime")
    def place_index_create_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the place index resource was created in ISO 8601 forma.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexName")
    def place_index_name(self) -> builtins.str:
        '''(experimental) The name of the place index.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexName"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexUpdateTime")
    def place_index_update_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the place index resource was last updated in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexUpdateTime"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location-alpha.PlaceIndexProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_source": "dataSource",
        "description": "description",
        "intended_use": "intendedUse",
        "place_index_name": "placeIndexName",
    },
)
class PlaceIndexProps:
    def __init__(
        self,
        *,
        data_source: typing.Optional[DataSource] = None,
        description: typing.Optional[builtins.str] = None,
        intended_use: typing.Optional[IntendedUse] = None,
        place_index_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a place index.

        :param data_source: (experimental) Data source for the place index. Default: DataSource.ESRI
        :param description: (experimental) A description for the place index. Default: - no description
        :param intended_use: (experimental) Intend use for the results of an operation. Default: IntendedUse.SINGLE_USE
        :param place_index_name: (experimental) A name for the place index. Default: - A name is automatically generated

        :stability: experimental
        :exampleMetadata: infused

        Example::

            location.PlaceIndex(self, "PlaceIndex",
                place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
                data_source=location.DataSource.HERE
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e973a0eacea346fe0253fb892d398121998cd91fd16cfdf5bb8eef740a62ae)
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument intended_use", value=intended_use, expected_type=type_hints["intended_use"])
            check_type(argname="argument place_index_name", value=place_index_name, expected_type=type_hints["place_index_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_source is not None:
            self._values["data_source"] = data_source
        if description is not None:
            self._values["description"] = description
        if intended_use is not None:
            self._values["intended_use"] = intended_use
        if place_index_name is not None:
            self._values["place_index_name"] = place_index_name

    @builtins.property
    def data_source(self) -> typing.Optional[DataSource]:
        '''(experimental) Data source for the place index.

        :default: DataSource.ESRI

        :stability: experimental
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional[DataSource], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the place index.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def intended_use(self) -> typing.Optional[IntendedUse]:
        '''(experimental) Intend use for the results of an operation.

        :default: IntendedUse.SINGLE_USE

        :stability: experimental
        '''
        result = self._values.get("intended_use")
        return typing.cast(typing.Optional[IntendedUse], result)

    @builtins.property
    def place_index_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the place index.

        :default: - A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("place_index_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlaceIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataSource",
    "IPlaceIndex",
    "IntendedUse",
    "PlaceIndex",
    "PlaceIndexProps",
]

publication.publish()

def _typecheckingstub__45352af3f6c713374f537c829e98f8db51c9684d0ccc55eedcc24f34b4115a7d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    data_source: typing.Optional[DataSource] = None,
    description: typing.Optional[builtins.str] = None,
    intended_use: typing.Optional[IntendedUse] = None,
    place_index_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248ee08bccad0771877a2fcc90a9b08d64668a1cf797c90deb8c53fec79af85d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    place_index_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8d45231ce3a808cab553413e12ee6462eb276374dc71795aae0d1b4cbc7651(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    place_index_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f4422a489b304c7bbc9bfabd28b7282eb0ff8e5a625351b01c27528783eef2(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d5a407a04ad6cfe5d7ad704c60c4485d954e37151f87d42b4a0f8aae3e8fcf(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e973a0eacea346fe0253fb892d398121998cd91fd16cfdf5bb8eef740a62ae(
    *,
    data_source: typing.Optional[DataSource] = None,
    description: typing.Optional[builtins.str] = None,
    intended_use: typing.Optional[IntendedUse] = None,
    place_index_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
