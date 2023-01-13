'''
# `okta_security_notification_emails`

Refer to the Terraform Registory for docs: [`okta_security_notification_emails`](https://www.terraform.io/docs/providers/okta/r/security_notification_emails).
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


class SecurityNotificationEmails(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.securityNotificationEmails.SecurityNotificationEmails",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails okta_security_notification_emails}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        report_suspicious_activity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_email_for_factor_enrollment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_email_for_factor_reset_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_email_for_new_device_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_email_for_password_changed_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails okta_security_notification_emails} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#id SecurityNotificationEmails#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param report_suspicious_activity_enabled: Notifies end users about suspicious or unrecognized activity from their account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#report_suspicious_activity_enabled SecurityNotificationEmails#report_suspicious_activity_enabled}
        :param send_email_for_factor_enrollment_enabled: Notifies end users of any activity on their account related to MFA factor enrollment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_factor_enrollment_enabled SecurityNotificationEmails#send_email_for_factor_enrollment_enabled}
        :param send_email_for_factor_reset_enabled: Notifies end users that one or more factors have been reset for their account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_factor_reset_enabled SecurityNotificationEmails#send_email_for_factor_reset_enabled}
        :param send_email_for_new_device_enabled: Notifies end users about new sign-on activity. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_new_device_enabled SecurityNotificationEmails#send_email_for_new_device_enabled}
        :param send_email_for_password_changed_enabled: Notifies end users that the password for their account has changed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_password_changed_enabled SecurityNotificationEmails#send_email_for_password_changed_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f203d4baee6e5f4b7a37b40e906c899f0b441997135a70a081c36a9862d13fe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SecurityNotificationEmailsConfig(
            id=id,
            report_suspicious_activity_enabled=report_suspicious_activity_enabled,
            send_email_for_factor_enrollment_enabled=send_email_for_factor_enrollment_enabled,
            send_email_for_factor_reset_enabled=send_email_for_factor_reset_enabled,
            send_email_for_new_device_enabled=send_email_for_new_device_enabled,
            send_email_for_password_changed_enabled=send_email_for_password_changed_enabled,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetReportSuspiciousActivityEnabled")
    def reset_report_suspicious_activity_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReportSuspiciousActivityEnabled", []))

    @jsii.member(jsii_name="resetSendEmailForFactorEnrollmentEnabled")
    def reset_send_email_for_factor_enrollment_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendEmailForFactorEnrollmentEnabled", []))

    @jsii.member(jsii_name="resetSendEmailForFactorResetEnabled")
    def reset_send_email_for_factor_reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendEmailForFactorResetEnabled", []))

    @jsii.member(jsii_name="resetSendEmailForNewDeviceEnabled")
    def reset_send_email_for_new_device_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendEmailForNewDeviceEnabled", []))

    @jsii.member(jsii_name="resetSendEmailForPasswordChangedEnabled")
    def reset_send_email_for_password_changed_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendEmailForPasswordChangedEnabled", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="reportSuspiciousActivityEnabledInput")
    def report_suspicious_activity_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reportSuspiciousActivityEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sendEmailForFactorEnrollmentEnabledInput")
    def send_email_for_factor_enrollment_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendEmailForFactorEnrollmentEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sendEmailForFactorResetEnabledInput")
    def send_email_for_factor_reset_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendEmailForFactorResetEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sendEmailForNewDeviceEnabledInput")
    def send_email_for_new_device_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendEmailForNewDeviceEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sendEmailForPasswordChangedEnabledInput")
    def send_email_for_password_changed_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendEmailForPasswordChangedEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2076cf53196cc5886b8be9ce844d7c20f5d919f9f871d3e21631ba12336641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="reportSuspiciousActivityEnabled")
    def report_suspicious_activity_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reportSuspiciousActivityEnabled"))

    @report_suspicious_activity_enabled.setter
    def report_suspicious_activity_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecae12a1597a20594089159847a7b0f9f41367a0922a1755e82d7df1ff9af014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportSuspiciousActivityEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="sendEmailForFactorEnrollmentEnabled")
    def send_email_for_factor_enrollment_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendEmailForFactorEnrollmentEnabled"))

    @send_email_for_factor_enrollment_enabled.setter
    def send_email_for_factor_enrollment_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb98700bf56e4cad6ab56d72aa114e90e100148206e9bf1e5723aa17e9476351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendEmailForFactorEnrollmentEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="sendEmailForFactorResetEnabled")
    def send_email_for_factor_reset_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendEmailForFactorResetEnabled"))

    @send_email_for_factor_reset_enabled.setter
    def send_email_for_factor_reset_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bdf2e243edc111fa76fd17f1069ac94a925cca2ddb8a138ad5f411a5ec8db62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendEmailForFactorResetEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="sendEmailForNewDeviceEnabled")
    def send_email_for_new_device_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendEmailForNewDeviceEnabled"))

    @send_email_for_new_device_enabled.setter
    def send_email_for_new_device_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e20abe2efceb01c34a4cc807c0ef497fc32a8fcb9ae68ca3ab5d1813ba456c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendEmailForNewDeviceEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="sendEmailForPasswordChangedEnabled")
    def send_email_for_password_changed_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendEmailForPasswordChangedEnabled"))

    @send_email_for_password_changed_enabled.setter
    def send_email_for_password_changed_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9b8605db270e1b2a0dacdc1a7604feab7878d88264835512d5c0c812b490fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendEmailForPasswordChangedEnabled", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.securityNotificationEmails.SecurityNotificationEmailsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "report_suspicious_activity_enabled": "reportSuspiciousActivityEnabled",
        "send_email_for_factor_enrollment_enabled": "sendEmailForFactorEnrollmentEnabled",
        "send_email_for_factor_reset_enabled": "sendEmailForFactorResetEnabled",
        "send_email_for_new_device_enabled": "sendEmailForNewDeviceEnabled",
        "send_email_for_password_changed_enabled": "sendEmailForPasswordChangedEnabled",
    },
)
class SecurityNotificationEmailsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        report_suspicious_activity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_email_for_factor_enrollment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_email_for_factor_reset_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_email_for_new_device_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_email_for_password_changed_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#id SecurityNotificationEmails#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param report_suspicious_activity_enabled: Notifies end users about suspicious or unrecognized activity from their account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#report_suspicious_activity_enabled SecurityNotificationEmails#report_suspicious_activity_enabled}
        :param send_email_for_factor_enrollment_enabled: Notifies end users of any activity on their account related to MFA factor enrollment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_factor_enrollment_enabled SecurityNotificationEmails#send_email_for_factor_enrollment_enabled}
        :param send_email_for_factor_reset_enabled: Notifies end users that one or more factors have been reset for their account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_factor_reset_enabled SecurityNotificationEmails#send_email_for_factor_reset_enabled}
        :param send_email_for_new_device_enabled: Notifies end users about new sign-on activity. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_new_device_enabled SecurityNotificationEmails#send_email_for_new_device_enabled}
        :param send_email_for_password_changed_enabled: Notifies end users that the password for their account has changed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_password_changed_enabled SecurityNotificationEmails#send_email_for_password_changed_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d990f791d8cf6d495374bcf135b9712f98c4238fd028afdf9a71ca6ba9061470)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument report_suspicious_activity_enabled", value=report_suspicious_activity_enabled, expected_type=type_hints["report_suspicious_activity_enabled"])
            check_type(argname="argument send_email_for_factor_enrollment_enabled", value=send_email_for_factor_enrollment_enabled, expected_type=type_hints["send_email_for_factor_enrollment_enabled"])
            check_type(argname="argument send_email_for_factor_reset_enabled", value=send_email_for_factor_reset_enabled, expected_type=type_hints["send_email_for_factor_reset_enabled"])
            check_type(argname="argument send_email_for_new_device_enabled", value=send_email_for_new_device_enabled, expected_type=type_hints["send_email_for_new_device_enabled"])
            check_type(argname="argument send_email_for_password_changed_enabled", value=send_email_for_password_changed_enabled, expected_type=type_hints["send_email_for_password_changed_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if report_suspicious_activity_enabled is not None:
            self._values["report_suspicious_activity_enabled"] = report_suspicious_activity_enabled
        if send_email_for_factor_enrollment_enabled is not None:
            self._values["send_email_for_factor_enrollment_enabled"] = send_email_for_factor_enrollment_enabled
        if send_email_for_factor_reset_enabled is not None:
            self._values["send_email_for_factor_reset_enabled"] = send_email_for_factor_reset_enabled
        if send_email_for_new_device_enabled is not None:
            self._values["send_email_for_new_device_enabled"] = send_email_for_new_device_enabled
        if send_email_for_password_changed_enabled is not None:
            self._values["send_email_for_password_changed_enabled"] = send_email_for_password_changed_enabled

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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#id SecurityNotificationEmails#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def report_suspicious_activity_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Notifies end users about suspicious or unrecognized activity from their account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#report_suspicious_activity_enabled SecurityNotificationEmails#report_suspicious_activity_enabled}
        '''
        result = self._values.get("report_suspicious_activity_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_email_for_factor_enrollment_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Notifies end users of any activity on their account related to MFA factor enrollment.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_factor_enrollment_enabled SecurityNotificationEmails#send_email_for_factor_enrollment_enabled}
        '''
        result = self._values.get("send_email_for_factor_enrollment_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_email_for_factor_reset_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Notifies end users that one or more factors have been reset for their account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_factor_reset_enabled SecurityNotificationEmails#send_email_for_factor_reset_enabled}
        '''
        result = self._values.get("send_email_for_factor_reset_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_email_for_new_device_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Notifies end users about new sign-on activity.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_new_device_enabled SecurityNotificationEmails#send_email_for_new_device_enabled}
        '''
        result = self._values.get("send_email_for_new_device_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_email_for_password_changed_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Notifies end users that the password for their account has changed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/security_notification_emails#send_email_for_password_changed_enabled SecurityNotificationEmails#send_email_for_password_changed_enabled}
        '''
        result = self._values.get("send_email_for_password_changed_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityNotificationEmailsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SecurityNotificationEmails",
    "SecurityNotificationEmailsConfig",
]

publication.publish()

def _typecheckingstub__9f203d4baee6e5f4b7a37b40e906c899f0b441997135a70a081c36a9862d13fe(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    report_suspicious_activity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_email_for_factor_enrollment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_email_for_factor_reset_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_email_for_new_device_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_email_for_password_changed_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__3d2076cf53196cc5886b8be9ce844d7c20f5d919f9f871d3e21631ba12336641(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecae12a1597a20594089159847a7b0f9f41367a0922a1755e82d7df1ff9af014(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb98700bf56e4cad6ab56d72aa114e90e100148206e9bf1e5723aa17e9476351(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bdf2e243edc111fa76fd17f1069ac94a925cca2ddb8a138ad5f411a5ec8db62(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e20abe2efceb01c34a4cc807c0ef497fc32a8fcb9ae68ca3ab5d1813ba456c8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9b8605db270e1b2a0dacdc1a7604feab7878d88264835512d5c0c812b490fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d990f791d8cf6d495374bcf135b9712f98c4238fd028afdf9a71ca6ba9061470(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    report_suspicious_activity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_email_for_factor_enrollment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_email_for_factor_reset_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_email_for_new_device_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_email_for_password_changed_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
