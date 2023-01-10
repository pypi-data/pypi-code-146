'''
# `aws_cloudformation_stack_set_instance`

Refer to the Terraform Registory for docs: [`aws_cloudformation_stack_set_instance`](https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance).
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


class CloudformationStackSetInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudformationStackSetInstance.CloudformationStackSetInstance",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance aws_cloudformation_stack_set_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        stack_set_name: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        call_as: typing.Optional[builtins.str] = None,
        deployment_targets: typing.Optional[typing.Union["CloudformationStackSetInstanceDeploymentTargets", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        operation_preferences: typing.Optional[typing.Union["CloudformationStackSetInstanceOperationPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        parameter_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        retain_stack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["CloudformationStackSetInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance aws_cloudformation_stack_set_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param stack_set_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#stack_set_name CloudformationStackSetInstance#stack_set_name}.
        :param account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#account_id CloudformationStackSetInstance#account_id}.
        :param call_as: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#call_as CloudformationStackSetInstance#call_as}.
        :param deployment_targets: deployment_targets block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#deployment_targets CloudformationStackSetInstance#deployment_targets}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#id CloudformationStackSetInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operation_preferences: operation_preferences block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#operation_preferences CloudformationStackSetInstance#operation_preferences}
        :param parameter_overrides: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#parameter_overrides CloudformationStackSetInstance#parameter_overrides}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#region CloudformationStackSetInstance#region}.
        :param retain_stack: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#retain_stack CloudformationStackSetInstance#retain_stack}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#timeouts CloudformationStackSetInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61bca441a67a64ba5025d94ed4187929d70be0b4574e60901f495e8b696df177)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudformationStackSetInstanceConfig(
            stack_set_name=stack_set_name,
            account_id=account_id,
            call_as=call_as,
            deployment_targets=deployment_targets,
            id=id,
            operation_preferences=operation_preferences,
            parameter_overrides=parameter_overrides,
            region=region,
            retain_stack=retain_stack,
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

    @jsii.member(jsii_name="putDeploymentTargets")
    def put_deployment_targets(
        self,
        *,
        organizational_unit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param organizational_unit_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#organizational_unit_ids CloudformationStackSetInstance#organizational_unit_ids}.
        '''
        value = CloudformationStackSetInstanceDeploymentTargets(
            organizational_unit_ids=organizational_unit_ids
        )

        return typing.cast(None, jsii.invoke(self, "putDeploymentTargets", [value]))

    @jsii.member(jsii_name="putOperationPreferences")
    def put_operation_preferences(
        self,
        *,
        failure_tolerance_count: typing.Optional[jsii.Number] = None,
        failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
        max_concurrent_count: typing.Optional[jsii.Number] = None,
        max_concurrent_percentage: typing.Optional[jsii.Number] = None,
        region_concurrency_type: typing.Optional[builtins.str] = None,
        region_order: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param failure_tolerance_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#failure_tolerance_count CloudformationStackSetInstance#failure_tolerance_count}.
        :param failure_tolerance_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#failure_tolerance_percentage CloudformationStackSetInstance#failure_tolerance_percentage}.
        :param max_concurrent_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#max_concurrent_count CloudformationStackSetInstance#max_concurrent_count}.
        :param max_concurrent_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#max_concurrent_percentage CloudformationStackSetInstance#max_concurrent_percentage}.
        :param region_concurrency_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#region_concurrency_type CloudformationStackSetInstance#region_concurrency_type}.
        :param region_order: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#region_order CloudformationStackSetInstance#region_order}.
        '''
        value = CloudformationStackSetInstanceOperationPreferences(
            failure_tolerance_count=failure_tolerance_count,
            failure_tolerance_percentage=failure_tolerance_percentage,
            max_concurrent_count=max_concurrent_count,
            max_concurrent_percentage=max_concurrent_percentage,
            region_concurrency_type=region_concurrency_type,
            region_order=region_order,
        )

        return typing.cast(None, jsii.invoke(self, "putOperationPreferences", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#create CloudformationStackSetInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#delete CloudformationStackSetInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#update CloudformationStackSetInstance#update}.
        '''
        value = CloudformationStackSetInstanceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetCallAs")
    def reset_call_as(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCallAs", []))

    @jsii.member(jsii_name="resetDeploymentTargets")
    def reset_deployment_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentTargets", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOperationPreferences")
    def reset_operation_preferences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationPreferences", []))

    @jsii.member(jsii_name="resetParameterOverrides")
    def reset_parameter_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameterOverrides", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRetainStack")
    def reset_retain_stack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainStack", []))

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
    @jsii.member(jsii_name="deploymentTargets")
    def deployment_targets(
        self,
    ) -> "CloudformationStackSetInstanceDeploymentTargetsOutputReference":
        return typing.cast("CloudformationStackSetInstanceDeploymentTargetsOutputReference", jsii.get(self, "deploymentTargets"))

    @builtins.property
    @jsii.member(jsii_name="operationPreferences")
    def operation_preferences(
        self,
    ) -> "CloudformationStackSetInstanceOperationPreferencesOutputReference":
        return typing.cast("CloudformationStackSetInstanceOperationPreferencesOutputReference", jsii.get(self, "operationPreferences"))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitId")
    def organizational_unit_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationalUnitId"))

    @builtins.property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudformationStackSetInstanceTimeoutsOutputReference":
        return typing.cast("CloudformationStackSetInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="callAsInput")
    def call_as_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "callAsInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentTargetsInput")
    def deployment_targets_input(
        self,
    ) -> typing.Optional["CloudformationStackSetInstanceDeploymentTargets"]:
        return typing.cast(typing.Optional["CloudformationStackSetInstanceDeploymentTargets"], jsii.get(self, "deploymentTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="operationPreferencesInput")
    def operation_preferences_input(
        self,
    ) -> typing.Optional["CloudformationStackSetInstanceOperationPreferences"]:
        return typing.cast(typing.Optional["CloudformationStackSetInstanceOperationPreferences"], jsii.get(self, "operationPreferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterOverridesInput")
    def parameter_overrides_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parameterOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="retainStackInput")
    def retain_stack_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retainStackInput"))

    @builtins.property
    @jsii.member(jsii_name="stackSetNameInput")
    def stack_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stackSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["CloudformationStackSetInstanceTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["CloudformationStackSetInstanceTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a204d1e0d1391303ce7e1efb348dfc74620b1f995483726d44dd3e9e3dfb9d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="callAs")
    def call_as(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "callAs"))

    @call_as.setter
    def call_as(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89290d170e863571c2b4e798a4f9b9cdf6b280d2f03dc35f16933db1d63cbc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callAs", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f0da616d4704e17d2a99eb241c37a06b50a26b9bbb725cd7eca236b13b6b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="parameterOverrides")
    def parameter_overrides(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameterOverrides"))

    @parameter_overrides.setter
    def parameter_overrides(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d9c9a8e5d5aa871aad0d4fd3e55414f32d8d79b7066dea7f56dd875169d7f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterOverrides", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5b94c41ce76ed950e620efe8c46524e2add31c0503578c928cc5fc5cac4c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="retainStack")
    def retain_stack(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retainStack"))

    @retain_stack.setter
    def retain_stack(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9985cea8d7ddfce676826127fcdd98fad99eede1540b72192d1d70683bbd04b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainStack", value)

    @builtins.property
    @jsii.member(jsii_name="stackSetName")
    def stack_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackSetName"))

    @stack_set_name.setter
    def stack_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4b6ab62a3ec59a047e62d453dc30e306f1819197950a7b73c0f4fcbc1f5a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackSetName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudformationStackSetInstance.CloudformationStackSetInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "stack_set_name": "stackSetName",
        "account_id": "accountId",
        "call_as": "callAs",
        "deployment_targets": "deploymentTargets",
        "id": "id",
        "operation_preferences": "operationPreferences",
        "parameter_overrides": "parameterOverrides",
        "region": "region",
        "retain_stack": "retainStack",
        "timeouts": "timeouts",
    },
)
class CloudformationStackSetInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        stack_set_name: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        call_as: typing.Optional[builtins.str] = None,
        deployment_targets: typing.Optional[typing.Union["CloudformationStackSetInstanceDeploymentTargets", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        operation_preferences: typing.Optional[typing.Union["CloudformationStackSetInstanceOperationPreferences", typing.Dict[builtins.str, typing.Any]]] = None,
        parameter_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        retain_stack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["CloudformationStackSetInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param stack_set_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#stack_set_name CloudformationStackSetInstance#stack_set_name}.
        :param account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#account_id CloudformationStackSetInstance#account_id}.
        :param call_as: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#call_as CloudformationStackSetInstance#call_as}.
        :param deployment_targets: deployment_targets block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#deployment_targets CloudformationStackSetInstance#deployment_targets}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#id CloudformationStackSetInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operation_preferences: operation_preferences block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#operation_preferences CloudformationStackSetInstance#operation_preferences}
        :param parameter_overrides: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#parameter_overrides CloudformationStackSetInstance#parameter_overrides}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#region CloudformationStackSetInstance#region}.
        :param retain_stack: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#retain_stack CloudformationStackSetInstance#retain_stack}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#timeouts CloudformationStackSetInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(deployment_targets, dict):
            deployment_targets = CloudformationStackSetInstanceDeploymentTargets(**deployment_targets)
        if isinstance(operation_preferences, dict):
            operation_preferences = CloudformationStackSetInstanceOperationPreferences(**operation_preferences)
        if isinstance(timeouts, dict):
            timeouts = CloudformationStackSetInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec9fe139622773d750dae082b8b6ea1f8566872d27188c602f9722cc0578045)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument stack_set_name", value=stack_set_name, expected_type=type_hints["stack_set_name"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument call_as", value=call_as, expected_type=type_hints["call_as"])
            check_type(argname="argument deployment_targets", value=deployment_targets, expected_type=type_hints["deployment_targets"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument operation_preferences", value=operation_preferences, expected_type=type_hints["operation_preferences"])
            check_type(argname="argument parameter_overrides", value=parameter_overrides, expected_type=type_hints["parameter_overrides"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument retain_stack", value=retain_stack, expected_type=type_hints["retain_stack"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stack_set_name": stack_set_name,
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
        if call_as is not None:
            self._values["call_as"] = call_as
        if deployment_targets is not None:
            self._values["deployment_targets"] = deployment_targets
        if id is not None:
            self._values["id"] = id
        if operation_preferences is not None:
            self._values["operation_preferences"] = operation_preferences
        if parameter_overrides is not None:
            self._values["parameter_overrides"] = parameter_overrides
        if region is not None:
            self._values["region"] = region
        if retain_stack is not None:
            self._values["retain_stack"] = retain_stack
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
    def stack_set_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#stack_set_name CloudformationStackSetInstance#stack_set_name}.'''
        result = self._values.get("stack_set_name")
        assert result is not None, "Required property 'stack_set_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#account_id CloudformationStackSetInstance#account_id}.'''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def call_as(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#call_as CloudformationStackSetInstance#call_as}.'''
        result = self._values.get("call_as")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_targets(
        self,
    ) -> typing.Optional["CloudformationStackSetInstanceDeploymentTargets"]:
        '''deployment_targets block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#deployment_targets CloudformationStackSetInstance#deployment_targets}
        '''
        result = self._values.get("deployment_targets")
        return typing.cast(typing.Optional["CloudformationStackSetInstanceDeploymentTargets"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#id CloudformationStackSetInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation_preferences(
        self,
    ) -> typing.Optional["CloudformationStackSetInstanceOperationPreferences"]:
        '''operation_preferences block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#operation_preferences CloudformationStackSetInstance#operation_preferences}
        '''
        result = self._values.get("operation_preferences")
        return typing.cast(typing.Optional["CloudformationStackSetInstanceOperationPreferences"], result)

    @builtins.property
    def parameter_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#parameter_overrides CloudformationStackSetInstance#parameter_overrides}.'''
        result = self._values.get("parameter_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#region CloudformationStackSetInstance#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retain_stack(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#retain_stack CloudformationStackSetInstance#retain_stack}.'''
        result = self._values.get("retain_stack")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudformationStackSetInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#timeouts CloudformationStackSetInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudformationStackSetInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudformationStackSetInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudformationStackSetInstance.CloudformationStackSetInstanceDeploymentTargets",
    jsii_struct_bases=[],
    name_mapping={"organizational_unit_ids": "organizationalUnitIds"},
)
class CloudformationStackSetInstanceDeploymentTargets:
    def __init__(
        self,
        *,
        organizational_unit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param organizational_unit_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#organizational_unit_ids CloudformationStackSetInstance#organizational_unit_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e402b104e5e49cefbe01d706b6a167e681891958dc4aa1801ae1e0b3afcc3d)
            check_type(argname="argument organizational_unit_ids", value=organizational_unit_ids, expected_type=type_hints["organizational_unit_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if organizational_unit_ids is not None:
            self._values["organizational_unit_ids"] = organizational_unit_ids

    @builtins.property
    def organizational_unit_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#organizational_unit_ids CloudformationStackSetInstance#organizational_unit_ids}.'''
        result = self._values.get("organizational_unit_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudformationStackSetInstanceDeploymentTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudformationStackSetInstanceDeploymentTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudformationStackSetInstance.CloudformationStackSetInstanceDeploymentTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52ba6a2abe5b81b173d613979317774e4bba80c59e7912038f38d5e038c01ed0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOrganizationalUnitIds")
    def reset_organizational_unit_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationalUnitIds", []))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitIdsInput")
    def organizational_unit_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "organizationalUnitIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitIds")
    def organizational_unit_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "organizationalUnitIds"))

    @organizational_unit_ids.setter
    def organizational_unit_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3bd9578994414dc47aa0ab66a641779e00fdc63abd560a53d8e70f56e81227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnitIds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudformationStackSetInstanceDeploymentTargets]:
        return typing.cast(typing.Optional[CloudformationStackSetInstanceDeploymentTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudformationStackSetInstanceDeploymentTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117871081bbdb401a9ce6cbe4e6b41adf0b18cf8057f3855c7d8d1797c14d05a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudformationStackSetInstance.CloudformationStackSetInstanceOperationPreferences",
    jsii_struct_bases=[],
    name_mapping={
        "failure_tolerance_count": "failureToleranceCount",
        "failure_tolerance_percentage": "failureTolerancePercentage",
        "max_concurrent_count": "maxConcurrentCount",
        "max_concurrent_percentage": "maxConcurrentPercentage",
        "region_concurrency_type": "regionConcurrencyType",
        "region_order": "regionOrder",
    },
)
class CloudformationStackSetInstanceOperationPreferences:
    def __init__(
        self,
        *,
        failure_tolerance_count: typing.Optional[jsii.Number] = None,
        failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
        max_concurrent_count: typing.Optional[jsii.Number] = None,
        max_concurrent_percentage: typing.Optional[jsii.Number] = None,
        region_concurrency_type: typing.Optional[builtins.str] = None,
        region_order: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param failure_tolerance_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#failure_tolerance_count CloudformationStackSetInstance#failure_tolerance_count}.
        :param failure_tolerance_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#failure_tolerance_percentage CloudformationStackSetInstance#failure_tolerance_percentage}.
        :param max_concurrent_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#max_concurrent_count CloudformationStackSetInstance#max_concurrent_count}.
        :param max_concurrent_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#max_concurrent_percentage CloudformationStackSetInstance#max_concurrent_percentage}.
        :param region_concurrency_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#region_concurrency_type CloudformationStackSetInstance#region_concurrency_type}.
        :param region_order: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#region_order CloudformationStackSetInstance#region_order}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82e3f473acfcc95c49ca1502dd9f3ff711ec068357464aa72653a27da359046)
            check_type(argname="argument failure_tolerance_count", value=failure_tolerance_count, expected_type=type_hints["failure_tolerance_count"])
            check_type(argname="argument failure_tolerance_percentage", value=failure_tolerance_percentage, expected_type=type_hints["failure_tolerance_percentage"])
            check_type(argname="argument max_concurrent_count", value=max_concurrent_count, expected_type=type_hints["max_concurrent_count"])
            check_type(argname="argument max_concurrent_percentage", value=max_concurrent_percentage, expected_type=type_hints["max_concurrent_percentage"])
            check_type(argname="argument region_concurrency_type", value=region_concurrency_type, expected_type=type_hints["region_concurrency_type"])
            check_type(argname="argument region_order", value=region_order, expected_type=type_hints["region_order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failure_tolerance_count is not None:
            self._values["failure_tolerance_count"] = failure_tolerance_count
        if failure_tolerance_percentage is not None:
            self._values["failure_tolerance_percentage"] = failure_tolerance_percentage
        if max_concurrent_count is not None:
            self._values["max_concurrent_count"] = max_concurrent_count
        if max_concurrent_percentage is not None:
            self._values["max_concurrent_percentage"] = max_concurrent_percentage
        if region_concurrency_type is not None:
            self._values["region_concurrency_type"] = region_concurrency_type
        if region_order is not None:
            self._values["region_order"] = region_order

    @builtins.property
    def failure_tolerance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#failure_tolerance_count CloudformationStackSetInstance#failure_tolerance_count}.'''
        result = self._values.get("failure_tolerance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def failure_tolerance_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#failure_tolerance_percentage CloudformationStackSetInstance#failure_tolerance_percentage}.'''
        result = self._values.get("failure_tolerance_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_concurrent_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#max_concurrent_count CloudformationStackSetInstance#max_concurrent_count}.'''
        result = self._values.get("max_concurrent_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_concurrent_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#max_concurrent_percentage CloudformationStackSetInstance#max_concurrent_percentage}.'''
        result = self._values.get("max_concurrent_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region_concurrency_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#region_concurrency_type CloudformationStackSetInstance#region_concurrency_type}.'''
        result = self._values.get("region_concurrency_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_order(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#region_order CloudformationStackSetInstance#region_order}.'''
        result = self._values.get("region_order")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudformationStackSetInstanceOperationPreferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudformationStackSetInstanceOperationPreferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudformationStackSetInstance.CloudformationStackSetInstanceOperationPreferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2636dc59bceb6d1b9c37cb491ba05a062711c29a5238d457bd700255f9196148)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFailureToleranceCount")
    def reset_failure_tolerance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureToleranceCount", []))

    @jsii.member(jsii_name="resetFailureTolerancePercentage")
    def reset_failure_tolerance_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureTolerancePercentage", []))

    @jsii.member(jsii_name="resetMaxConcurrentCount")
    def reset_max_concurrent_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentCount", []))

    @jsii.member(jsii_name="resetMaxConcurrentPercentage")
    def reset_max_concurrent_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentPercentage", []))

    @jsii.member(jsii_name="resetRegionConcurrencyType")
    def reset_region_concurrency_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionConcurrencyType", []))

    @jsii.member(jsii_name="resetRegionOrder")
    def reset_region_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionOrder", []))

    @builtins.property
    @jsii.member(jsii_name="failureToleranceCountInput")
    def failure_tolerance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureToleranceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="failureTolerancePercentageInput")
    def failure_tolerance_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureTolerancePercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentCountInput")
    def max_concurrent_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentPercentageInput")
    def max_concurrent_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="regionConcurrencyTypeInput")
    def region_concurrency_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionConcurrencyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="regionOrderInput")
    def region_order_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "regionOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="failureToleranceCount")
    def failure_tolerance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureToleranceCount"))

    @failure_tolerance_count.setter
    def failure_tolerance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3efb125e0fa2e8c984512e25d6a5592b50469d87a81d0a98fbbfd85bcbc9f6d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureToleranceCount", value)

    @builtins.property
    @jsii.member(jsii_name="failureTolerancePercentage")
    def failure_tolerance_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureTolerancePercentage"))

    @failure_tolerance_percentage.setter
    def failure_tolerance_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43335b850ecf0a2e6fe293232bacb38f6f7c9227caeb4ebdc605143029a6bb6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureTolerancePercentage", value)

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentCount")
    def max_concurrent_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentCount"))

    @max_concurrent_count.setter
    def max_concurrent_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e53e8a038ffb7e50ed0346589c9672b61720802154cea23b499b4e24606b095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentCount", value)

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentPercentage")
    def max_concurrent_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentPercentage"))

    @max_concurrent_percentage.setter
    def max_concurrent_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b1aeb598e98384466bda9574d3464d131d35b9331e86d6d7c5fadb7a3f3507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentPercentage", value)

    @builtins.property
    @jsii.member(jsii_name="regionConcurrencyType")
    def region_concurrency_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionConcurrencyType"))

    @region_concurrency_type.setter
    def region_concurrency_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47234fd29ff9e26e581d987479b34ade792aed0229064f91b23bec21ef84b390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionConcurrencyType", value)

    @builtins.property
    @jsii.member(jsii_name="regionOrder")
    def region_order(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regionOrder"))

    @region_order.setter
    def region_order(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d558a657fd6b02f672e4454b82240d9d096e9a86b2d1ed1179fed4f6474af0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionOrder", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudformationStackSetInstanceOperationPreferences]:
        return typing.cast(typing.Optional[CloudformationStackSetInstanceOperationPreferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudformationStackSetInstanceOperationPreferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c210f6a350e1722ee58177871693af4d2e0da6522bfd81d7f5fed25d825247e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudformationStackSetInstance.CloudformationStackSetInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudformationStackSetInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#create CloudformationStackSetInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#delete CloudformationStackSetInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#update CloudformationStackSetInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04bd20a007d252559a6a52c1ca30ed79c3a030b97f2091519ffb23fee5e19f2)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#create CloudformationStackSetInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#delete CloudformationStackSetInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudformation_stack_set_instance#update CloudformationStackSetInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudformationStackSetInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudformationStackSetInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudformationStackSetInstance.CloudformationStackSetInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5586e1ad3c3f61c787e02fd7c26827d3bf5d485d4639529e149c8baec15f884b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__99aa74d179ebe492c42a86667eb4effc0a7699f5c0509fea305d78966e97b8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ee71e078b1a308d877d8833a42de4339e2fbbdc2fda60ab10a58b53b6637b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fb6b5f1ecdc3c68b6a6c6c5aeac6a633742fae6874f7094c954f8693990655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CloudformationStackSetInstanceTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CloudformationStackSetInstanceTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CloudformationStackSetInstanceTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8115c97a274831b932231adfb27eafa783b91909780ef50361c72558214186fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CloudformationStackSetInstance",
    "CloudformationStackSetInstanceConfig",
    "CloudformationStackSetInstanceDeploymentTargets",
    "CloudformationStackSetInstanceDeploymentTargetsOutputReference",
    "CloudformationStackSetInstanceOperationPreferences",
    "CloudformationStackSetInstanceOperationPreferencesOutputReference",
    "CloudformationStackSetInstanceTimeouts",
    "CloudformationStackSetInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__61bca441a67a64ba5025d94ed4187929d70be0b4574e60901f495e8b696df177(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    stack_set_name: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    call_as: typing.Optional[builtins.str] = None,
    deployment_targets: typing.Optional[typing.Union[CloudformationStackSetInstanceDeploymentTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    operation_preferences: typing.Optional[typing.Union[CloudformationStackSetInstanceOperationPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    parameter_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    retain_stack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[CloudformationStackSetInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a204d1e0d1391303ce7e1efb348dfc74620b1f995483726d44dd3e9e3dfb9d61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89290d170e863571c2b4e798a4f9b9cdf6b280d2f03dc35f16933db1d63cbc20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f0da616d4704e17d2a99eb241c37a06b50a26b9bbb725cd7eca236b13b6b74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d9c9a8e5d5aa871aad0d4fd3e55414f32d8d79b7066dea7f56dd875169d7f1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5b94c41ce76ed950e620efe8c46524e2add31c0503578c928cc5fc5cac4c1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9985cea8d7ddfce676826127fcdd98fad99eede1540b72192d1d70683bbd04b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4b6ab62a3ec59a047e62d453dc30e306f1819197950a7b73c0f4fcbc1f5a62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec9fe139622773d750dae082b8b6ea1f8566872d27188c602f9722cc0578045(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stack_set_name: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    call_as: typing.Optional[builtins.str] = None,
    deployment_targets: typing.Optional[typing.Union[CloudformationStackSetInstanceDeploymentTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    operation_preferences: typing.Optional[typing.Union[CloudformationStackSetInstanceOperationPreferences, typing.Dict[builtins.str, typing.Any]]] = None,
    parameter_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    retain_stack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[CloudformationStackSetInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e402b104e5e49cefbe01d706b6a167e681891958dc4aa1801ae1e0b3afcc3d(
    *,
    organizational_unit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ba6a2abe5b81b173d613979317774e4bba80c59e7912038f38d5e038c01ed0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3bd9578994414dc47aa0ab66a641779e00fdc63abd560a53d8e70f56e81227(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117871081bbdb401a9ce6cbe4e6b41adf0b18cf8057f3855c7d8d1797c14d05a(
    value: typing.Optional[CloudformationStackSetInstanceDeploymentTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82e3f473acfcc95c49ca1502dd9f3ff711ec068357464aa72653a27da359046(
    *,
    failure_tolerance_count: typing.Optional[jsii.Number] = None,
    failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
    max_concurrent_count: typing.Optional[jsii.Number] = None,
    max_concurrent_percentage: typing.Optional[jsii.Number] = None,
    region_concurrency_type: typing.Optional[builtins.str] = None,
    region_order: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2636dc59bceb6d1b9c37cb491ba05a062711c29a5238d457bd700255f9196148(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3efb125e0fa2e8c984512e25d6a5592b50469d87a81d0a98fbbfd85bcbc9f6d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43335b850ecf0a2e6fe293232bacb38f6f7c9227caeb4ebdc605143029a6bb6e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e53e8a038ffb7e50ed0346589c9672b61720802154cea23b499b4e24606b095(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b1aeb598e98384466bda9574d3464d131d35b9331e86d6d7c5fadb7a3f3507(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47234fd29ff9e26e581d987479b34ade792aed0229064f91b23bec21ef84b390(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d558a657fd6b02f672e4454b82240d9d096e9a86b2d1ed1179fed4f6474af0d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c210f6a350e1722ee58177871693af4d2e0da6522bfd81d7f5fed25d825247e(
    value: typing.Optional[CloudformationStackSetInstanceOperationPreferences],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04bd20a007d252559a6a52c1ca30ed79c3a030b97f2091519ffb23fee5e19f2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5586e1ad3c3f61c787e02fd7c26827d3bf5d485d4639529e149c8baec15f884b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99aa74d179ebe492c42a86667eb4effc0a7699f5c0509fea305d78966e97b8f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ee71e078b1a308d877d8833a42de4339e2fbbdc2fda60ab10a58b53b6637b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fb6b5f1ecdc3c68b6a6c6c5aeac6a633742fae6874f7094c954f8693990655(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8115c97a274831b932231adfb27eafa783b91909780ef50361c72558214186fb(
    value: typing.Optional[typing.Union[CloudformationStackSetInstanceTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
