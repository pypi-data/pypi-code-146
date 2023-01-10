'''
# `aws_appmesh_gateway_route`

Refer to the Terraform Registory for docs: [`aws_appmesh_gateway_route`](https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route).
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

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class AppmeshGatewayRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRoute",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route aws_appmesh_gateway_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        mesh_name: builtins.str,
        name: builtins.str,
        spec: typing.Union["AppmeshGatewayRouteSpec", typing.Dict[builtins.str, typing.Any]],
        virtual_gateway_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route aws_appmesh_gateway_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param mesh_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#mesh_name AppmeshGatewayRoute#mesh_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#name AppmeshGatewayRoute#name}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#spec AppmeshGatewayRoute#spec}
        :param virtual_gateway_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_gateway_name AppmeshGatewayRoute#virtual_gateway_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#id AppmeshGatewayRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mesh_owner: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#mesh_owner AppmeshGatewayRoute#mesh_owner}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#tags AppmeshGatewayRoute#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#tags_all AppmeshGatewayRoute#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a777c4143d9c31b71bf8d30f600e1429287b5585f484125e84cacfbb33a4dc92)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppmeshGatewayRouteConfig(
            mesh_name=mesh_name,
            name=name,
            spec=spec,
            virtual_gateway_name=virtual_gateway_name,
            id=id,
            mesh_owner=mesh_owner,
            tags=tags,
            tags_all=tags_all,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        grpc_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecGrpcRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        http2_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2Route", typing.Dict[builtins.str, typing.Any]]] = None,
        http_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRoute", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param grpc_route: grpc_route block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#grpc_route AppmeshGatewayRoute#grpc_route}
        :param http2_route: http2_route block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#http2_route AppmeshGatewayRoute#http2_route}
        :param http_route: http_route block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#http_route AppmeshGatewayRoute#http_route}
        '''
        value = AppmeshGatewayRouteSpec(
            grpc_route=grpc_route, http2_route=http2_route, http_route=http_route
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMeshOwner")
    def reset_mesh_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMeshOwner", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="createdDate")
    def created_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdDate"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedDate")
    def last_updated_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedDate"))

    @builtins.property
    @jsii.member(jsii_name="resourceOwner")
    def resource_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceOwner"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "AppmeshGatewayRouteSpecOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="meshNameInput")
    def mesh_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshNameInput"))

    @builtins.property
    @jsii.member(jsii_name="meshOwnerInput")
    def mesh_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["AppmeshGatewayRouteSpec"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualGatewayNameInput")
    def virtual_gateway_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualGatewayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98bdbb0720e3b7095e9839f18362dffa2ca4dff5625b87c522a95057c7fb4c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "meshName"))

    @mesh_name.setter
    def mesh_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfb5ef135ee5c1b84267d88df0bea00286cbfca4c7568c8efacb5f652e045e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "meshName", value)

    @builtins.property
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "meshOwner"))

    @mesh_owner.setter
    def mesh_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4601d2e31650d20464f2cbc80634581522cea091b218b21cffad4e3a442461f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "meshOwner", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a3128855aa817b54a71f80d39ad791c9f49110ce40d88e0531379d8a3770a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c621a6b5c8280b0dc9e46ba0ef337be6aa6d9d3673c8e2e1fd5f40e84fd91120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ec4445abc0599b565ca59ff59eed1ca87efa25c810b70bffefe81643f3e24a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="virtualGatewayName")
    def virtual_gateway_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualGatewayName"))

    @virtual_gateway_name.setter
    def virtual_gateway_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1290e080ec4c464cd4486fd231258fbbf0f8eb55f14dc1db475392986b0f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualGatewayName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "mesh_name": "meshName",
        "name": "name",
        "spec": "spec",
        "virtual_gateway_name": "virtualGatewayName",
        "id": "id",
        "mesh_owner": "meshOwner",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class AppmeshGatewayRouteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        mesh_name: builtins.str,
        name: builtins.str,
        spec: typing.Union["AppmeshGatewayRouteSpec", typing.Dict[builtins.str, typing.Any]],
        virtual_gateway_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        mesh_owner: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param mesh_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#mesh_name AppmeshGatewayRoute#mesh_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#name AppmeshGatewayRoute#name}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#spec AppmeshGatewayRoute#spec}
        :param virtual_gateway_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_gateway_name AppmeshGatewayRoute#virtual_gateway_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#id AppmeshGatewayRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mesh_owner: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#mesh_owner AppmeshGatewayRoute#mesh_owner}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#tags AppmeshGatewayRoute#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#tags_all AppmeshGatewayRoute#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(spec, dict):
            spec = AppmeshGatewayRouteSpec(**spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f66556134b08211f9bda7a3437147ccfaaaae1069bb1fd20f422601b2f37e3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument mesh_name", value=mesh_name, expected_type=type_hints["mesh_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument virtual_gateway_name", value=virtual_gateway_name, expected_type=type_hints["virtual_gateway_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mesh_owner", value=mesh_owner, expected_type=type_hints["mesh_owner"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mesh_name": mesh_name,
            "name": name,
            "spec": spec,
            "virtual_gateway_name": virtual_gateway_name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if id is not None:
            self._values["id"] = id
        if mesh_owner is not None:
            self._values["mesh_owner"] = mesh_owner
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def mesh_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#mesh_name AppmeshGatewayRoute#mesh_name}.'''
        result = self._values.get("mesh_name")
        assert result is not None, "Required property 'mesh_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#name AppmeshGatewayRoute#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec(self) -> "AppmeshGatewayRouteSpec":
        '''spec block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#spec AppmeshGatewayRoute#spec}
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("AppmeshGatewayRouteSpec", result)

    @builtins.property
    def virtual_gateway_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_gateway_name AppmeshGatewayRoute#virtual_gateway_name}.'''
        result = self._values.get("virtual_gateway_name")
        assert result is not None, "Required property 'virtual_gateway_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#id AppmeshGatewayRoute#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh_owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#mesh_owner AppmeshGatewayRoute#mesh_owner}.'''
        result = self._values.get("mesh_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#tags AppmeshGatewayRoute#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#tags_all AppmeshGatewayRoute#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpec",
    jsii_struct_bases=[],
    name_mapping={
        "grpc_route": "grpcRoute",
        "http2_route": "http2Route",
        "http_route": "httpRoute",
    },
)
class AppmeshGatewayRouteSpec:
    def __init__(
        self,
        *,
        grpc_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecGrpcRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        http2_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2Route", typing.Dict[builtins.str, typing.Any]]] = None,
        http_route: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRoute", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param grpc_route: grpc_route block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#grpc_route AppmeshGatewayRoute#grpc_route}
        :param http2_route: http2_route block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#http2_route AppmeshGatewayRoute#http2_route}
        :param http_route: http_route block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#http_route AppmeshGatewayRoute#http_route}
        '''
        if isinstance(grpc_route, dict):
            grpc_route = AppmeshGatewayRouteSpecGrpcRoute(**grpc_route)
        if isinstance(http2_route, dict):
            http2_route = AppmeshGatewayRouteSpecHttp2Route(**http2_route)
        if isinstance(http_route, dict):
            http_route = AppmeshGatewayRouteSpecHttpRoute(**http_route)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7940c8016870085d0d985d73d4043b0aa55e756d1c2bb991654f8018da2db3c9)
            check_type(argname="argument grpc_route", value=grpc_route, expected_type=type_hints["grpc_route"])
            check_type(argname="argument http2_route", value=http2_route, expected_type=type_hints["http2_route"])
            check_type(argname="argument http_route", value=http_route, expected_type=type_hints["http_route"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grpc_route is not None:
            self._values["grpc_route"] = grpc_route
        if http2_route is not None:
            self._values["http2_route"] = http2_route
        if http_route is not None:
            self._values["http_route"] = http_route

    @builtins.property
    def grpc_route(self) -> typing.Optional["AppmeshGatewayRouteSpecGrpcRoute"]:
        '''grpc_route block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#grpc_route AppmeshGatewayRoute#grpc_route}
        '''
        result = self._values.get("grpc_route")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecGrpcRoute"], result)

    @builtins.property
    def http2_route(self) -> typing.Optional["AppmeshGatewayRouteSpecHttp2Route"]:
        '''http2_route block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#http2_route AppmeshGatewayRoute#http2_route}
        '''
        result = self._values.get("http2_route")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2Route"], result)

    @builtins.property
    def http_route(self) -> typing.Optional["AppmeshGatewayRouteSpecHttpRoute"]:
        '''http_route block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#http_route AppmeshGatewayRoute#http_route}
        '''
        result = self._values.get("http_route")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRoute"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRoute",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "match": "match"},
)
class AppmeshGatewayRouteSpecGrpcRoute:
    def __init__(
        self,
        *,
        action: typing.Union["AppmeshGatewayRouteSpecGrpcRouteAction", typing.Dict[builtins.str, typing.Any]],
        match: typing.Union["AppmeshGatewayRouteSpecGrpcRouteMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        if isinstance(action, dict):
            action = AppmeshGatewayRouteSpecGrpcRouteAction(**action)
        if isinstance(match, dict):
            match = AppmeshGatewayRouteSpecGrpcRouteMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__537a881568bb73c24d65c3b086a38b98a82a4c5e2f8daab4f6d6f09959faafb9)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
        }

    @builtins.property
    def action(self) -> "AppmeshGatewayRouteSpecGrpcRouteAction":
        '''action block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteAction", result)

    @builtins.property
    def match(self) -> "AppmeshGatewayRouteSpecGrpcRouteMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteMatch", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecGrpcRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteAction",
    jsii_struct_bases=[],
    name_mapping={"target": "target"},
)
class AppmeshGatewayRouteSpecGrpcRouteAction:
    def __init__(
        self,
        *,
        target: typing.Union["AppmeshGatewayRouteSpecGrpcRouteActionTarget", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        '''
        if isinstance(target, dict):
            target = AppmeshGatewayRouteSpecGrpcRouteActionTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5545abfede7bba722e5caf060bf23b5112f04dc87ea6d5323538f5c66b95742b)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }

    @builtins.property
    def target(self) -> "AppmeshGatewayRouteSpecGrpcRouteActionTarget":
        '''target block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteActionTarget", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecGrpcRouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecGrpcRouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteActionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d1e5ea2cb72092800cd1598594c08104853ce9346ad40dae73eb8a118efbc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        value = AppmeshGatewayRouteSpecGrpcRouteActionTarget(
            virtual_service=virtual_service
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "AppmeshGatewayRouteSpecGrpcRouteActionTargetOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteActionTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecGrpcRouteActionTarget"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecGrpcRouteActionTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fa4815bc94dcd858a072a489f7627cb722fc5cf43b95c763786987d0bdfe6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteActionTarget",
    jsii_struct_bases=[],
    name_mapping={"virtual_service": "virtualService"},
)
class AppmeshGatewayRouteSpecGrpcRouteActionTarget:
    def __init__(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        if isinstance(virtual_service, dict):
            virtual_service = AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService(**virtual_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b65d6b2070220cbe91af21d9de7f7e040e47ea6b7589d82fa9dfd077a0306ae8)
            check_type(argname="argument virtual_service", value=virtual_service, expected_type=type_hints["virtual_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service": virtual_service,
        }

    @builtins.property
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService":
        '''virtual_service block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        result = self._values.get("virtual_service")
        assert result is not None, "Required property 'virtual_service' is missing"
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecGrpcRouteActionTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecGrpcRouteActionTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteActionTargetOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22fd2a108c1b1c2a45923f6c3bc7ca69ebb9021b1f47872b97a83169bd001922)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVirtualService")
    def put_virtual_service(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        value = AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService(
            virtual_service_name=virtual_service_name
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualService", [value]))

    @builtins.property
    @jsii.member(jsii_name="virtualService")
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualServiceOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualServiceOutputReference", jsii.get(self, "virtualService"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceInput")
    def virtual_service_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService"], jsii.get(self, "virtualServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTarget]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a220525822b09fbfbb20b4a68dfcd63d54dae1782313012c744f76a7d13f73c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService",
    jsii_struct_bases=[],
    name_mapping={"virtual_service_name": "virtualServiceName"},
)
class AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService:
    def __init__(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb63ce84aae52475febf1a0caab518396dbe45d706a35624f0979baf955e41ff)
            check_type(argname="argument virtual_service_name", value=virtual_service_name, expected_type=type_hints["virtual_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service_name": virtual_service_name,
        }

    @builtins.property
    def virtual_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.'''
        result = self._values.get("virtual_service_name")
        assert result is not None, "Required property 'virtual_service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualServiceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb8053f72bc27e1096b4cfaa03a84b8b36d2e2114cc5785ab508324113ff044)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="virtualServiceNameInput")
    def virtual_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceName"))

    @virtual_service_name.setter
    def virtual_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740d4c744bd8e9fe4f2985f91759068065b2dcae2b87270283091c82d64781dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualServiceName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41afca36a44605e202261c8fcd5aacd07819bb405ea06474a1e22ad33b8beea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteMatch",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName"},
)
class AppmeshGatewayRouteSpecGrpcRouteMatch:
    def __init__(self, *, service_name: builtins.str) -> None:
        '''
        :param service_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#service_name AppmeshGatewayRoute#service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d96db30d4321e8cac5b5f7bf6ca798ad83b6e1f9b9c93722e25eb1017e52d0)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_name": service_name,
        }

    @builtins.property
    def service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#service_name AppmeshGatewayRoute#service_name}.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecGrpcRouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecGrpcRouteMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteMatchOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61463ab138bf588c898b874bbf0db343225aca7015ac657064831ef1431d612c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32d14cf24d59f9d00a51859b1e0aad5724f84f4f650e0469bce5ac5c4669ab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dda5acd96495b926e84f2baae12ee0898893472c9b5d879230fa1180f29b03e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppmeshGatewayRouteSpecGrpcRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecGrpcRouteOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c073a42927749e82f3406eb3ba561dc2f508296e8b210b5f6eabfc65f5487c17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        target: typing.Union[AppmeshGatewayRouteSpecGrpcRouteActionTarget, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        '''
        value = AppmeshGatewayRouteSpecGrpcRouteAction(target=target)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(self, *, service_name: builtins.str) -> None:
        '''
        :param service_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#service_name AppmeshGatewayRoute#service_name}.
        '''
        value = AppmeshGatewayRouteSpecGrpcRouteMatch(service_name=service_name)

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> AppmeshGatewayRouteSpecGrpcRouteActionOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecGrpcRouteActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshGatewayRouteSpecGrpcRouteMatchOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecGrpcRouteMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRoute]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecGrpcRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e675848a9b68c3d9b4377795ff1c9fbd85c32ec6658c2dff8fb308e814551ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2Route",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "match": "match"},
)
class AppmeshGatewayRouteSpecHttp2Route:
    def __init__(
        self,
        *,
        action: typing.Union["AppmeshGatewayRouteSpecHttp2RouteAction", typing.Dict[builtins.str, typing.Any]],
        match: typing.Union["AppmeshGatewayRouteSpecHttp2RouteMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        if isinstance(action, dict):
            action = AppmeshGatewayRouteSpecHttp2RouteAction(**action)
        if isinstance(match, dict):
            match = AppmeshGatewayRouteSpecHttp2RouteMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a78bf62a9ffaaa26ce4b8664e86c2427e373d50a51c3358e73492ed252909c)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
        }

    @builtins.property
    def action(self) -> "AppmeshGatewayRouteSpecHttp2RouteAction":
        '''action block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteAction", result)

    @builtins.property
    def match(self) -> "AppmeshGatewayRouteSpecHttp2RouteMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteMatch", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2Route(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteAction",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "rewrite": "rewrite"},
)
class AppmeshGatewayRouteSpecHttp2RouteAction:
    def __init__(
        self,
        *,
        target: typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionTarget", typing.Dict[builtins.str, typing.Any]],
        rewrite: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        :param rewrite: rewrite block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        if isinstance(target, dict):
            target = AppmeshGatewayRouteSpecHttp2RouteActionTarget(**target)
        if isinstance(rewrite, dict):
            rewrite = AppmeshGatewayRouteSpecHttp2RouteActionRewrite(**rewrite)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8215426fd7a4f9429108ec9959beb16ab2b93114a43af98314b61fbebc1a9f)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument rewrite", value=rewrite, expected_type=type_hints["rewrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }
        if rewrite is not None:
            self._values["rewrite"] = rewrite

    @builtins.property
    def target(self) -> "AppmeshGatewayRouteSpecHttp2RouteActionTarget":
        '''target block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionTarget", result)

    @builtins.property
    def rewrite(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewrite"]:
        '''rewrite block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        result = self._values.get("rewrite")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewrite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2cb5bc5f908d642b65f770cbb2e0605c10f599fc38790bcea1485dd5183efe8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRewrite")
    def put_rewrite(
        self,
        *,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param prefix: prefix block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteActionRewrite(
            hostname=hostname, prefix=prefix
        )

        return typing.cast(None, jsii.invoke(self, "putRewrite", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteActionTarget(
            virtual_service=virtual_service
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="resetRewrite")
    def reset_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewrite", []))

    @builtins.property
    @jsii.member(jsii_name="rewrite")
    def rewrite(
        self,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteActionRewriteOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionRewriteOutputReference", jsii.get(self, "rewrite"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "AppmeshGatewayRouteSpecHttp2RouteActionTargetOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="rewriteInput")
    def rewrite_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewrite"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewrite"], jsii.get(self, "rewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionTarget"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af94131d6917ccaf2f0a12aa6aec538f2dc02f679c8cfd4145d84797fb6b6326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewrite",
    jsii_struct_bases=[],
    name_mapping={"hostname": "hostname", "prefix": "prefix"},
)
class AppmeshGatewayRouteSpecHttp2RouteActionRewrite:
    def __init__(
        self,
        *,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param prefix: prefix block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        if isinstance(hostname, dict):
            hostname = AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname(**hostname)
        if isinstance(prefix, dict):
            prefix = AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix(**prefix)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fca5e5a2d477c7e101ffe1823d2d45c61463a4d6b8eb2b83e2f0c235425efcf)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hostname is not None:
            self._values["hostname"] = hostname
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def hostname(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname"]:
        '''hostname block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname"], result)

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix"]:
        '''prefix block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteActionRewrite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname",
    jsii_struct_bases=[],
    name_mapping={"default_target_hostname": "defaultTargetHostname"},
)
class AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname:
    def __init__(self, *, default_target_hostname: builtins.str) -> None:
        '''
        :param default_target_hostname: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf9e1a744ccd05fdd3d39b3cc85ce7d6c6f143271dc52879341b1e97c1e946b)
            check_type(argname="argument default_target_hostname", value=default_target_hostname, expected_type=type_hints["default_target_hostname"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_target_hostname": default_target_hostname,
        }

    @builtins.property
    def default_target_hostname(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.'''
        result = self._values.get("default_target_hostname")
        assert result is not None, "Required property 'default_target_hostname' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostnameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostnameOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c332936968fa658e89449dfa16f1ba5496590bcc46dcbc3f0da00804ad5b60b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultTargetHostnameInput")
    def default_target_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTargetHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTargetHostname")
    def default_target_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTargetHostname"))

    @default_target_hostname.setter
    def default_target_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d93ff791bef72c82eaf65b815fe8a6d7e57d5f487e3104608908b5e676e3333f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTargetHostname", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd909203a87e2e1ab56a0eeec7df5e01eaacfd22d65f8e868bf42c8bdbb3c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppmeshGatewayRouteSpecHttp2RouteActionRewriteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewriteOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae51b6ed8e7eb8372830137761662751f2aedf558f15c0cb7c4f0dd6b42e7769)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHostname")
    def put_hostname(self, *, default_target_hostname: builtins.str) -> None:
        '''
        :param default_target_hostname: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname(
            default_target_hostname=default_target_hostname
        )

        return typing.cast(None, jsii.invoke(self, "putHostname", [value]))

    @jsii.member(jsii_name="putPrefix")
    def put_prefix(
        self,
        *,
        default_prefix: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#value AppmeshGatewayRoute#value}.
        '''
        value_ = AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix(
            default_prefix=default_prefix, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putPrefix", [value_]))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(
        self,
    ) -> AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostnameOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostnameOutputReference, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(
        self,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefixOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefixOutputReference", jsii.get(self, "prefix"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix"], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewrite]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewrite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewrite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05934dd34dbdc705004503a12a1d9fc26af7a255c343e2dafb496a88a2a90cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix",
    jsii_struct_bases=[],
    name_mapping={"default_prefix": "defaultPrefix", "value": "value"},
)
class AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix:
    def __init__(
        self,
        *,
        default_prefix: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#value AppmeshGatewayRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b944f8f4337901e916017185cc4e68ee6b82f79e845fd1d82a8a841e0173865)
            check_type(argname="argument default_prefix", value=default_prefix, expected_type=type_hints["default_prefix"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_prefix is not None:
            self._values["default_prefix"] = default_prefix
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def default_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.'''
        result = self._values.get("default_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#value AppmeshGatewayRoute#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefixOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefixOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367f84d9ac1d8a4f69daffc7e66061cb9945a7526035ff9276a34a422fb7a61a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultPrefix")
    def reset_default_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPrefix", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="defaultPrefixInput")
    def default_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPrefix")
    def default_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPrefix"))

    @default_prefix.setter
    def default_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4c71f16ff7c62abca1cb60c5711613fc5d64e5aee3a7a67315f0ea950d347f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0459b3c829270bc3e07edf5de731629a9417b0d32fd87ec10b8e8d931c246bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f541e9fa78fa39677d4536b13458f000f63e476f620e747bc2187580175e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionTarget",
    jsii_struct_bases=[],
    name_mapping={"virtual_service": "virtualService"},
)
class AppmeshGatewayRouteSpecHttp2RouteActionTarget:
    def __init__(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        if isinstance(virtual_service, dict):
            virtual_service = AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService(**virtual_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9596797cbc1b38916c99c36ddd07536f3930a7071e2336d88a8ed3c0d7c511)
            check_type(argname="argument virtual_service", value=virtual_service, expected_type=type_hints["virtual_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service": virtual_service,
        }

    @builtins.property
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService":
        '''virtual_service block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        result = self._values.get("virtual_service")
        assert result is not None, "Required property 'virtual_service' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteActionTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteActionTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionTargetOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002c6b9f52375405b54989d4c85a18e684b733870458da717484b95220937db5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVirtualService")
    def put_virtual_service(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService(
            virtual_service_name=virtual_service_name
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualService", [value]))

    @builtins.property
    @jsii.member(jsii_name="virtualService")
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualServiceOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualServiceOutputReference", jsii.get(self, "virtualService"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceInput")
    def virtual_service_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService"], jsii.get(self, "virtualServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTarget]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e16b736fa7301c53d1d7f169fc59f24f03d37b7793f4418067f157443538de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService",
    jsii_struct_bases=[],
    name_mapping={"virtual_service_name": "virtualServiceName"},
)
class AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService:
    def __init__(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5114646cd76daf1b4ac291dea8fd7ade5b52cf612cf9af13b7b275fe5965a17)
            check_type(argname="argument virtual_service_name", value=virtual_service_name, expected_type=type_hints["virtual_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service_name": virtual_service_name,
        }

    @builtins.property
    def virtual_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.'''
        result = self._values.get("virtual_service_name")
        assert result is not None, "Required property 'virtual_service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualServiceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca1c5058e640f756a526937412e8f476fa6e0e04ed0f8b59d8e89f60aaf5205)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="virtualServiceNameInput")
    def virtual_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceName"))

    @virtual_service_name.setter
    def virtual_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e328abaad64fc02acf63c6fccdb42233da3881d3d6e0e8c4c4be4db21d1db7d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualServiceName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db71933bd644c7152207a3d012fae1bfdf6cb41a6675bf4b716c673e5718bb0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatch",
    jsii_struct_bases=[],
    name_mapping={"hostname": "hostname", "prefix": "prefix"},
)
class AppmeshGatewayRouteSpecHttp2RouteMatch:
    def __init__(
        self,
        *,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttp2RouteMatchHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        '''
        if isinstance(hostname, dict):
            hostname = AppmeshGatewayRouteSpecHttp2RouteMatchHostname(**hostname)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f995d0139eebf348730c4d1b1636c383c683cccd5a586789b4ab2a8d8dd877a3)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hostname is not None:
            self._values["hostname"] = hostname
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def hostname(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchHostname"]:
        '''hostname block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttp2RouteMatchHostname"], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchHostname",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact", "suffix": "suffix"},
)
class AppmeshGatewayRouteSpecHttp2RouteMatchHostname:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param suffix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da8d99cc4439d2501492455dbc188f1318b1b0f5256c7707e8f18f41579d4b4)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.'''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttp2RouteMatchHostname(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttp2RouteMatchHostnameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchHostnameOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16efbf8d6d250979ffb0c756215a4fdda56e578c377a31351cfd5042f6f97535)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f67e8b75acae70c2473527120858db3f0b3fa125a3b392200908c0b8c2c8a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value)

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a102594ae3a5d9326ad549a4bee6dc15d243bc347fc242a2f47b8f44e7698212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f3fced859d8f1ba5ac344fed30e942e203426451153ae8bc31324e7fa07070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppmeshGatewayRouteSpecHttp2RouteMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteMatchOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f3d530504187a62c902507bd39da9497dcba4ccfe00abdfb640e92eb103a74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHostname")
    def put_hostname(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param suffix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteMatchHostname(
            exact=exact, suffix=suffix
        )

        return typing.cast(None, jsii.invoke(self, "putHostname", [value]))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> AppmeshGatewayRouteSpecHttp2RouteMatchHostnameOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteMatchHostnameOutputReference, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b06614002b103ca086417a475d61843e07b453629f87440f487234b6451c474e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a1e59ebd546bbc102df39cdb2aed6bd84ff74aa927367619f6e5b62f41ccff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppmeshGatewayRouteSpecHttp2RouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttp2RouteOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db2fb7756fc065ec3e9257fb0d8779f98fb7b6da6da7575e6afc1ceaacfecee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        target: typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionTarget, typing.Dict[builtins.str, typing.Any]],
        rewrite: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        :param rewrite: rewrite block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteAction(target=target, rewrite=rewrite)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchHostname, typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        '''
        value = AppmeshGatewayRouteSpecHttp2RouteMatch(
            hostname=hostname, prefix=prefix
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> AppmeshGatewayRouteSpecHttp2RouteActionOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshGatewayRouteSpecHttp2RouteMatchOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecHttp2Route]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2Route], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttp2Route],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe08a7e67eb4650a93600073e25208530b7c1fd1f13db156fb17bca851a79f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRoute",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "match": "match"},
)
class AppmeshGatewayRouteSpecHttpRoute:
    def __init__(
        self,
        *,
        action: typing.Union["AppmeshGatewayRouteSpecHttpRouteAction", typing.Dict[builtins.str, typing.Any]],
        match: typing.Union["AppmeshGatewayRouteSpecHttpRouteMatch", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        if isinstance(action, dict):
            action = AppmeshGatewayRouteSpecHttpRouteAction(**action)
        if isinstance(match, dict):
            match = AppmeshGatewayRouteSpecHttpRouteMatch(**match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eddf4d72dd6db89ab77ae46ef31b870a9c3bc5503a8ee0c1a606354a560cf22)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
        }

    @builtins.property
    def action(self) -> "AppmeshGatewayRouteSpecHttpRouteAction":
        '''action block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteAction", result)

    @builtins.property
    def match(self) -> "AppmeshGatewayRouteSpecHttpRouteMatch":
        '''match block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteMatch", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteAction",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "rewrite": "rewrite"},
)
class AppmeshGatewayRouteSpecHttpRouteAction:
    def __init__(
        self,
        *,
        target: typing.Union["AppmeshGatewayRouteSpecHttpRouteActionTarget", typing.Dict[builtins.str, typing.Any]],
        rewrite: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        :param rewrite: rewrite block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        if isinstance(target, dict):
            target = AppmeshGatewayRouteSpecHttpRouteActionTarget(**target)
        if isinstance(rewrite, dict):
            rewrite = AppmeshGatewayRouteSpecHttpRouteActionRewrite(**rewrite)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3ceb719f6fd1c5696386fc28aa53aa84f1d378397427926cfc797084e55a6f)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument rewrite", value=rewrite, expected_type=type_hints["rewrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }
        if rewrite is not None:
            self._values["rewrite"] = rewrite

    @builtins.property
    def target(self) -> "AppmeshGatewayRouteSpecHttpRouteActionTarget":
        '''target block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionTarget", result)

    @builtins.property
    def rewrite(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewrite"]:
        '''rewrite block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        result = self._values.get("rewrite")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewrite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__addb7c2d8cbd83fe5822409cb7f1ff7e43c3397febf87416b6d6eb75921132e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRewrite")
    def put_rewrite(
        self,
        *,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param prefix: prefix block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        value = AppmeshGatewayRouteSpecHttpRouteActionRewrite(
            hostname=hostname, prefix=prefix
        )

        return typing.cast(None, jsii.invoke(self, "putRewrite", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        value = AppmeshGatewayRouteSpecHttpRouteActionTarget(
            virtual_service=virtual_service
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="resetRewrite")
    def reset_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewrite", []))

    @builtins.property
    @jsii.member(jsii_name="rewrite")
    def rewrite(self) -> "AppmeshGatewayRouteSpecHttpRouteActionRewriteOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionRewriteOutputReference", jsii.get(self, "rewrite"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "AppmeshGatewayRouteSpecHttpRouteActionTargetOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="rewriteInput")
    def rewrite_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewrite"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewrite"], jsii.get(self, "rewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionTarget"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187d20ce260d53c6906d1aed58f45d0f14d16ababb7d99084ed7c02d3acf1866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewrite",
    jsii_struct_bases=[],
    name_mapping={"hostname": "hostname", "prefix": "prefix"},
)
class AppmeshGatewayRouteSpecHttpRouteActionRewrite:
    def __init__(
        self,
        *,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param prefix: prefix block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        if isinstance(hostname, dict):
            hostname = AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname(**hostname)
        if isinstance(prefix, dict):
            prefix = AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix(**prefix)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df7a52aa98cdbfd320bcd19dd5424708b1f37202ef53c8e6fd872fac5b9c84d8)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hostname is not None:
            self._values["hostname"] = hostname
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def hostname(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname"]:
        '''hostname block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname"], result)

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix"]:
        '''prefix block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteActionRewrite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname",
    jsii_struct_bases=[],
    name_mapping={"default_target_hostname": "defaultTargetHostname"},
)
class AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname:
    def __init__(self, *, default_target_hostname: builtins.str) -> None:
        '''
        :param default_target_hostname: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048c6ffd4a3d57c6ae9de2310274073e8fc9e0dff787ddf5aad4a8a99208afaf)
            check_type(argname="argument default_target_hostname", value=default_target_hostname, expected_type=type_hints["default_target_hostname"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_target_hostname": default_target_hostname,
        }

    @builtins.property
    def default_target_hostname(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.'''
        result = self._values.get("default_target_hostname")
        assert result is not None, "Required property 'default_target_hostname' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteActionRewriteHostnameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewriteHostnameOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0a8ccbe672e9dc4016eec082dc1dc46debec52cbbaab756d33439869785c7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultTargetHostnameInput")
    def default_target_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTargetHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTargetHostname")
    def default_target_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTargetHostname"))

    @default_target_hostname.setter
    def default_target_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659fad1ae18ceaedcfe0c546eb080b53bd9b3f41147ea0b794795897a58472e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTargetHostname", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f63ea20dd31d6aad78b7302e3d5623c2c1a587b1704781a7a69846d37fe62b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppmeshGatewayRouteSpecHttpRouteActionRewriteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewriteOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f76708ce6bd3ad3416ea6decad9c515e50b30cb16d23c959fe37d6a29bd241)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHostname")
    def put_hostname(self, *, default_target_hostname: builtins.str) -> None:
        '''
        :param default_target_hostname: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_target_hostname AppmeshGatewayRoute#default_target_hostname}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname(
            default_target_hostname=default_target_hostname
        )

        return typing.cast(None, jsii.invoke(self, "putHostname", [value]))

    @jsii.member(jsii_name="putPrefix")
    def put_prefix(
        self,
        *,
        default_prefix: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#value AppmeshGatewayRoute#value}.
        '''
        value_ = AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix(
            default_prefix=default_prefix, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putPrefix", [value_]))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(
        self,
    ) -> AppmeshGatewayRouteSpecHttpRouteActionRewriteHostnameOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteActionRewriteHostnameOutputReference, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(
        self,
    ) -> "AppmeshGatewayRouteSpecHttpRouteActionRewritePrefixOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionRewritePrefixOutputReference", jsii.get(self, "prefix"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix"], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewrite]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewrite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewrite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b871c4a8ca562225b1a639b8369842d22a993044d832d650f0a92bb27adb35e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix",
    jsii_struct_bases=[],
    name_mapping={"default_prefix": "defaultPrefix", "value": "value"},
)
class AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix:
    def __init__(
        self,
        *,
        default_prefix: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#value AppmeshGatewayRoute#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70926ac39fb20d9f6ede0459ee24f540873e26a9a73986543033c5778e155413)
            check_type(argname="argument default_prefix", value=default_prefix, expected_type=type_hints["default_prefix"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_prefix is not None:
            self._values["default_prefix"] = default_prefix
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def default_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#default_prefix AppmeshGatewayRoute#default_prefix}.'''
        result = self._values.get("default_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#value AppmeshGatewayRoute#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteActionRewritePrefixOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionRewritePrefixOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fa0051d97694d280f46ec4ac6d593a8f6f49abc0dd863dbeabca9dbd480c47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultPrefix")
    def reset_default_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPrefix", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="defaultPrefixInput")
    def default_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPrefix")
    def default_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPrefix"))

    @default_prefix.setter
    def default_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079001d5a07829272ed8d94776e70d2b9154e04568a9b52898d207abf084d079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81237ea077e54f01940f1e817dfb25729e68c7653a572c717f76872a7a78e2e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c92b5ffa40b20d27ffd45514fdce73c8d9d6661addea4d3d9fc3e8bc4ce757c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionTarget",
    jsii_struct_bases=[],
    name_mapping={"virtual_service": "virtualService"},
)
class AppmeshGatewayRouteSpecHttpRouteActionTarget:
    def __init__(
        self,
        *,
        virtual_service: typing.Union["AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param virtual_service: virtual_service block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        if isinstance(virtual_service, dict):
            virtual_service = AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService(**virtual_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0671c61558ec8df4536354483c46017c0789a9aed147b82f817a5860159875c5)
            check_type(argname="argument virtual_service", value=virtual_service, expected_type=type_hints["virtual_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service": virtual_service,
        }

    @builtins.property
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService":
        '''virtual_service block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service AppmeshGatewayRoute#virtual_service}
        '''
        result = self._values.get("virtual_service")
        assert result is not None, "Required property 'virtual_service' is missing"
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteActionTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteActionTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionTargetOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053be28363b55811b3e5fb30dc96915c54865e5c547652e7512b0fa9cde0fe21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVirtualService")
    def put_virtual_service(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService(
            virtual_service_name=virtual_service_name
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualService", [value]))

    @builtins.property
    @jsii.member(jsii_name="virtualService")
    def virtual_service(
        self,
    ) -> "AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualServiceOutputReference":
        return typing.cast("AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualServiceOutputReference", jsii.get(self, "virtualService"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceInput")
    def virtual_service_input(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService"]:
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService"], jsii.get(self, "virtualServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTarget]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314f53af1abc2e47099069cdcf1acf5d19ceac7ff47c7c128db54602ad9f29d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService",
    jsii_struct_bases=[],
    name_mapping={"virtual_service_name": "virtualServiceName"},
)
class AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService:
    def __init__(self, *, virtual_service_name: builtins.str) -> None:
        '''
        :param virtual_service_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c709d6d322c9276447646bd0a265dc9c9c2e23943cdf87415bc4c05c06847a)
            check_type(argname="argument virtual_service_name", value=virtual_service_name, expected_type=type_hints["virtual_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_service_name": virtual_service_name,
        }

    @builtins.property
    def virtual_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#virtual_service_name AppmeshGatewayRoute#virtual_service_name}.'''
        result = self._values.get("virtual_service_name")
        assert result is not None, "Required property 'virtual_service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualServiceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3baa2c0d75308e803ec5d880ddca3a5829d0fc573a9c2417432348bdd4301fc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="virtualServiceNameInput")
    def virtual_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceName"))

    @virtual_service_name.setter
    def virtual_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26cf747cdead6c825c3187f1d0d0572bfc8ce148c145f48156aa4edc33934d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualServiceName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f8236f15e9a1fd4cb8d654b09bbdf6d5c9234748aa578a84249b41e1bb5b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatch",
    jsii_struct_bases=[],
    name_mapping={"hostname": "hostname", "prefix": "prefix"},
)
class AppmeshGatewayRouteSpecHttpRouteMatch:
    def __init__(
        self,
        *,
        hostname: typing.Optional[typing.Union["AppmeshGatewayRouteSpecHttpRouteMatchHostname", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        '''
        if isinstance(hostname, dict):
            hostname = AppmeshGatewayRouteSpecHttpRouteMatchHostname(**hostname)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7e1c3bc4db19d440b59d7940440310eb714201548d62234aa3d784c8ba37a8)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hostname is not None:
            self._values["hostname"] = hostname
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def hostname(
        self,
    ) -> typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchHostname"]:
        '''hostname block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional["AppmeshGatewayRouteSpecHttpRouteMatchHostname"], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchHostname",
    jsii_struct_bases=[],
    name_mapping={"exact": "exact", "suffix": "suffix"},
)
class AppmeshGatewayRouteSpecHttpRouteMatchHostname:
    def __init__(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param suffix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d41646d880450216f963307cc63a096aabf8442775f16ea0c1e185076ba076)
            check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact is not None:
            self._values["exact"] = exact
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.'''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.'''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppmeshGatewayRouteSpecHttpRouteMatchHostname(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppmeshGatewayRouteSpecHttpRouteMatchHostnameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchHostnameOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844fb35c4bdb1623cc8ce94d4c2f66a44fd1cd50a6e4efb99f8a98ded1657b78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExact")
    def reset_exact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExact", []))

    @jsii.member(jsii_name="resetSuffix")
    def reset_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="exactInput")
    def exact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixInput")
    def suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixInput"))

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d47b2689690c5182e87326d8b6dd7b0f8f9d1087fd24e2147e17c7095366773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exact", value)

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9a5fc6389f17a9d1d751176d3b808be3c0ecc8ac3cccf1c381816175ee7481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b1070aed85b33b35f540ca9d2aafe0856cbd27342228e22c6d91de688ecffce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppmeshGatewayRouteSpecHttpRouteMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteMatchOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45162d619709986c97890b6a623bf3bb50021db10787fdcbff1a380e55cdb9a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHostname")
    def put_hostname(
        self,
        *,
        exact: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#exact AppmeshGatewayRoute#exact}.
        :param suffix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#suffix AppmeshGatewayRoute#suffix}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteMatchHostname(
            exact=exact, suffix=suffix
        )

        return typing.cast(None, jsii.invoke(self, "putHostname", [value]))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> AppmeshGatewayRouteSpecHttpRouteMatchHostnameOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteMatchHostnameOutputReference, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(
        self,
    ) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418996476b02022c89b36289c6266bf5392b41ccc27dfdec935e2589549196c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f60eb76d4b9667265239962116a28ea74be86171c5c85be83115f44791351b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppmeshGatewayRouteSpecHttpRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecHttpRouteOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d690ab4168ad26c84f24d8f01375a517d7e77d3bf1e9102e4fec8971f54c7f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        target: typing.Union[AppmeshGatewayRouteSpecHttpRouteActionTarget, typing.Dict[builtins.str, typing.Any]],
        rewrite: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteActionRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target: target block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#target AppmeshGatewayRoute#target}
        :param rewrite: rewrite block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#rewrite AppmeshGatewayRoute#rewrite}
        '''
        value = AppmeshGatewayRouteSpecHttpRouteAction(target=target, rewrite=rewrite)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchHostname, typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: hostname block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#hostname AppmeshGatewayRoute#hostname}
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#prefix AppmeshGatewayRoute#prefix}.
        '''
        value = AppmeshGatewayRouteSpecHttpRouteMatch(hostname=hostname, prefix=prefix)

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> AppmeshGatewayRouteSpecHttpRouteActionOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> AppmeshGatewayRouteSpecHttpRouteMatchOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRoute]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppmeshGatewayRouteSpecHttpRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efeeb7078bc6c298c26f7d1d7f5daada1ef99e2e1e9fa3f5d70e46b207f7e38e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppmeshGatewayRouteSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appmeshGatewayRoute.AppmeshGatewayRouteSpecOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae17c973e9300e571fadad415debd9b61500610da414fa7ee79143e68013326e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrpcRoute")
    def put_grpc_route(
        self,
        *,
        action: typing.Union[AppmeshGatewayRouteSpecGrpcRouteAction, typing.Dict[builtins.str, typing.Any]],
        match: typing.Union[AppmeshGatewayRouteSpecGrpcRouteMatch, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        value = AppmeshGatewayRouteSpecGrpcRoute(action=action, match=match)

        return typing.cast(None, jsii.invoke(self, "putGrpcRoute", [value]))

    @jsii.member(jsii_name="putHttp2Route")
    def put_http2_route(
        self,
        *,
        action: typing.Union[AppmeshGatewayRouteSpecHttp2RouteAction, typing.Dict[builtins.str, typing.Any]],
        match: typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatch, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        value = AppmeshGatewayRouteSpecHttp2Route(action=action, match=match)

        return typing.cast(None, jsii.invoke(self, "putHttp2Route", [value]))

    @jsii.member(jsii_name="putHttpRoute")
    def put_http_route(
        self,
        *,
        action: typing.Union[AppmeshGatewayRouteSpecHttpRouteAction, typing.Dict[builtins.str, typing.Any]],
        match: typing.Union[AppmeshGatewayRouteSpecHttpRouteMatch, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#action AppmeshGatewayRoute#action}
        :param match: match block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/appmesh_gateway_route#match AppmeshGatewayRoute#match}
        '''
        value = AppmeshGatewayRouteSpecHttpRoute(action=action, match=match)

        return typing.cast(None, jsii.invoke(self, "putHttpRoute", [value]))

    @jsii.member(jsii_name="resetGrpcRoute")
    def reset_grpc_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcRoute", []))

    @jsii.member(jsii_name="resetHttp2Route")
    def reset_http2_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2Route", []))

    @jsii.member(jsii_name="resetHttpRoute")
    def reset_http_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpRoute", []))

    @builtins.property
    @jsii.member(jsii_name="grpcRoute")
    def grpc_route(self) -> AppmeshGatewayRouteSpecGrpcRouteOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecGrpcRouteOutputReference, jsii.get(self, "grpcRoute"))

    @builtins.property
    @jsii.member(jsii_name="http2Route")
    def http2_route(self) -> AppmeshGatewayRouteSpecHttp2RouteOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttp2RouteOutputReference, jsii.get(self, "http2Route"))

    @builtins.property
    @jsii.member(jsii_name="httpRoute")
    def http_route(self) -> AppmeshGatewayRouteSpecHttpRouteOutputReference:
        return typing.cast(AppmeshGatewayRouteSpecHttpRouteOutputReference, jsii.get(self, "httpRoute"))

    @builtins.property
    @jsii.member(jsii_name="grpcRouteInput")
    def grpc_route_input(self) -> typing.Optional[AppmeshGatewayRouteSpecGrpcRoute]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecGrpcRoute], jsii.get(self, "grpcRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="http2RouteInput")
    def http2_route_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttp2Route]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttp2Route], jsii.get(self, "http2RouteInput"))

    @builtins.property
    @jsii.member(jsii_name="httpRouteInput")
    def http_route_input(self) -> typing.Optional[AppmeshGatewayRouteSpecHttpRoute]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpecHttpRoute], jsii.get(self, "httpRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppmeshGatewayRouteSpec]:
        return typing.cast(typing.Optional[AppmeshGatewayRouteSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppmeshGatewayRouteSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efd07e505ee9cc1d486a89b5a69fa5df9a1d49d9918dcacab36ed5c96f98ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AppmeshGatewayRoute",
    "AppmeshGatewayRouteConfig",
    "AppmeshGatewayRouteSpec",
    "AppmeshGatewayRouteSpecGrpcRoute",
    "AppmeshGatewayRouteSpecGrpcRouteAction",
    "AppmeshGatewayRouteSpecGrpcRouteActionOutputReference",
    "AppmeshGatewayRouteSpecGrpcRouteActionTarget",
    "AppmeshGatewayRouteSpecGrpcRouteActionTargetOutputReference",
    "AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService",
    "AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualServiceOutputReference",
    "AppmeshGatewayRouteSpecGrpcRouteMatch",
    "AppmeshGatewayRouteSpecGrpcRouteMatchOutputReference",
    "AppmeshGatewayRouteSpecGrpcRouteOutputReference",
    "AppmeshGatewayRouteSpecHttp2Route",
    "AppmeshGatewayRouteSpecHttp2RouteAction",
    "AppmeshGatewayRouteSpecHttp2RouteActionOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewrite",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostnameOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewriteOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix",
    "AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefixOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteActionTarget",
    "AppmeshGatewayRouteSpecHttp2RouteActionTargetOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService",
    "AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualServiceOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteMatch",
    "AppmeshGatewayRouteSpecHttp2RouteMatchHostname",
    "AppmeshGatewayRouteSpecHttp2RouteMatchHostnameOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteMatchOutputReference",
    "AppmeshGatewayRouteSpecHttp2RouteOutputReference",
    "AppmeshGatewayRouteSpecHttpRoute",
    "AppmeshGatewayRouteSpecHttpRouteAction",
    "AppmeshGatewayRouteSpecHttpRouteActionOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteActionRewrite",
    "AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname",
    "AppmeshGatewayRouteSpecHttpRouteActionRewriteHostnameOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteActionRewriteOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix",
    "AppmeshGatewayRouteSpecHttpRouteActionRewritePrefixOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteActionTarget",
    "AppmeshGatewayRouteSpecHttpRouteActionTargetOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService",
    "AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualServiceOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteMatch",
    "AppmeshGatewayRouteSpecHttpRouteMatchHostname",
    "AppmeshGatewayRouteSpecHttpRouteMatchHostnameOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteMatchOutputReference",
    "AppmeshGatewayRouteSpecHttpRouteOutputReference",
    "AppmeshGatewayRouteSpecOutputReference",
]

publication.publish()

def _typecheckingstub__a777c4143d9c31b71bf8d30f600e1429287b5585f484125e84cacfbb33a4dc92(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    mesh_name: builtins.str,
    name: builtins.str,
    spec: typing.Union[AppmeshGatewayRouteSpec, typing.Dict[builtins.str, typing.Any]],
    virtual_gateway_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98bdbb0720e3b7095e9839f18362dffa2ca4dff5625b87c522a95057c7fb4c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb5ef135ee5c1b84267d88df0bea00286cbfca4c7568c8efacb5f652e045e59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4601d2e31650d20464f2cbc80634581522cea091b218b21cffad4e3a442461f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3128855aa817b54a71f80d39ad791c9f49110ce40d88e0531379d8a3770a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c621a6b5c8280b0dc9e46ba0ef337be6aa6d9d3673c8e2e1fd5f40e84fd91120(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ec4445abc0599b565ca59ff59eed1ca87efa25c810b70bffefe81643f3e24a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1290e080ec4c464cd4486fd231258fbbf0f8eb55f14dc1db475392986b0f29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f66556134b08211f9bda7a3437147ccfaaaae1069bb1fd20f422601b2f37e3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mesh_name: builtins.str,
    name: builtins.str,
    spec: typing.Union[AppmeshGatewayRouteSpec, typing.Dict[builtins.str, typing.Any]],
    virtual_gateway_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    mesh_owner: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7940c8016870085d0d985d73d4043b0aa55e756d1c2bb991654f8018da2db3c9(
    *,
    grpc_route: typing.Optional[typing.Union[AppmeshGatewayRouteSpecGrpcRoute, typing.Dict[builtins.str, typing.Any]]] = None,
    http2_route: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2Route, typing.Dict[builtins.str, typing.Any]]] = None,
    http_route: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRoute, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537a881568bb73c24d65c3b086a38b98a82a4c5e2f8daab4f6d6f09959faafb9(
    *,
    action: typing.Union[AppmeshGatewayRouteSpecGrpcRouteAction, typing.Dict[builtins.str, typing.Any]],
    match: typing.Union[AppmeshGatewayRouteSpecGrpcRouteMatch, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5545abfede7bba722e5caf060bf23b5112f04dc87ea6d5323538f5c66b95742b(
    *,
    target: typing.Union[AppmeshGatewayRouteSpecGrpcRouteActionTarget, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d1e5ea2cb72092800cd1598594c08104853ce9346ad40dae73eb8a118efbc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fa4815bc94dcd858a072a489f7627cb722fc5cf43b95c763786987d0bdfe6e(
    value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b65d6b2070220cbe91af21d9de7f7e040e47ea6b7589d82fa9dfd077a0306ae8(
    *,
    virtual_service: typing.Union[AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22fd2a108c1b1c2a45923f6c3bc7ca69ebb9021b1f47872b97a83169bd001922(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a220525822b09fbfbb20b4a68dfcd63d54dae1782313012c744f76a7d13f73c7(
    value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb63ce84aae52475febf1a0caab518396dbe45d706a35624f0979baf955e41ff(
    *,
    virtual_service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb8053f72bc27e1096b4cfaa03a84b8b36d2e2114cc5785ab508324113ff044(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740d4c744bd8e9fe4f2985f91759068065b2dcae2b87270283091c82d64781dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41afca36a44605e202261c8fcd5aacd07819bb405ea06474a1e22ad33b8beea(
    value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteActionTargetVirtualService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d96db30d4321e8cac5b5f7bf6ca798ad83b6e1f9b9c93722e25eb1017e52d0(
    *,
    service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61463ab138bf588c898b874bbf0db343225aca7015ac657064831ef1431d612c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32d14cf24d59f9d00a51859b1e0aad5724f84f4f650e0469bce5ac5c4669ab1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda5acd96495b926e84f2baae12ee0898893472c9b5d879230fa1180f29b03e7(
    value: typing.Optional[AppmeshGatewayRouteSpecGrpcRouteMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c073a42927749e82f3406eb3ba561dc2f508296e8b210b5f6eabfc65f5487c17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e675848a9b68c3d9b4377795ff1c9fbd85c32ec6658c2dff8fb308e814551ec(
    value: typing.Optional[AppmeshGatewayRouteSpecGrpcRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a78bf62a9ffaaa26ce4b8664e86c2427e373d50a51c3358e73492ed252909c(
    *,
    action: typing.Union[AppmeshGatewayRouteSpecHttp2RouteAction, typing.Dict[builtins.str, typing.Any]],
    match: typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatch, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8215426fd7a4f9429108ec9959beb16ab2b93114a43af98314b61fbebc1a9f(
    *,
    target: typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionTarget, typing.Dict[builtins.str, typing.Any]],
    rewrite: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2cb5bc5f908d642b65f770cbb2e0605c10f599fc38790bcea1485dd5183efe8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af94131d6917ccaf2f0a12aa6aec538f2dc02f679c8cfd4145d84797fb6b6326(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fca5e5a2d477c7e101ffe1823d2d45c61463a4d6b8eb2b83e2f0c235425efcf(
    *,
    hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf9e1a744ccd05fdd3d39b3cc85ce7d6c6f143271dc52879341b1e97c1e946b(
    *,
    default_target_hostname: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c332936968fa658e89449dfa16f1ba5496590bcc46dcbc3f0da00804ad5b60b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93ff791bef72c82eaf65b815fe8a6d7e57d5f487e3104608908b5e676e3333f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd909203a87e2e1ab56a0eeec7df5e01eaacfd22d65f8e868bf42c8bdbb3c6b(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewriteHostname],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae51b6ed8e7eb8372830137761662751f2aedf558f15c0cb7c4f0dd6b42e7769(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05934dd34dbdc705004503a12a1d9fc26af7a255c343e2dafb496a88a2a90cf1(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewrite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b944f8f4337901e916017185cc4e68ee6b82f79e845fd1d82a8a841e0173865(
    *,
    default_prefix: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367f84d9ac1d8a4f69daffc7e66061cb9945a7526035ff9276a34a422fb7a61a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4c71f16ff7c62abca1cb60c5711613fc5d64e5aee3a7a67315f0ea950d347f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0459b3c829270bc3e07edf5de731629a9417b0d32fd87ec10b8e8d931c246bec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f541e9fa78fa39677d4536b13458f000f63e476f620e747bc2187580175e26(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionRewritePrefix],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9596797cbc1b38916c99c36ddd07536f3930a7071e2336d88a8ed3c0d7c511(
    *,
    virtual_service: typing.Union[AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002c6b9f52375405b54989d4c85a18e684b733870458da717484b95220937db5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e16b736fa7301c53d1d7f169fc59f24f03d37b7793f4418067f157443538de(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5114646cd76daf1b4ac291dea8fd7ade5b52cf612cf9af13b7b275fe5965a17(
    *,
    virtual_service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca1c5058e640f756a526937412e8f476fa6e0e04ed0f8b59d8e89f60aaf5205(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e328abaad64fc02acf63c6fccdb42233da3881d3d6e0e8c4c4be4db21d1db7d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db71933bd644c7152207a3d012fae1bfdf6cb41a6675bf4b716c673e5718bb0f(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteActionTargetVirtualService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f995d0139eebf348730c4d1b1636c383c683cccd5a586789b4ab2a8d8dd877a3(
    *,
    hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttp2RouteMatchHostname, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da8d99cc4439d2501492455dbc188f1318b1b0f5256c7707e8f18f41579d4b4(
    *,
    exact: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16efbf8d6d250979ffb0c756215a4fdda56e578c377a31351cfd5042f6f97535(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f67e8b75acae70c2473527120858db3f0b3fa125a3b392200908c0b8c2c8a0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a102594ae3a5d9326ad549a4bee6dc15d243bc347fc242a2f47b8f44e7698212(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f3fced859d8f1ba5ac344fed30e942e203426451153ae8bc31324e7fa07070(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatchHostname],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f3d530504187a62c902507bd39da9497dcba4ccfe00abdfb640e92eb103a74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06614002b103ca086417a475d61843e07b453629f87440f487234b6451c474e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a1e59ebd546bbc102df39cdb2aed6bd84ff74aa927367619f6e5b62f41ccff(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2RouteMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db2fb7756fc065ec3e9257fb0d8779f98fb7b6da6da7575e6afc1ceaacfecee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe08a7e67eb4650a93600073e25208530b7c1fd1f13db156fb17bca851a79f58(
    value: typing.Optional[AppmeshGatewayRouteSpecHttp2Route],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eddf4d72dd6db89ab77ae46ef31b870a9c3bc5503a8ee0c1a606354a560cf22(
    *,
    action: typing.Union[AppmeshGatewayRouteSpecHttpRouteAction, typing.Dict[builtins.str, typing.Any]],
    match: typing.Union[AppmeshGatewayRouteSpecHttpRouteMatch, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3ceb719f6fd1c5696386fc28aa53aa84f1d378397427926cfc797084e55a6f(
    *,
    target: typing.Union[AppmeshGatewayRouteSpecHttpRouteActionTarget, typing.Dict[builtins.str, typing.Any]],
    rewrite: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteActionRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__addb7c2d8cbd83fe5822409cb7f1ff7e43c3397febf87416b6d6eb75921132e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187d20ce260d53c6906d1aed58f45d0f14d16ababb7d99084ed7c02d3acf1866(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7a52aa98cdbfd320bcd19dd5424708b1f37202ef53c8e6fd872fac5b9c84d8(
    *,
    hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048c6ffd4a3d57c6ae9de2310274073e8fc9e0dff787ddf5aad4a8a99208afaf(
    *,
    default_target_hostname: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0a8ccbe672e9dc4016eec082dc1dc46debec52cbbaab756d33439869785c7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659fad1ae18ceaedcfe0c546eb080b53bd9b3f41147ea0b794795897a58472e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f63ea20dd31d6aad78b7302e3d5623c2c1a587b1704781a7a69846d37fe62b(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewriteHostname],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f76708ce6bd3ad3416ea6decad9c515e50b30cb16d23c959fe37d6a29bd241(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b871c4a8ca562225b1a639b8369842d22a993044d832d650f0a92bb27adb35e(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewrite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70926ac39fb20d9f6ede0459ee24f540873e26a9a73986543033c5778e155413(
    *,
    default_prefix: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fa0051d97694d280f46ec4ac6d593a8f6f49abc0dd863dbeabca9dbd480c47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079001d5a07829272ed8d94776e70d2b9154e04568a9b52898d207abf084d079(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81237ea077e54f01940f1e817dfb25729e68c7653a572c717f76872a7a78e2e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c92b5ffa40b20d27ffd45514fdce73c8d9d6661addea4d3d9fc3e8bc4ce757c(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionRewritePrefix],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0671c61558ec8df4536354483c46017c0789a9aed147b82f817a5860159875c5(
    *,
    virtual_service: typing.Union[AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053be28363b55811b3e5fb30dc96915c54865e5c547652e7512b0fa9cde0fe21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314f53af1abc2e47099069cdcf1acf5d19ceac7ff47c7c128db54602ad9f29d9(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c709d6d322c9276447646bd0a265dc9c9c2e23943cdf87415bc4c05c06847a(
    *,
    virtual_service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3baa2c0d75308e803ec5d880ddca3a5829d0fc573a9c2417432348bdd4301fc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cf747cdead6c825c3187f1d0d0572bfc8ce148c145f48156aa4edc33934d4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f8236f15e9a1fd4cb8d654b09bbdf6d5c9234748aa578a84249b41e1bb5b45(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteActionTargetVirtualService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7e1c3bc4db19d440b59d7940440310eb714201548d62234aa3d784c8ba37a8(
    *,
    hostname: typing.Optional[typing.Union[AppmeshGatewayRouteSpecHttpRouteMatchHostname, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d41646d880450216f963307cc63a096aabf8442775f16ea0c1e185076ba076(
    *,
    exact: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844fb35c4bdb1623cc8ce94d4c2f66a44fd1cd50a6e4efb99f8a98ded1657b78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d47b2689690c5182e87326d8b6dd7b0f8f9d1087fd24e2147e17c7095366773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9a5fc6389f17a9d1d751176d3b808be3c0ecc8ac3cccf1c381816175ee7481(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1070aed85b33b35f540ca9d2aafe0856cbd27342228e22c6d91de688ecffce(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatchHostname],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45162d619709986c97890b6a623bf3bb50021db10787fdcbff1a380e55cdb9a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418996476b02022c89b36289c6266bf5392b41ccc27dfdec935e2589549196c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f60eb76d4b9667265239962116a28ea74be86171c5c85be83115f44791351b(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRouteMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d690ab4168ad26c84f24d8f01375a517d7e77d3bf1e9102e4fec8971f54c7f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efeeb7078bc6c298c26f7d1d7f5daada1ef99e2e1e9fa3f5d70e46b207f7e38e(
    value: typing.Optional[AppmeshGatewayRouteSpecHttpRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae17c973e9300e571fadad415debd9b61500610da414fa7ee79143e68013326e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efd07e505ee9cc1d486a89b5a69fa5df9a1d49d9918dcacab36ed5c96f98ceb(
    value: typing.Optional[AppmeshGatewayRouteSpec],
) -> None:
    """Type checking stubs"""
    pass
