'''
# `azurerm_sql_managed_instance_failover_group`

Refer to the Terraform Registory for docs: [`azurerm_sql_managed_instance_failover_group`](https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group).
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


class SqlManagedInstanceFailoverGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlManagedInstanceFailoverGroup.SqlManagedInstanceFailoverGroup",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group azurerm_sql_managed_instance_failover_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        managed_instance_name: builtins.str,
        name: builtins.str,
        partner_managed_instance_id: builtins.str,
        read_write_endpoint_failover_policy: typing.Union["SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        readonly_endpoint_failover_policy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["SqlManagedInstanceFailoverGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group azurerm_sql_managed_instance_failover_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#location SqlManagedInstanceFailoverGroup#location}.
        :param managed_instance_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#managed_instance_name SqlManagedInstanceFailoverGroup#managed_instance_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#name SqlManagedInstanceFailoverGroup#name}.
        :param partner_managed_instance_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#partner_managed_instance_id SqlManagedInstanceFailoverGroup#partner_managed_instance_id}.
        :param read_write_endpoint_failover_policy: read_write_endpoint_failover_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#read_write_endpoint_failover_policy SqlManagedInstanceFailoverGroup#read_write_endpoint_failover_policy}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#resource_group_name SqlManagedInstanceFailoverGroup#resource_group_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#id SqlManagedInstanceFailoverGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param readonly_endpoint_failover_policy_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#readonly_endpoint_failover_policy_enabled SqlManagedInstanceFailoverGroup#readonly_endpoint_failover_policy_enabled}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#timeouts SqlManagedInstanceFailoverGroup#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c29765f2fdfc2cf4ca3ac34f0f1d436a6f6facd3b31da4c685278b0e1ac52e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SqlManagedInstanceFailoverGroupConfig(
            location=location,
            managed_instance_name=managed_instance_name,
            name=name,
            partner_managed_instance_id=partner_managed_instance_id,
            read_write_endpoint_failover_policy=read_write_endpoint_failover_policy,
            resource_group_name=resource_group_name,
            id=id,
            readonly_endpoint_failover_policy_enabled=readonly_endpoint_failover_policy_enabled,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putReadWriteEndpointFailoverPolicy")
    def put_read_write_endpoint_failover_policy(
        self,
        *,
        mode: builtins.str,
        grace_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#mode SqlManagedInstanceFailoverGroup#mode}.
        :param grace_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#grace_minutes SqlManagedInstanceFailoverGroup#grace_minutes}.
        '''
        value = SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy(
            mode=mode, grace_minutes=grace_minutes
        )

        return typing.cast(None, jsii.invoke(self, "putReadWriteEndpointFailoverPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#create SqlManagedInstanceFailoverGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#delete SqlManagedInstanceFailoverGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#read SqlManagedInstanceFailoverGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#update SqlManagedInstanceFailoverGroup#update}.
        '''
        value = SqlManagedInstanceFailoverGroupTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetReadonlyEndpointFailoverPolicyEnabled")
    def reset_readonly_endpoint_failover_policy_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadonlyEndpointFailoverPolicyEnabled", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="partnerRegion")
    def partner_region(self) -> "SqlManagedInstanceFailoverGroupPartnerRegionList":
        return typing.cast("SqlManagedInstanceFailoverGroupPartnerRegionList", jsii.get(self, "partnerRegion"))

    @builtins.property
    @jsii.member(jsii_name="readWriteEndpointFailoverPolicy")
    def read_write_endpoint_failover_policy(
        self,
    ) -> "SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicyOutputReference":
        return typing.cast("SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicyOutputReference", jsii.get(self, "readWriteEndpointFailoverPolicy"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SqlManagedInstanceFailoverGroupTimeoutsOutputReference":
        return typing.cast("SqlManagedInstanceFailoverGroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedInstanceNameInput")
    def managed_instance_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedInstanceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="partnerManagedInstanceIdInput")
    def partner_managed_instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partnerManagedInstanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="readonlyEndpointFailoverPolicyEnabledInput")
    def readonly_endpoint_failover_policy_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readonlyEndpointFailoverPolicyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="readWriteEndpointFailoverPolicyInput")
    def read_write_endpoint_failover_policy_input(
        self,
    ) -> typing.Optional["SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy"]:
        return typing.cast(typing.Optional["SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy"], jsii.get(self, "readWriteEndpointFailoverPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["SqlManagedInstanceFailoverGroupTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["SqlManagedInstanceFailoverGroupTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6766937d3ed46166de4f6af1cedbfde78078aeee8b528936ee065128374b6ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0533b750f2aa510c09640453e0c91c5ee26a85c4f2d8ef1d760437409d40bcf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="managedInstanceName")
    def managed_instance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedInstanceName"))

    @managed_instance_name.setter
    def managed_instance_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5595764d879a91007282b4a83abe68242d181d445339c74c9b4b85587e64cc1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedInstanceName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcfe269d2ce0fc8f7144df49b16b1286a02bbe3214b4a2eaa721e81269ae2cd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="partnerManagedInstanceId")
    def partner_managed_instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partnerManagedInstanceId"))

    @partner_managed_instance_id.setter
    def partner_managed_instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a10d6534120e1b1ee37860195bb1f231d832a370d4f29e6e7ea9cbf77e88c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partnerManagedInstanceId", value)

    @builtins.property
    @jsii.member(jsii_name="readonlyEndpointFailoverPolicyEnabled")
    def readonly_endpoint_failover_policy_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readonlyEndpointFailoverPolicyEnabled"))

    @readonly_endpoint_failover_policy_enabled.setter
    def readonly_endpoint_failover_policy_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__226f93d4673f8172873d2c2028a379ca5eb84a84d2e8e9dd9817a77813d87daf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readonlyEndpointFailoverPolicyEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305752017343149daed0b4b0a43068e91f9039baddc04ecccb7625cf2e7f5cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlManagedInstanceFailoverGroup.SqlManagedInstanceFailoverGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "managed_instance_name": "managedInstanceName",
        "name": "name",
        "partner_managed_instance_id": "partnerManagedInstanceId",
        "read_write_endpoint_failover_policy": "readWriteEndpointFailoverPolicy",
        "resource_group_name": "resourceGroupName",
        "id": "id",
        "readonly_endpoint_failover_policy_enabled": "readonlyEndpointFailoverPolicyEnabled",
        "timeouts": "timeouts",
    },
)
class SqlManagedInstanceFailoverGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        managed_instance_name: builtins.str,
        name: builtins.str,
        partner_managed_instance_id: builtins.str,
        read_write_endpoint_failover_policy: typing.Union["SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        readonly_endpoint_failover_policy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["SqlManagedInstanceFailoverGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#location SqlManagedInstanceFailoverGroup#location}.
        :param managed_instance_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#managed_instance_name SqlManagedInstanceFailoverGroup#managed_instance_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#name SqlManagedInstanceFailoverGroup#name}.
        :param partner_managed_instance_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#partner_managed_instance_id SqlManagedInstanceFailoverGroup#partner_managed_instance_id}.
        :param read_write_endpoint_failover_policy: read_write_endpoint_failover_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#read_write_endpoint_failover_policy SqlManagedInstanceFailoverGroup#read_write_endpoint_failover_policy}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#resource_group_name SqlManagedInstanceFailoverGroup#resource_group_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#id SqlManagedInstanceFailoverGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param readonly_endpoint_failover_policy_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#readonly_endpoint_failover_policy_enabled SqlManagedInstanceFailoverGroup#readonly_endpoint_failover_policy_enabled}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#timeouts SqlManagedInstanceFailoverGroup#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(read_write_endpoint_failover_policy, dict):
            read_write_endpoint_failover_policy = SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy(**read_write_endpoint_failover_policy)
        if isinstance(timeouts, dict):
            timeouts = SqlManagedInstanceFailoverGroupTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d391452b770f9bba97c02d2d13a8278d8c1ce263eda450ae3ce9ae293b99d8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument managed_instance_name", value=managed_instance_name, expected_type=type_hints["managed_instance_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument partner_managed_instance_id", value=partner_managed_instance_id, expected_type=type_hints["partner_managed_instance_id"])
            check_type(argname="argument read_write_endpoint_failover_policy", value=read_write_endpoint_failover_policy, expected_type=type_hints["read_write_endpoint_failover_policy"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument readonly_endpoint_failover_policy_enabled", value=readonly_endpoint_failover_policy_enabled, expected_type=type_hints["readonly_endpoint_failover_policy_enabled"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "managed_instance_name": managed_instance_name,
            "name": name,
            "partner_managed_instance_id": partner_managed_instance_id,
            "read_write_endpoint_failover_policy": read_write_endpoint_failover_policy,
            "resource_group_name": resource_group_name,
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
        if readonly_endpoint_failover_policy_enabled is not None:
            self._values["readonly_endpoint_failover_policy_enabled"] = readonly_endpoint_failover_policy_enabled
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#location SqlManagedInstanceFailoverGroup#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def managed_instance_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#managed_instance_name SqlManagedInstanceFailoverGroup#managed_instance_name}.'''
        result = self._values.get("managed_instance_name")
        assert result is not None, "Required property 'managed_instance_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#name SqlManagedInstanceFailoverGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partner_managed_instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#partner_managed_instance_id SqlManagedInstanceFailoverGroup#partner_managed_instance_id}.'''
        result = self._values.get("partner_managed_instance_id")
        assert result is not None, "Required property 'partner_managed_instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_write_endpoint_failover_policy(
        self,
    ) -> "SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy":
        '''read_write_endpoint_failover_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#read_write_endpoint_failover_policy SqlManagedInstanceFailoverGroup#read_write_endpoint_failover_policy}
        '''
        result = self._values.get("read_write_endpoint_failover_policy")
        assert result is not None, "Required property 'read_write_endpoint_failover_policy' is missing"
        return typing.cast("SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy", result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#resource_group_name SqlManagedInstanceFailoverGroup#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#id SqlManagedInstanceFailoverGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readonly_endpoint_failover_policy_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#readonly_endpoint_failover_policy_enabled SqlManagedInstanceFailoverGroup#readonly_endpoint_failover_policy_enabled}.'''
        result = self._values.get("readonly_endpoint_failover_policy_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SqlManagedInstanceFailoverGroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#timeouts SqlManagedInstanceFailoverGroup#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SqlManagedInstanceFailoverGroupTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlManagedInstanceFailoverGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlManagedInstanceFailoverGroup.SqlManagedInstanceFailoverGroupPartnerRegion",
    jsii_struct_bases=[],
    name_mapping={},
)
class SqlManagedInstanceFailoverGroupPartnerRegion:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlManagedInstanceFailoverGroupPartnerRegion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlManagedInstanceFailoverGroupPartnerRegionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlManagedInstanceFailoverGroup.SqlManagedInstanceFailoverGroupPartnerRegionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c073f0557db2476ad773da0414fdb64931479688dc9d2e6c42ab0e3e6cf68115)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SqlManagedInstanceFailoverGroupPartnerRegionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ece0e1914a40b604c431209afe9b80b650cdcd56420fd0eaeb1d59ca5a223c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SqlManagedInstanceFailoverGroupPartnerRegionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de81cb7f1fe88ad86a268a3305fbdd4ed9c93623c1f10c80d4fe87b96b679a69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8995a4b3ee4ec78a21d01b3c5000f628e3e065e15eaf57b313b4d50ae8e80b58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5360a3431ba72ae0e6833fbb69b5dfba9f0bdb77de87764be0af25d6d6c6be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class SqlManagedInstanceFailoverGroupPartnerRegionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlManagedInstanceFailoverGroup.SqlManagedInstanceFailoverGroupPartnerRegionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5702a1b13b430025721d624b422fa0b0fea38cd8b95dab3542135332dd708ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlManagedInstanceFailoverGroupPartnerRegion]:
        return typing.cast(typing.Optional[SqlManagedInstanceFailoverGroupPartnerRegion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlManagedInstanceFailoverGroupPartnerRegion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f4fb608f0dd629e2a7ee5d4c5cc64179b509758bb762af0b41ea88298ee372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlManagedInstanceFailoverGroup.SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "grace_minutes": "graceMinutes"},
)
class SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy:
    def __init__(
        self,
        *,
        mode: builtins.str,
        grace_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#mode SqlManagedInstanceFailoverGroup#mode}.
        :param grace_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#grace_minutes SqlManagedInstanceFailoverGroup#grace_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f199829b53269b87b5e9c5cbf445fb336e47c8e258f39bbcff5e60747b88c6f)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument grace_minutes", value=grace_minutes, expected_type=type_hints["grace_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if grace_minutes is not None:
            self._values["grace_minutes"] = grace_minutes

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#mode SqlManagedInstanceFailoverGroup#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def grace_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#grace_minutes SqlManagedInstanceFailoverGroup#grace_minutes}.'''
        result = self._values.get("grace_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlManagedInstanceFailoverGroup.SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30687ec502d005b81d4731bf0d0e07e44f1ffe9800c3e50e40acd3b9ef87c77d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGraceMinutes")
    def reset_grace_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGraceMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="graceMinutesInput")
    def grace_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "graceMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="graceMinutes")
    def grace_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "graceMinutes"))

    @grace_minutes.setter
    def grace_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce8943553caf9e2c62505c588edd3f50996fa719e3e1299ae12f02566040ee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "graceMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daca52359ab0f0d8a14dc2401841fc21e35ba4292d94d777ff35038559c68158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy]:
        return typing.cast(typing.Optional[SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e38b0aef97791659e838bdb162391309f973884e51e0f2724cb3259c773228b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlManagedInstanceFailoverGroup.SqlManagedInstanceFailoverGroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SqlManagedInstanceFailoverGroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#create SqlManagedInstanceFailoverGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#delete SqlManagedInstanceFailoverGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#read SqlManagedInstanceFailoverGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#update SqlManagedInstanceFailoverGroup#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55ca9c255313d17488c4864db65979e54d4469585275ec08863469a775005b3)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#create SqlManagedInstanceFailoverGroup#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#delete SqlManagedInstanceFailoverGroup#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#read SqlManagedInstanceFailoverGroup#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_managed_instance_failover_group#update SqlManagedInstanceFailoverGroup#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlManagedInstanceFailoverGroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlManagedInstanceFailoverGroupTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlManagedInstanceFailoverGroup.SqlManagedInstanceFailoverGroupTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af69e03158aed35a2144d9f99b689233ae1619f7b9f605dc41ec28edd5815912)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b482c0b71ce0556c5843adb2521c2d67950517013f01829f40f50e6ecb4c257d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9692c4b951f4d539670e9f20c1a4714766950f7378d98451da47c4c645b6fd99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af52f813e598effc7d443cbaed38f9a915259b7f14ce2ef4b1d176c260d1e12d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__543424f26fc875a086fc16ebfe0cf1a50c14abda0cf741b6f61ebe05cb76e473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SqlManagedInstanceFailoverGroupTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SqlManagedInstanceFailoverGroupTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SqlManagedInstanceFailoverGroupTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a18e282df77b96beabc0cb8dc8612087f2d9b5783951db8d4c68c0e653a6cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SqlManagedInstanceFailoverGroup",
    "SqlManagedInstanceFailoverGroupConfig",
    "SqlManagedInstanceFailoverGroupPartnerRegion",
    "SqlManagedInstanceFailoverGroupPartnerRegionList",
    "SqlManagedInstanceFailoverGroupPartnerRegionOutputReference",
    "SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy",
    "SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicyOutputReference",
    "SqlManagedInstanceFailoverGroupTimeouts",
    "SqlManagedInstanceFailoverGroupTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a3c29765f2fdfc2cf4ca3ac34f0f1d436a6f6facd3b31da4c685278b0e1ac52e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    managed_instance_name: builtins.str,
    name: builtins.str,
    partner_managed_instance_id: builtins.str,
    read_write_endpoint_failover_policy: typing.Union[SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    readonly_endpoint_failover_policy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[SqlManagedInstanceFailoverGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b6766937d3ed46166de4f6af1cedbfde78078aeee8b528936ee065128374b6ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0533b750f2aa510c09640453e0c91c5ee26a85c4f2d8ef1d760437409d40bcf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5595764d879a91007282b4a83abe68242d181d445339c74c9b4b85587e64cc1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcfe269d2ce0fc8f7144df49b16b1286a02bbe3214b4a2eaa721e81269ae2cd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a10d6534120e1b1ee37860195bb1f231d832a370d4f29e6e7ea9cbf77e88c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226f93d4673f8172873d2c2028a379ca5eb84a84d2e8e9dd9817a77813d87daf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305752017343149daed0b4b0a43068e91f9039baddc04ecccb7625cf2e7f5cd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d391452b770f9bba97c02d2d13a8278d8c1ce263eda450ae3ce9ae293b99d8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    managed_instance_name: builtins.str,
    name: builtins.str,
    partner_managed_instance_id: builtins.str,
    read_write_endpoint_failover_policy: typing.Union[SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    readonly_endpoint_failover_policy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[SqlManagedInstanceFailoverGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c073f0557db2476ad773da0414fdb64931479688dc9d2e6c42ab0e3e6cf68115(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ece0e1914a40b604c431209afe9b80b650cdcd56420fd0eaeb1d59ca5a223c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de81cb7f1fe88ad86a268a3305fbdd4ed9c93623c1f10c80d4fe87b96b679a69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8995a4b3ee4ec78a21d01b3c5000f628e3e065e15eaf57b313b4d50ae8e80b58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5360a3431ba72ae0e6833fbb69b5dfba9f0bdb77de87764be0af25d6d6c6be6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5702a1b13b430025721d624b422fa0b0fea38cd8b95dab3542135332dd708ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f4fb608f0dd629e2a7ee5d4c5cc64179b509758bb762af0b41ea88298ee372(
    value: typing.Optional[SqlManagedInstanceFailoverGroupPartnerRegion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f199829b53269b87b5e9c5cbf445fb336e47c8e258f39bbcff5e60747b88c6f(
    *,
    mode: builtins.str,
    grace_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30687ec502d005b81d4731bf0d0e07e44f1ffe9800c3e50e40acd3b9ef87c77d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce8943553caf9e2c62505c588edd3f50996fa719e3e1299ae12f02566040ee1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daca52359ab0f0d8a14dc2401841fc21e35ba4292d94d777ff35038559c68158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e38b0aef97791659e838bdb162391309f973884e51e0f2724cb3259c773228b(
    value: typing.Optional[SqlManagedInstanceFailoverGroupReadWriteEndpointFailoverPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55ca9c255313d17488c4864db65979e54d4469585275ec08863469a775005b3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af69e03158aed35a2144d9f99b689233ae1619f7b9f605dc41ec28edd5815912(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b482c0b71ce0556c5843adb2521c2d67950517013f01829f40f50e6ecb4c257d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9692c4b951f4d539670e9f20c1a4714766950f7378d98451da47c4c645b6fd99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af52f813e598effc7d443cbaed38f9a915259b7f14ce2ef4b1d176c260d1e12d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__543424f26fc875a086fc16ebfe0cf1a50c14abda0cf741b6f61ebe05cb76e473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a18e282df77b96beabc0cb8dc8612087f2d9b5783951db8d4c68c0e653a6cfc(
    value: typing.Optional[typing.Union[SqlManagedInstanceFailoverGroupTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
