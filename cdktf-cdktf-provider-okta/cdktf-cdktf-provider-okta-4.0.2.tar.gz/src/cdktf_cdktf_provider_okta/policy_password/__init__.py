'''
# `okta_policy_password`

Refer to the Terraform Registory for docs: [`okta_policy_password`](https://www.terraform.io/docs/providers/okta/r/policy_password).
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


class PolicyPassword(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyPassword.PolicyPassword",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/policy_password okta_policy_password}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        auth_provider: typing.Optional[builtins.str] = None,
        call_recovery: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        email_recovery: typing.Optional[builtins.str] = None,
        groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        priority: typing.Optional[jsii.Number] = None,
        question_min_length: typing.Optional[jsii.Number] = None,
        question_recovery: typing.Optional[builtins.str] = None,
        recovery_email_token: typing.Optional[jsii.Number] = None,
        skip_unlock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sms_recovery: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/policy_password okta_policy_password} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#name PolicyPassword#name}
        :param auth_provider: Authentication Provider: OKTA, ACTIVE_DIRECTORY or LDAP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#auth_provider PolicyPassword#auth_provider}
        :param call_recovery: Enable or disable voice call recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#call_recovery PolicyPassword#call_recovery}
        :param description: Policy Description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#description PolicyPassword#description}
        :param email_recovery: Enable or disable email password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#email_recovery PolicyPassword#email_recovery}
        :param groups_included: List of Group IDs to Include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#groups_included PolicyPassword#groups_included}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#id PolicyPassword#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password_auto_unlock_minutes: Number of minutes before a locked account is unlocked: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_auto_unlock_minutes PolicyPassword#password_auto_unlock_minutes}
        :param password_dictionary_lookup: Check Passwords Against Common Password Dictionary. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_dictionary_lookup PolicyPassword#password_dictionary_lookup}
        :param password_exclude_first_name: User firstName attribute must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_exclude_first_name PolicyPassword#password_exclude_first_name}
        :param password_exclude_last_name: User lastName attribute must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_exclude_last_name PolicyPassword#password_exclude_last_name}
        :param password_exclude_username: If the user name must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_exclude_username PolicyPassword#password_exclude_username}
        :param password_expire_warn_days: Length in days a user will be warned before password expiry: 0 = no warning. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_expire_warn_days PolicyPassword#password_expire_warn_days}
        :param password_history_count: Number of distinct passwords that must be created before they can be reused: 0 = none. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_history_count PolicyPassword#password_history_count}
        :param password_lockout_notification_channels: Notification channels to use to notify a user when their account has been locked. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_lockout_notification_channels PolicyPassword#password_lockout_notification_channels}
        :param password_max_age_days: Length in days a password is valid before expiry: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_max_age_days PolicyPassword#password_max_age_days}
        :param password_max_lockout_attempts: Number of unsuccessful login attempts allowed before lockout: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_max_lockout_attempts PolicyPassword#password_max_lockout_attempts}
        :param password_min_age_minutes: Minimum time interval in minutes between password changes: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_age_minutes PolicyPassword#password_min_age_minutes}
        :param password_min_length: Minimum password length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_length PolicyPassword#password_min_length}
        :param password_min_lowercase: If a password must contain at least one lower case letter: 0 = no, 1 = yes. Default = 1 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_lowercase PolicyPassword#password_min_lowercase}
        :param password_min_number: If a password must contain at least one number: 0 = no, 1 = yes. Default = 1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_number PolicyPassword#password_min_number}
        :param password_min_symbol: If a password must contain at least one symbol (!@#$%^&*): 0 = no, 1 = yes. Default = 1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_symbol PolicyPassword#password_min_symbol}
        :param password_min_uppercase: If a password must contain at least one upper case letter: 0 = no, 1 = yes. Default = 1 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_uppercase PolicyPassword#password_min_uppercase}
        :param password_show_lockout_failures: If a user should be informed when their account is locked. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_show_lockout_failures PolicyPassword#password_show_lockout_failures}
        :param priority: Policy Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#priority PolicyPassword#priority}
        :param question_min_length: Min length of the password recovery question answer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#question_min_length PolicyPassword#question_min_length}
        :param question_recovery: Enable or disable security question password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#question_recovery PolicyPassword#question_recovery}
        :param recovery_email_token: Lifetime in minutes of the recovery email token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#recovery_email_token PolicyPassword#recovery_email_token}
        :param skip_unlock: When an Active Directory user is locked out of Okta, the Okta unlock operation should also attempt to unlock the user's Windows account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#skip_unlock PolicyPassword#skip_unlock}
        :param sms_recovery: Enable or disable SMS password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#sms_recovery PolicyPassword#sms_recovery}
        :param status: Policy Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#status PolicyPassword#status}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f56d8a3a8a4cdb12a07eb7ead7ed6aee0b817b76976888b811a4eb3f44733c12)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PolicyPasswordConfig(
            name=name,
            auth_provider=auth_provider,
            call_recovery=call_recovery,
            description=description,
            email_recovery=email_recovery,
            groups_included=groups_included,
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
            priority=priority,
            question_min_length=question_min_length,
            question_recovery=question_recovery,
            recovery_email_token=recovery_email_token,
            skip_unlock=skip_unlock,
            sms_recovery=sms_recovery,
            status=status,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAuthProvider")
    def reset_auth_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthProvider", []))

    @jsii.member(jsii_name="resetCallRecovery")
    def reset_call_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCallRecovery", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEmailRecovery")
    def reset_email_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailRecovery", []))

    @jsii.member(jsii_name="resetGroupsIncluded")
    def reset_groups_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsIncluded", []))

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

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

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

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="authProviderInput")
    def auth_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="callRecoveryInput")
    def call_recovery_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "callRecoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="emailRecoveryInput")
    def email_recovery_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailRecoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsIncludedInput")
    def groups_included_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsIncludedInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

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
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="authProvider")
    def auth_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authProvider"))

    @auth_provider.setter
    def auth_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17110594a6373d64888a42ce50347d4408c99ab757e70f4c6aa01c55383aa83e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authProvider", value)

    @builtins.property
    @jsii.member(jsii_name="callRecovery")
    def call_recovery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "callRecovery"))

    @call_recovery.setter
    def call_recovery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3573be31fbd58ff59ef921ccbdf6dcdc6ca0cd8aef99332bb6b6a0b9730f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callRecovery", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b03517de0496f771f4ce4b071c6c37567a061c048f9835985d083714bfd3f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="emailRecovery")
    def email_recovery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailRecovery"))

    @email_recovery.setter
    def email_recovery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__005b4a2979b91c31256a42a74b646eaa62aaea62f299083c6e0bf87efb44f521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailRecovery", value)

    @builtins.property
    @jsii.member(jsii_name="groupsIncluded")
    def groups_included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsIncluded"))

    @groups_included.setter
    def groups_included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31ae48b086b5174bbaaf92f7a3ac58d7e51333e08d92b04a47bd4324731a8ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsIncluded", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669666cfcf38f14fa194a04cc5357eeb89f6b30196e539ad7b69fed13998d46b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84369b2c6fe0a82ef6cc9463af0e9cdd11e7d5da368b386e7595212cdecece4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="passwordAutoUnlockMinutes")
    def password_auto_unlock_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordAutoUnlockMinutes"))

    @password_auto_unlock_minutes.setter
    def password_auto_unlock_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1500d4cb166c078ce7449003db51c1c69ed32779d1a852d53103f7d6946e8da1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e711b64d5a1450c7e2a1a9d8b94cf6b5f2d60f6c7ba8695a5e99ba99d2165412)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b6c5e2019b61bc81c3ae908e7f9aa6485f271ff594698123f71020690322e1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81ab3d708e16586b3de34077be888145768d88ac2f73b903951991a7db6b63e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a87bd5445774d0dea237bb543d960407f7f2bfb12490693382b4128cd570bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordExcludeUsername", value)

    @builtins.property
    @jsii.member(jsii_name="passwordExpireWarnDays")
    def password_expire_warn_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordExpireWarnDays"))

    @password_expire_warn_days.setter
    def password_expire_warn_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995303fd8b4a831e05b734f9004aa3f3a0c5cb0b80a88cca2825ce46bc5719db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordExpireWarnDays", value)

    @builtins.property
    @jsii.member(jsii_name="passwordHistoryCount")
    def password_history_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordHistoryCount"))

    @password_history_count.setter
    def password_history_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cf1e12ccd6288877117e6507e7259fbcd18fa068e724c3f3a62d3eb9de89fd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdadaf0fae9133d35a343a0989e1baede85429446866d00222f669ac001d4b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordLockoutNotificationChannels", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMaxAgeDays")
    def password_max_age_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMaxAgeDays"))

    @password_max_age_days.setter
    def password_max_age_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4daaf556a631faf37427c1a0b0c31512ca3ac879a7b0d792be1ff54e53a80374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMaxAgeDays", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMaxLockoutAttempts")
    def password_max_lockout_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMaxLockoutAttempts"))

    @password_max_lockout_attempts.setter
    def password_max_lockout_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a3db9b9d4241da73731b23b391a89b42365bf2a483804b6dbc139b173ffb6fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMaxLockoutAttempts", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinAgeMinutes")
    def password_min_age_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinAgeMinutes"))

    @password_min_age_minutes.setter
    def password_min_age_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d1921454be1133c51d5b0b3bb992213c75ea1a5f1074083be41e36877e7577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMinAgeMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinLength")
    def password_min_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinLength"))

    @password_min_length.setter
    def password_min_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9676c607f2090457f982145784f18755a29ddda0bf73928cd84040ceeecf86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMinLength", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinLowercase")
    def password_min_lowercase(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinLowercase"))

    @password_min_lowercase.setter
    def password_min_lowercase(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5d0c4afe82767a0e0a6a93ba4c753e319c6f00557bee5ee810f709d1154059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMinLowercase", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinNumber")
    def password_min_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinNumber"))

    @password_min_number.setter
    def password_min_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e1ada2f2df3659c2c51ded4814bf3ea769dff6d6ece555c15ec72bda1ebd00c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMinNumber", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinSymbol")
    def password_min_symbol(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinSymbol"))

    @password_min_symbol.setter
    def password_min_symbol(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113a9b7a4202b3489ff39d958cd7fee7a3881539b049694f547d95a9a1459c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordMinSymbol", value)

    @builtins.property
    @jsii.member(jsii_name="passwordMinUppercase")
    def password_min_uppercase(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordMinUppercase"))

    @password_min_uppercase.setter
    def password_min_uppercase(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b68e8b95584abf87b10e5984e8b6ce55bae07aff2f3fea115c27f405669da0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8380363c187692a34afc40eede65ee3a2d7b0dd16ec54e99023fac293e883f86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordShowLockoutFailures", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5808f24da2e1cea828273f7c25fc9aa2e125ead877e54e11c8a054a6bfd49f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="questionMinLength")
    def question_min_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "questionMinLength"))

    @question_min_length.setter
    def question_min_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d84fe28b69d2e58418f6b378f809199cedea3042212b21fd95b7ce4e3db0e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "questionMinLength", value)

    @builtins.property
    @jsii.member(jsii_name="questionRecovery")
    def question_recovery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "questionRecovery"))

    @question_recovery.setter
    def question_recovery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0b0d343219471190aab3b3dd167cdc663674e6f81376860282bd8f0293a85e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "questionRecovery", value)

    @builtins.property
    @jsii.member(jsii_name="recoveryEmailToken")
    def recovery_email_token(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "recoveryEmailToken"))

    @recovery_email_token.setter
    def recovery_email_token(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03fc7ebe666b82b44ac65f684d821dc7619cdad4b2f9b4a4678a7bc0884d753)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa501189e1f2030a4c38cb0bffca77626cdea489282ba179b75a5fa3eb1ae274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipUnlock", value)

    @builtins.property
    @jsii.member(jsii_name="smsRecovery")
    def sms_recovery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "smsRecovery"))

    @sms_recovery.setter
    def sms_recovery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07654aa37ab83e0585f4b7fe65dcff506307febbfd95dee510bea1822451dbf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smsRecovery", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45f0451680a66d094c1f741f03684f3f9cdc78cd1b6d08d7a826fdd9135c62f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyPassword.PolicyPasswordConfig",
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
        "auth_provider": "authProvider",
        "call_recovery": "callRecovery",
        "description": "description",
        "email_recovery": "emailRecovery",
        "groups_included": "groupsIncluded",
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
        "priority": "priority",
        "question_min_length": "questionMinLength",
        "question_recovery": "questionRecovery",
        "recovery_email_token": "recoveryEmailToken",
        "skip_unlock": "skipUnlock",
        "sms_recovery": "smsRecovery",
        "status": "status",
    },
)
class PolicyPasswordConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auth_provider: typing.Optional[builtins.str] = None,
        call_recovery: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        email_recovery: typing.Optional[builtins.str] = None,
        groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        priority: typing.Optional[jsii.Number] = None,
        question_min_length: typing.Optional[jsii.Number] = None,
        question_recovery: typing.Optional[builtins.str] = None,
        recovery_email_token: typing.Optional[jsii.Number] = None,
        skip_unlock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sms_recovery: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Policy Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#name PolicyPassword#name}
        :param auth_provider: Authentication Provider: OKTA, ACTIVE_DIRECTORY or LDAP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#auth_provider PolicyPassword#auth_provider}
        :param call_recovery: Enable or disable voice call recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#call_recovery PolicyPassword#call_recovery}
        :param description: Policy Description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#description PolicyPassword#description}
        :param email_recovery: Enable or disable email password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#email_recovery PolicyPassword#email_recovery}
        :param groups_included: List of Group IDs to Include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#groups_included PolicyPassword#groups_included}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#id PolicyPassword#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password_auto_unlock_minutes: Number of minutes before a locked account is unlocked: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_auto_unlock_minutes PolicyPassword#password_auto_unlock_minutes}
        :param password_dictionary_lookup: Check Passwords Against Common Password Dictionary. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_dictionary_lookup PolicyPassword#password_dictionary_lookup}
        :param password_exclude_first_name: User firstName attribute must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_exclude_first_name PolicyPassword#password_exclude_first_name}
        :param password_exclude_last_name: User lastName attribute must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_exclude_last_name PolicyPassword#password_exclude_last_name}
        :param password_exclude_username: If the user name must be excluded from the password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_exclude_username PolicyPassword#password_exclude_username}
        :param password_expire_warn_days: Length in days a user will be warned before password expiry: 0 = no warning. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_expire_warn_days PolicyPassword#password_expire_warn_days}
        :param password_history_count: Number of distinct passwords that must be created before they can be reused: 0 = none. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_history_count PolicyPassword#password_history_count}
        :param password_lockout_notification_channels: Notification channels to use to notify a user when their account has been locked. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_lockout_notification_channels PolicyPassword#password_lockout_notification_channels}
        :param password_max_age_days: Length in days a password is valid before expiry: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_max_age_days PolicyPassword#password_max_age_days}
        :param password_max_lockout_attempts: Number of unsuccessful login attempts allowed before lockout: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_max_lockout_attempts PolicyPassword#password_max_lockout_attempts}
        :param password_min_age_minutes: Minimum time interval in minutes between password changes: 0 = no limit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_age_minutes PolicyPassword#password_min_age_minutes}
        :param password_min_length: Minimum password length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_length PolicyPassword#password_min_length}
        :param password_min_lowercase: If a password must contain at least one lower case letter: 0 = no, 1 = yes. Default = 1 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_lowercase PolicyPassword#password_min_lowercase}
        :param password_min_number: If a password must contain at least one number: 0 = no, 1 = yes. Default = 1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_number PolicyPassword#password_min_number}
        :param password_min_symbol: If a password must contain at least one symbol (!@#$%^&*): 0 = no, 1 = yes. Default = 1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_symbol PolicyPassword#password_min_symbol}
        :param password_min_uppercase: If a password must contain at least one upper case letter: 0 = no, 1 = yes. Default = 1 Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_uppercase PolicyPassword#password_min_uppercase}
        :param password_show_lockout_failures: If a user should be informed when their account is locked. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_show_lockout_failures PolicyPassword#password_show_lockout_failures}
        :param priority: Policy Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#priority PolicyPassword#priority}
        :param question_min_length: Min length of the password recovery question answer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#question_min_length PolicyPassword#question_min_length}
        :param question_recovery: Enable or disable security question password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#question_recovery PolicyPassword#question_recovery}
        :param recovery_email_token: Lifetime in minutes of the recovery email token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#recovery_email_token PolicyPassword#recovery_email_token}
        :param skip_unlock: When an Active Directory user is locked out of Okta, the Okta unlock operation should also attempt to unlock the user's Windows account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#skip_unlock PolicyPassword#skip_unlock}
        :param sms_recovery: Enable or disable SMS password recovery: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#sms_recovery PolicyPassword#sms_recovery}
        :param status: Policy Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#status PolicyPassword#status}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089de61fbb7625505c3b7fc1d7b4042876550bf913e1bc409e53e9f4d46bd175)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auth_provider", value=auth_provider, expected_type=type_hints["auth_provider"])
            check_type(argname="argument call_recovery", value=call_recovery, expected_type=type_hints["call_recovery"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument email_recovery", value=email_recovery, expected_type=type_hints["email_recovery"])
            check_type(argname="argument groups_included", value=groups_included, expected_type=type_hints["groups_included"])
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
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument question_min_length", value=question_min_length, expected_type=type_hints["question_min_length"])
            check_type(argname="argument question_recovery", value=question_recovery, expected_type=type_hints["question_recovery"])
            check_type(argname="argument recovery_email_token", value=recovery_email_token, expected_type=type_hints["recovery_email_token"])
            check_type(argname="argument skip_unlock", value=skip_unlock, expected_type=type_hints["skip_unlock"])
            check_type(argname="argument sms_recovery", value=sms_recovery, expected_type=type_hints["sms_recovery"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if auth_provider is not None:
            self._values["auth_provider"] = auth_provider
        if call_recovery is not None:
            self._values["call_recovery"] = call_recovery
        if description is not None:
            self._values["description"] = description
        if email_recovery is not None:
            self._values["email_recovery"] = email_recovery
        if groups_included is not None:
            self._values["groups_included"] = groups_included
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
        if priority is not None:
            self._values["priority"] = priority
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
        if status is not None:
            self._values["status"] = status

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
        '''Policy Name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#name PolicyPassword#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_provider(self) -> typing.Optional[builtins.str]:
        '''Authentication Provider: OKTA, ACTIVE_DIRECTORY or LDAP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#auth_provider PolicyPassword#auth_provider}
        '''
        result = self._values.get("auth_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def call_recovery(self) -> typing.Optional[builtins.str]:
        '''Enable or disable voice call recovery: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#call_recovery PolicyPassword#call_recovery}
        '''
        result = self._values.get("call_recovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Policy Description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#description PolicyPassword#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_recovery(self) -> typing.Optional[builtins.str]:
        '''Enable or disable email password recovery: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#email_recovery PolicyPassword#email_recovery}
        '''
        result = self._values.get("email_recovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_included(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of Group IDs to Include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#groups_included PolicyPassword#groups_included}
        '''
        result = self._values.get("groups_included")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#id PolicyPassword#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_auto_unlock_minutes(self) -> typing.Optional[jsii.Number]:
        '''Number of minutes before a locked account is unlocked: 0 = no limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_auto_unlock_minutes PolicyPassword#password_auto_unlock_minutes}
        '''
        result = self._values.get("password_auto_unlock_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_dictionary_lookup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Check Passwords Against Common Password Dictionary.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_dictionary_lookup PolicyPassword#password_dictionary_lookup}
        '''
        result = self._values.get("password_dictionary_lookup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_exclude_first_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''User firstName attribute must be excluded from the password.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_exclude_first_name PolicyPassword#password_exclude_first_name}
        '''
        result = self._values.get("password_exclude_first_name")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_exclude_last_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''User lastName attribute must be excluded from the password.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_exclude_last_name PolicyPassword#password_exclude_last_name}
        '''
        result = self._values.get("password_exclude_last_name")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_exclude_username(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the user name must be excluded from the password.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_exclude_username PolicyPassword#password_exclude_username}
        '''
        result = self._values.get("password_exclude_username")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_expire_warn_days(self) -> typing.Optional[jsii.Number]:
        '''Length in days a user will be warned before password expiry: 0 = no warning.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_expire_warn_days PolicyPassword#password_expire_warn_days}
        '''
        result = self._values.get("password_expire_warn_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_history_count(self) -> typing.Optional[jsii.Number]:
        '''Number of distinct passwords that must be created before they can be reused: 0 = none.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_history_count PolicyPassword#password_history_count}
        '''
        result = self._values.get("password_history_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_lockout_notification_channels(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Notification channels to use to notify a user when their account has been locked.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_lockout_notification_channels PolicyPassword#password_lockout_notification_channels}
        '''
        result = self._values.get("password_lockout_notification_channels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def password_max_age_days(self) -> typing.Optional[jsii.Number]:
        '''Length in days a password is valid before expiry: 0 = no limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_max_age_days PolicyPassword#password_max_age_days}
        '''
        result = self._values.get("password_max_age_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_max_lockout_attempts(self) -> typing.Optional[jsii.Number]:
        '''Number of unsuccessful login attempts allowed before lockout: 0 = no limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_max_lockout_attempts PolicyPassword#password_max_lockout_attempts}
        '''
        result = self._values.get("password_max_lockout_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_age_minutes(self) -> typing.Optional[jsii.Number]:
        '''Minimum time interval in minutes between password changes: 0 = no limit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_age_minutes PolicyPassword#password_min_age_minutes}
        '''
        result = self._values.get("password_min_age_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_length(self) -> typing.Optional[jsii.Number]:
        '''Minimum password length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_length PolicyPassword#password_min_length}
        '''
        result = self._values.get("password_min_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_lowercase(self) -> typing.Optional[jsii.Number]:
        '''If a password must contain at least one lower case letter: 0 = no, 1 = yes.

        Default = 1

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_lowercase PolicyPassword#password_min_lowercase}
        '''
        result = self._values.get("password_min_lowercase")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_number(self) -> typing.Optional[jsii.Number]:
        '''If a password must contain at least one number: 0 = no, 1 = yes. Default = 1.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_number PolicyPassword#password_min_number}
        '''
        result = self._values.get("password_min_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_symbol(self) -> typing.Optional[jsii.Number]:
        '''If a password must contain at least one symbol (!@#$%^&*): 0 = no, 1 = yes. Default = 1.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_symbol PolicyPassword#password_min_symbol}
        '''
        result = self._values.get("password_min_symbol")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_min_uppercase(self) -> typing.Optional[jsii.Number]:
        '''If a password must contain at least one upper case letter: 0 = no, 1 = yes.

        Default = 1

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_min_uppercase PolicyPassword#password_min_uppercase}
        '''
        result = self._values.get("password_min_uppercase")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_show_lockout_failures(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If a user should be informed when their account is locked.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#password_show_lockout_failures PolicyPassword#password_show_lockout_failures}
        '''
        result = self._values.get("password_show_lockout_failures")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Policy Priority, this attribute can be set to a valid priority.

        To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#priority PolicyPassword#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def question_min_length(self) -> typing.Optional[jsii.Number]:
        '''Min length of the password recovery question answer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#question_min_length PolicyPassword#question_min_length}
        '''
        result = self._values.get("question_min_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def question_recovery(self) -> typing.Optional[builtins.str]:
        '''Enable or disable security question password recovery: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#question_recovery PolicyPassword#question_recovery}
        '''
        result = self._values.get("question_recovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recovery_email_token(self) -> typing.Optional[jsii.Number]:
        '''Lifetime in minutes of the recovery email token.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#recovery_email_token PolicyPassword#recovery_email_token}
        '''
        result = self._values.get("recovery_email_token")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def skip_unlock(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When an Active Directory user is locked out of Okta, the Okta unlock operation should also attempt to unlock the user's Windows account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#skip_unlock PolicyPassword#skip_unlock}
        '''
        result = self._values.get("skip_unlock")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sms_recovery(self) -> typing.Optional[builtins.str]:
        '''Enable or disable SMS password recovery: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#sms_recovery PolicyPassword#sms_recovery}
        '''
        result = self._values.get("sms_recovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Policy Status: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_password#status PolicyPassword#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyPasswordConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PolicyPassword",
    "PolicyPasswordConfig",
]

publication.publish()

def _typecheckingstub__f56d8a3a8a4cdb12a07eb7ead7ed6aee0b817b76976888b811a4eb3f44733c12(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    auth_provider: typing.Optional[builtins.str] = None,
    call_recovery: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    email_recovery: typing.Optional[builtins.str] = None,
    groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
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
    priority: typing.Optional[jsii.Number] = None,
    question_min_length: typing.Optional[jsii.Number] = None,
    question_recovery: typing.Optional[builtins.str] = None,
    recovery_email_token: typing.Optional[jsii.Number] = None,
    skip_unlock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sms_recovery: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__17110594a6373d64888a42ce50347d4408c99ab757e70f4c6aa01c55383aa83e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3573be31fbd58ff59ef921ccbdf6dcdc6ca0cd8aef99332bb6b6a0b9730f93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b03517de0496f771f4ce4b071c6c37567a061c048f9835985d083714bfd3f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005b4a2979b91c31256a42a74b646eaa62aaea62f299083c6e0bf87efb44f521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31ae48b086b5174bbaaf92f7a3ac58d7e51333e08d92b04a47bd4324731a8ef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669666cfcf38f14fa194a04cc5357eeb89f6b30196e539ad7b69fed13998d46b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84369b2c6fe0a82ef6cc9463af0e9cdd11e7d5da368b386e7595212cdecece4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1500d4cb166c078ce7449003db51c1c69ed32779d1a852d53103f7d6946e8da1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e711b64d5a1450c7e2a1a9d8b94cf6b5f2d60f6c7ba8695a5e99ba99d2165412(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6c5e2019b61bc81c3ae908e7f9aa6485f271ff594698123f71020690322e1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ab3d708e16586b3de34077be888145768d88ac2f73b903951991a7db6b63e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a87bd5445774d0dea237bb543d960407f7f2bfb12490693382b4128cd570bcd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995303fd8b4a831e05b734f9004aa3f3a0c5cb0b80a88cca2825ce46bc5719db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf1e12ccd6288877117e6507e7259fbcd18fa068e724c3f3a62d3eb9de89fd2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdadaf0fae9133d35a343a0989e1baede85429446866d00222f669ac001d4b58(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4daaf556a631faf37427c1a0b0c31512ca3ac879a7b0d792be1ff54e53a80374(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3db9b9d4241da73731b23b391a89b42365bf2a483804b6dbc139b173ffb6fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d1921454be1133c51d5b0b3bb992213c75ea1a5f1074083be41e36877e7577(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9676c607f2090457f982145784f18755a29ddda0bf73928cd84040ceeecf86(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5d0c4afe82767a0e0a6a93ba4c753e319c6f00557bee5ee810f709d1154059(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1ada2f2df3659c2c51ded4814bf3ea769dff6d6ece555c15ec72bda1ebd00c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113a9b7a4202b3489ff39d958cd7fee7a3881539b049694f547d95a9a1459c80(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b68e8b95584abf87b10e5984e8b6ce55bae07aff2f3fea115c27f405669da0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8380363c187692a34afc40eede65ee3a2d7b0dd16ec54e99023fac293e883f86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5808f24da2e1cea828273f7c25fc9aa2e125ead877e54e11c8a054a6bfd49f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d84fe28b69d2e58418f6b378f809199cedea3042212b21fd95b7ce4e3db0e13(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0b0d343219471190aab3b3dd167cdc663674e6f81376860282bd8f0293a85e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03fc7ebe666b82b44ac65f684d821dc7619cdad4b2f9b4a4678a7bc0884d753(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa501189e1f2030a4c38cb0bffca77626cdea489282ba179b75a5fa3eb1ae274(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07654aa37ab83e0585f4b7fe65dcff506307febbfd95dee510bea1822451dbf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45f0451680a66d094c1f741f03684f3f9cdc78cd1b6d08d7a826fdd9135c62f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089de61fbb7625505c3b7fc1d7b4042876550bf913e1bc409e53e9f4d46bd175(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    auth_provider: typing.Optional[builtins.str] = None,
    call_recovery: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    email_recovery: typing.Optional[builtins.str] = None,
    groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
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
    priority: typing.Optional[jsii.Number] = None,
    question_min_length: typing.Optional[jsii.Number] = None,
    question_recovery: typing.Optional[builtins.str] = None,
    recovery_email_token: typing.Optional[jsii.Number] = None,
    skip_unlock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sms_recovery: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
