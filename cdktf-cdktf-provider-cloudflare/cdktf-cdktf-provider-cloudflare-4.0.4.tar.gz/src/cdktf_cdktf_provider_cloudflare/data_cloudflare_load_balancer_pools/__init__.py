'''
# `data_cloudflare_load_balancer_pools`

Refer to the Terraform Registory for docs: [`data_cloudflare_load_balancer_pools`](https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools).
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


class DataCloudflareLoadBalancerPools(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPools",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools cloudflare_load_balancer_pools}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        filter: typing.Optional[typing.Union["DataCloudflareLoadBalancerPoolsFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataCloudflareLoadBalancerPoolsPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools cloudflare_load_balancer_pools} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the datasource lookups. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#account_id DataCloudflareLoadBalancerPools#account_id}
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#filter DataCloudflareLoadBalancerPools#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#id DataCloudflareLoadBalancerPools#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pools: pools block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#pools DataCloudflareLoadBalancerPools#pools}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a543d8ecf8da82de879416c65e1cb816dc56d3f49c397d82bd536ca25400de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataCloudflareLoadBalancerPoolsConfig(
            account_id=account_id,
            filter=filter,
            id=id,
            pools=pools,
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
    def put_filter(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: A regular expression matching the name of the Load Balancer pool to lookup. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#name DataCloudflareLoadBalancerPools#name}
        '''
        value = DataCloudflareLoadBalancerPoolsFilter(name=name)

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putPools")
    def put_pools(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataCloudflareLoadBalancerPoolsPools", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41401766cec23e0ab3804b7079df3cadeaf0cb181b523f2f67d78f1e9b691809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPools", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPools")
    def reset_pools(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPools", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "DataCloudflareLoadBalancerPoolsFilterOutputReference":
        return typing.cast("DataCloudflareLoadBalancerPoolsFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="pools")
    def pools(self) -> "DataCloudflareLoadBalancerPoolsPoolsList":
        return typing.cast("DataCloudflareLoadBalancerPoolsPoolsList", jsii.get(self, "pools"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional["DataCloudflareLoadBalancerPoolsFilter"]:
        return typing.cast(typing.Optional["DataCloudflareLoadBalancerPoolsFilter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="poolsInput")
    def pools_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataCloudflareLoadBalancerPoolsPools"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataCloudflareLoadBalancerPoolsPools"]]], jsii.get(self, "poolsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c675443ea26cd1ab4448e32495942369683982de65f862294928febd63faf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2b454a0eb8694046923603a1451ef3371325d1b224ac7d5e73327257cff809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_id": "accountId",
        "filter": "filter",
        "id": "id",
        "pools": "pools",
    },
)
class DataCloudflareLoadBalancerPoolsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_id: builtins.str,
        filter: typing.Optional[typing.Union["DataCloudflareLoadBalancerPoolsFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataCloudflareLoadBalancerPoolsPools", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the datasource lookups. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#account_id DataCloudflareLoadBalancerPools#account_id}
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#filter DataCloudflareLoadBalancerPools#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#id DataCloudflareLoadBalancerPools#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pools: pools block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#pools DataCloudflareLoadBalancerPools#pools}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = DataCloudflareLoadBalancerPoolsFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12311f51bc6c3f75dd49ad8e4e6082df4a2c03b72c6ede80fb38a80ac3762bb1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pools", value=pools, expected_type=type_hints["pools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
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
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
        if pools is not None:
            self._values["pools"] = pools

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
    def account_id(self) -> builtins.str:
        '''The account identifier to target for the datasource lookups.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#account_id DataCloudflareLoadBalancerPools#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> typing.Optional["DataCloudflareLoadBalancerPoolsFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#filter DataCloudflareLoadBalancerPools#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["DataCloudflareLoadBalancerPoolsFilter"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#id DataCloudflareLoadBalancerPools#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pools(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataCloudflareLoadBalancerPoolsPools"]]]:
        '''pools block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#pools DataCloudflareLoadBalancerPools#pools}
        '''
        result = self._values.get("pools")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataCloudflareLoadBalancerPoolsPools"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareLoadBalancerPoolsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsFilter",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DataCloudflareLoadBalancerPoolsFilter:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: A regular expression matching the name of the Load Balancer pool to lookup. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#name DataCloudflareLoadBalancerPools#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca98f996aef79fdb906dbc608219e083ceeca5b550e6fbe8da7d745a984bbc70)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A regular expression matching the name of the Load Balancer pool to lookup.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/load_balancer_pools#name DataCloudflareLoadBalancerPools#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareLoadBalancerPoolsFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareLoadBalancerPoolsFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__417088007d1ad3848f581996534d7d98dce5dda4abddb9be9097fb07b36013b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a9e7f07ed0a25445fc9a284fac45b17bb64b0a788f005699b48c80b67d3d6b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataCloudflareLoadBalancerPoolsFilter]:
        return typing.cast(typing.Optional[DataCloudflareLoadBalancerPoolsFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCloudflareLoadBalancerPoolsFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49f372dcad70f2b9da5abe3cef6fe8581366a7d34298d7cef59776b40a9eb5f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPools",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCloudflareLoadBalancerPoolsPools:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareLoadBalancerPoolsPools(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareLoadBalancerPoolsPoolsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPoolsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9651b1808b35a2b8327461582a1b2556c073f45cdb293a0f40ff03636c156999)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCloudflareLoadBalancerPoolsPoolsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50fafbc62b9e1ed1c425eea7e83865a171c41410370537e258e6366137201f88)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCloudflareLoadBalancerPoolsPoolsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad765691c5ec51cc626c15fe765c40dceeed7bd4b1b3a7c5217165236cb42473)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cceed8509f8616034c627e6adbcf018abd390d4f868e8a9718ebf4ec27748071)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0164a27a90c3a837d947bfb2d401e14bada33b24cb31b580e41a87810b8e34e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCloudflareLoadBalancerPoolsPools]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCloudflareLoadBalancerPoolsPools]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCloudflareLoadBalancerPoolsPools]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f88f131a393ca7cf26292c9d248b34eea9f3a48ac7a06c15911222d4e749d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPoolsLoadShedding",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCloudflareLoadBalancerPoolsPoolsLoadShedding:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareLoadBalancerPoolsPoolsLoadShedding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareLoadBalancerPoolsPoolsLoadSheddingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPoolsLoadSheddingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b26f4c1c2386834cfaa795473a4d00e12bf9bb3c63f006b659b2155ec76dac9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCloudflareLoadBalancerPoolsPoolsLoadSheddingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__911e7e7d7d0bc4fc3b12d19e8b66d85e01d79e308242538befbd014d0f13231b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCloudflareLoadBalancerPoolsPoolsLoadSheddingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edcb46da47356b994ea15fd05ae4bb07febfdb65d1e02cf53d7e8244f98cd3f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1c1f114fca289fb61fc84e65a66bf5d71ad322bb05cc9d1d413fe7c9fe0ab64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b524a12996c9f1a57b28055fd2d580f766f5709c73ab6d173b4f9d2f85ba7e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataCloudflareLoadBalancerPoolsPoolsLoadSheddingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPoolsLoadSheddingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d87ee77bb17c7212404634380f68914655430d7cc86ba67504588f8933663168)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="defaultPercent")
    def default_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultPercent"))

    @builtins.property
    @jsii.member(jsii_name="defaultPolicy")
    def default_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPolicy"))

    @builtins.property
    @jsii.member(jsii_name="sessionPercent")
    def session_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionPercent"))

    @builtins.property
    @jsii.member(jsii_name="sessionPolicy")
    def session_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataCloudflareLoadBalancerPoolsPoolsLoadShedding]:
        return typing.cast(typing.Optional[DataCloudflareLoadBalancerPoolsPoolsLoadShedding], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCloudflareLoadBalancerPoolsPoolsLoadShedding],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ad18b4a56d8ae57fb915d6a4475102d698aef4413b612ded9203c3bcae953d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPoolsOrigins",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCloudflareLoadBalancerPoolsPoolsOrigins:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareLoadBalancerPoolsPoolsOrigins(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPoolsOriginsHeader",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCloudflareLoadBalancerPoolsPoolsOriginsHeader:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareLoadBalancerPoolsPoolsOriginsHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareLoadBalancerPoolsPoolsOriginsHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPoolsOriginsHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df4455b35885cf0d80488794a5c014cc37d3bd620f4bf5b67668b7c83d5a347e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCloudflareLoadBalancerPoolsPoolsOriginsHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7cbfd48758f3e9e4b0e8a108d8a8cc554349d2cca9413e78aa28aeab7ea335)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCloudflareLoadBalancerPoolsPoolsOriginsHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1c37b50c405501aa10a5953c51ce0c1e765d6d6ade0ff8952f4c924d70890a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de0e6b9cbe6765f0d00c7a178aebab82e68202d0af95577eefac2a9e22d258f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb0e932dc1e2072e731fbd5fe6750687d97df3349b273b9ce3784275b0b6ac0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataCloudflareLoadBalancerPoolsPoolsOriginsHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPoolsOriginsHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb45cf13f991e8120b19b9e309a898c94eaf659deab1a5d62209d2b3e91e4931)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataCloudflareLoadBalancerPoolsPoolsOriginsHeader]:
        return typing.cast(typing.Optional[DataCloudflareLoadBalancerPoolsPoolsOriginsHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCloudflareLoadBalancerPoolsPoolsOriginsHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f23b4a5cfd9c9eba6bdc524e8f1b666d0928c8e7e07b721142bca60f48f1d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataCloudflareLoadBalancerPoolsPoolsOriginsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPoolsOriginsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe39141163c9cd9c648b0793fbfc421d490c07c49a7e88fdf69b9cfe4468da3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCloudflareLoadBalancerPoolsPoolsOriginsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8730ca01d6dbdf6397cd42f06d237304565d4fa8361752a77065ae2c89c53bff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCloudflareLoadBalancerPoolsPoolsOriginsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9152b9900d55c61fa395c1ae7a51f3ca0de762a1f6ff3c1cf350d16b62cad768)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d57801b954bd89840146f0b6dfda248fb46c9d00fcb79a96038cbcb0cf69c4ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d334de5e41fdab65b7556a5b174f7f04b84e2428213b8a864bd4faca0e36469d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataCloudflareLoadBalancerPoolsPoolsOriginsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPoolsOriginsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f60f60739735e1037a18906748a3fbacd31705e5749270f0ccfe869c9c794c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> DataCloudflareLoadBalancerPoolsPoolsOriginsHeaderList:
        return typing.cast(DataCloudflareLoadBalancerPoolsPoolsOriginsHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataCloudflareLoadBalancerPoolsPoolsOrigins]:
        return typing.cast(typing.Optional[DataCloudflareLoadBalancerPoolsPoolsOrigins], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCloudflareLoadBalancerPoolsPoolsOrigins],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f541d0e81e831be53c0719a87fc8b2944ad9785e9d32fdf736af4150a1b18edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataCloudflareLoadBalancerPoolsPoolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareLoadBalancerPools.DataCloudflareLoadBalancerPoolsPoolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__038789b50be5206f78c332fc833873c1b8cc676d4e35a700fe882123c9b8979d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="checkRegions")
    def check_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "checkRegions"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="latitude")
    def latitude(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "latitude"))

    @builtins.property
    @jsii.member(jsii_name="loadShedding")
    def load_shedding(self) -> DataCloudflareLoadBalancerPoolsPoolsLoadSheddingList:
        return typing.cast(DataCloudflareLoadBalancerPoolsPoolsLoadSheddingList, jsii.get(self, "loadShedding"))

    @builtins.property
    @jsii.member(jsii_name="longitude")
    def longitude(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longitude"))

    @builtins.property
    @jsii.member(jsii_name="minimumOrigins")
    def minimum_origins(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumOrigins"))

    @builtins.property
    @jsii.member(jsii_name="modifiedOn")
    def modified_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedOn"))

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitor"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="notificationEmail")
    def notification_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationEmail"))

    @builtins.property
    @jsii.member(jsii_name="origins")
    def origins(self) -> DataCloudflareLoadBalancerPoolsPoolsOriginsList:
        return typing.cast(DataCloudflareLoadBalancerPoolsPoolsOriginsList, jsii.get(self, "origins"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataCloudflareLoadBalancerPoolsPools, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataCloudflareLoadBalancerPoolsPools, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataCloudflareLoadBalancerPoolsPools, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8efdcd574473f7995d3ee33ad772760dd6f0c6b118606c645b85f7ff65b5e765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataCloudflareLoadBalancerPools",
    "DataCloudflareLoadBalancerPoolsConfig",
    "DataCloudflareLoadBalancerPoolsFilter",
    "DataCloudflareLoadBalancerPoolsFilterOutputReference",
    "DataCloudflareLoadBalancerPoolsPools",
    "DataCloudflareLoadBalancerPoolsPoolsList",
    "DataCloudflareLoadBalancerPoolsPoolsLoadShedding",
    "DataCloudflareLoadBalancerPoolsPoolsLoadSheddingList",
    "DataCloudflareLoadBalancerPoolsPoolsLoadSheddingOutputReference",
    "DataCloudflareLoadBalancerPoolsPoolsOrigins",
    "DataCloudflareLoadBalancerPoolsPoolsOriginsHeader",
    "DataCloudflareLoadBalancerPoolsPoolsOriginsHeaderList",
    "DataCloudflareLoadBalancerPoolsPoolsOriginsHeaderOutputReference",
    "DataCloudflareLoadBalancerPoolsPoolsOriginsList",
    "DataCloudflareLoadBalancerPoolsPoolsOriginsOutputReference",
    "DataCloudflareLoadBalancerPoolsPoolsOutputReference",
]

publication.publish()

def _typecheckingstub__84a543d8ecf8da82de879416c65e1cb816dc56d3f49c397d82bd536ca25400de(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    filter: typing.Optional[typing.Union[DataCloudflareLoadBalancerPoolsFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataCloudflareLoadBalancerPoolsPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__41401766cec23e0ab3804b7079df3cadeaf0cb181b523f2f67d78f1e9b691809(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataCloudflareLoadBalancerPoolsPools, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c675443ea26cd1ab4448e32495942369683982de65f862294928febd63faf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2b454a0eb8694046923603a1451ef3371325d1b224ac7d5e73327257cff809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12311f51bc6c3f75dd49ad8e4e6082df4a2c03b72c6ede80fb38a80ac3762bb1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    filter: typing.Optional[typing.Union[DataCloudflareLoadBalancerPoolsFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    pools: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataCloudflareLoadBalancerPoolsPools, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca98f996aef79fdb906dbc608219e083ceeca5b550e6fbe8da7d745a984bbc70(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417088007d1ad3848f581996534d7d98dce5dda4abddb9be9097fb07b36013b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9e7f07ed0a25445fc9a284fac45b17bb64b0a788f005699b48c80b67d3d6b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f372dcad70f2b9da5abe3cef6fe8581366a7d34298d7cef59776b40a9eb5f4(
    value: typing.Optional[DataCloudflareLoadBalancerPoolsFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9651b1808b35a2b8327461582a1b2556c073f45cdb293a0f40ff03636c156999(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fafbc62b9e1ed1c425eea7e83865a171c41410370537e258e6366137201f88(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad765691c5ec51cc626c15fe765c40dceeed7bd4b1b3a7c5217165236cb42473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cceed8509f8616034c627e6adbcf018abd390d4f868e8a9718ebf4ec27748071(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0164a27a90c3a837d947bfb2d401e14bada33b24cb31b580e41a87810b8e34e3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f88f131a393ca7cf26292c9d248b34eea9f3a48ac7a06c15911222d4e749d8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCloudflareLoadBalancerPoolsPools]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26f4c1c2386834cfaa795473a4d00e12bf9bb3c63f006b659b2155ec76dac9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911e7e7d7d0bc4fc3b12d19e8b66d85e01d79e308242538befbd014d0f13231b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edcb46da47356b994ea15fd05ae4bb07febfdb65d1e02cf53d7e8244f98cd3f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c1f114fca289fb61fc84e65a66bf5d71ad322bb05cc9d1d413fe7c9fe0ab64(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b524a12996c9f1a57b28055fd2d580f766f5709c73ab6d173b4f9d2f85ba7e6b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87ee77bb17c7212404634380f68914655430d7cc86ba67504588f8933663168(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ad18b4a56d8ae57fb915d6a4475102d698aef4413b612ded9203c3bcae953d(
    value: typing.Optional[DataCloudflareLoadBalancerPoolsPoolsLoadShedding],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4455b35885cf0d80488794a5c014cc37d3bd620f4bf5b67668b7c83d5a347e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7cbfd48758f3e9e4b0e8a108d8a8cc554349d2cca9413e78aa28aeab7ea335(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1c37b50c405501aa10a5953c51ce0c1e765d6d6ade0ff8952f4c924d70890a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0e6b9cbe6765f0d00c7a178aebab82e68202d0af95577eefac2a9e22d258f0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0e932dc1e2072e731fbd5fe6750687d97df3349b273b9ce3784275b0b6ac0b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb45cf13f991e8120b19b9e309a898c94eaf659deab1a5d62209d2b3e91e4931(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f23b4a5cfd9c9eba6bdc524e8f1b666d0928c8e7e07b721142bca60f48f1d88(
    value: typing.Optional[DataCloudflareLoadBalancerPoolsPoolsOriginsHeader],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe39141163c9cd9c648b0793fbfc421d490c07c49a7e88fdf69b9cfe4468da3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8730ca01d6dbdf6397cd42f06d237304565d4fa8361752a77065ae2c89c53bff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9152b9900d55c61fa395c1ae7a51f3ca0de762a1f6ff3c1cf350d16b62cad768(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57801b954bd89840146f0b6dfda248fb46c9d00fcb79a96038cbcb0cf69c4ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d334de5e41fdab65b7556a5b174f7f04b84e2428213b8a864bd4faca0e36469d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f60f60739735e1037a18906748a3fbacd31705e5749270f0ccfe869c9c794c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f541d0e81e831be53c0719a87fc8b2944ad9785e9d32fdf736af4150a1b18edf(
    value: typing.Optional[DataCloudflareLoadBalancerPoolsPoolsOrigins],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038789b50be5206f78c332fc833873c1b8cc676d4e35a700fe882123c9b8979d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efdcd574473f7995d3ee33ad772760dd6f0c6b118606c645b85f7ff65b5e765(
    value: typing.Optional[typing.Union[DataCloudflareLoadBalancerPoolsPools, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
