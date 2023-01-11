'''
# `data_cloudflare_waf_rules`

Refer to the Terraform Registory for docs: [`data_cloudflare_waf_rules`](https://www.terraform.io/docs/providers/cloudflare/d/waf_rules).
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


class DataCloudflareWafRules(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafRules.DataCloudflareWafRules",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules cloudflare_waf_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        zone_id: builtins.str,
        filter: typing.Optional[typing.Union["DataCloudflareWafRulesFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        package_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules cloudflare_waf_rules} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param zone_id: The zone identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#zone_id DataCloudflareWafRules#zone_id}
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#filter DataCloudflareWafRules#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#id DataCloudflareWafRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param package_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#package_id DataCloudflareWafRules#package_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac79b29b214445656149fc240b6e29808749aaf4295e36e626371694c9445b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataCloudflareWafRulesConfig(
            zone_id=zone_id,
            filter=filter,
            id=id,
            package_id=package_id,
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
        description: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#description DataCloudflareWafRules#description}.
        :param group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#group_id DataCloudflareWafRules#group_id}.
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#mode DataCloudflareWafRules#mode}.
        '''
        value = DataCloudflareWafRulesFilter(
            description=description, group_id=group_id, mode=mode
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPackageId")
    def reset_package_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackageId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "DataCloudflareWafRulesFilterOutputReference":
        return typing.cast("DataCloudflareWafRulesFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "DataCloudflareWafRulesRulesList":
        return typing.cast("DataCloudflareWafRulesRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional["DataCloudflareWafRulesFilter"]:
        return typing.cast(typing.Optional["DataCloudflareWafRulesFilter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="packageIdInput")
    def package_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "packageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9837a9823f0be231113ec475db2d0d768a3d48b606b56ea890cc1d84fb9dbe9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="packageId")
    def package_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "packageId"))

    @package_id.setter
    def package_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5090245d5ba95c3143fabb24a9dd40757fb3a2ddee286b51595ffe57c15a09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageId", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68d35b0fa824ded9ae54fbbb40d8f4ed8570a4e1b06c37f1a69395c0483df4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafRules.DataCloudflareWafRulesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "zone_id": "zoneId",
        "filter": "filter",
        "id": "id",
        "package_id": "packageId",
    },
)
class DataCloudflareWafRulesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        zone_id: builtins.str,
        filter: typing.Optional[typing.Union["DataCloudflareWafRulesFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        package_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param zone_id: The zone identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#zone_id DataCloudflareWafRules#zone_id}
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#filter DataCloudflareWafRules#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#id DataCloudflareWafRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param package_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#package_id DataCloudflareWafRules#package_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = DataCloudflareWafRulesFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ddf9a8a8eb0e2f3f863d7195f3ff0e33f58bd9d1b1f0b0a33ccf4ce80eb87a0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument package_id", value=package_id, expected_type=type_hints["package_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "zone_id": zone_id,
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
        if package_id is not None:
            self._values["package_id"] = package_id

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
    def zone_id(self) -> builtins.str:
        '''The zone identifier to target for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#zone_id DataCloudflareWafRules#zone_id}
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> typing.Optional["DataCloudflareWafRulesFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#filter DataCloudflareWafRules#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["DataCloudflareWafRulesFilter"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#id DataCloudflareWafRules#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#package_id DataCloudflareWafRules#package_id}.'''
        result = self._values.get("package_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareWafRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafRules.DataCloudflareWafRulesFilter",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "group_id": "groupId", "mode": "mode"},
)
class DataCloudflareWafRulesFilter:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#description DataCloudflareWafRules#description}.
        :param group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#group_id DataCloudflareWafRules#group_id}.
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#mode DataCloudflareWafRules#mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afff99486928bc2bc21998503607c1524b5d16a6588484bc83dd93734681f461)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if group_id is not None:
            self._values["group_id"] = group_id
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#description DataCloudflareWafRules#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#group_id DataCloudflareWafRules#group_id}.'''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_rules#mode DataCloudflareWafRules#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareWafRulesFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareWafRulesFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafRules.DataCloudflareWafRulesFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4593d26c1fb6127cd6f659d92c9a1bdbd7335801203b2e04a8ab47a72d27978)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b662281aac0de3edbf4fc7be6528f7056f0e9b2ee7862a031fc19622ebc23319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dbd918b395b75d99340402c08ccf5a1fa3a30ae148328a7383e2899760d6369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e463e66a6338a2d1cc8445d3956ac385b4f93b0ca75644401b7bb65e7c1f708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataCloudflareWafRulesFilter]:
        return typing.cast(typing.Optional[DataCloudflareWafRulesFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCloudflareWafRulesFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9d1bb4be9af0e6878af194b217e98cd8359a8936de343792c1937bb7c03f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafRules.DataCloudflareWafRulesRules",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCloudflareWafRulesRules:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareWafRulesRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareWafRulesRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafRules.DataCloudflareWafRulesRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__243ec4369dbfc8e64415958e0a34c5775e819371f12c6b5d486ea5eea4a352f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataCloudflareWafRulesRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc460112beb2e687bbf59525c071caa5102178caca6133bc436c852a1306de3a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCloudflareWafRulesRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5304e1aeba8221c3e4cf2a7c3c80448df94ec641df80abebec29935d5f2e43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed40cfd4a81595237953d0c1d594462ed19f024d92cee97a2575e7065b7cbfe1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32bf32619ec2ca56db0947d6122e64d7381f0fbb16aca9f4be6c5cc612a2efaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataCloudflareWafRulesRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafRules.DataCloudflareWafRulesRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__660bdcd29d04bc0cfe9f795aa7e145618a0f710dcec6abe5846ad151a0d71e5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedModes")
    def allowed_modes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedModes"))

    @builtins.property
    @jsii.member(jsii_name="defaultMode")
    def default_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultMode"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="packageId")
    def package_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "packageId"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataCloudflareWafRulesRules]:
        return typing.cast(typing.Optional[DataCloudflareWafRulesRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCloudflareWafRulesRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860ea67425fe981970121d8244b7a4713b758705b0adbf77262b73d390ea6c55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataCloudflareWafRules",
    "DataCloudflareWafRulesConfig",
    "DataCloudflareWafRulesFilter",
    "DataCloudflareWafRulesFilterOutputReference",
    "DataCloudflareWafRulesRules",
    "DataCloudflareWafRulesRulesList",
    "DataCloudflareWafRulesRulesOutputReference",
]

publication.publish()

def _typecheckingstub__6ac79b29b214445656149fc240b6e29808749aaf4295e36e626371694c9445b4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    zone_id: builtins.str,
    filter: typing.Optional[typing.Union[DataCloudflareWafRulesFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    package_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__9837a9823f0be231113ec475db2d0d768a3d48b606b56ea890cc1d84fb9dbe9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5090245d5ba95c3143fabb24a9dd40757fb3a2ddee286b51595ffe57c15a09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68d35b0fa824ded9ae54fbbb40d8f4ed8570a4e1b06c37f1a69395c0483df4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ddf9a8a8eb0e2f3f863d7195f3ff0e33f58bd9d1b1f0b0a33ccf4ce80eb87a0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zone_id: builtins.str,
    filter: typing.Optional[typing.Union[DataCloudflareWafRulesFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    package_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afff99486928bc2bc21998503607c1524b5d16a6588484bc83dd93734681f461(
    *,
    description: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4593d26c1fb6127cd6f659d92c9a1bdbd7335801203b2e04a8ab47a72d27978(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b662281aac0de3edbf4fc7be6528f7056f0e9b2ee7862a031fc19622ebc23319(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbd918b395b75d99340402c08ccf5a1fa3a30ae148328a7383e2899760d6369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e463e66a6338a2d1cc8445d3956ac385b4f93b0ca75644401b7bb65e7c1f708(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9d1bb4be9af0e6878af194b217e98cd8359a8936de343792c1937bb7c03f4f(
    value: typing.Optional[DataCloudflareWafRulesFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243ec4369dbfc8e64415958e0a34c5775e819371f12c6b5d486ea5eea4a352f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc460112beb2e687bbf59525c071caa5102178caca6133bc436c852a1306de3a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5304e1aeba8221c3e4cf2a7c3c80448df94ec641df80abebec29935d5f2e43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed40cfd4a81595237953d0c1d594462ed19f024d92cee97a2575e7065b7cbfe1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32bf32619ec2ca56db0947d6122e64d7381f0fbb16aca9f4be6c5cc612a2efaf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660bdcd29d04bc0cfe9f795aa7e145618a0f710dcec6abe5846ad151a0d71e5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860ea67425fe981970121d8244b7a4713b758705b0adbf77262b73d390ea6c55(
    value: typing.Optional[DataCloudflareWafRulesRules],
) -> None:
    """Type checking stubs"""
    pass
