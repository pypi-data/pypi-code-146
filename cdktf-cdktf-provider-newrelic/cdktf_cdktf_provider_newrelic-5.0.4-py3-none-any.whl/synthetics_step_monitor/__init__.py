'''
# `newrelic_synthetics_step_monitor`

Refer to the Terraform Registory for docs: [`newrelic_synthetics_step_monitor`](https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor).
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


class SyntheticsStepMonitor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.syntheticsStepMonitor.SyntheticsStepMonitor",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor newrelic_synthetics_step_monitor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        period: builtins.str,
        status: builtins.str,
        steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsStepMonitorSteps", typing.Dict[builtins.str, typing.Any]]]],
        account_id: typing.Optional[jsii.Number] = None,
        enable_screenshot_on_failure_and_script: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        location_private: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsStepMonitorLocationPrivate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        locations_public: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsStepMonitorTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor newrelic_synthetics_step_monitor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The title of this monitor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#name SyntheticsStepMonitor#name}
        :param period: The interval at which this monitor should run. Valid values are EVERY_MINUTE, EVERY_5_MINUTES, EVERY_10_MINUTES, EVERY_15_MINUTES, EVERY_30_MINUTES, EVERY_HOUR, EVERY_6_HOURS, EVERY_12_HOURS, or EVERY_DAY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#period SyntheticsStepMonitor#period}
        :param status: The monitor status (i.e. ENABLED, MUTED, DISABLED). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#status SyntheticsStepMonitor#status}
        :param steps: steps block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#steps SyntheticsStepMonitor#steps}
        :param account_id: ID of the newrelic account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#account_id SyntheticsStepMonitor#account_id}
        :param enable_screenshot_on_failure_and_script: Capture a screenshot during job execution. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#enable_screenshot_on_failure_and_script SyntheticsStepMonitor#enable_screenshot_on_failure_and_script}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#id SyntheticsStepMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location_private: location_private block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#location_private SyntheticsStepMonitor#location_private}
        :param locations_public: The public location(s) that the monitor will run jobs from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#locations_public SyntheticsStepMonitor#locations_public}
        :param tag: tag block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#tag SyntheticsStepMonitor#tag}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc923233235e10497ebac35ac56231f9dabdf5574df2595705ddc35a4fa9671)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SyntheticsStepMonitorConfig(
            name=name,
            period=period,
            status=status,
            steps=steps,
            account_id=account_id,
            enable_screenshot_on_failure_and_script=enable_screenshot_on_failure_and_script,
            id=id,
            location_private=location_private,
            locations_public=locations_public,
            tag=tag,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putLocationPrivate")
    def put_location_private(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsStepMonitorLocationPrivate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258d8f04f8ef6b633b9f88f1968ddd4e7853cc5f4468fd05e6e63aaa89f8458a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLocationPrivate", [value]))

    @jsii.member(jsii_name="putSteps")
    def put_steps(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsStepMonitorSteps", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f94e05c40539f63bb25c595a0d575325cd1e2c314dce0c5c4d90324fc3f360c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSteps", [value]))

    @jsii.member(jsii_name="putTag")
    def put_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsStepMonitorTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac57e99b3bf628fd8ca3d7c3a9e589fa9119ceed1d6f2511d889ef54faf4dc7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTag", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetEnableScreenshotOnFailureAndScript")
    def reset_enable_screenshot_on_failure_and_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableScreenshotOnFailureAndScript", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocationPrivate")
    def reset_location_private(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationPrivate", []))

    @jsii.member(jsii_name="resetLocationsPublic")
    def reset_locations_public(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationsPublic", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="guid")
    def guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guid"))

    @builtins.property
    @jsii.member(jsii_name="locationPrivate")
    def location_private(self) -> "SyntheticsStepMonitorLocationPrivateList":
        return typing.cast("SyntheticsStepMonitorLocationPrivateList", jsii.get(self, "locationPrivate"))

    @builtins.property
    @jsii.member(jsii_name="steps")
    def steps(self) -> "SyntheticsStepMonitorStepsList":
        return typing.cast("SyntheticsStepMonitorStepsList", jsii.get(self, "steps"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> "SyntheticsStepMonitorTagList":
        return typing.cast("SyntheticsStepMonitorTagList", jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableScreenshotOnFailureAndScriptInput")
    def enable_screenshot_on_failure_and_script_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableScreenshotOnFailureAndScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationPrivateInput")
    def location_private_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorLocationPrivate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorLocationPrivate"]]], jsii.get(self, "locationPrivateInput"))

    @builtins.property
    @jsii.member(jsii_name="locationsPublicInput")
    def locations_public_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsPublicInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="stepsInput")
    def steps_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorSteps"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorSteps"]]], jsii.get(self, "stepsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorTag"]]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859d800729816d374c29ea29b2092c6b1a63858e8dd28c92e9cd7eff11228235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="enableScreenshotOnFailureAndScript")
    def enable_screenshot_on_failure_and_script(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableScreenshotOnFailureAndScript"))

    @enable_screenshot_on_failure_and_script.setter
    def enable_screenshot_on_failure_and_script(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f536aaabe3d406ae9f9047775d6b798e2a154ae665fa7d196220c39445b005f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableScreenshotOnFailureAndScript", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33a825c7f6f8c589825c7ec25aa2f9fb2ef20ef2cc7eb2d6eb714f8a5b2f2d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="locationsPublic")
    def locations_public(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locationsPublic"))

    @locations_public.setter
    def locations_public(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c816237f77429479938b759077f2b7da5f7dbdea9ef05a97b909c62aa2b2d79a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationsPublic", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa028c166b1c6c380df3c76140754b9e264ad3a885033004f3634822c6c1f024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "period"))

    @period.setter
    def period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96591611592a396db147f81aae3cd774de8482582298da0be7d2e9bef68bed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900927aaa69d48d7145b98bc0e28c4795c5e6767e70f4567ffe896034199c4e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.syntheticsStepMonitor.SyntheticsStepMonitorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "period": "period",
        "status": "status",
        "steps": "steps",
        "account_id": "accountId",
        "enable_screenshot_on_failure_and_script": "enableScreenshotOnFailureAndScript",
        "id": "id",
        "location_private": "locationPrivate",
        "locations_public": "locationsPublic",
        "tag": "tag",
    },
)
class SyntheticsStepMonitorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        period: builtins.str,
        status: builtins.str,
        steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsStepMonitorSteps", typing.Dict[builtins.str, typing.Any]]]],
        account_id: typing.Optional[jsii.Number] = None,
        enable_screenshot_on_failure_and_script: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        location_private: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsStepMonitorLocationPrivate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        locations_public: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsStepMonitorTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The title of this monitor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#name SyntheticsStepMonitor#name}
        :param period: The interval at which this monitor should run. Valid values are EVERY_MINUTE, EVERY_5_MINUTES, EVERY_10_MINUTES, EVERY_15_MINUTES, EVERY_30_MINUTES, EVERY_HOUR, EVERY_6_HOURS, EVERY_12_HOURS, or EVERY_DAY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#period SyntheticsStepMonitor#period}
        :param status: The monitor status (i.e. ENABLED, MUTED, DISABLED). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#status SyntheticsStepMonitor#status}
        :param steps: steps block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#steps SyntheticsStepMonitor#steps}
        :param account_id: ID of the newrelic account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#account_id SyntheticsStepMonitor#account_id}
        :param enable_screenshot_on_failure_and_script: Capture a screenshot during job execution. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#enable_screenshot_on_failure_and_script SyntheticsStepMonitor#enable_screenshot_on_failure_and_script}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#id SyntheticsStepMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location_private: location_private block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#location_private SyntheticsStepMonitor#location_private}
        :param locations_public: The public location(s) that the monitor will run jobs from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#locations_public SyntheticsStepMonitor#locations_public}
        :param tag: tag block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#tag SyntheticsStepMonitor#tag}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2aca27aa0fc2a16beb135575334a964bd8103a5af68f048ab410ce76944d5c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument enable_screenshot_on_failure_and_script", value=enable_screenshot_on_failure_and_script, expected_type=type_hints["enable_screenshot_on_failure_and_script"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location_private", value=location_private, expected_type=type_hints["location_private"])
            check_type(argname="argument locations_public", value=locations_public, expected_type=type_hints["locations_public"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "period": period,
            "status": status,
            "steps": steps,
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
        if enable_screenshot_on_failure_and_script is not None:
            self._values["enable_screenshot_on_failure_and_script"] = enable_screenshot_on_failure_and_script
        if id is not None:
            self._values["id"] = id
        if location_private is not None:
            self._values["location_private"] = location_private
        if locations_public is not None:
            self._values["locations_public"] = locations_public
        if tag is not None:
            self._values["tag"] = tag

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
    def name(self) -> builtins.str:
        '''The title of this monitor.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#name SyntheticsStepMonitor#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> builtins.str:
        '''The interval at which this monitor should run.

        Valid values are EVERY_MINUTE, EVERY_5_MINUTES, EVERY_10_MINUTES, EVERY_15_MINUTES, EVERY_30_MINUTES, EVERY_HOUR, EVERY_6_HOURS, EVERY_12_HOURS, or EVERY_DAY.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#period SyntheticsStepMonitor#period}
        '''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status(self) -> builtins.str:
        '''The monitor status (i.e. ENABLED, MUTED, DISABLED).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#status SyntheticsStepMonitor#status}
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def steps(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorSteps"]]:
        '''steps block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#steps SyntheticsStepMonitor#steps}
        '''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorSteps"]], result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''ID of the newrelic account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#account_id SyntheticsStepMonitor#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_screenshot_on_failure_and_script(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Capture a screenshot during job execution.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#enable_screenshot_on_failure_and_script SyntheticsStepMonitor#enable_screenshot_on_failure_and_script}
        '''
        result = self._values.get("enable_screenshot_on_failure_and_script")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#id SyntheticsStepMonitor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location_private(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorLocationPrivate"]]]:
        '''location_private block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#location_private SyntheticsStepMonitor#location_private}
        '''
        result = self._values.get("location_private")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorLocationPrivate"]]], result)

    @builtins.property
    def locations_public(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The public location(s) that the monitor will run jobs from.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#locations_public SyntheticsStepMonitor#locations_public}
        '''
        result = self._values.get("locations_public")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorTag"]]]:
        '''tag block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#tag SyntheticsStepMonitor#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsStepMonitorTag"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsStepMonitorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.syntheticsStepMonitor.SyntheticsStepMonitorLocationPrivate",
    jsii_struct_bases=[],
    name_mapping={"guid": "guid", "vse_password": "vsePassword"},
)
class SyntheticsStepMonitorLocationPrivate:
    def __init__(
        self,
        *,
        guid: builtins.str,
        vse_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param guid: The unique identifier for the Synthetics private location in New Relic. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#guid SyntheticsStepMonitor#guid}
        :param vse_password: The location's Verified Script Execution password (Only necessary if Verified Script Execution is enabled for the location). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#vse_password SyntheticsStepMonitor#vse_password}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cdcebcf4575db280dba5ebf48c3c2bd90e815b47f4b97930462db577b968ff9)
            check_type(argname="argument guid", value=guid, expected_type=type_hints["guid"])
            check_type(argname="argument vse_password", value=vse_password, expected_type=type_hints["vse_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "guid": guid,
        }
        if vse_password is not None:
            self._values["vse_password"] = vse_password

    @builtins.property
    def guid(self) -> builtins.str:
        '''The unique identifier for the Synthetics private location in New Relic.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#guid SyntheticsStepMonitor#guid}
        '''
        result = self._values.get("guid")
        assert result is not None, "Required property 'guid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vse_password(self) -> typing.Optional[builtins.str]:
        '''The location's Verified Script Execution password (Only necessary if Verified Script Execution is enabled for the location).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#vse_password SyntheticsStepMonitor#vse_password}
        '''
        result = self._values.get("vse_password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsStepMonitorLocationPrivate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsStepMonitorLocationPrivateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.syntheticsStepMonitor.SyntheticsStepMonitorLocationPrivateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc5a7f2e9f458c50647dfe206a6826a89815fa7a1dce9e1debdf042b48ac4066)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SyntheticsStepMonitorLocationPrivateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be99044af70c7bbb0284ee54f63272b2cbada438bac3f8679a65add6517e79ee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsStepMonitorLocationPrivateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138e00d675bbc183d9263a933e3a2a27f048e281a2f183a444fff2dfcb25d2db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45ace2fcede0afdc1ae7190bf4d9a9b0f603c6692f41567525df7fc1f6c501d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86145cff3b502258dd2ea55208d15831eafaeb5c1a074f168606f15abe2f4397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorLocationPrivate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorLocationPrivate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorLocationPrivate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f86e5918e0c4ae4322b2b3bd968b9beb1dfc7ba55fd3675f28475695f0b334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsStepMonitorLocationPrivateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.syntheticsStepMonitor.SyntheticsStepMonitorLocationPrivateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__462424fd5dca80af5d6e5710d8aaa940470e6de6add824d9780c4cba8208e835)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetVsePassword")
    def reset_vse_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsePassword", []))

    @builtins.property
    @jsii.member(jsii_name="guidInput")
    def guid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "guidInput"))

    @builtins.property
    @jsii.member(jsii_name="vsePasswordInput")
    def vse_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vsePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="guid")
    def guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guid"))

    @guid.setter
    def guid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a30e7502f8ec46170c47994daa35cdd34bf570fb06d70f4f698bcc66b91739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guid", value)

    @builtins.property
    @jsii.member(jsii_name="vsePassword")
    def vse_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vsePassword"))

    @vse_password.setter
    def vse_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3ccefe5c5d9a7e0ff4045b734457c7ad93b2fe6ee064e74a266fd835007074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsePassword", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SyntheticsStepMonitorLocationPrivate, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SyntheticsStepMonitorLocationPrivate, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SyntheticsStepMonitorLocationPrivate, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd64b9451b3f575cbdc422cf3674ce1885e9468bdea9b4cba436a1b1c13919a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.syntheticsStepMonitor.SyntheticsStepMonitorSteps",
    jsii_struct_bases=[],
    name_mapping={"ordinal": "ordinal", "type": "type", "values": "values"},
)
class SyntheticsStepMonitorSteps:
    def __init__(
        self,
        *,
        ordinal: jsii.Number,
        type: builtins.str,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ordinal: The position of the step within the script ranging from 0-100. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#ordinal SyntheticsStepMonitor#ordinal}
        :param type: The type of step to be added to the script. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#type SyntheticsStepMonitor#type}
        :param values: The metadata values related to the check the step performs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#values SyntheticsStepMonitor#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248632e3c992d5a5c2ec919403a2a7b9b63931d2e6d35c72ffb1825d307bcf37)
            check_type(argname="argument ordinal", value=ordinal, expected_type=type_hints["ordinal"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ordinal": ordinal,
            "type": type,
        }
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def ordinal(self) -> jsii.Number:
        '''The position of the step within the script ranging from 0-100.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#ordinal SyntheticsStepMonitor#ordinal}
        '''
        result = self._values.get("ordinal")
        assert result is not None, "Required property 'ordinal' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of step to be added to the script.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#type SyntheticsStepMonitor#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The metadata values related to the check the step performs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#values SyntheticsStepMonitor#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsStepMonitorSteps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsStepMonitorStepsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.syntheticsStepMonitor.SyntheticsStepMonitorStepsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fbff69966565586b6afc596febe904ff1f358422ea63781f13a3be5c65d4a33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SyntheticsStepMonitorStepsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40dfe2c08c9f625a31461ee59f80b6aa310bd4e206dfffe5fdfc6dac3586ef2c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsStepMonitorStepsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25eaa4276e15aa80d6b821b3efe35daac048f7286f053db7d47f6461e1d5c69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9665b3e815c23f7736799c46901d3111a41d245a34714ef054337f0ee57fbd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__524ce797e2866003f41b8972a3ada417fe5d6f5a20b7da61c2c2028e1d16a5f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorSteps]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorSteps]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorSteps]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb04c8ccd03d22ac2e265be09eb0c2d2a988812b79d9db75b0d2e2fb53218dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsStepMonitorStepsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.syntheticsStepMonitor.SyntheticsStepMonitorStepsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4acd4e5db9bf159005e7189bb7b64fac1e95a34b04d77c40cfb58ee5b3fbb3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="ordinalInput")
    def ordinal_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ordinalInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="ordinal")
    def ordinal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ordinal"))

    @ordinal.setter
    def ordinal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec909960f850f9629284d81244b63d0854a10f060abb9b77477b3b9291e47c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ordinal", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8361a8a72e90004d53abf1f055d5b2f3ce88611132c8fbecffcf2a65bbeed88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2df667b632d7d04db47565f612a9c3190c1afef3f2ddccb657abf3c9cdc508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SyntheticsStepMonitorSteps, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SyntheticsStepMonitorSteps, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SyntheticsStepMonitorSteps, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64cd0bd7effa6e898097e3ea5be3b436dbd748eceb650ccab5779c56b5604d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.syntheticsStepMonitor.SyntheticsStepMonitorTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class SyntheticsStepMonitorTag:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Name of the tag key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#key SyntheticsStepMonitor#key}
        :param values: Values associated with the tag key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#values SyntheticsStepMonitor#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897c79b249acf8c79d7a6060b6ba55d89d87326e5111e765d12da1df3b02203b)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Name of the tag key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#key SyntheticsStepMonitor#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Values associated with the tag key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_step_monitor#values SyntheticsStepMonitor#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsStepMonitorTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsStepMonitorTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.syntheticsStepMonitor.SyntheticsStepMonitorTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f2f53a8c9d830061dd67335e8516857d6c80a00230d32934bf36276d4568507)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SyntheticsStepMonitorTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a9addee1e65132abc1eff251994b86ebca83cdc3344b3993e9f2f91be18d63)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsStepMonitorTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52c5cceb316ae1a1eb99cf38eb7904134150f823df40c86747933ab382883b0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2775e37bc51420bc3fc1c5ec693688eae084333abb04f872f056bf17f06730d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d8383dfe39f5e0a90ca7157e30db38e2ac12bf1cf3ee9bc940af285060ba828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f7095c548eabcc9e9c23f3e8c38a9dfcf860f3a3fb78c4f738781aa4721d9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsStepMonitorTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.syntheticsStepMonitor.SyntheticsStepMonitorTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc3f21d822d7c4f3e9fc9f960c6f016f29fbcf319ee963f32dfc0d49ce93aeb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0184f3151bee70fbcd4fcf7a3a00cfa73495b5346a08f23b84bbd0606e2cf834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502d066b407e2fb7a86aa84605e52321ce2125af7c4e8f8afcfed74aa1e40820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SyntheticsStepMonitorTag, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SyntheticsStepMonitorTag, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SyntheticsStepMonitorTag, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce0d59a5f6ed8a0542610b91e1c9472626743465bb7cc165830a1a3946aa93b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SyntheticsStepMonitor",
    "SyntheticsStepMonitorConfig",
    "SyntheticsStepMonitorLocationPrivate",
    "SyntheticsStepMonitorLocationPrivateList",
    "SyntheticsStepMonitorLocationPrivateOutputReference",
    "SyntheticsStepMonitorSteps",
    "SyntheticsStepMonitorStepsList",
    "SyntheticsStepMonitorStepsOutputReference",
    "SyntheticsStepMonitorTag",
    "SyntheticsStepMonitorTagList",
    "SyntheticsStepMonitorTagOutputReference",
]

publication.publish()

def _typecheckingstub__2bc923233235e10497ebac35ac56231f9dabdf5574df2595705ddc35a4fa9671(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    period: builtins.str,
    status: builtins.str,
    steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsStepMonitorSteps, typing.Dict[builtins.str, typing.Any]]]],
    account_id: typing.Optional[jsii.Number] = None,
    enable_screenshot_on_failure_and_script: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    location_private: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsStepMonitorLocationPrivate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    locations_public: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsStepMonitorTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__258d8f04f8ef6b633b9f88f1968ddd4e7853cc5f4468fd05e6e63aaa89f8458a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsStepMonitorLocationPrivate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f94e05c40539f63bb25c595a0d575325cd1e2c314dce0c5c4d90324fc3f360c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsStepMonitorSteps, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac57e99b3bf628fd8ca3d7c3a9e589fa9119ceed1d6f2511d889ef54faf4dc7f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsStepMonitorTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859d800729816d374c29ea29b2092c6b1a63858e8dd28c92e9cd7eff11228235(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f536aaabe3d406ae9f9047775d6b798e2a154ae665fa7d196220c39445b005f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33a825c7f6f8c589825c7ec25aa2f9fb2ef20ef2cc7eb2d6eb714f8a5b2f2d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c816237f77429479938b759077f2b7da5f7dbdea9ef05a97b909c62aa2b2d79a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa028c166b1c6c380df3c76140754b9e264ad3a885033004f3634822c6c1f024(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96591611592a396db147f81aae3cd774de8482582298da0be7d2e9bef68bed0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900927aaa69d48d7145b98bc0e28c4795c5e6767e70f4567ffe896034199c4e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2aca27aa0fc2a16beb135575334a964bd8103a5af68f048ab410ce76944d5c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    period: builtins.str,
    status: builtins.str,
    steps: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsStepMonitorSteps, typing.Dict[builtins.str, typing.Any]]]],
    account_id: typing.Optional[jsii.Number] = None,
    enable_screenshot_on_failure_and_script: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    location_private: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsStepMonitorLocationPrivate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    locations_public: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsStepMonitorTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cdcebcf4575db280dba5ebf48c3c2bd90e815b47f4b97930462db577b968ff9(
    *,
    guid: builtins.str,
    vse_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5a7f2e9f458c50647dfe206a6826a89815fa7a1dce9e1debdf042b48ac4066(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be99044af70c7bbb0284ee54f63272b2cbada438bac3f8679a65add6517e79ee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138e00d675bbc183d9263a933e3a2a27f048e281a2f183a444fff2dfcb25d2db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ace2fcede0afdc1ae7190bf4d9a9b0f603c6692f41567525df7fc1f6c501d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86145cff3b502258dd2ea55208d15831eafaeb5c1a074f168606f15abe2f4397(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f86e5918e0c4ae4322b2b3bd968b9beb1dfc7ba55fd3675f28475695f0b334(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorLocationPrivate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462424fd5dca80af5d6e5710d8aaa940470e6de6add824d9780c4cba8208e835(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a30e7502f8ec46170c47994daa35cdd34bf570fb06d70f4f698bcc66b91739(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3ccefe5c5d9a7e0ff4045b734457c7ad93b2fe6ee064e74a266fd835007074(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd64b9451b3f575cbdc422cf3674ce1885e9468bdea9b4cba436a1b1c13919a(
    value: typing.Optional[typing.Union[SyntheticsStepMonitorLocationPrivate, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248632e3c992d5a5c2ec919403a2a7b9b63931d2e6d35c72ffb1825d307bcf37(
    *,
    ordinal: jsii.Number,
    type: builtins.str,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fbff69966565586b6afc596febe904ff1f358422ea63781f13a3be5c65d4a33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40dfe2c08c9f625a31461ee59f80b6aa310bd4e206dfffe5fdfc6dac3586ef2c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25eaa4276e15aa80d6b821b3efe35daac048f7286f053db7d47f6461e1d5c69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9665b3e815c23f7736799c46901d3111a41d245a34714ef054337f0ee57fbd4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524ce797e2866003f41b8972a3ada417fe5d6f5a20b7da61c2c2028e1d16a5f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb04c8ccd03d22ac2e265be09eb0c2d2a988812b79d9db75b0d2e2fb53218dbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorSteps]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4acd4e5db9bf159005e7189bb7b64fac1e95a34b04d77c40cfb58ee5b3fbb3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec909960f850f9629284d81244b63d0854a10f060abb9b77477b3b9291e47c58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8361a8a72e90004d53abf1f055d5b2f3ce88611132c8fbecffcf2a65bbeed88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2df667b632d7d04db47565f612a9c3190c1afef3f2ddccb657abf3c9cdc508(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cd0bd7effa6e898097e3ea5be3b436dbd748eceb650ccab5779c56b5604d05(
    value: typing.Optional[typing.Union[SyntheticsStepMonitorSteps, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897c79b249acf8c79d7a6060b6ba55d89d87326e5111e765d12da1df3b02203b(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2f53a8c9d830061dd67335e8516857d6c80a00230d32934bf36276d4568507(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a9addee1e65132abc1eff251994b86ebca83cdc3344b3993e9f2f91be18d63(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c5cceb316ae1a1eb99cf38eb7904134150f823df40c86747933ab382883b0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2775e37bc51420bc3fc1c5ec693688eae084333abb04f872f056bf17f06730d5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d8383dfe39f5e0a90ca7157e30db38e2ac12bf1cf3ee9bc940af285060ba828(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f7095c548eabcc9e9c23f3e8c38a9dfcf860f3a3fb78c4f738781aa4721d9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsStepMonitorTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3f21d822d7c4f3e9fc9f960c6f016f29fbcf319ee963f32dfc0d49ce93aeb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0184f3151bee70fbcd4fcf7a3a00cfa73495b5346a08f23b84bbd0606e2cf834(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502d066b407e2fb7a86aa84605e52321ce2125af7c4e8f8afcfed74aa1e40820(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce0d59a5f6ed8a0542610b91e1c9472626743465bb7cc165830a1a3946aa93b(
    value: typing.Optional[typing.Union[SyntheticsStepMonitorTag, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
