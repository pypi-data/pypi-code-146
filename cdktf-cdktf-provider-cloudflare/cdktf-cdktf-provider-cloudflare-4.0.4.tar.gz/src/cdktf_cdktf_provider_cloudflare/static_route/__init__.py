'''
# `cloudflare_static_route`

Refer to the Terraform Registory for docs: [`cloudflare_static_route`](https://www.terraform.io/docs/providers/cloudflare/r/static_route).
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


class StaticRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.staticRoute.StaticRoute",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route cloudflare_static_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        nexthop: builtins.str,
        prefix: builtins.str,
        priority: jsii.Number,
        account_id: typing.Optional[builtins.str] = None,
        colo_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        colo_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route cloudflare_static_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param nexthop: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#nexthop StaticRoute#nexthop}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#prefix StaticRoute#prefix}.
        :param priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#priority StaticRoute#priority}.
        :param account_id: The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#account_id StaticRoute#account_id}
        :param colo_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#colo_names StaticRoute#colo_names}.
        :param colo_regions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#colo_regions StaticRoute#colo_regions}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#description StaticRoute#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#id StaticRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param weight: **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#weight StaticRoute#weight}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8916fd93ac51b87081f6b56f284ef57533ee998106b846e9dec161f2124c32a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StaticRouteConfig(
            nexthop=nexthop,
            prefix=prefix,
            priority=priority,
            account_id=account_id,
            colo_names=colo_names,
            colo_regions=colo_regions,
            description=description,
            id=id,
            weight=weight,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetColoNames")
    def reset_colo_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColoNames", []))

    @jsii.member(jsii_name="resetColoRegions")
    def reset_colo_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColoRegions", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="coloNamesInput")
    def colo_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "coloNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="coloRegionsInput")
    def colo_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "coloRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nexthopInput")
    def nexthop_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nexthopInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ce5ef322d3f2d1e9ae463ab75f91b78629c8f8fceed3d4415bd555b4de603e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="coloNames")
    def colo_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "coloNames"))

    @colo_names.setter
    def colo_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b764a1507e9b9bd79ea7296f0c4d400ac97cd83c385365c652369144d0d23de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coloNames", value)

    @builtins.property
    @jsii.member(jsii_name="coloRegions")
    def colo_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "coloRegions"))

    @colo_regions.setter
    def colo_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b320f665cc124ee81607531238ba4f66a2e9ee475320ee5d906a0f682e2ae6d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coloRegions", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78684f03f8531594932272f1ff0455c5041defd6b44dbf60d3754a035f555879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf861f3ea4552c36b01e4a1513105825e9939337fd65302ad3de45229835171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="nexthop")
    def nexthop(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nexthop"))

    @nexthop.setter
    def nexthop(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33093248b340b68ce9eb4f0e058cdb4c448c15a074efb70fe9ce5c2baad5b291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nexthop", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487a135b41f1703a9d66d4a02aff915a8834db9694a77a23f00c37384df04b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53d10c6a0f59b46603502fb416e923dc5b5f2202471a6fb7ab4094f461c3505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f09356fd4c46b9f2cd90d441ef2d8b4ee39c7b7028d2e37d4f1fb3f9b162fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.staticRoute.StaticRouteConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "nexthop": "nexthop",
        "prefix": "prefix",
        "priority": "priority",
        "account_id": "accountId",
        "colo_names": "coloNames",
        "colo_regions": "coloRegions",
        "description": "description",
        "id": "id",
        "weight": "weight",
    },
)
class StaticRouteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        nexthop: builtins.str,
        prefix: builtins.str,
        priority: jsii.Number,
        account_id: typing.Optional[builtins.str] = None,
        colo_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        colo_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param nexthop: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#nexthop StaticRoute#nexthop}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#prefix StaticRoute#prefix}.
        :param priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#priority StaticRoute#priority}.
        :param account_id: The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#account_id StaticRoute#account_id}
        :param colo_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#colo_names StaticRoute#colo_names}.
        :param colo_regions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#colo_regions StaticRoute#colo_regions}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#description StaticRoute#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#id StaticRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param weight: **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#weight StaticRoute#weight}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f80089b7aa99b4ea3bb1527189c02479fdf1648889c211d9a1414c45515ee56)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument nexthop", value=nexthop, expected_type=type_hints["nexthop"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument colo_names", value=colo_names, expected_type=type_hints["colo_names"])
            check_type(argname="argument colo_regions", value=colo_regions, expected_type=type_hints["colo_regions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "nexthop": nexthop,
            "prefix": prefix,
            "priority": priority,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if colo_names is not None:
            self._values["colo_names"] = colo_names
        if colo_regions is not None:
            self._values["colo_regions"] = colo_regions
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if weight is not None:
            self._values["weight"] = weight

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
    def nexthop(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#nexthop StaticRoute#nexthop}.'''
        result = self._values.get("nexthop")
        assert result is not None, "Required property 'nexthop' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#prefix StaticRoute#prefix}.'''
        result = self._values.get("prefix")
        assert result is not None, "Required property 'prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#priority StaticRoute#priority}.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#account_id StaticRoute#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def colo_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#colo_names StaticRoute#colo_names}.'''
        result = self._values.get("colo_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def colo_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#colo_regions StaticRoute#colo_regions}.'''
        result = self._values.get("colo_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#description StaticRoute#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#id StaticRoute#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''**Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/static_route#weight StaticRoute#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StaticRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "StaticRoute",
    "StaticRouteConfig",
]

publication.publish()

def _typecheckingstub__8916fd93ac51b87081f6b56f284ef57533ee998106b846e9dec161f2124c32a7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    nexthop: builtins.str,
    prefix: builtins.str,
    priority: jsii.Number,
    account_id: typing.Optional[builtins.str] = None,
    colo_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    colo_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__58ce5ef322d3f2d1e9ae463ab75f91b78629c8f8fceed3d4415bd555b4de603e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b764a1507e9b9bd79ea7296f0c4d400ac97cd83c385365c652369144d0d23de6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b320f665cc124ee81607531238ba4f66a2e9ee475320ee5d906a0f682e2ae6d8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78684f03f8531594932272f1ff0455c5041defd6b44dbf60d3754a035f555879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf861f3ea4552c36b01e4a1513105825e9939337fd65302ad3de45229835171(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33093248b340b68ce9eb4f0e058cdb4c448c15a074efb70fe9ce5c2baad5b291(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487a135b41f1703a9d66d4a02aff915a8834db9694a77a23f00c37384df04b11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53d10c6a0f59b46603502fb416e923dc5b5f2202471a6fb7ab4094f461c3505(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f09356fd4c46b9f2cd90d441ef2d8b4ee39c7b7028d2e37d4f1fb3f9b162fd0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f80089b7aa99b4ea3bb1527189c02479fdf1648889c211d9a1414c45515ee56(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    nexthop: builtins.str,
    prefix: builtins.str,
    priority: jsii.Number,
    account_id: typing.Optional[builtins.str] = None,
    colo_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    colo_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
