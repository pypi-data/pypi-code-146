'''
# `google_access_context_manager_access_level_condition`

Refer to the Terraform Registory for docs: [`google_access_context_manager_access_level_condition`](https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition).
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


class AccessContextManagerAccessLevelCondition(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevelCondition.AccessContextManagerAccessLevelCondition",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition google_access_context_manager_access_level_condition}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        access_level: builtins.str,
        device_policy: typing.Optional[typing.Union["AccessContextManagerAccessLevelConditionDevicePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
        members: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        required_access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerAccessLevelConditionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition google_access_context_manager_access_level_condition} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_level: The name of the Access Level to add this condition to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#access_level AccessContextManagerAccessLevelCondition#access_level}
        :param device_policy: device_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#device_policy AccessContextManagerAccessLevelCondition#device_policy}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#id AccessContextManagerAccessLevelCondition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_subnetworks: A list of CIDR block IP subnetwork specification. May be IPv4 or IPv6. Note that for a CIDR IP address block, the specified IP address portion must be properly truncated (i.e. all the host bits must be zero) or the input is considered malformed. For example, "192.0.2.0/24" is accepted but "192.0.2.1/24" is not. Similarly, for IPv6, "2001:db8::/32" is accepted whereas "2001:db8::1/32" is not. The originating IP of a request must be in one of the listed subnets in order for this Condition to be true. If empty, all IP addresses are allowed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#ip_subnetworks AccessContextManagerAccessLevelCondition#ip_subnetworks}
        :param members: An allowed list of members (users, service accounts). Using groups is not supported yet. The signed-in user originating the request must be a part of one of the provided members. If not specified, a request may come from any user (logged in/not logged in, not present in any groups, etc.). Formats: 'user:{emailid}', 'serviceAccount:{emailid}' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#members AccessContextManagerAccessLevelCondition#members}
        :param negate: Whether to negate the Condition. If true, the Condition becomes a NAND over its non-empty fields, each field must be false for the Condition overall to be satisfied. Defaults to false. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#negate AccessContextManagerAccessLevelCondition#negate}
        :param regions: The request must originate from one of the provided countries/regions. Format: A valid ISO 3166-1 alpha-2 code. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#regions AccessContextManagerAccessLevelCondition#regions}
        :param required_access_levels: A list of other access levels defined in the same Policy, referenced by resource name. Referencing an AccessLevel which does not exist is an error. All access levels listed must be granted for the Condition to be true. Format: accessPolicies/{policy_id}/accessLevels/{short_name} Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#required_access_levels AccessContextManagerAccessLevelCondition#required_access_levels}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#timeouts AccessContextManagerAccessLevelCondition#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43cdd759647c71fe7c4579b634facb3ed72bf434c2ffdccd492282f8f7b9616f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessContextManagerAccessLevelConditionConfig(
            access_level=access_level,
            device_policy=device_policy,
            id=id,
            ip_subnetworks=ip_subnetworks,
            members=members,
            negate=negate,
            regions=regions,
            required_access_levels=required_access_levels,
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

    @jsii.member(jsii_name="putDevicePolicy")
    def put_device_policy(
        self,
        *,
        allowed_device_management_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_encryption_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_constraints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        require_admin_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_corp_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_device_management_levels: A list of allowed device management levels. An empty list allows all management levels. Possible values: ["MANAGEMENT_UNSPECIFIED", "NONE", "BASIC", "COMPLETE"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#allowed_device_management_levels AccessContextManagerAccessLevelCondition#allowed_device_management_levels}
        :param allowed_encryption_statuses: A list of allowed encryptions statuses. An empty list allows all statuses. Possible values: ["ENCRYPTION_UNSPECIFIED", "ENCRYPTION_UNSUPPORTED", "UNENCRYPTED", "ENCRYPTED"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#allowed_encryption_statuses AccessContextManagerAccessLevelCondition#allowed_encryption_statuses}
        :param os_constraints: os_constraints block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#os_constraints AccessContextManagerAccessLevelCondition#os_constraints}
        :param require_admin_approval: Whether the device needs to be approved by the customer admin. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#require_admin_approval AccessContextManagerAccessLevelCondition#require_admin_approval}
        :param require_corp_owned: Whether the device needs to be corp owned. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#require_corp_owned AccessContextManagerAccessLevelCondition#require_corp_owned}
        :param require_screen_lock: Whether or not screenlock is required for the DevicePolicy to be true. Defaults to false. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#require_screen_lock AccessContextManagerAccessLevelCondition#require_screen_lock}
        '''
        value = AccessContextManagerAccessLevelConditionDevicePolicy(
            allowed_device_management_levels=allowed_device_management_levels,
            allowed_encryption_statuses=allowed_encryption_statuses,
            os_constraints=os_constraints,
            require_admin_approval=require_admin_approval,
            require_corp_owned=require_corp_owned,
            require_screen_lock=require_screen_lock,
        )

        return typing.cast(None, jsii.invoke(self, "putDevicePolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#create AccessContextManagerAccessLevelCondition#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#delete AccessContextManagerAccessLevelCondition#delete}.
        '''
        value = AccessContextManagerAccessLevelConditionTimeouts(
            create=create, delete=delete
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDevicePolicy")
    def reset_device_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevicePolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpSubnetworks")
    def reset_ip_subnetworks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpSubnetworks", []))

    @jsii.member(jsii_name="resetMembers")
    def reset_members(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembers", []))

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @jsii.member(jsii_name="resetRegions")
    def reset_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegions", []))

    @jsii.member(jsii_name="resetRequiredAccessLevels")
    def reset_required_access_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredAccessLevels", []))

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
    @jsii.member(jsii_name="devicePolicy")
    def device_policy(
        self,
    ) -> "AccessContextManagerAccessLevelConditionDevicePolicyOutputReference":
        return typing.cast("AccessContextManagerAccessLevelConditionDevicePolicyOutputReference", jsii.get(self, "devicePolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "AccessContextManagerAccessLevelConditionTimeoutsOutputReference":
        return typing.cast("AccessContextManagerAccessLevelConditionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelInput")
    def access_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="devicePolicyInput")
    def device_policy_input(
        self,
    ) -> typing.Optional["AccessContextManagerAccessLevelConditionDevicePolicy"]:
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelConditionDevicePolicy"], jsii.get(self, "devicePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipSubnetworksInput")
    def ip_subnetworks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipSubnetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="membersInput")
    def members_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "membersInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="regionsInput")
    def regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "regionsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredAccessLevelsInput")
    def required_access_levels_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "requiredAccessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["AccessContextManagerAccessLevelConditionTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["AccessContextManagerAccessLevelConditionTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevel")
    def access_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessLevel"))

    @access_level.setter
    def access_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a82a9c12ac0d8f3b6d43e4f6460e40b77a941f0f9cea80c5279e733de4e322d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevel", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ba6b87220384ce384542e63945df8e4aa0625aed2bbe8b3c0b285cf6feb7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipSubnetworks")
    def ip_subnetworks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipSubnetworks"))

    @ip_subnetworks.setter
    def ip_subnetworks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cdb26aa79a7d9cfe5a5fee252cd7937b16549890660e9a089483657208752f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipSubnetworks", value)

    @builtins.property
    @jsii.member(jsii_name="members")
    def members(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "members"))

    @members.setter
    def members(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48305faf69a54e167ce8bf2453de175a774054babfb147c2e9136d5c028da4b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "members", value)

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9874ff366cd8d226f637f0a6e424d3137034b1d69b77f308ccdfd4b7959c2c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value)

    @builtins.property
    @jsii.member(jsii_name="regions")
    def regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regions"))

    @regions.setter
    def regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0deed6d8d539c3858300e41d0cb33ac72f2fd41e4f60eda869827a1638ac3da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regions", value)

    @builtins.property
    @jsii.member(jsii_name="requiredAccessLevels")
    def required_access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requiredAccessLevels"))

    @required_access_levels.setter
    def required_access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ade261a40d712ca8f331f81301940be82701e5124e191b58378b3d3b1db4c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredAccessLevels", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevelCondition.AccessContextManagerAccessLevelConditionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "access_level": "accessLevel",
        "device_policy": "devicePolicy",
        "id": "id",
        "ip_subnetworks": "ipSubnetworks",
        "members": "members",
        "negate": "negate",
        "regions": "regions",
        "required_access_levels": "requiredAccessLevels",
        "timeouts": "timeouts",
    },
)
class AccessContextManagerAccessLevelConditionConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        access_level: builtins.str,
        device_policy: typing.Optional[typing.Union["AccessContextManagerAccessLevelConditionDevicePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
        members: typing.Optional[typing.Sequence[builtins.str]] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        required_access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerAccessLevelConditionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param access_level: The name of the Access Level to add this condition to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#access_level AccessContextManagerAccessLevelCondition#access_level}
        :param device_policy: device_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#device_policy AccessContextManagerAccessLevelCondition#device_policy}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#id AccessContextManagerAccessLevelCondition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_subnetworks: A list of CIDR block IP subnetwork specification. May be IPv4 or IPv6. Note that for a CIDR IP address block, the specified IP address portion must be properly truncated (i.e. all the host bits must be zero) or the input is considered malformed. For example, "192.0.2.0/24" is accepted but "192.0.2.1/24" is not. Similarly, for IPv6, "2001:db8::/32" is accepted whereas "2001:db8::1/32" is not. The originating IP of a request must be in one of the listed subnets in order for this Condition to be true. If empty, all IP addresses are allowed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#ip_subnetworks AccessContextManagerAccessLevelCondition#ip_subnetworks}
        :param members: An allowed list of members (users, service accounts). Using groups is not supported yet. The signed-in user originating the request must be a part of one of the provided members. If not specified, a request may come from any user (logged in/not logged in, not present in any groups, etc.). Formats: 'user:{emailid}', 'serviceAccount:{emailid}' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#members AccessContextManagerAccessLevelCondition#members}
        :param negate: Whether to negate the Condition. If true, the Condition becomes a NAND over its non-empty fields, each field must be false for the Condition overall to be satisfied. Defaults to false. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#negate AccessContextManagerAccessLevelCondition#negate}
        :param regions: The request must originate from one of the provided countries/regions. Format: A valid ISO 3166-1 alpha-2 code. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#regions AccessContextManagerAccessLevelCondition#regions}
        :param required_access_levels: A list of other access levels defined in the same Policy, referenced by resource name. Referencing an AccessLevel which does not exist is an error. All access levels listed must be granted for the Condition to be true. Format: accessPolicies/{policy_id}/accessLevels/{short_name} Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#required_access_levels AccessContextManagerAccessLevelCondition#required_access_levels}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#timeouts AccessContextManagerAccessLevelCondition#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(device_policy, dict):
            device_policy = AccessContextManagerAccessLevelConditionDevicePolicy(**device_policy)
        if isinstance(timeouts, dict):
            timeouts = AccessContextManagerAccessLevelConditionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35fc0a2065c3721c199e0de68120ab96706cb540fee955504264d77402b60e9c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument device_policy", value=device_policy, expected_type=type_hints["device_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_subnetworks", value=ip_subnetworks, expected_type=type_hints["ip_subnetworks"])
            check_type(argname="argument members", value=members, expected_type=type_hints["members"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument required_access_levels", value=required_access_levels, expected_type=type_hints["required_access_levels"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_level": access_level,
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
        if device_policy is not None:
            self._values["device_policy"] = device_policy
        if id is not None:
            self._values["id"] = id
        if ip_subnetworks is not None:
            self._values["ip_subnetworks"] = ip_subnetworks
        if members is not None:
            self._values["members"] = members
        if negate is not None:
            self._values["negate"] = negate
        if regions is not None:
            self._values["regions"] = regions
        if required_access_levels is not None:
            self._values["required_access_levels"] = required_access_levels
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
    def access_level(self) -> builtins.str:
        '''The name of the Access Level to add this condition to.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#access_level AccessContextManagerAccessLevelCondition#access_level}
        '''
        result = self._values.get("access_level")
        assert result is not None, "Required property 'access_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def device_policy(
        self,
    ) -> typing.Optional["AccessContextManagerAccessLevelConditionDevicePolicy"]:
        '''device_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#device_policy AccessContextManagerAccessLevelCondition#device_policy}
        '''
        result = self._values.get("device_policy")
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelConditionDevicePolicy"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#id AccessContextManagerAccessLevelCondition#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_subnetworks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of CIDR block IP subnetwork specification.

        May be IPv4
        or IPv6.
        Note that for a CIDR IP address block, the specified IP address
        portion must be properly truncated (i.e. all the host bits must
        be zero) or the input is considered malformed. For example,
        "192.0.2.0/24" is accepted but "192.0.2.1/24" is not. Similarly,
        for IPv6, "2001:db8::/32" is accepted whereas "2001:db8::1/32"
        is not. The originating IP of a request must be in one of the
        listed subnets in order for this Condition to be true.
        If empty, all IP addresses are allowed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#ip_subnetworks AccessContextManagerAccessLevelCondition#ip_subnetworks}
        '''
        result = self._values.get("ip_subnetworks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def members(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An allowed list of members (users, service accounts). Using groups is not supported yet.

        The signed-in user originating the request must be a part of one
        of the provided members. If not specified, a request may come
        from any user (logged in/not logged in, not present in any
        groups, etc.).
        Formats: 'user:{emailid}', 'serviceAccount:{emailid}'

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#members AccessContextManagerAccessLevelCondition#members}
        '''
        result = self._values.get("members")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to negate the Condition.

        If true, the Condition becomes
        a NAND over its non-empty fields, each field must be false for
        the Condition overall to be satisfied. Defaults to false.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#negate AccessContextManagerAccessLevelCondition#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The request must originate from one of the provided countries/regions. Format: A valid ISO 3166-1 alpha-2 code.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#regions AccessContextManagerAccessLevelCondition#regions}
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def required_access_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of other access levels defined in the same Policy, referenced by resource name.

        Referencing an AccessLevel which
        does not exist is an error. All access levels listed must be
        granted for the Condition to be true.
        Format: accessPolicies/{policy_id}/accessLevels/{short_name}

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#required_access_levels AccessContextManagerAccessLevelCondition#required_access_levels}
        '''
        result = self._values.get("required_access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["AccessContextManagerAccessLevelConditionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#timeouts AccessContextManagerAccessLevelCondition#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AccessContextManagerAccessLevelConditionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelConditionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevelCondition.AccessContextManagerAccessLevelConditionDevicePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_device_management_levels": "allowedDeviceManagementLevels",
        "allowed_encryption_statuses": "allowedEncryptionStatuses",
        "os_constraints": "osConstraints",
        "require_admin_approval": "requireAdminApproval",
        "require_corp_owned": "requireCorpOwned",
        "require_screen_lock": "requireScreenLock",
    },
)
class AccessContextManagerAccessLevelConditionDevicePolicy:
    def __init__(
        self,
        *,
        allowed_device_management_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_encryption_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_constraints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        require_admin_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_corp_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_device_management_levels: A list of allowed device management levels. An empty list allows all management levels. Possible values: ["MANAGEMENT_UNSPECIFIED", "NONE", "BASIC", "COMPLETE"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#allowed_device_management_levels AccessContextManagerAccessLevelCondition#allowed_device_management_levels}
        :param allowed_encryption_statuses: A list of allowed encryptions statuses. An empty list allows all statuses. Possible values: ["ENCRYPTION_UNSPECIFIED", "ENCRYPTION_UNSUPPORTED", "UNENCRYPTED", "ENCRYPTED"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#allowed_encryption_statuses AccessContextManagerAccessLevelCondition#allowed_encryption_statuses}
        :param os_constraints: os_constraints block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#os_constraints AccessContextManagerAccessLevelCondition#os_constraints}
        :param require_admin_approval: Whether the device needs to be approved by the customer admin. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#require_admin_approval AccessContextManagerAccessLevelCondition#require_admin_approval}
        :param require_corp_owned: Whether the device needs to be corp owned. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#require_corp_owned AccessContextManagerAccessLevelCondition#require_corp_owned}
        :param require_screen_lock: Whether or not screenlock is required for the DevicePolicy to be true. Defaults to false. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#require_screen_lock AccessContextManagerAccessLevelCondition#require_screen_lock}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91a3709783bf6f0887f216447f7e91c6a7c686d87abc46f2376fc857706a7d53)
            check_type(argname="argument allowed_device_management_levels", value=allowed_device_management_levels, expected_type=type_hints["allowed_device_management_levels"])
            check_type(argname="argument allowed_encryption_statuses", value=allowed_encryption_statuses, expected_type=type_hints["allowed_encryption_statuses"])
            check_type(argname="argument os_constraints", value=os_constraints, expected_type=type_hints["os_constraints"])
            check_type(argname="argument require_admin_approval", value=require_admin_approval, expected_type=type_hints["require_admin_approval"])
            check_type(argname="argument require_corp_owned", value=require_corp_owned, expected_type=type_hints["require_corp_owned"])
            check_type(argname="argument require_screen_lock", value=require_screen_lock, expected_type=type_hints["require_screen_lock"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_device_management_levels is not None:
            self._values["allowed_device_management_levels"] = allowed_device_management_levels
        if allowed_encryption_statuses is not None:
            self._values["allowed_encryption_statuses"] = allowed_encryption_statuses
        if os_constraints is not None:
            self._values["os_constraints"] = os_constraints
        if require_admin_approval is not None:
            self._values["require_admin_approval"] = require_admin_approval
        if require_corp_owned is not None:
            self._values["require_corp_owned"] = require_corp_owned
        if require_screen_lock is not None:
            self._values["require_screen_lock"] = require_screen_lock

    @builtins.property
    def allowed_device_management_levels(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of allowed device management levels. An empty list allows all management levels. Possible values: ["MANAGEMENT_UNSPECIFIED", "NONE", "BASIC", "COMPLETE"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#allowed_device_management_levels AccessContextManagerAccessLevelCondition#allowed_device_management_levels}
        '''
        result = self._values.get("allowed_device_management_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_encryption_statuses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of allowed encryptions statuses. An empty list allows all statuses. Possible values: ["ENCRYPTION_UNSPECIFIED", "ENCRYPTION_UNSUPPORTED", "UNENCRYPTED", "ENCRYPTED"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#allowed_encryption_statuses AccessContextManagerAccessLevelCondition#allowed_encryption_statuses}
        '''
        result = self._values.get("allowed_encryption_statuses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def os_constraints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints"]]]:
        '''os_constraints block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#os_constraints AccessContextManagerAccessLevelCondition#os_constraints}
        '''
        result = self._values.get("os_constraints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints"]]], result)

    @builtins.property
    def require_admin_approval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the device needs to be approved by the customer admin.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#require_admin_approval AccessContextManagerAccessLevelCondition#require_admin_approval}
        '''
        result = self._values.get("require_admin_approval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_corp_owned(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the device needs to be corp owned.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#require_corp_owned AccessContextManagerAccessLevelCondition#require_corp_owned}
        '''
        result = self._values.get("require_corp_owned")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_screen_lock(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not screenlock is required for the DevicePolicy to be true. Defaults to false.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#require_screen_lock AccessContextManagerAccessLevelCondition#require_screen_lock}
        '''
        result = self._values.get("require_screen_lock")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelConditionDevicePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevelCondition.AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints",
    jsii_struct_bases=[],
    name_mapping={"os_type": "osType", "minimum_version": "minimumVersion"},
)
class AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints:
    def __init__(
        self,
        *,
        os_type: builtins.str,
        minimum_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_type: The operating system type of the device. Possible values: ["OS_UNSPECIFIED", "DESKTOP_MAC", "DESKTOP_WINDOWS", "DESKTOP_LINUX", "DESKTOP_CHROME_OS", "ANDROID", "IOS"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#os_type AccessContextManagerAccessLevelCondition#os_type}
        :param minimum_version: The minimum allowed OS version. If not set, any version of this OS satisfies the constraint. Format: "major.minor.patch" such as "10.5.301", "9.2.1". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#minimum_version AccessContextManagerAccessLevelCondition#minimum_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db5fd46796fb4ee3195141e733ab01f4dd2d13aa66aff9306f5fa5697ba7b45)
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument minimum_version", value=minimum_version, expected_type=type_hints["minimum_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "os_type": os_type,
        }
        if minimum_version is not None:
            self._values["minimum_version"] = minimum_version

    @builtins.property
    def os_type(self) -> builtins.str:
        '''The operating system type of the device. Possible values: ["OS_UNSPECIFIED", "DESKTOP_MAC", "DESKTOP_WINDOWS", "DESKTOP_LINUX", "DESKTOP_CHROME_OS", "ANDROID", "IOS"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#os_type AccessContextManagerAccessLevelCondition#os_type}
        '''
        result = self._values.get("os_type")
        assert result is not None, "Required property 'os_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def minimum_version(self) -> typing.Optional[builtins.str]:
        '''The minimum allowed OS version.

        If not set, any version
        of this OS satisfies the constraint.
        Format: "major.minor.patch" such as "10.5.301", "9.2.1".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#minimum_version AccessContextManagerAccessLevelCondition#minimum_version}
        '''
        result = self._values.get("minimum_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelConditionDevicePolicyOsConstraintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevelCondition.AccessContextManagerAccessLevelConditionDevicePolicyOsConstraintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94f11de8ed0db625c515e482ad31cdcfaab132c3f4ae68b4dbef0d5498e995b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerAccessLevelConditionDevicePolicyOsConstraintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__695ef5abd15aea6c7d18cdd1e0bd754f5aac7a1e2af53069feb7c0d61228821f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerAccessLevelConditionDevicePolicyOsConstraintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa2429aba7f8d6eb66933809cca1d94c8ce0d384cc155f19a8d91fdd8f478da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e876b518a90b0e04b124905022926179999308e29b7ba5c1e38ed2144c3100a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61e906de59fde763207711210b4fd4a9520f47b0af874bfa9f885a9e0921c65a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519e048ca9f605f4bc6007c209723ed7f541527eb9be9aed60f6a1cae56659ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessContextManagerAccessLevelConditionDevicePolicyOsConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevelCondition.AccessContextManagerAccessLevelConditionDevicePolicyOsConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7962514378535a2ddfe9636314b29113fbf33c16b8b2630982a316e9b8c3ed94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMinimumVersion")
    def reset_minimum_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumVersion", []))

    @builtins.property
    @jsii.member(jsii_name="minimumVersionInput")
    def minimum_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumVersion")
    def minimum_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumVersion"))

    @minimum_version.setter
    def minimum_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__022aa6989bf1301fccd1d5442d186623d109aa1e2ee7d631ac32fadf14569392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumVersion", value)

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6eb786888d3d3eda49dd8f9f32a805591c2248b93d108bc2ccbf6dd240e94e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48da05ca9e263127796a84911ebb3acee70e5ff1717e02ea84c9a64a32a11580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessContextManagerAccessLevelConditionDevicePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevelCondition.AccessContextManagerAccessLevelConditionDevicePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__410e0a386035e448d206283a639667ff3ba2ac04cb2ef1c7690f25e1044a2a69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOsConstraints")
    def put_os_constraints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c149d298bad3bcf3c2ae2b571d820992c5bbf4c3205bc3e1ff4ea363b87b8b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOsConstraints", [value]))

    @jsii.member(jsii_name="resetAllowedDeviceManagementLevels")
    def reset_allowed_device_management_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedDeviceManagementLevels", []))

    @jsii.member(jsii_name="resetAllowedEncryptionStatuses")
    def reset_allowed_encryption_statuses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedEncryptionStatuses", []))

    @jsii.member(jsii_name="resetOsConstraints")
    def reset_os_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsConstraints", []))

    @jsii.member(jsii_name="resetRequireAdminApproval")
    def reset_require_admin_approval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireAdminApproval", []))

    @jsii.member(jsii_name="resetRequireCorpOwned")
    def reset_require_corp_owned(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireCorpOwned", []))

    @jsii.member(jsii_name="resetRequireScreenLock")
    def reset_require_screen_lock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireScreenLock", []))

    @builtins.property
    @jsii.member(jsii_name="osConstraints")
    def os_constraints(
        self,
    ) -> AccessContextManagerAccessLevelConditionDevicePolicyOsConstraintsList:
        return typing.cast(AccessContextManagerAccessLevelConditionDevicePolicyOsConstraintsList, jsii.get(self, "osConstraints"))

    @builtins.property
    @jsii.member(jsii_name="allowedDeviceManagementLevelsInput")
    def allowed_device_management_levels_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedDeviceManagementLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedEncryptionStatusesInput")
    def allowed_encryption_statuses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedEncryptionStatusesInput"))

    @builtins.property
    @jsii.member(jsii_name="osConstraintsInput")
    def os_constraints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints]]], jsii.get(self, "osConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="requireAdminApprovalInput")
    def require_admin_approval_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireAdminApprovalInput"))

    @builtins.property
    @jsii.member(jsii_name="requireCorpOwnedInput")
    def require_corp_owned_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireCorpOwnedInput"))

    @builtins.property
    @jsii.member(jsii_name="requireScreenLockInput")
    def require_screen_lock_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireScreenLockInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedDeviceManagementLevels")
    def allowed_device_management_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedDeviceManagementLevels"))

    @allowed_device_management_levels.setter
    def allowed_device_management_levels(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0a0814a5606a6cb202ef7d07177285d0c343b6934dcb9e1b234996dc3f3a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedDeviceManagementLevels", value)

    @builtins.property
    @jsii.member(jsii_name="allowedEncryptionStatuses")
    def allowed_encryption_statuses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedEncryptionStatuses"))

    @allowed_encryption_statuses.setter
    def allowed_encryption_statuses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70c403269310e14297463f20d368014dfffceec501460792df0f36d3ff99041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedEncryptionStatuses", value)

    @builtins.property
    @jsii.member(jsii_name="requireAdminApproval")
    def require_admin_approval(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireAdminApproval"))

    @require_admin_approval.setter
    def require_admin_approval(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0509f9b4e12507a66e6d28aa4f7b47b6f90666d41cd81bf4794cd635d3afbe26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAdminApproval", value)

    @builtins.property
    @jsii.member(jsii_name="requireCorpOwned")
    def require_corp_owned(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireCorpOwned"))

    @require_corp_owned.setter
    def require_corp_owned(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4378a34e77538b730605674bf58b0b8c41b668fd5d40d0573e7c4d00fd8da68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireCorpOwned", value)

    @builtins.property
    @jsii.member(jsii_name="requireScreenLock")
    def require_screen_lock(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireScreenLock"))

    @require_screen_lock.setter
    def require_screen_lock(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e0f62cdb72bd0fe682cb6badaf030e0392383a75a21137ece23a55dbf75815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireScreenLock", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerAccessLevelConditionDevicePolicy]:
        return typing.cast(typing.Optional[AccessContextManagerAccessLevelConditionDevicePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerAccessLevelConditionDevicePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8c8dcee3d30c1789c2d3df5744d79b6c0bbac8dd006a285b5c804633dda7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevelCondition.AccessContextManagerAccessLevelConditionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class AccessContextManagerAccessLevelConditionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#create AccessContextManagerAccessLevelCondition#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#delete AccessContextManagerAccessLevelCondition#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15559ec8632c22e571597ee4624adbe3e45fc0ceead6defc6e5312d4e092043c)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#create AccessContextManagerAccessLevelCondition#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/access_context_manager_access_level_condition#delete AccessContextManagerAccessLevelCondition#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerAccessLevelConditionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerAccessLevelConditionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerAccessLevelCondition.AccessContextManagerAccessLevelConditionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6ab381bc501d6f03ed0788d8779ae53594b7fd399950697c2a72acba091fe06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4385d7cc430b91bd452c8ca5b3131d2715d2c77e73010f0f29633860934b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84915b12c309c4030ac62afd09ea563dd4d7b593f73e525f1e9c408bd32409e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051d619d2c582bfcaa618694f85f9c28b4ae407867a5695ae4117f01c41f3317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AccessContextManagerAccessLevelCondition",
    "AccessContextManagerAccessLevelConditionConfig",
    "AccessContextManagerAccessLevelConditionDevicePolicy",
    "AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints",
    "AccessContextManagerAccessLevelConditionDevicePolicyOsConstraintsList",
    "AccessContextManagerAccessLevelConditionDevicePolicyOsConstraintsOutputReference",
    "AccessContextManagerAccessLevelConditionDevicePolicyOutputReference",
    "AccessContextManagerAccessLevelConditionTimeouts",
    "AccessContextManagerAccessLevelConditionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__43cdd759647c71fe7c4579b634facb3ed72bf434c2ffdccd492282f8f7b9616f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    access_level: builtins.str,
    device_policy: typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionDevicePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    required_access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9a82a9c12ac0d8f3b6d43e4f6460e40b77a941f0f9cea80c5279e733de4e322d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ba6b87220384ce384542e63945df8e4aa0625aed2bbe8b3c0b285cf6feb7c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cdb26aa79a7d9cfe5a5fee252cd7937b16549890660e9a089483657208752f7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48305faf69a54e167ce8bf2453de175a774054babfb147c2e9136d5c028da4b5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9874ff366cd8d226f637f0a6e424d3137034b1d69b77f308ccdfd4b7959c2c61(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0deed6d8d539c3858300e41d0cb33ac72f2fd41e4f60eda869827a1638ac3da(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ade261a40d712ca8f331f81301940be82701e5124e191b58378b3d3b1db4c2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35fc0a2065c3721c199e0de68120ab96706cb540fee955504264d77402b60e9c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    access_level: builtins.str,
    device_policy: typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionDevicePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_subnetworks: typing.Optional[typing.Sequence[builtins.str]] = None,
    members: typing.Optional[typing.Sequence[builtins.str]] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    required_access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a3709783bf6f0887f216447f7e91c6a7c686d87abc46f2376fc857706a7d53(
    *,
    allowed_device_management_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_encryption_statuses: typing.Optional[typing.Sequence[builtins.str]] = None,
    os_constraints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    require_admin_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_corp_owned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db5fd46796fb4ee3195141e733ab01f4dd2d13aa66aff9306f5fa5697ba7b45(
    *,
    os_type: builtins.str,
    minimum_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f11de8ed0db625c515e482ad31cdcfaab132c3f4ae68b4dbef0d5498e995b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695ef5abd15aea6c7d18cdd1e0bd754f5aac7a1e2af53069feb7c0d61228821f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa2429aba7f8d6eb66933809cca1d94c8ce0d384cc155f19a8d91fdd8f478da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e876b518a90b0e04b124905022926179999308e29b7ba5c1e38ed2144c3100a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e906de59fde763207711210b4fd4a9520f47b0af874bfa9f885a9e0921c65a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519e048ca9f605f4bc6007c209723ed7f541527eb9be9aed60f6a1cae56659ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7962514378535a2ddfe9636314b29113fbf33c16b8b2630982a316e9b8c3ed94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022aa6989bf1301fccd1d5442d186623d109aa1e2ee7d631ac32fadf14569392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6eb786888d3d3eda49dd8f9f32a805591c2248b93d108bc2ccbf6dd240e94e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48da05ca9e263127796a84911ebb3acee70e5ff1717e02ea84c9a64a32a11580(
    value: typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410e0a386035e448d206283a639667ff3ba2ac04cb2ef1c7690f25e1044a2a69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c149d298bad3bcf3c2ae2b571d820992c5bbf4c3205bc3e1ff4ea363b87b8b6e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerAccessLevelConditionDevicePolicyOsConstraints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0a0814a5606a6cb202ef7d07177285d0c343b6934dcb9e1b234996dc3f3a36(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70c403269310e14297463f20d368014dfffceec501460792df0f36d3ff99041(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0509f9b4e12507a66e6d28aa4f7b47b6f90666d41cd81bf4794cd635d3afbe26(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4378a34e77538b730605674bf58b0b8c41b668fd5d40d0573e7c4d00fd8da68(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e0f62cdb72bd0fe682cb6badaf030e0392383a75a21137ece23a55dbf75815(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8c8dcee3d30c1789c2d3df5744d79b6c0bbac8dd006a285b5c804633dda7eb(
    value: typing.Optional[AccessContextManagerAccessLevelConditionDevicePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15559ec8632c22e571597ee4624adbe3e45fc0ceead6defc6e5312d4e092043c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ab381bc501d6f03ed0788d8779ae53594b7fd399950697c2a72acba091fe06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4385d7cc430b91bd452c8ca5b3131d2715d2c77e73010f0f29633860934b4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84915b12c309c4030ac62afd09ea563dd4d7b593f73e525f1e9c408bd32409e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051d619d2c582bfcaa618694f85f9c28b4ae407867a5695ae4117f01c41f3317(
    value: typing.Optional[typing.Union[AccessContextManagerAccessLevelConditionTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
