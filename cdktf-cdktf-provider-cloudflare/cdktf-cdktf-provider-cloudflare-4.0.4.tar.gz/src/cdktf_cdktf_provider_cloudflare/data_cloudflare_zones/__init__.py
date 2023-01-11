'''
# `data_cloudflare_zones`

Refer to the Terraform Registory for docs: [`data_cloudflare_zones`](https://www.terraform.io/docs/providers/cloudflare/d/zones).
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


class DataCloudflareZones(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZones.DataCloudflareZones",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/d/zones cloudflare_zones}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter: typing.Union["DataCloudflareZonesFilter", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/d/zones cloudflare_zones} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#filter DataCloudflareZones#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#id DataCloudflareZones#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b98280ad9922459ce47702bddcfd30cbc14a5225b6592e1875170959031620)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataCloudflareZonesConfig(
            filter=filter,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        lookup_type: typing.Optional[builtins.str] = None,
        match: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#account_id DataCloudflareZones#account_id}
        :param lookup_type: Defaults to ``exact``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#lookup_type DataCloudflareZones#lookup_type}
        :param match: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#match DataCloudflareZones#match}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#name DataCloudflareZones#name}.
        :param paused: Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#paused DataCloudflareZones#paused}
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#status DataCloudflareZones#status}.
        '''
        value = DataCloudflareZonesFilter(
            account_id=account_id,
            lookup_type=lookup_type,
            match=match,
            name=name,
            paused=paused,
            status=status,
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "DataCloudflareZonesFilterOutputReference":
        return typing.cast("DataCloudflareZonesFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> "DataCloudflareZonesZonesList":
        return typing.cast("DataCloudflareZonesZonesList", jsii.get(self, "zones"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional["DataCloudflareZonesFilter"]:
        return typing.cast(typing.Optional["DataCloudflareZonesFilter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ffc70f1f98cee10ff7b76f5fbbd1b51d40109c96b3c51abe78a1a8a2ab1a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZones.DataCloudflareZonesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "filter": "filter",
        "id": "id",
    },
)
class DataCloudflareZonesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filter: typing.Union["DataCloudflareZonesFilter", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#filter DataCloudflareZones#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#id DataCloudflareZones#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = DataCloudflareZonesFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__955d281bd63bff22a6c3d2a0f9b97fc6f525538c9a973b3f3c3d9d845e45ef49)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
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
    def filter(self) -> "DataCloudflareZonesFilter":
        '''filter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#filter DataCloudflareZones#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast("DataCloudflareZonesFilter", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#id DataCloudflareZones#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareZonesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZones.DataCloudflareZonesFilter",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "lookup_type": "lookupType",
        "match": "match",
        "name": "name",
        "paused": "paused",
        "status": "status",
    },
)
class DataCloudflareZonesFilter:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        lookup_type: typing.Optional[builtins.str] = None,
        match: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#account_id DataCloudflareZones#account_id}
        :param lookup_type: Defaults to ``exact``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#lookup_type DataCloudflareZones#lookup_type}
        :param match: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#match DataCloudflareZones#match}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#name DataCloudflareZones#name}.
        :param paused: Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#paused DataCloudflareZones#paused}
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#status DataCloudflareZones#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5589aade97b4d007207542f6c203280cb2da4d6bcb14561849e2fe01367bb95)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument lookup_type", value=lookup_type, expected_type=type_hints["lookup_type"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument paused", value=paused, expected_type=type_hints["paused"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if lookup_type is not None:
            self._values["lookup_type"] = lookup_type
        if match is not None:
            self._values["match"] = match
        if name is not None:
            self._values["name"] = name
        if paused is not None:
            self._values["paused"] = paused
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#account_id DataCloudflareZones#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lookup_type(self) -> typing.Optional[builtins.str]:
        '''Defaults to ``exact``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#lookup_type DataCloudflareZones#lookup_type}
        '''
        result = self._values.get("lookup_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#match DataCloudflareZones#match}.'''
        result = self._values.get("match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#name DataCloudflareZones#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#paused DataCloudflareZones#paused}
        '''
        result = self._values.get("paused")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/zones#status DataCloudflareZones#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareZonesFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareZonesFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZones.DataCloudflareZonesFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52fd4588f1cd022f5cc40a32ecdcdd552b36eaccb546ec7734d3bfd2f517e944)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetLookupType")
    def reset_lookup_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLookupType", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPaused")
    def reset_paused(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaused", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="lookupTypeInput")
    def lookup_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lookupTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pausedInput")
    def paused_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pausedInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1bfb8ce0c3efb0baf52b96c6a720af37a2968764962d0c465cd79e3a8fe6d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="lookupType")
    def lookup_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lookupType"))

    @lookup_type.setter
    def lookup_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b11554f467e2d6553ebbb8e90516b7674ec02d9619f7634decabc2e6ba68799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lookupType", value)

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "match"))

    @match.setter
    def match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__266b71aa4c0d58c62a0c0f768819eca7bca17f3c392ee4edb762970f12a1e9f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "match", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef9e71ac237abe812db2d30d56c9177de19fe893102b7f6e919a7cabc9426c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="paused")
    def paused(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "paused"))

    @paused.setter
    def paused(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77768b55e5ead91c7dd53c8a8b74e1c322cec32ebdf1f0b8b70f03741ebae27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paused", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5555a55f76d976484fb9243f22937d3ee9d8d1e60c5e984f366cf0b4325eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataCloudflareZonesFilter]:
        return typing.cast(typing.Optional[DataCloudflareZonesFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataCloudflareZonesFilter]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051dec5c8b6eca70cfe1c912915e30d2105c384bcdbf51381c60941a290fb571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZones.DataCloudflareZonesZones",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCloudflareZonesZones:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareZonesZones(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareZonesZonesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZones.DataCloudflareZonesZonesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eaf4cb32bebba49437baf358b8ae3cd18ad630cb825447cec40d8f37c802716)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataCloudflareZonesZonesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11cbef37d0358a534e6369eee33eee9c04e37009d84955a5f75e62198b8cf24a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCloudflareZonesZonesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c5a229d74c3644efc9321b541071e377f37c1a741a33d7cdf1c44012d8f426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ba863a476070dad26fbb001eb98ac417e5b1065dc4f252dc4894202c7af0eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84330b97625d666c3a3cff40de35d9159d70587c04ae6d62bdab71e72b88530d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataCloudflareZonesZonesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZones.DataCloudflareZonesZonesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d229b7e24a571267990fead007d6a89ac8a936d54158018ab6563f3295186c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataCloudflareZonesZones]:
        return typing.cast(typing.Optional[DataCloudflareZonesZones], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataCloudflareZonesZones]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d3b0a4118154405036fa6b4d0966ec0ee5cbf409f6ab6ecf82642e9d284a4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataCloudflareZones",
    "DataCloudflareZonesConfig",
    "DataCloudflareZonesFilter",
    "DataCloudflareZonesFilterOutputReference",
    "DataCloudflareZonesZones",
    "DataCloudflareZonesZonesList",
    "DataCloudflareZonesZonesOutputReference",
]

publication.publish()

def _typecheckingstub__10b98280ad9922459ce47702bddcfd30cbc14a5225b6592e1875170959031620(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter: typing.Union[DataCloudflareZonesFilter, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__59ffc70f1f98cee10ff7b76f5fbbd1b51d40109c96b3c51abe78a1a8a2ab1a5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__955d281bd63bff22a6c3d2a0f9b97fc6f525538c9a973b3f3c3d9d845e45ef49(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter: typing.Union[DataCloudflareZonesFilter, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5589aade97b4d007207542f6c203280cb2da4d6bcb14561849e2fe01367bb95(
    *,
    account_id: typing.Optional[builtins.str] = None,
    lookup_type: typing.Optional[builtins.str] = None,
    match: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fd4588f1cd022f5cc40a32ecdcdd552b36eaccb546ec7734d3bfd2f517e944(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1bfb8ce0c3efb0baf52b96c6a720af37a2968764962d0c465cd79e3a8fe6d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b11554f467e2d6553ebbb8e90516b7674ec02d9619f7634decabc2e6ba68799(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266b71aa4c0d58c62a0c0f768819eca7bca17f3c392ee4edb762970f12a1e9f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef9e71ac237abe812db2d30d56c9177de19fe893102b7f6e919a7cabc9426c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77768b55e5ead91c7dd53c8a8b74e1c322cec32ebdf1f0b8b70f03741ebae27(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5555a55f76d976484fb9243f22937d3ee9d8d1e60c5e984f366cf0b4325eca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051dec5c8b6eca70cfe1c912915e30d2105c384bcdbf51381c60941a290fb571(
    value: typing.Optional[DataCloudflareZonesFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eaf4cb32bebba49437baf358b8ae3cd18ad630cb825447cec40d8f37c802716(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11cbef37d0358a534e6369eee33eee9c04e37009d84955a5f75e62198b8cf24a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c5a229d74c3644efc9321b541071e377f37c1a741a33d7cdf1c44012d8f426(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ba863a476070dad26fbb001eb98ac417e5b1065dc4f252dc4894202c7af0eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84330b97625d666c3a3cff40de35d9159d70587c04ae6d62bdab71e72b88530d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d229b7e24a571267990fead007d6a89ac8a936d54158018ab6563f3295186c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d3b0a4118154405036fa6b4d0966ec0ee5cbf409f6ab6ecf82642e9d284a4b(
    value: typing.Optional[DataCloudflareZonesZones],
) -> None:
    """Type checking stubs"""
    pass
