'''
# `okta_mfa_policy`

Refer to the Terraform Registory for docs: [`okta_mfa_policy`](https://www.terraform.io/docs/providers/okta/r/mfa_policy).
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


class MfaPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.mfaPolicy.MfaPolicy",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy okta_mfa_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        duo: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        external_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fido_u2_f: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fido_webauthn: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        google_otp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        hotp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        is_oie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        okta_call: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_email: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_otp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_password: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_push: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_question: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_sms: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_verify: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        onprem_mfa: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        phone_number: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
        rsa_token: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        security_question: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        symantec_vip: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        webauthn: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        yubikey_token: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy okta_mfa_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#name MfaPolicy#name}
        :param description: Policy Description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#description MfaPolicy#description}
        :param duo: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#duo MfaPolicy#duo}.
        :param external_idp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#external_idp MfaPolicy#external_idp}.
        :param fido_u2_f: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#fido_u2f MfaPolicy#fido_u2f}.
        :param fido_webauthn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#fido_webauthn MfaPolicy#fido_webauthn}.
        :param google_otp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#google_otp MfaPolicy#google_otp}.
        :param groups_included: List of Group IDs to Include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#groups_included MfaPolicy#groups_included}
        :param hotp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#hotp MfaPolicy#hotp}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#id MfaPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_oie: Is the policy using Okta Identity Engine (OIE) with authenticators instead of factors? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#is_oie MfaPolicy#is_oie}
        :param okta_call: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_call MfaPolicy#okta_call}.
        :param okta_email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_email MfaPolicy#okta_email}.
        :param okta_otp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_otp MfaPolicy#okta_otp}.
        :param okta_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_password MfaPolicy#okta_password}.
        :param okta_push: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_push MfaPolicy#okta_push}.
        :param okta_question: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_question MfaPolicy#okta_question}.
        :param okta_sms: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_sms MfaPolicy#okta_sms}.
        :param okta_verify: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_verify MfaPolicy#okta_verify}.
        :param onprem_mfa: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#onprem_mfa MfaPolicy#onprem_mfa}.
        :param phone_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#phone_number MfaPolicy#phone_number}.
        :param priority: Policy Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#priority MfaPolicy#priority}
        :param rsa_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#rsa_token MfaPolicy#rsa_token}.
        :param security_question: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#security_question MfaPolicy#security_question}.
        :param status: Policy Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#status MfaPolicy#status}
        :param symantec_vip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#symantec_vip MfaPolicy#symantec_vip}.
        :param webauthn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#webauthn MfaPolicy#webauthn}.
        :param yubikey_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#yubikey_token MfaPolicy#yubikey_token}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6af37653a9d0240da18984536c909fde5b396d51187faa46c9d9b532d91a26a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MfaPolicyConfig(
            name=name,
            description=description,
            duo=duo,
            external_idp=external_idp,
            fido_u2_f=fido_u2_f,
            fido_webauthn=fido_webauthn,
            google_otp=google_otp,
            groups_included=groups_included,
            hotp=hotp,
            id=id,
            is_oie=is_oie,
            okta_call=okta_call,
            okta_email=okta_email,
            okta_otp=okta_otp,
            okta_password=okta_password,
            okta_push=okta_push,
            okta_question=okta_question,
            okta_sms=okta_sms,
            okta_verify=okta_verify,
            onprem_mfa=onprem_mfa,
            phone_number=phone_number,
            priority=priority,
            rsa_token=rsa_token,
            security_question=security_question,
            status=status,
            symantec_vip=symantec_vip,
            webauthn=webauthn,
            yubikey_token=yubikey_token,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDuo")
    def reset_duo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuo", []))

    @jsii.member(jsii_name="resetExternalIdp")
    def reset_external_idp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalIdp", []))

    @jsii.member(jsii_name="resetFidoU2F")
    def reset_fido_u2_f(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFidoU2F", []))

    @jsii.member(jsii_name="resetFidoWebauthn")
    def reset_fido_webauthn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFidoWebauthn", []))

    @jsii.member(jsii_name="resetGoogleOtp")
    def reset_google_otp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleOtp", []))

    @jsii.member(jsii_name="resetGroupsIncluded")
    def reset_groups_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsIncluded", []))

    @jsii.member(jsii_name="resetHotp")
    def reset_hotp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHotp", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsOie")
    def reset_is_oie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsOie", []))

    @jsii.member(jsii_name="resetOktaCall")
    def reset_okta_call(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOktaCall", []))

    @jsii.member(jsii_name="resetOktaEmail")
    def reset_okta_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOktaEmail", []))

    @jsii.member(jsii_name="resetOktaOtp")
    def reset_okta_otp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOktaOtp", []))

    @jsii.member(jsii_name="resetOktaPassword")
    def reset_okta_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOktaPassword", []))

    @jsii.member(jsii_name="resetOktaPush")
    def reset_okta_push(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOktaPush", []))

    @jsii.member(jsii_name="resetOktaQuestion")
    def reset_okta_question(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOktaQuestion", []))

    @jsii.member(jsii_name="resetOktaSms")
    def reset_okta_sms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOktaSms", []))

    @jsii.member(jsii_name="resetOktaVerify")
    def reset_okta_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOktaVerify", []))

    @jsii.member(jsii_name="resetOnpremMfa")
    def reset_onprem_mfa(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnpremMfa", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetRsaToken")
    def reset_rsa_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRsaToken", []))

    @jsii.member(jsii_name="resetSecurityQuestion")
    def reset_security_question(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityQuestion", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetSymantecVip")
    def reset_symantec_vip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSymantecVip", []))

    @jsii.member(jsii_name="resetWebauthn")
    def reset_webauthn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebauthn", []))

    @jsii.member(jsii_name="resetYubikeyToken")
    def reset_yubikey_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYubikeyToken", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="duoInput")
    def duo_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "duoInput"))

    @builtins.property
    @jsii.member(jsii_name="externalIdpInput")
    def external_idp_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "externalIdpInput"))

    @builtins.property
    @jsii.member(jsii_name="fidoU2FInput")
    def fido_u2_f_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "fidoU2FInput"))

    @builtins.property
    @jsii.member(jsii_name="fidoWebauthnInput")
    def fido_webauthn_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "fidoWebauthnInput"))

    @builtins.property
    @jsii.member(jsii_name="googleOtpInput")
    def google_otp_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "googleOtpInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsIncludedInput")
    def groups_included_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsIncludedInput"))

    @builtins.property
    @jsii.member(jsii_name="hotpInput")
    def hotp_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "hotpInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isOieInput")
    def is_oie_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isOieInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaCallInput")
    def okta_call_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "oktaCallInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaEmailInput")
    def okta_email_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "oktaEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaOtpInput")
    def okta_otp_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "oktaOtpInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaPasswordInput")
    def okta_password_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "oktaPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaPushInput")
    def okta_push_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "oktaPushInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaQuestionInput")
    def okta_question_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "oktaQuestionInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaSmsInput")
    def okta_sms_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "oktaSmsInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaVerifyInput")
    def okta_verify_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "oktaVerifyInput"))

    @builtins.property
    @jsii.member(jsii_name="onpremMfaInput")
    def onprem_mfa_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "onpremMfaInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="rsaTokenInput")
    def rsa_token_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "rsaTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="securityQuestionInput")
    def security_question_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "securityQuestionInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="symantecVipInput")
    def symantec_vip_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "symantecVipInput"))

    @builtins.property
    @jsii.member(jsii_name="webauthnInput")
    def webauthn_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "webauthnInput"))

    @builtins.property
    @jsii.member(jsii_name="yubikeyTokenInput")
    def yubikey_token_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "yubikeyTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65abefce511e7f2c1b6b8243321c74a2de49f036b9c4c0109f932acefc4908a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="duo")
    def duo(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "duo"))

    @duo.setter
    def duo(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f50716842c9dcf31d685ce20d83c6c90ba959afd624ddcad453acaeef5e4eac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duo", value)

    @builtins.property
    @jsii.member(jsii_name="externalIdp")
    def external_idp(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "externalIdp"))

    @external_idp.setter
    def external_idp(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff8527de23228080616fce9705cc462e1397b2d46d2f34c54ecc5b08d46c7a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIdp", value)

    @builtins.property
    @jsii.member(jsii_name="fidoU2F")
    def fido_u2_f(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "fidoU2F"))

    @fido_u2_f.setter
    def fido_u2_f(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d52f47ccbcd3eac7898ef8a66b017dedf9bebf9e9cbff7f48ebe7c3a2d9a1625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fidoU2F", value)

    @builtins.property
    @jsii.member(jsii_name="fidoWebauthn")
    def fido_webauthn(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "fidoWebauthn"))

    @fido_webauthn.setter
    def fido_webauthn(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ab3ba52080be64a868fcf0b719677cd125a9cf609e82e619bc1bc8d51a6746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fidoWebauthn", value)

    @builtins.property
    @jsii.member(jsii_name="googleOtp")
    def google_otp(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "googleOtp"))

    @google_otp.setter
    def google_otp(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1b11ee67d6d738b723f8ef1f1b0bcbde074c58fa9ae593a29ad42814dd83eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "googleOtp", value)

    @builtins.property
    @jsii.member(jsii_name="groupsIncluded")
    def groups_included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsIncluded"))

    @groups_included.setter
    def groups_included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588d7e3f0f7fd45e4b5176b7bc931b9200e6f3c48500fb0e4a157436da938b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsIncluded", value)

    @builtins.property
    @jsii.member(jsii_name="hotp")
    def hotp(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "hotp"))

    @hotp.setter
    def hotp(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b9a35a38bafa1eb3468c397f63602eaaa200574fc0c94acf875d85dec8564c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hotp", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c4b59090866aa8be39e0dee1c38e0073387af3b54161a87cddf71e514e9b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="isOie")
    def is_oie(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isOie"))

    @is_oie.setter
    def is_oie(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a4cb86ee1af019bc869471ed25ceff81f6bf0abf636d7cf3970d03c7779b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isOie", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a073036ed1c973f92145e3e260da76efe65d36667f0963371c8b76d62d4374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="oktaCall")
    def okta_call(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "oktaCall"))

    @okta_call.setter
    def okta_call(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f8babb25751f96e89417325fdfffa341b0cf9da16743187ca3dbb5ef1a52cd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oktaCall", value)

    @builtins.property
    @jsii.member(jsii_name="oktaEmail")
    def okta_email(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "oktaEmail"))

    @okta_email.setter
    def okta_email(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9abbaa2980526787cb0444fa770547444adce6817c11c8f26de884a8b12d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oktaEmail", value)

    @builtins.property
    @jsii.member(jsii_name="oktaOtp")
    def okta_otp(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "oktaOtp"))

    @okta_otp.setter
    def okta_otp(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__276c70f7624139b2898dda9fb554d42c53ab0fd2a533e9406a3ae37ac53bd901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oktaOtp", value)

    @builtins.property
    @jsii.member(jsii_name="oktaPassword")
    def okta_password(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "oktaPassword"))

    @okta_password.setter
    def okta_password(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d41df998e173b072fbf4abb91e63bfee4c15312ba28966562b383f9f74a43bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oktaPassword", value)

    @builtins.property
    @jsii.member(jsii_name="oktaPush")
    def okta_push(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "oktaPush"))

    @okta_push.setter
    def okta_push(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5cb535db7c585426dce59338b18d4345d1a776ef0cdee888e0c1065893c9871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oktaPush", value)

    @builtins.property
    @jsii.member(jsii_name="oktaQuestion")
    def okta_question(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "oktaQuestion"))

    @okta_question.setter
    def okta_question(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91cf176b2abdcd5304e4aa49a3ba243c97a7e593c64ddd5776ff6964c039e92f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oktaQuestion", value)

    @builtins.property
    @jsii.member(jsii_name="oktaSms")
    def okta_sms(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "oktaSms"))

    @okta_sms.setter
    def okta_sms(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327a23880029fd72371c6ffc70099e50eec8c1a55ac99501159908077e57da2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oktaSms", value)

    @builtins.property
    @jsii.member(jsii_name="oktaVerify")
    def okta_verify(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "oktaVerify"))

    @okta_verify.setter
    def okta_verify(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1c1113f86841738e413cb614972bc824db84f610d0b6e59b4b58e33bde8655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oktaVerify", value)

    @builtins.property
    @jsii.member(jsii_name="onpremMfa")
    def onprem_mfa(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "onpremMfa"))

    @onprem_mfa.setter
    def onprem_mfa(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30b53f6460cc83e5bced3c28ed29fc20ad5b982bf8caf644767dc06f4d4b44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onpremMfa", value)

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283524b12ffe5457c7e18af51f3ba87d516e233c0f370a51282a54238013ae8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572570e849d43c0172da98aef74859dac2647d2287fe16984d4a17523140e7c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="rsaToken")
    def rsa_token(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "rsaToken"))

    @rsa_token.setter
    def rsa_token(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42409529fa1d6bfec7d8054df6aa655a05f079492705fd48234cafae73073302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaToken", value)

    @builtins.property
    @jsii.member(jsii_name="securityQuestion")
    def security_question(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "securityQuestion"))

    @security_question.setter
    def security_question(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01d4867b08c2a75f29724a947bee331de0e3416f2fb0c558fd4d355d8ff26b42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityQuestion", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ecaceb947d9c979893f928b0d52291833aae9b2b5535501ccd25eea56f40b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="symantecVip")
    def symantec_vip(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "symantecVip"))

    @symantec_vip.setter
    def symantec_vip(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b06e58b5b9b81dfd39aa956f00d6403282e4d2348fed08f3bff0c4b83f2998c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "symantecVip", value)

    @builtins.property
    @jsii.member(jsii_name="webauthn")
    def webauthn(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "webauthn"))

    @webauthn.setter
    def webauthn(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8925a464b9d520e9e1b6ff864c293ff9afa43b6b2877e9050954fa6b9ec5620e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webauthn", value)

    @builtins.property
    @jsii.member(jsii_name="yubikeyToken")
    def yubikey_token(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "yubikeyToken"))

    @yubikey_token.setter
    def yubikey_token(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69867c4cddf3e35817535cae2a532e0b929ce75e9d749c0a0a2739402d7b6b92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "yubikeyToken", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.mfaPolicy.MfaPolicyConfig",
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
        "description": "description",
        "duo": "duo",
        "external_idp": "externalIdp",
        "fido_u2_f": "fidoU2F",
        "fido_webauthn": "fidoWebauthn",
        "google_otp": "googleOtp",
        "groups_included": "groupsIncluded",
        "hotp": "hotp",
        "id": "id",
        "is_oie": "isOie",
        "okta_call": "oktaCall",
        "okta_email": "oktaEmail",
        "okta_otp": "oktaOtp",
        "okta_password": "oktaPassword",
        "okta_push": "oktaPush",
        "okta_question": "oktaQuestion",
        "okta_sms": "oktaSms",
        "okta_verify": "oktaVerify",
        "onprem_mfa": "onpremMfa",
        "phone_number": "phoneNumber",
        "priority": "priority",
        "rsa_token": "rsaToken",
        "security_question": "securityQuestion",
        "status": "status",
        "symantec_vip": "symantecVip",
        "webauthn": "webauthn",
        "yubikey_token": "yubikeyToken",
    },
)
class MfaPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: typing.Optional[builtins.str] = None,
        duo: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        external_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fido_u2_f: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fido_webauthn: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        google_otp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        hotp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        is_oie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        okta_call: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_email: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_otp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_password: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_push: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_question: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_sms: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        okta_verify: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        onprem_mfa: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        phone_number: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
        rsa_token: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        security_question: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        symantec_vip: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        webauthn: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        yubikey_token: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Policy Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#name MfaPolicy#name}
        :param description: Policy Description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#description MfaPolicy#description}
        :param duo: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#duo MfaPolicy#duo}.
        :param external_idp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#external_idp MfaPolicy#external_idp}.
        :param fido_u2_f: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#fido_u2f MfaPolicy#fido_u2f}.
        :param fido_webauthn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#fido_webauthn MfaPolicy#fido_webauthn}.
        :param google_otp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#google_otp MfaPolicy#google_otp}.
        :param groups_included: List of Group IDs to Include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#groups_included MfaPolicy#groups_included}
        :param hotp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#hotp MfaPolicy#hotp}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#id MfaPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_oie: Is the policy using Okta Identity Engine (OIE) with authenticators instead of factors? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#is_oie MfaPolicy#is_oie}
        :param okta_call: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_call MfaPolicy#okta_call}.
        :param okta_email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_email MfaPolicy#okta_email}.
        :param okta_otp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_otp MfaPolicy#okta_otp}.
        :param okta_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_password MfaPolicy#okta_password}.
        :param okta_push: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_push MfaPolicy#okta_push}.
        :param okta_question: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_question MfaPolicy#okta_question}.
        :param okta_sms: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_sms MfaPolicy#okta_sms}.
        :param okta_verify: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_verify MfaPolicy#okta_verify}.
        :param onprem_mfa: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#onprem_mfa MfaPolicy#onprem_mfa}.
        :param phone_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#phone_number MfaPolicy#phone_number}.
        :param priority: Policy Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#priority MfaPolicy#priority}
        :param rsa_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#rsa_token MfaPolicy#rsa_token}.
        :param security_question: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#security_question MfaPolicy#security_question}.
        :param status: Policy Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#status MfaPolicy#status}
        :param symantec_vip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#symantec_vip MfaPolicy#symantec_vip}.
        :param webauthn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#webauthn MfaPolicy#webauthn}.
        :param yubikey_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#yubikey_token MfaPolicy#yubikey_token}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7897cb7c2d69e5a9235502cd0b53086cdb45f0d5ec77d5f83709971af7b8d1d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument duo", value=duo, expected_type=type_hints["duo"])
            check_type(argname="argument external_idp", value=external_idp, expected_type=type_hints["external_idp"])
            check_type(argname="argument fido_u2_f", value=fido_u2_f, expected_type=type_hints["fido_u2_f"])
            check_type(argname="argument fido_webauthn", value=fido_webauthn, expected_type=type_hints["fido_webauthn"])
            check_type(argname="argument google_otp", value=google_otp, expected_type=type_hints["google_otp"])
            check_type(argname="argument groups_included", value=groups_included, expected_type=type_hints["groups_included"])
            check_type(argname="argument hotp", value=hotp, expected_type=type_hints["hotp"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_oie", value=is_oie, expected_type=type_hints["is_oie"])
            check_type(argname="argument okta_call", value=okta_call, expected_type=type_hints["okta_call"])
            check_type(argname="argument okta_email", value=okta_email, expected_type=type_hints["okta_email"])
            check_type(argname="argument okta_otp", value=okta_otp, expected_type=type_hints["okta_otp"])
            check_type(argname="argument okta_password", value=okta_password, expected_type=type_hints["okta_password"])
            check_type(argname="argument okta_push", value=okta_push, expected_type=type_hints["okta_push"])
            check_type(argname="argument okta_question", value=okta_question, expected_type=type_hints["okta_question"])
            check_type(argname="argument okta_sms", value=okta_sms, expected_type=type_hints["okta_sms"])
            check_type(argname="argument okta_verify", value=okta_verify, expected_type=type_hints["okta_verify"])
            check_type(argname="argument onprem_mfa", value=onprem_mfa, expected_type=type_hints["onprem_mfa"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument rsa_token", value=rsa_token, expected_type=type_hints["rsa_token"])
            check_type(argname="argument security_question", value=security_question, expected_type=type_hints["security_question"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument symantec_vip", value=symantec_vip, expected_type=type_hints["symantec_vip"])
            check_type(argname="argument webauthn", value=webauthn, expected_type=type_hints["webauthn"])
            check_type(argname="argument yubikey_token", value=yubikey_token, expected_type=type_hints["yubikey_token"])
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
        if description is not None:
            self._values["description"] = description
        if duo is not None:
            self._values["duo"] = duo
        if external_idp is not None:
            self._values["external_idp"] = external_idp
        if fido_u2_f is not None:
            self._values["fido_u2_f"] = fido_u2_f
        if fido_webauthn is not None:
            self._values["fido_webauthn"] = fido_webauthn
        if google_otp is not None:
            self._values["google_otp"] = google_otp
        if groups_included is not None:
            self._values["groups_included"] = groups_included
        if hotp is not None:
            self._values["hotp"] = hotp
        if id is not None:
            self._values["id"] = id
        if is_oie is not None:
            self._values["is_oie"] = is_oie
        if okta_call is not None:
            self._values["okta_call"] = okta_call
        if okta_email is not None:
            self._values["okta_email"] = okta_email
        if okta_otp is not None:
            self._values["okta_otp"] = okta_otp
        if okta_password is not None:
            self._values["okta_password"] = okta_password
        if okta_push is not None:
            self._values["okta_push"] = okta_push
        if okta_question is not None:
            self._values["okta_question"] = okta_question
        if okta_sms is not None:
            self._values["okta_sms"] = okta_sms
        if okta_verify is not None:
            self._values["okta_verify"] = okta_verify
        if onprem_mfa is not None:
            self._values["onprem_mfa"] = onprem_mfa
        if phone_number is not None:
            self._values["phone_number"] = phone_number
        if priority is not None:
            self._values["priority"] = priority
        if rsa_token is not None:
            self._values["rsa_token"] = rsa_token
        if security_question is not None:
            self._values["security_question"] = security_question
        if status is not None:
            self._values["status"] = status
        if symantec_vip is not None:
            self._values["symantec_vip"] = symantec_vip
        if webauthn is not None:
            self._values["webauthn"] = webauthn
        if yubikey_token is not None:
            self._values["yubikey_token"] = yubikey_token

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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#name MfaPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Policy Description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#description MfaPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def duo(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#duo MfaPolicy#duo}.'''
        result = self._values.get("duo")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def external_idp(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#external_idp MfaPolicy#external_idp}.'''
        result = self._values.get("external_idp")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def fido_u2_f(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#fido_u2f MfaPolicy#fido_u2f}.'''
        result = self._values.get("fido_u2_f")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def fido_webauthn(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#fido_webauthn MfaPolicy#fido_webauthn}.'''
        result = self._values.get("fido_webauthn")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def google_otp(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#google_otp MfaPolicy#google_otp}.'''
        result = self._values.get("google_otp")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def groups_included(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of Group IDs to Include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#groups_included MfaPolicy#groups_included}
        '''
        result = self._values.get("groups_included")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def hotp(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#hotp MfaPolicy#hotp}.'''
        result = self._values.get("hotp")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#id MfaPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_oie(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Is the policy using Okta Identity Engine (OIE) with authenticators instead of factors?

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#is_oie MfaPolicy#is_oie}
        '''
        result = self._values.get("is_oie")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def okta_call(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_call MfaPolicy#okta_call}.'''
        result = self._values.get("okta_call")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def okta_email(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_email MfaPolicy#okta_email}.'''
        result = self._values.get("okta_email")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def okta_otp(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_otp MfaPolicy#okta_otp}.'''
        result = self._values.get("okta_otp")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def okta_password(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_password MfaPolicy#okta_password}.'''
        result = self._values.get("okta_password")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def okta_push(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_push MfaPolicy#okta_push}.'''
        result = self._values.get("okta_push")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def okta_question(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_question MfaPolicy#okta_question}.'''
        result = self._values.get("okta_question")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def okta_sms(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_sms MfaPolicy#okta_sms}.'''
        result = self._values.get("okta_sms")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def okta_verify(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#okta_verify MfaPolicy#okta_verify}.'''
        result = self._values.get("okta_verify")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def onprem_mfa(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#onprem_mfa MfaPolicy#onprem_mfa}.'''
        result = self._values.get("onprem_mfa")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def phone_number(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#phone_number MfaPolicy#phone_number}.'''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Policy Priority, this attribute can be set to a valid priority.

        To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#priority MfaPolicy#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rsa_token(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#rsa_token MfaPolicy#rsa_token}.'''
        result = self._values.get("rsa_token")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def security_question(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#security_question MfaPolicy#security_question}.'''
        result = self._values.get("security_question")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Policy Status: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#status MfaPolicy#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def symantec_vip(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#symantec_vip MfaPolicy#symantec_vip}.'''
        result = self._values.get("symantec_vip")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def webauthn(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#webauthn MfaPolicy#webauthn}.'''
        result = self._values.get("webauthn")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def yubikey_token(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/mfa_policy#yubikey_token MfaPolicy#yubikey_token}.'''
        result = self._values.get("yubikey_token")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MfaPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "MfaPolicy",
    "MfaPolicyConfig",
]

publication.publish()

def _typecheckingstub__a6af37653a9d0240da18984536c909fde5b396d51187faa46c9d9b532d91a26a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    duo: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    external_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    fido_u2_f: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    fido_webauthn: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    google_otp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
    hotp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    is_oie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    okta_call: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_email: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_otp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_password: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_push: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_question: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_sms: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_verify: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    onprem_mfa: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    phone_number: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    priority: typing.Optional[jsii.Number] = None,
    rsa_token: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    security_question: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    symantec_vip: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    webauthn: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    yubikey_token: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__65abefce511e7f2c1b6b8243321c74a2de49f036b9c4c0109f932acefc4908a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f50716842c9dcf31d685ce20d83c6c90ba959afd624ddcad453acaeef5e4eac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff8527de23228080616fce9705cc462e1397b2d46d2f34c54ecc5b08d46c7a4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52f47ccbcd3eac7898ef8a66b017dedf9bebf9e9cbff7f48ebe7c3a2d9a1625(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ab3ba52080be64a868fcf0b719677cd125a9cf609e82e619bc1bc8d51a6746(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1b11ee67d6d738b723f8ef1f1b0bcbde074c58fa9ae593a29ad42814dd83eb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588d7e3f0f7fd45e4b5176b7bc931b9200e6f3c48500fb0e4a157436da938b76(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b9a35a38bafa1eb3468c397f63602eaaa200574fc0c94acf875d85dec8564c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c4b59090866aa8be39e0dee1c38e0073387af3b54161a87cddf71e514e9b15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a4cb86ee1af019bc869471ed25ceff81f6bf0abf636d7cf3970d03c7779b89(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a073036ed1c973f92145e3e260da76efe65d36667f0963371c8b76d62d4374(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8babb25751f96e89417325fdfffa341b0cf9da16743187ca3dbb5ef1a52cd7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9abbaa2980526787cb0444fa770547444adce6817c11c8f26de884a8b12d5e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276c70f7624139b2898dda9fb554d42c53ab0fd2a533e9406a3ae37ac53bd901(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41df998e173b072fbf4abb91e63bfee4c15312ba28966562b383f9f74a43bcc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5cb535db7c585426dce59338b18d4345d1a776ef0cdee888e0c1065893c9871(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91cf176b2abdcd5304e4aa49a3ba243c97a7e593c64ddd5776ff6964c039e92f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327a23880029fd72371c6ffc70099e50eec8c1a55ac99501159908077e57da2c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1c1113f86841738e413cb614972bc824db84f610d0b6e59b4b58e33bde8655(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30b53f6460cc83e5bced3c28ed29fc20ad5b982bf8caf644767dc06f4d4b44a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283524b12ffe5457c7e18af51f3ba87d516e233c0f370a51282a54238013ae8b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572570e849d43c0172da98aef74859dac2647d2287fe16984d4a17523140e7c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42409529fa1d6bfec7d8054df6aa655a05f079492705fd48234cafae73073302(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d4867b08c2a75f29724a947bee331de0e3416f2fb0c558fd4d355d8ff26b42(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecaceb947d9c979893f928b0d52291833aae9b2b5535501ccd25eea56f40b78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06e58b5b9b81dfd39aa956f00d6403282e4d2348fed08f3bff0c4b83f2998c2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8925a464b9d520e9e1b6ff864c293ff9afa43b6b2877e9050954fa6b9ec5620e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69867c4cddf3e35817535cae2a532e0b929ce75e9d749c0a0a2739402d7b6b92(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7897cb7c2d69e5a9235502cd0b53086cdb45f0d5ec77d5f83709971af7b8d1d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    duo: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    external_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    fido_u2_f: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    fido_webauthn: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    google_otp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
    hotp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    is_oie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    okta_call: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_email: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_otp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_password: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_push: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_question: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_sms: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    okta_verify: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    onprem_mfa: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    phone_number: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    priority: typing.Optional[jsii.Number] = None,
    rsa_token: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    security_question: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    symantec_vip: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    webauthn: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    yubikey_token: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
