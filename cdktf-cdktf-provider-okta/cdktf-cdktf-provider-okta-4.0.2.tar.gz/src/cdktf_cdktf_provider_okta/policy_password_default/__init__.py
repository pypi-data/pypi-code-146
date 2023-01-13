'''
# `okta_policy_password_default`

Refer to the Terraform Registory for docs: [`okta_policy_password_default`](https://www.terraform.io/docs/providers/okta/r/policy_password_default).
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


class PolicyPasswordDefault(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyPasswordDefault.PolicyPasswordDefault",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default okta_policy_password_default}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        call_recovery: typing.Optional[builtins.str] = None,
        email_recovery: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        password_auto_unlock_minutes: typing.Optional[jsii.Number] = None,
        password_dictionary_lookup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_exclude_first_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_exclude_last_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_exclude_username: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_expire_warn_days: typing.Optional[jsii.Number] = None,
        password_history_count: typing.Optional[jsii.Number] = None,
        password_lockout_notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
        password_max_age_days: typing.Optional[jsii.Number] = None,
        password_max_lockout_attempts: typing.Optional[jsii.Number] = None,
        password_min_age_minutes: typing.Optional[jsii.Number] = None,
        password_min_length: typing.Optional[jsii.Number] = None,
        password_min_lowercase: typing.Optional[jsii.Number] = None,
        password_min_number: typing.Optional[jsii.Number] = None,
        password_min_symbol: typing.Optional[jsii.Number] = None,
        password_min_uppercase: typing.Optional[jsii.Number] = None,
        password_show_lockout_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        question_min_length: typing.Optional[jsii.Number] = None,
        question_recovery: typing.Optional[builtins.str] = None,
        recovery_email_token: typing.Optional[jsii.Number] = None,
        skip_unlock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sms_recovery: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default okta_policy_password_default} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param call_recovery: Enable or disable voice call recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#call_recovery PolicyPasswordDefault#call_recovery}
        :param email_recovery: Enable or disable email password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#email_recovery PolicyPasswordDefault#email_recovery}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#id PolicyPasswordDefault#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password_auto_unlock_minutes: Number of minutes before a locked account is unlocked: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_auto_unlock_minutes PolicyPasswordDefault#password_auto_unlock_minutes}
        :param password_dictionary_lookup: Check Passwords Against Common Password Dictionary. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_dictionary_lookup PolicyPasswordDefault#password_dictionary_lookup}
        :param password_exclude_first_name: User firstName attribute must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_exclude_first_name PolicyPasswordDefault#password_exclude_first_name}
        :param password_exclude_last_name: User lastName attribute must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_exclude_last_name PolicyPasswordDefault#password_exclude_last_name}
        :param password_exclude_username: If the user name must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_exclude_username PolicyPasswordDefault#password_exclude_username}
        :param password_expire_warn_days: Length in days a user will be warned before password expiry: 0 = no warning. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_expire_warn_days PolicyPasswordDefault#password_expire_warn_days}
        :param password_history_count: Number of distinct passwords that must be created before they can be reused: 0 = none. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_history_count PolicyPasswordDefault#password_history_count}
        :param password_lockout_notification_channels: Notification channels to use to notify a user when their account has been locked. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_lockout_notification_channels PolicyPasswordDefault#password_lockout_notification_channels}
        :param password_max_age_days: Length in days a password is valid before expiry: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_max_age_days PolicyPasswordDefault#password_max_age_days}
        :param password_max_lockout_attempts: Number of unsuccessful login attempts allowed before lockout: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_max_lockout_attempts PolicyPasswordDefault#password_max_lockout_attempts}
        :param password_min_age_minutes: Minimum time interval in minutes between password changes: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_age_minutes PolicyPasswordDefault#password_min_age_minutes}
        :param password_min_length: Minimum password length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_length PolicyPasswordDefault#password_min_length}
        :param password_min_lowercase: If a password must contain at least one lower case letter: 0 = no, 1 = yes. Default = 1 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_lowercase PolicyPasswordDefault#password_min_lowercase}
        :param password_min_number: If a password must contain at least one number: 0 = no, 1 = yes. Default = 1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_number PolicyPasswordDefault#password_min_number}
        :param password_min_symbol: If a password must contain at least one symbol (!@#$%^&*): 0 = no, 1 = yes. Default = 1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_symbol PolicyPasswordDefault#password_min_symbol}
        :param password_min_uppercase: If a password must contain at least one upper case letter: 0 = no, 1 = yes. Default = 1 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_uppercase PolicyPasswordDefault#password_min_uppercase}
        :param password_show_lockout_failures: If a user should be informed when their account is locked. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_show_lockout_failures PolicyPasswordDefault#password_show_lockout_failures}
        :param question_min_length: Min length of the password recovery question answer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#question_min_length PolicyPasswordDefault#question_min_length}
        :param question_recovery: Enable or disable security question password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#question_recovery PolicyPasswordDefault#question_recovery}
        :param recovery_email_token: Lifetime in minutes of the recovery email token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#recovery_email_token PolicyPasswordDefault#recovery_email_token}
        :param skip_unlock: When an Active Directory user is locked out of Okta, the Okta unlock operation should also attempt to unlock the user's Windows account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#skip_unlock PolicyPasswordDefault#skip_unlock}
        :param sms_recovery: Enable or disable SMS password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#sms_recovery PolicyPasswordDefault#sms_recovery}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517b7310311cf8648ed1a3f63922a95ab0393cbceb106f07434a44fd0d458791)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PolicyPasswordDefaultConfig(
            call_recovery=call_recovery,
            email_recovery=email_recovery,
            id=id,
            password_auto_unlock_minutes=password_auto_unlock_minutes,
            password_dictionary_lookup=password_dictionary_lookup,
            password_exclude_first_name=password_exclude_first_name,
            password_exclude_last_name=password_exclude_last_name,
            password_exclude_username=password_exclude_username,
            password_expire_warn_days=password_expire_warn_days,
            password_history_count=password_history_count,
            password_lockout_notification_channels=password_lockout_notification_channels,
            password_max_age_days=password_max_age_days,
            password_max_lockout_attempts=password_max_lockout_attempts,
            password_min_age_minutes=password_min_age_minutes,
            password_min_length=password_min_length,
            password_min_lowercase=password_min_lowercase,
            password_min_number=password_min_number,
            password_min_symbol=password_min_symbol,
            password_min_uppercase=password_min_uppercase,
            password_show_lockout_failures=password_show_lockout_failures,
            question_min_length=question_min_length,
            question_recovery=question_recovery,
            recovery_email_token=recovery_email_token,
            skip_unlock=skip_unlock,
            sms_recovery=sms_recovery,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetCallRecovery")
    def reset_call_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCallRecovery", []))

    @jsii.member(jsii_name="resetEmailRecovery")
    def reset_email_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailRecovery", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPasswordAutoUnlockMinutes")
    def reset_password_auto_unlock_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordAutoUnlockMinutes", []))

    @jsii.member(jsii_name="resetPasswordDictionaryLookup")
    def reset_password_dictionary_lookup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordDictionaryLookup", []))

    @jsii.member(jsii_name="resetPasswordExcludeFirstName")
    def reset_password_exclude_first_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordExcludeFirstName", []))

    @jsii.member(jsii_name="resetPasswordExcludeLastName")
    def reset_password_exclude_last_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordExcludeLastName", []))

    @jsii.member(jsii_name="resetPasswordExcludeUsername")
    def reset_password_exclude_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordExcludeUsername", []))

    @jsii.member(jsii_name="resetPasswordExpireWarnDays")
    def reset_password_expire_warn_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordExpireWarnDays", []))

    @jsii.member(jsii_name="resetPasswordHistoryCount")
    def reset_password_history_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordHistoryCount", []))

    @jsii.member(jsii_name="resetPasswordLockoutNotificationChannels")
    def reset_password_lockout_notification_channels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordLockoutNotificationChannels", []))

    @jsii.member(jsii_name="resetPasswordMaxAgeDays")
    def reset_password_max_age_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordMaxAgeDays", []))

    @jsii.member(jsii_name="resetPasswordMaxLockoutAttempts")
    def reset_password_max_lockout_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordMaxLockoutAttempts", []))

    @jsii.member(jsii_name="resetPasswordMinAgeMinutes")
    def reset_password_min_age_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordMinAgeMinutes", []))

    @jsii.member(jsii_name="resetPasswordMinLength")
    def reset_password_min_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordMinLength", []))

    @jsii.member(jsii_name="resetPasswordMinLowercase")
    def reset_password_min_lowercase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordMinLowercase", []))

    @jsii.member(jsii_name="resetPasswordMinNumber")
    def reset_password_min_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordMinNumber", []))

    @jsii.member(jsii_name="resetPasswordMinSymbol")
    def reset_password_min_symbol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordMinSymbol", []))

    @jsii.member(jsii_name="resetPasswordMinUppercase")
    def reset_password_min_uppercase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordMinUppercase", []))

    @jsii.member(jsii_name="resetPasswordShowLockoutFailures")
    def reset_password_show_lockout_failures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordShowLockoutFailures", []))

    @jsii.member(jsii_name="resetQuestionMinLength")
    def reset_question_min_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuestionMinLength", []))

    @jsii.member(jsii_name="resetQuestionRecovery")
    def reset_question_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuestionRecovery", []))

    @jsii.member(jsii_name="resetRecoveryEmailToken")
    def reset_recovery_email_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryEmailToken", []))

    @jsii.member(jsii_name="resetSkipUnlock")
    def reset_skip_unlock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipUnlock", []))

    @jsii.member(jsii_name="resetSmsRecovery")
    def reset_sms_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmsRecovery", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="defaultAuthProvider")
    def default_auth_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultAuthProvider"))

    @builtins.property
    @jsii.member(jsii_name="defaultIncludedGroupId")
    def default_included_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultIncludedGroupId"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="callRecoveryInput")
    def call_recovery_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "callRecoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="emailRecoveryInput")
    def email_recovery_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailRecoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordAutoUnlockMinutesInput")
    def password_auto_unlock_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordAutoUnlockMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordDictionaryLookupInput")
    def password_dictionary_lookup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordDictionaryLookupInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordExcludeFirstNameInput")
    def password_exclude_first_name_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordExcludeFirstNameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordExcludeLastNameInput")
    def password_exclude_last_name_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordExcludeLastNameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordExcludeUsernameInput")
    def password_exclude_username_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordExcludeUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordExpireWarnDaysInput")
    def password_expire_warn_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordExpireWarnDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordHistoryCountInput")
    def password_history_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordHistoryCountInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordLockoutNotificationChannelsInput")
    def password_lockout_notification_channels_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "passwordLockoutNotificationChannelsInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordMaxAgeDaysInput")
    def password_max_age_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordMaxAgeDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordMaxLockoutAttemptsInput")
    def password_max_lockout_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordMaxLockoutAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordMinAgeMinutesInput")
    def password_min_age_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordMinAgeMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordMinLengthInput")
    def password_min_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordMinLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordMinLowercaseInput")
    def password_min_lowercase_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordMinLowercaseInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordMinNumberInput")
    def password_min_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordMinNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordMinSymbolInput")
    def password_min_symbol_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordMinSymbolInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordMinUppercaseInput")
    def password_min_uppercase_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordMinUppercaseInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordShowLockoutFailuresInput")
    def password_show_lockout_failures_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordShowLockoutFailuresInput"))

    @builtins.property
    @jsii.member(jsii_name="questionMinLengthInput")
    def question_min_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "questionMinLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="questionRecoveryInput")
    def question_recovery_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "questionRecoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryEmailTokenInput")
    def recovery_email_token_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "recoveryEmailTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="skipUnlockInput")
    def skip_unlock_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipUnlockInput"))

    @builtins.property
    @jsii.member(jsii_name="smsRecoveryInput")
    def sms_recovery_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "smsRecoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="callRecovery")
    def call_recovery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "callRecovery"))

    @call_recovery.setter
    def call_recovery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818f9d145e431ecb2a4882e037101e4a8cf9f4d2f7937761b6bc4a3b8558d20e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callRecovery", value)

    @builtins.property
    @jsii.member(jsii_name="emailRecovery")
    def email_recovery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailRecovery"))

    @email_recovery.setter
    def email_recovery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d1139013ea5662985fad3fdbd64b1d41698788479b64d914a30d24fdcc0ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailRecovery", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271e911fbdd8a351431e30e67d8c6436246d94a1dcd0e11e923fff0e1005dd16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="passwordAutoUnlockMinutes")
    def password_auto_unlock_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordAutoUnlockMinutes"))

    @password_auto_unlock_minutes.setter
    def password_auto_unlock_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974f16ab4f56f1bed578b3678b1ed3fe4123bb1b70351a0b6a97d945a53b2635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordAutoUnlockMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="passwordDictionaryLookup")
    def password_dictionary_lookup(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordDictionaryLookup"))

    @password_dictionary_lookup.setter
    def password_dictionary_lookup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39871651e1a9aa9f6e49d81ea039a9038f2c9bfefe55158884bd7898beebe83c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordDictionaryLookup", value)

    @builtins.property
    @jsii.member(jsii_name="passwordExcludeFirstName")
    def password_exclude_first_name(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordExcludeFirstName"))

    @password_exclude_first_name.setter
    def password_exclude_first_name(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d84bb839e79012330f299f40432a3b7709f01fa01d3b706335e891971c97377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordExcludeFirstName", value)

    @builtins.property
    @jsii.member(jsii_name="passwordExcludeLastName")
    def password_exclude_last_name(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordExcludeLastName"))

    @password_exclude_last_name.setter
    def password_exclude_last_name(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85612e832b57a8acd45407f31f1c1df5f10656ca66c119bb4d4fd2e9c0db0c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordExcludeLastName", value)

    @builtins.property
    @jsii.member(jsii_name="passwordExcludeUsername")
    def password_exclude_username(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordExcludeUsername"))

    @password_exclude_username.setter
    def password_exclude_username(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c836a4af087ec8fb01795a2d13cd27d9e21ad94bb5433502ef0522c82d1d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordExcludeUsername", value)

    @builtins.property
    @jsii.member(jsii_name="passwordExpireWarnDays")
    def password_expire_warn_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordExpireWarnDays"))

    @password_expire_warn_days.setter
    def password_expire_warn_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55cbd87db54839c950dac73d1b8e00c73a806751a3387a0a94c2ab0c495586ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordExpireWarnDays", value)

    @builtins.property
    @jsii.member(jsii_name="passwordHistoryCount")
    def password_history_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordHistoryCount"))

    @password_history_count.setter
    def password_history_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02aabbccd09ecbb1511ffb47a744d7a7b8ae1808150fad264f9295dbd7d481f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordHistoryCount", value)

    @builtins.property
    @jsii.member(jsii_name="passwordLockoutNotificationChannels")
    def password_lockout_notification_channels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "passwordLockoutNotificationChannels"))

    @password_lockout_notification_channels.setter
    def password_lockout_notification_channels(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8cd83f22df6fcc5c8a9b87a47272ede58ee997c8a3cbea19ae41e7390547b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordLockoutNotificationChannels", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMaxAgeDays")
    def password_max_age_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMaxAgeDays"))

    @password_max_age_days.setter
    def password_max_age_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ada2cb5823a6ac2c26bec4bdc52adbf8bcc2399cbc40e01657e16cd7f8def8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMaxAgeDays", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMaxLockoutAttempts")
    def password_max_lockout_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMaxLockoutAttempts"))

    @password_max_lockout_attempts.setter
    def password_max_lockout_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98405dd049e32ffa41c350f7f07c2d62ee13e747cce9151e0e3b253534c844e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMaxLockoutAttempts", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinAgeMinutes")
    def password_min_age_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinAgeMinutes"))

    @password_min_age_minutes.setter
    def password_min_age_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bf3cd52f62fdbd14b1c97ba8593655aa8a537266dfb51b3c11fb9a671fff87a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMinAgeMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinLength")
    def password_min_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinLength"))

    @password_min_length.setter
    def password_min_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7e4a3694c376ffc9e65cd15a4e1c2440fea8719327d09c7376bba4136d151a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMinLength", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinLowercase")
    def password_min_lowercase(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinLowercase"))

    @password_min_lowercase.setter
    def password_min_lowercase(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d41a85a8e4b078ba9284541d691f0527bfa589fe6eb544487857e3387f9e0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMinLowercase", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinNumber")
    def password_min_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinNumber"))

    @password_min_number.setter
    def password_min_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab20120dfd7c15b604d1b098f97d008be7b13c81e8e4e7605744532b7ed7069b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMinNumber", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinSymbol")
    def password_min_symbol(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinSymbol"))

    @password_min_symbol.setter
    def password_min_symbol(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4339e8e996070ec4651d9134655b3d25ca5b2bac08a04c595684fa6236c824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMinSymbol", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinUppercase")
    def password_min_uppercase(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinUppercase"))

    @password_min_uppercase.setter
    def password_min_uppercase(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8939ce6eb743fc73910f74fa3f7eee2e3ce9ae5f70e1534498fe73904b5e7c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMinUppercase", value)

    @builtins.property
    @jsii.member(jsii_name="passwordShowLockoutFailures")
    def password_show_lockout_failures(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordShowLockoutFailures"))

    @password_show_lockout_failures.setter
    def password_show_lockout_failures(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f202ce451c96ae22e4c0b34743680e61f2122cf4b8ee480c490acd4af70c4b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordShowLockoutFailures", value)

    @builtins.property
    @jsii.member(jsii_name="questionMinLength")
    def question_min_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "questionMinLength"))

    @question_min_length.setter
    def question_min_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0360fc644fc4b0af22ec57c1abfaeafdb4129f5e44c6a7d0b6fe745ae1e0f0b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "questionMinLength", value)

    @builtins.property
    @jsii.member(jsii_name="questionRecovery")
    def question_recovery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "questionRecovery"))

    @question_recovery.setter
    def question_recovery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de14b6f429cb2c1111eae829c8dc1a1a319c75cb5a7d0db0e2462cd95925087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "questionRecovery", value)

    @builtins.property
    @jsii.member(jsii_name="recoveryEmailToken")
    def recovery_email_token(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "recoveryEmailToken"))

    @recovery_email_token.setter
    def recovery_email_token(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1daf006d12d67d974ba321b6cfa322b94fdd02736059a73901dbb7f6d5f3450b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryEmailToken", value)

    @builtins.property
    @jsii.member(jsii_name="skipUnlock")
    def skip_unlock(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipUnlock"))

    @skip_unlock.setter
    def skip_unlock(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46aa32e334df4e5021af300ae22de0d87146e9a286595a51019f40d8eae8309b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipUnlock", value)

    @builtins.property
    @jsii.member(jsii_name="smsRecovery")
    def sms_recovery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "smsRecovery"))

    @sms_recovery.setter
    def sms_recovery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917a1ac11b48ad54bdc31115c9080858b0beba696310e7d08d44a44fec3bfa6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smsRecovery", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyPasswordDefault.PolicyPasswordDefaultConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "call_recovery": "callRecovery",
        "email_recovery": "emailRecovery",
        "id": "id",
        "password_auto_unlock_minutes": "passwordAutoUnlockMinutes",
        "password_dictionary_lookup": "passwordDictionaryLookup",
        "password_exclude_first_name": "passwordExcludeFirstName",
        "password_exclude_last_name": "passwordExcludeLastName",
        "password_exclude_username": "passwordExcludeUsername",
        "password_expire_warn_days": "passwordExpireWarnDays",
        "password_history_count": "passwordHistoryCount",
        "password_lockout_notification_channels": "passwordLockoutNotificationChannels",
        "password_max_age_days": "passwordMaxAgeDays",
        "password_max_lockout_attempts": "passwordMaxLockoutAttempts",
        "password_min_age_minutes": "passwordMinAgeMinutes",
        "password_min_length": "passwordMinLength",
        "password_min_lowercase": "passwordMinLowercase",
        "password_min_number": "passwordMinNumber",
        "password_min_symbol": "passwordMinSymbol",
        "password_min_uppercase": "passwordMinUppercase",
        "password_show_lockout_failures": "passwordShowLockoutFailures",
        "question_min_length": "questionMinLength",
        "question_recovery": "questionRecovery",
        "recovery_email_token": "recoveryEmailToken",
        "skip_unlock": "skipUnlock",
        "sms_recovery": "smsRecovery",
    },
)
class PolicyPasswordDefaultConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        call_recovery: typing.Optional[builtins.str] = None,
        email_recovery: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        password_auto_unlock_minutes: typing.Optional[jsii.Number] = None,
        password_dictionary_lookup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_exclude_first_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_exclude_last_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_exclude_username: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_expire_warn_days: typing.Optional[jsii.Number] = None,
        password_history_count: typing.Optional[jsii.Number] = None,
        password_lockout_notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
        password_max_age_days: typing.Optional[jsii.Number] = None,
        password_max_lockout_attempts: typing.Optional[jsii.Number] = None,
        password_min_age_minutes: typing.Optional[jsii.Number] = None,
        password_min_length: typing.Optional[jsii.Number] = None,
        password_min_lowercase: typing.Optional[jsii.Number] = None,
        password_min_number: typing.Optional[jsii.Number] = None,
        password_min_symbol: typing.Optional[jsii.Number] = None,
        password_min_uppercase: typing.Optional[jsii.Number] = None,
        password_show_lockout_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        question_min_length: typing.Optional[jsii.Number] = None,
        question_recovery: typing.Optional[builtins.str] = None,
        recovery_email_token: typing.Optional[jsii.Number] = None,
        skip_unlock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sms_recovery: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param call_recovery: Enable or disable voice call recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#call_recovery PolicyPasswordDefault#call_recovery}
        :param email_recovery: Enable or disable email password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#email_recovery PolicyPasswordDefault#email_recovery}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#id PolicyPasswordDefault#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password_auto_unlock_minutes: Number of minutes before a locked account is unlocked: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_auto_unlock_minutes PolicyPasswordDefault#password_auto_unlock_minutes}
        :param password_dictionary_lookup: Check Passwords Against Common Password Dictionary. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_dictionary_lookup PolicyPasswordDefault#password_dictionary_lookup}
        :param password_exclude_first_name: User firstName attribute must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_exclude_first_name PolicyPasswordDefault#password_exclude_first_name}
        :param password_exclude_last_name: User lastName attribute must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_exclude_last_name PolicyPasswordDefault#password_exclude_last_name}
        :param password_exclude_username: If the user name must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_exclude_username PolicyPasswordDefault#password_exclude_username}
        :param password_expire_warn_days: Length in days a user will be warned before password expiry: 0 = no warning. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_expire_warn_days PolicyPasswordDefault#password_expire_warn_days}
        :param password_history_count: Number of distinct passwords that must be created before they can be reused: 0 = none. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_history_count PolicyPasswordDefault#password_history_count}
        :param password_lockout_notification_channels: Notification channels to use to notify a user when their account has been locked. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_lockout_notification_channels PolicyPasswordDefault#password_lockout_notification_channels}
        :param password_max_age_days: Length in days a password is valid before expiry: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_max_age_days PolicyPasswordDefault#password_max_age_days}
        :param password_max_lockout_attempts: Number of unsuccessful login attempts allowed before lockout: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_max_lockout_attempts PolicyPasswordDefault#password_max_lockout_attempts}
        :param password_min_age_minutes: Minimum time interval in minutes between password changes: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_age_minutes PolicyPasswordDefault#password_min_age_minutes}
        :param password_min_length: Minimum password length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_length PolicyPasswordDefault#password_min_length}
        :param password_min_lowercase: If a password must contain at least one lower case letter: 0 = no, 1 = yes. Default = 1 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_lowercase PolicyPasswordDefault#password_min_lowercase}
        :param password_min_number: If a password must contain at least one number: 0 = no, 1 = yes. Default = 1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_number PolicyPasswordDefault#password_min_number}
        :param password_min_symbol: If a password must contain at least one symbol (!@#$%^&*): 0 = no, 1 = yes. Default = 1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_symbol PolicyPasswordDefault#password_min_symbol}
        :param password_min_uppercase: If a password must contain at least one upper case letter: 0 = no, 1 = yes. Default = 1 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_uppercase PolicyPasswordDefault#password_min_uppercase}
        :param password_show_lockout_failures: If a user should be informed when their account is locked. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_show_lockout_failures PolicyPasswordDefault#password_show_lockout_failures}
        :param question_min_length: Min length of the password recovery question answer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#question_min_length PolicyPasswordDefault#question_min_length}
        :param question_recovery: Enable or disable security question password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#question_recovery PolicyPasswordDefault#question_recovery}
        :param recovery_email_token: Lifetime in minutes of the recovery email token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#recovery_email_token PolicyPasswordDefault#recovery_email_token}
        :param skip_unlock: When an Active Directory user is locked out of Okta, the Okta unlock operation should also attempt to unlock the user's Windows account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#skip_unlock PolicyPasswordDefault#skip_unlock}
        :param sms_recovery: Enable or disable SMS password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#sms_recovery PolicyPasswordDefault#sms_recovery}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9167266e245f532f14b7cd84bfaa2d9bc2ce8ca8c73002bff179a936d393998a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument call_recovery", value=call_recovery, expected_type=type_hints["call_recovery"])
            check_type(argname="argument email_recovery", value=email_recovery, expected_type=type_hints["email_recovery"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument password_auto_unlock_minutes", value=password_auto_unlock_minutes, expected_type=type_hints["password_auto_unlock_minutes"])
            check_type(argname="argument password_dictionary_lookup", value=password_dictionary_lookup, expected_type=type_hints["password_dictionary_lookup"])
            check_type(argname="argument password_exclude_first_name", value=password_exclude_first_name, expected_type=type_hints["password_exclude_first_name"])
            check_type(argname="argument password_exclude_last_name", value=password_exclude_last_name, expected_type=type_hints["password_exclude_last_name"])
            check_type(argname="argument password_exclude_username", value=password_exclude_username, expected_type=type_hints["password_exclude_username"])
            check_type(argname="argument password_expire_warn_days", value=password_expire_warn_days, expected_type=type_hints["password_expire_warn_days"])
            check_type(argname="argument password_history_count", value=password_history_count, expected_type=type_hints["password_history_count"])
            check_type(argname="argument password_lockout_notification_channels", value=password_lockout_notification_channels, expected_type=type_hints["password_lockout_notification_channels"])
            check_type(argname="argument password_max_age_days", value=password_max_age_days, expected_type=type_hints["password_max_age_days"])
            check_type(argname="argument password_max_lockout_attempts", value=password_max_lockout_attempts, expected_type=type_hints["password_max_lockout_attempts"])
            check_type(argname="argument password_min_age_minutes", value=password_min_age_minutes, expected_type=type_hints["password_min_age_minutes"])
            check_type(argname="argument password_min_length", value=password_min_length, expected_type=type_hints["password_min_length"])
            check_type(argname="argument password_min_lowercase", value=password_min_lowercase, expected_type=type_hints["password_min_lowercase"])
            check_type(argname="argument password_min_number", value=password_min_number, expected_type=type_hints["password_min_number"])
            check_type(argname="argument password_min_symbol", value=password_min_symbol, expected_type=type_hints["password_min_symbol"])
            check_type(argname="argument password_min_uppercase", value=password_min_uppercase, expected_type=type_hints["password_min_uppercase"])
            check_type(argname="argument password_show_lockout_failures", value=password_show_lockout_failures, expected_type=type_hints["password_show_lockout_failures"])
            check_type(argname="argument question_min_length", value=question_min_length, expected_type=type_hints["question_min_length"])
            check_type(argname="argument question_recovery", value=question_recovery, expected_type=type_hints["question_recovery"])
            check_type(argname="argument recovery_email_token", value=recovery_email_token, expected_type=type_hints["recovery_email_token"])
            check_type(argname="argument skip_unlock", value=skip_unlock, expected_type=type_hints["skip_unlock"])
            check_type(argname="argument sms_recovery", value=sms_recovery, expected_type=type_hints["sms_recovery"])
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
        if call_recovery is not None:
            self._values["call_recovery"] = call_recovery
        if email_recovery is not None:
            self._values["email_recovery"] = email_recovery
        if id is not None:
            self._values["id"] = id
        if password_auto_unlock_minutes is not None:
            self._values["password_auto_unlock_minutes"] = password_auto_unlock_minutes
        if password_dictionary_lookup is not None:
            self._values["password_dictionary_lookup"] = password_dictionary_lookup
        if password_exclude_first_name is not None:
            self._values["password_exclude_first_name"] = password_exclude_first_name
        if password_exclude_last_name is not None:
            self._values["password_exclude_last_name"] = password_exclude_last_name
        if password_exclude_username is not None:
            self._values["password_exclude_username"] = password_exclude_username
        if password_expire_warn_days is not None:
            self._values["password_expire_warn_days"] = password_expire_warn_days
        if password_history_count is not None:
            self._values["password_history_count"] = password_history_count
        if password_lockout_notification_channels is not None:
            self._values["password_lockout_notification_channels"] = password_lockout_notification_channels
        if password_max_age_days is not None:
            self._values["password_max_age_days"] = password_max_age_days
        if password_max_lockout_attempts is not None:
            self._values["password_max_lockout_attempts"] = password_max_lockout_attempts
        if password_min_age_minutes is not None:
            self._values["password_min_age_minutes"] = password_min_age_minutes
        if password_min_length is not None:
            self._values["password_min_length"] = password_min_length
        if password_min_lowercase is not None:
            self._values["password_min_lowercase"] = password_min_lowercase
        if password_min_number is not None:
            self._values["password_min_number"] = password_min_number
        if password_min_symbol is not None:
            self._values["password_min_symbol"] = password_min_symbol
        if password_min_uppercase is not None:
            self._values["password_min_uppercase"] = password_min_uppercase
        if password_show_lockout_failures is not None:
            self._values["password_show_lockout_failures"] = password_show_lockout_failures
        if question_min_length is not None:
            self._values["question_min_length"] = question_min_length
        if question_recovery is not None:
            self._values["question_recovery"] = question_recovery
        if recovery_email_token is not None:
            self._values["recovery_email_token"] = recovery_email_token
        if skip_unlock is not None:
            self._values["skip_unlock"] = skip_unlock
        if sms_recovery is not None:
            self._values["sms_recovery"] = sms_recovery

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
    def call_recovery(self) -> typing.Optional[builtins.str]:
        '''Enable or disable voice call recovery: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#call_recovery PolicyPasswordDefault#call_recovery}
        '''
        result = self._values.get("call_recovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_recovery(self) -> typing.Optional[builtins.str]:
        '''Enable or disable email password recovery: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#email_recovery PolicyPasswordDefault#email_recovery}
        '''
        result = self._values.get("email_recovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#id PolicyPasswordDefault#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_auto_unlock_minutes(self) -> typing.Optional[jsii.Number]:
        '''Number of minutes before a locked account is unlocked: 0 = no limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_auto_unlock_minutes PolicyPasswordDefault#password_auto_unlock_minutes}
        '''
        result = self._values.get("password_auto_unlock_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_dictionary_lookup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Check Passwords Against Common Password Dictionary.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_dictionary_lookup PolicyPasswordDefault#password_dictionary_lookup}
        '''
        result = self._values.get("password_dictionary_lookup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_exclude_first_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''User firstName attribute must be excluded from the password.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_exclude_first_name PolicyPasswordDefault#password_exclude_first_name}
        '''
        result = self._values.get("password_exclude_first_name")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_exclude_last_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''User lastName attribute must be excluded from the password.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_exclude_last_name PolicyPasswordDefault#password_exclude_last_name}
        '''
        result = self._values.get("password_exclude_last_name")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_exclude_username(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the user name must be excluded from the password.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_exclude_username PolicyPasswordDefault#password_exclude_username}
        '''
        result = self._values.get("password_exclude_username")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_expire_warn_days(self) -> typing.Optional[jsii.Number]:
        '''Length in days a user will be warned before password expiry: 0 = no warning.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_expire_warn_days PolicyPasswordDefault#password_expire_warn_days}
        '''
        result = self._values.get("password_expire_warn_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_history_count(self) -> typing.Optional[jsii.Number]:
        '''Number of distinct passwords that must be created before they can be reused: 0 = none.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_history_count PolicyPasswordDefault#password_history_count}
        '''
        result = self._values.get("password_history_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_lockout_notification_channels(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Notification channels to use to notify a user when their account has been locked.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_lockout_notification_channels PolicyPasswordDefault#password_lockout_notification_channels}
        '''
        result = self._values.get("password_lockout_notification_channels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def password_max_age_days(self) -> typing.Optional[jsii.Number]:
        '''Length in days a password is valid before expiry: 0 = no limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_max_age_days PolicyPasswordDefault#password_max_age_days}
        '''
        result = self._values.get("password_max_age_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_max_lockout_attempts(self) -> typing.Optional[jsii.Number]:
        '''Number of unsuccessful login attempts allowed before lockout: 0 = no limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_max_lockout_attempts PolicyPasswordDefault#password_max_lockout_attempts}
        '''
        result = self._values.get("password_max_lockout_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_age_minutes(self) -> typing.Optional[jsii.Number]:
        '''Minimum time interval in minutes between password changes: 0 = no limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_age_minutes PolicyPasswordDefault#password_min_age_minutes}
        '''
        result = self._values.get("password_min_age_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_length(self) -> typing.Optional[jsii.Number]:
        '''Minimum password length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_length PolicyPasswordDefault#password_min_length}
        '''
        result = self._values.get("password_min_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_lowercase(self) -> typing.Optional[jsii.Number]:
        '''If a password must contain at least one lower case letter: 0 = no, 1 = yes.

        Default = 1

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_lowercase PolicyPasswordDefault#password_min_lowercase}
        '''
        result = self._values.get("password_min_lowercase")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_number(self) -> typing.Optional[jsii.Number]:
        '''If a password must contain at least one number: 0 = no, 1 = yes. Default = 1.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_number PolicyPasswordDefault#password_min_number}
        '''
        result = self._values.get("password_min_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_symbol(self) -> typing.Optional[jsii.Number]:
        '''If a password must contain at least one symbol (!@#$%^&*): 0 = no, 1 = yes. Default = 1.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_symbol PolicyPasswordDefault#password_min_symbol}
        '''
        result = self._values.get("password_min_symbol")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_uppercase(self) -> typing.Optional[jsii.Number]:
        '''If a password must contain at least one upper case letter: 0 = no, 1 = yes.

        Default = 1

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_min_uppercase PolicyPasswordDefault#password_min_uppercase}
        '''
        result = self._values.get("password_min_uppercase")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_show_lockout_failures(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If a user should be informed when their account is locked.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#password_show_lockout_failures PolicyPasswordDefault#password_show_lockout_failures}
        '''
        result = self._values.get("password_show_lockout_failures")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def question_min_length(self) -> typing.Optional[jsii.Number]:
        '''Min length of the password recovery question answer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#question_min_length PolicyPasswordDefault#question_min_length}
        '''
        result = self._values.get("question_min_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def question_recovery(self) -> typing.Optional[builtins.str]:
        '''Enable or disable security question password recovery: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#question_recovery PolicyPasswordDefault#question_recovery}
        '''
        result = self._values.get("question_recovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recovery_email_token(self) -> typing.Optional[jsii.Number]:
        '''Lifetime in minutes of the recovery email token.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#recovery_email_token PolicyPasswordDefault#recovery_email_token}
        '''
        result = self._values.get("recovery_email_token")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def skip_unlock(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When an Active Directory user is locked out of Okta, the Okta unlock operation should also attempt to unlock the user's Windows account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#skip_unlock PolicyPasswordDefault#skip_unlock}
        '''
        result = self._values.get("skip_unlock")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sms_recovery(self) -> typing.Optional[builtins.str]:
        '''Enable or disable SMS password recovery: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password_default#sms_recovery PolicyPasswordDefault#sms_recovery}
        '''
        result = self._values.get("sms_recovery")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyPasswordDefaultConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PolicyPasswordDefault",
    "PolicyPasswordDefaultConfig",
]

publication.publish()

def _typecheckingstub__517b7310311cf8648ed1a3f63922a95ab0393cbceb106f07434a44fd0d458791(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    call_recovery: typing.Optional[builtins.str] = None,
    email_recovery: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    password_auto_unlock_minutes: typing.Optional[jsii.Number] = None,
    password_dictionary_lookup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_exclude_first_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_exclude_last_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_exclude_username: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_expire_warn_days: typing.Optional[jsii.Number] = None,
    password_history_count: typing.Optional[jsii.Number] = None,
    password_lockout_notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
    password_max_age_days: typing.Optional[jsii.Number] = None,
    password_max_lockout_attempts: typing.Optional[jsii.Number] = None,
    password_min_age_minutes: typing.Optional[jsii.Number] = None,
    password_min_length: typing.Optional[jsii.Number] = None,
    password_min_lowercase: typing.Optional[jsii.Number] = None,
    password_min_number: typing.Optional[jsii.Number] = None,
    password_min_symbol: typing.Optional[jsii.Number] = None,
    password_min_uppercase: typing.Optional[jsii.Number] = None,
    password_show_lockout_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    question_min_length: typing.Optional[jsii.Number] = None,
    question_recovery: typing.Optional[builtins.str] = None,
    recovery_email_token: typing.Optional[jsii.Number] = None,
    skip_unlock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sms_recovery: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__818f9d145e431ecb2a4882e037101e4a8cf9f4d2f7937761b6bc4a3b8558d20e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d1139013ea5662985fad3fdbd64b1d41698788479b64d914a30d24fdcc0ce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271e911fbdd8a351431e30e67d8c6436246d94a1dcd0e11e923fff0e1005dd16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974f16ab4f56f1bed578b3678b1ed3fe4123bb1b70351a0b6a97d945a53b2635(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39871651e1a9aa9f6e49d81ea039a9038f2c9bfefe55158884bd7898beebe83c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d84bb839e79012330f299f40432a3b7709f01fa01d3b706335e891971c97377(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85612e832b57a8acd45407f31f1c1df5f10656ca66c119bb4d4fd2e9c0db0c8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c836a4af087ec8fb01795a2d13cd27d9e21ad94bb5433502ef0522c82d1d4e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55cbd87db54839c950dac73d1b8e00c73a806751a3387a0a94c2ab0c495586ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02aabbccd09ecbb1511ffb47a744d7a7b8ae1808150fad264f9295dbd7d481f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8cd83f22df6fcc5c8a9b87a47272ede58ee997c8a3cbea19ae41e7390547b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ada2cb5823a6ac2c26bec4bdc52adbf8bcc2399cbc40e01657e16cd7f8def8e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98405dd049e32ffa41c350f7f07c2d62ee13e747cce9151e0e3b253534c844e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf3cd52f62fdbd14b1c97ba8593655aa8a537266dfb51b3c11fb9a671fff87a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7e4a3694c376ffc9e65cd15a4e1c2440fea8719327d09c7376bba4136d151a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d41a85a8e4b078ba9284541d691f0527bfa589fe6eb544487857e3387f9e0af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab20120dfd7c15b604d1b098f97d008be7b13c81e8e4e7605744532b7ed7069b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4339e8e996070ec4651d9134655b3d25ca5b2bac08a04c595684fa6236c824(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8939ce6eb743fc73910f74fa3f7eee2e3ce9ae5f70e1534498fe73904b5e7c1a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f202ce451c96ae22e4c0b34743680e61f2122cf4b8ee480c490acd4af70c4b09(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0360fc644fc4b0af22ec57c1abfaeafdb4129f5e44c6a7d0b6fe745ae1e0f0b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de14b6f429cb2c1111eae829c8dc1a1a319c75cb5a7d0db0e2462cd95925087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1daf006d12d67d974ba321b6cfa322b94fdd02736059a73901dbb7f6d5f3450b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46aa32e334df4e5021af300ae22de0d87146e9a286595a51019f40d8eae8309b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917a1ac11b48ad54bdc31115c9080858b0beba696310e7d08d44a44fec3bfa6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9167266e245f532f14b7cd84bfaa2d9bc2ce8ca8c73002bff179a936d393998a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    call_recovery: typing.Optional[builtins.str] = None,
    email_recovery: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    password_auto_unlock_minutes: typing.Optional[jsii.Number] = None,
    password_dictionary_lookup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_exclude_first_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_exclude_last_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_exclude_username: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_expire_warn_days: typing.Optional[jsii.Number] = None,
    password_history_count: typing.Optional[jsii.Number] = None,
    password_lockout_notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
    password_max_age_days: typing.Optional[jsii.Number] = None,
    password_max_lockout_attempts: typing.Optional[jsii.Number] = None,
    password_min_age_minutes: typing.Optional[jsii.Number] = None,
    password_min_length: typing.Optional[jsii.Number] = None,
    password_min_lowercase: typing.Optional[jsii.Number] = None,
    password_min_number: typing.Optional[jsii.Number] = None,
    password_min_symbol: typing.Optional[jsii.Number] = None,
    password_min_uppercase: typing.Optional[jsii.Number] = None,
    password_show_lockout_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    question_min_length: typing.Optional[jsii.Number] = None,
    question_recovery: typing.Optional[builtins.str] = None,
    recovery_email_token: typing.Optional[jsii.Number] = None,
    skip_unlock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sms_recovery: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
