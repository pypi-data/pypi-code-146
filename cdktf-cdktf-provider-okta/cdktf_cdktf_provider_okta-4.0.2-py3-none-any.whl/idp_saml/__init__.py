'''
# `okta_idp_saml`

Refer to the Terraform Registory for docs: [`okta_idp_saml`](https://www.terraform.io/docs/providers/okta/r/idp_saml).
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


class IdpSaml(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.idpSaml.IdpSaml",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/idp_saml okta_idp_saml}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        issuer: builtins.str,
        kid: builtins.str,
        name: builtins.str,
        sso_url: builtins.str,
        account_link_action: typing.Optional[builtins.str] = None,
        account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        acs_binding: typing.Optional[builtins.str] = None,
        acs_type: typing.Optional[builtins.str] = None,
        deprovisioned_action: typing.Optional[builtins.str] = None,
        groups_action: typing.Optional[builtins.str] = None,
        groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_attribute: typing.Optional[builtins.str] = None,
        groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        max_clock_skew: typing.Optional[jsii.Number] = None,
        name_format: typing.Optional[builtins.str] = None,
        profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_action: typing.Optional[builtins.str] = None,
        request_signature_algorithm: typing.Optional[builtins.str] = None,
        request_signature_scope: typing.Optional[builtins.str] = None,
        response_signature_algorithm: typing.Optional[builtins.str] = None,
        response_signature_scope: typing.Optional[builtins.str] = None,
        sso_binding: typing.Optional[builtins.str] = None,
        sso_destination: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        subject_filter: typing.Optional[builtins.str] = None,
        subject_format: typing.Optional[typing.Sequence[builtins.str]] = None,
        subject_match_attribute: typing.Optional[builtins.str] = None,
        subject_match_type: typing.Optional[builtins.str] = None,
        suspended_action: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/idp_saml okta_idp_saml} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param issuer: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#issuer IdpSaml#issuer}.
        :param kid: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#kid IdpSaml#kid}.
        :param name: Name of the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#name IdpSaml#name}
        :param sso_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#sso_url IdpSaml#sso_url}.
        :param account_link_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#account_link_action IdpSaml#account_link_action}.
        :param account_link_group_include: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#account_link_group_include IdpSaml#account_link_group_include}.
        :param acs_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#acs_binding IdpSaml#acs_binding}.
        :param acs_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#acs_type IdpSaml#acs_type}.
        :param deprovisioned_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#deprovisioned_action IdpSaml#deprovisioned_action}.
        :param groups_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_action IdpSaml#groups_action}.
        :param groups_assignment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_assignment IdpSaml#groups_assignment}.
        :param groups_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_attribute IdpSaml#groups_attribute}.
        :param groups_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_filter IdpSaml#groups_filter}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#id IdpSaml#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_mode: Indicates whether Okta uses the original Okta org domain URL, or a custom domain URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#issuer_mode IdpSaml#issuer_mode}
        :param max_clock_skew: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#max_clock_skew IdpSaml#max_clock_skew}.
        :param name_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#name_format IdpSaml#name_format}.
        :param profile_master: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#profile_master IdpSaml#profile_master}.
        :param provisioning_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#provisioning_action IdpSaml#provisioning_action}.
        :param request_signature_algorithm: The XML digital Signature Algorithm used when signing an message. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#request_signature_algorithm IdpSaml#request_signature_algorithm}
        :param request_signature_scope: Specifies whether to digitally sign messages to the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#request_signature_scope IdpSaml#request_signature_scope}
        :param response_signature_algorithm: The minimum XML digital Signature Algorithm allowed when verifying a message or element. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#response_signature_algorithm IdpSaml#response_signature_algorithm}
        :param response_signature_scope: Specifies whether to verify a message or element XML digital signature. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#response_signature_scope IdpSaml#response_signature_scope}
        :param sso_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#sso_binding IdpSaml#sso_binding}.
        :param sso_destination: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#sso_destination IdpSaml#sso_destination}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#status IdpSaml#status}.
        :param subject_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_filter IdpSaml#subject_filter}.
        :param subject_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_format IdpSaml#subject_format}.
        :param subject_match_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_match_attribute IdpSaml#subject_match_attribute}.
        :param subject_match_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_match_type IdpSaml#subject_match_type}.
        :param suspended_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#suspended_action IdpSaml#suspended_action}.
        :param username_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#username_template IdpSaml#username_template}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56dfbe40e32b3dfef94dccffcf0bf422e48db9b7d4d4475385ed11e496281c3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IdpSamlConfig(
            issuer=issuer,
            kid=kid,
            name=name,
            sso_url=sso_url,
            account_link_action=account_link_action,
            account_link_group_include=account_link_group_include,
            acs_binding=acs_binding,
            acs_type=acs_type,
            deprovisioned_action=deprovisioned_action,
            groups_action=groups_action,
            groups_assignment=groups_assignment,
            groups_attribute=groups_attribute,
            groups_filter=groups_filter,
            id=id,
            issuer_mode=issuer_mode,
            max_clock_skew=max_clock_skew,
            name_format=name_format,
            profile_master=profile_master,
            provisioning_action=provisioning_action,
            request_signature_algorithm=request_signature_algorithm,
            request_signature_scope=request_signature_scope,
            response_signature_algorithm=response_signature_algorithm,
            response_signature_scope=response_signature_scope,
            sso_binding=sso_binding,
            sso_destination=sso_destination,
            status=status,
            subject_filter=subject_filter,
            subject_format=subject_format,
            subject_match_attribute=subject_match_attribute,
            subject_match_type=subject_match_type,
            suspended_action=suspended_action,
            username_template=username_template,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAccountLinkAction")
    def reset_account_link_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountLinkAction", []))

    @jsii.member(jsii_name="resetAccountLinkGroupInclude")
    def reset_account_link_group_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountLinkGroupInclude", []))

    @jsii.member(jsii_name="resetAcsBinding")
    def reset_acs_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcsBinding", []))

    @jsii.member(jsii_name="resetAcsType")
    def reset_acs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcsType", []))

    @jsii.member(jsii_name="resetDeprovisionedAction")
    def reset_deprovisioned_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeprovisionedAction", []))

    @jsii.member(jsii_name="resetGroupsAction")
    def reset_groups_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsAction", []))

    @jsii.member(jsii_name="resetGroupsAssignment")
    def reset_groups_assignment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsAssignment", []))

    @jsii.member(jsii_name="resetGroupsAttribute")
    def reset_groups_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsAttribute", []))

    @jsii.member(jsii_name="resetGroupsFilter")
    def reset_groups_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIssuerMode")
    def reset_issuer_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuerMode", []))

    @jsii.member(jsii_name="resetMaxClockSkew")
    def reset_max_clock_skew(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxClockSkew", []))

    @jsii.member(jsii_name="resetNameFormat")
    def reset_name_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameFormat", []))

    @jsii.member(jsii_name="resetProfileMaster")
    def reset_profile_master(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileMaster", []))

    @jsii.member(jsii_name="resetProvisioningAction")
    def reset_provisioning_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisioningAction", []))

    @jsii.member(jsii_name="resetRequestSignatureAlgorithm")
    def reset_request_signature_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestSignatureAlgorithm", []))

    @jsii.member(jsii_name="resetRequestSignatureScope")
    def reset_request_signature_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestSignatureScope", []))

    @jsii.member(jsii_name="resetResponseSignatureAlgorithm")
    def reset_response_signature_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseSignatureAlgorithm", []))

    @jsii.member(jsii_name="resetResponseSignatureScope")
    def reset_response_signature_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseSignatureScope", []))

    @jsii.member(jsii_name="resetSsoBinding")
    def reset_sso_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsoBinding", []))

    @jsii.member(jsii_name="resetSsoDestination")
    def reset_sso_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsoDestination", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetSubjectFilter")
    def reset_subject_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectFilter", []))

    @jsii.member(jsii_name="resetSubjectFormat")
    def reset_subject_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectFormat", []))

    @jsii.member(jsii_name="resetSubjectMatchAttribute")
    def reset_subject_match_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectMatchAttribute", []))

    @jsii.member(jsii_name="resetSubjectMatchType")
    def reset_subject_match_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectMatchType", []))

    @jsii.member(jsii_name="resetSuspendedAction")
    def reset_suspended_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspendedAction", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="userTypeId")
    def user_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTypeId"))

    @builtins.property
    @jsii.member(jsii_name="accountLinkActionInput")
    def account_link_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountLinkActionInput"))

    @builtins.property
    @jsii.member(jsii_name="accountLinkGroupIncludeInput")
    def account_link_group_include_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accountLinkGroupIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="acsBindingInput")
    def acs_binding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acsBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="acsTypeInput")
    def acs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="deprovisionedActionInput")
    def deprovisioned_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deprovisionedActionInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsActionInput")
    def groups_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupsActionInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsAssignmentInput")
    def groups_assignment_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsAssignmentInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsAttributeInput")
    def groups_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupsAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsFilterInput")
    def groups_filter_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerModeInput")
    def issuer_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerModeInput"))

    @builtins.property
    @jsii.member(jsii_name="kidInput")
    def kid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kidInput"))

    @builtins.property
    @jsii.member(jsii_name="maxClockSkewInput")
    def max_clock_skew_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxClockSkewInput"))

    @builtins.property
    @jsii.member(jsii_name="nameFormatInput")
    def name_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="profileMasterInput")
    def profile_master_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "profileMasterInput"))

    @builtins.property
    @jsii.member(jsii_name="provisioningActionInput")
    def provisioning_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provisioningActionInput"))

    @builtins.property
    @jsii.member(jsii_name="requestSignatureAlgorithmInput")
    def request_signature_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestSignatureAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="requestSignatureScopeInput")
    def request_signature_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestSignatureScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="responseSignatureAlgorithmInput")
    def response_signature_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseSignatureAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="responseSignatureScopeInput")
    def response_signature_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseSignatureScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoBindingInput")
    def sso_binding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssoBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoDestinationInput")
    def sso_destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssoDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoUrlInput")
    def sso_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssoUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectFilterInput")
    def subject_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectFormatInput")
    def subject_format_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subjectFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectMatchAttributeInput")
    def subject_match_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectMatchAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectMatchTypeInput")
    def subject_match_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectMatchTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendedActionInput")
    def suspended_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suspendedActionInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="accountLinkAction")
    def account_link_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountLinkAction"))

    @account_link_action.setter
    def account_link_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832bc5f92e788fa37a757015cfdbb1c8dbcbb9018e1d1d938666cc2e4689db3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountLinkAction", value)

    @builtins.property
    @jsii.member(jsii_name="accountLinkGroupInclude")
    def account_link_group_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountLinkGroupInclude"))

    @account_link_group_include.setter
    def account_link_group_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0965d47d48381e0ad5f8f5630069d89bb07634d2ad24e0631e81f9920f290bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountLinkGroupInclude", value)

    @builtins.property
    @jsii.member(jsii_name="acsBinding")
    def acs_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acsBinding"))

    @acs_binding.setter
    def acs_binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3beb6bb76de916a535fa70905d9fc0dea8b2914cf984f5176691bb33633cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acsBinding", value)

    @builtins.property
    @jsii.member(jsii_name="acsType")
    def acs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acsType"))

    @acs_type.setter
    def acs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59f44a4742ca9bbff964846d383df8b1f5424e859606ef42f9816d90f8ac031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acsType", value)

    @builtins.property
    @jsii.member(jsii_name="deprovisionedAction")
    def deprovisioned_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deprovisionedAction"))

    @deprovisioned_action.setter
    def deprovisioned_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b296692dc9cb0ed741e798920833b00225470cd7724e345d65675076d61e7107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deprovisionedAction", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAction")
    def groups_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupsAction"))

    @groups_action.setter
    def groups_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99fe29065f290f45749f00f7009855ccb87d16c3bf9db24cbd138a384d242fd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAction", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAssignment")
    def groups_assignment(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsAssignment"))

    @groups_assignment.setter
    def groups_assignment(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b16bb396ceea1ccde95b9f8e512fcff77937c6f90169e37d1b60dacaff543bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAssignment", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAttribute")
    def groups_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupsAttribute"))

    @groups_attribute.setter
    def groups_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef729b43ec61f369639be3b1a9130ad252d620a3165ba85bb3b3c2ade1a8918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="groupsFilter")
    def groups_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsFilter"))

    @groups_filter.setter
    def groups_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2427c6b788208aaa5aa3a7a26f902497b0c4d55114f2acd3ec31a5f3120edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsFilter", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e479a41f5062f94e5494ce1a82e14faf3059f0420df8da02a7a6d30d0493fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d41a99bac902acf38f892e47c53cc3239764c92af28d2ded4ad00392bfe1751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value)

    @builtins.property
    @jsii.member(jsii_name="issuerMode")
    def issuer_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerMode"))

    @issuer_mode.setter
    def issuer_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7efff200d77fc6cdd016442a7fdbdb625f94b3c7a2b631351967cc23ebca2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerMode", value)

    @builtins.property
    @jsii.member(jsii_name="kid")
    def kid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kid"))

    @kid.setter
    def kid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60bb8dcc3814d8af249536690843310c1afeff751f9eb6a725288f0229384929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kid", value)

    @builtins.property
    @jsii.member(jsii_name="maxClockSkew")
    def max_clock_skew(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClockSkew"))

    @max_clock_skew.setter
    def max_clock_skew(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4f218e6be8c0dc6c2123dbda7a4f845d947d5765fee4dedbc35d62e66b9cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxClockSkew", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe957fd25fbf6543260aac8b86fdbc8a4264907e53c82f2c30ce4bb9b97ca2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nameFormat")
    def name_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameFormat"))

    @name_format.setter
    def name_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de5d793991ea4b8c914f38e309628c399882af9a28488419461652c357f99184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameFormat", value)

    @builtins.property
    @jsii.member(jsii_name="profileMaster")
    def profile_master(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "profileMaster"))

    @profile_master.setter
    def profile_master(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50217b68f32653f0e1459a6f5082dcf5463deb1accafb0318af51c6d887adaef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileMaster", value)

    @builtins.property
    @jsii.member(jsii_name="provisioningAction")
    def provisioning_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisioningAction"))

    @provisioning_action.setter
    def provisioning_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d7d3a4e76278da672e143b8796517193ea25143ba2ed2cba745692d432130b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningAction", value)

    @builtins.property
    @jsii.member(jsii_name="requestSignatureAlgorithm")
    def request_signature_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestSignatureAlgorithm"))

    @request_signature_algorithm.setter
    def request_signature_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5f76768310c65f9edf3fa0661af554e8e01922a3e7b8d05fa01297eae22021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestSignatureAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="requestSignatureScope")
    def request_signature_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestSignatureScope"))

    @request_signature_scope.setter
    def request_signature_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6d12f52380e40f1a38448bc94037dc8ad816b0585de9fc5ace8f52d1642bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestSignatureScope", value)

    @builtins.property
    @jsii.member(jsii_name="responseSignatureAlgorithm")
    def response_signature_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseSignatureAlgorithm"))

    @response_signature_algorithm.setter
    def response_signature_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec250dc2a4ebde38c1dce820182e24f21cd6b4965734af49929cf9eb21be934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseSignatureAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="responseSignatureScope")
    def response_signature_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseSignatureScope"))

    @response_signature_scope.setter
    def response_signature_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebaf38480a7da2d81dff33c1d609e4814f0091f1e780d9054f93c8fa89971310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseSignatureScope", value)

    @builtins.property
    @jsii.member(jsii_name="ssoBinding")
    def sso_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoBinding"))

    @sso_binding.setter
    def sso_binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17487e197bd3939f9e334dccd64a05c74b2d24bec722f99a72db0e44b34f72f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoBinding", value)

    @builtins.property
    @jsii.member(jsii_name="ssoDestination")
    def sso_destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoDestination"))

    @sso_destination.setter
    def sso_destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a38916194b959bddd32e5725c00b698092a7a0c01ff69e50071b9a59054e7dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoDestination", value)

    @builtins.property
    @jsii.member(jsii_name="ssoUrl")
    def sso_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoUrl"))

    @sso_url.setter
    def sso_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a902bac3e8b0726b0db2c334d8e3682304919e4f500d00cced0a70009eb97c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoUrl", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f325b91ed41f836d5c2fc1f16ce5ab81e8230f19829b00803a624761e1571e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="subjectFilter")
    def subject_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectFilter"))

    @subject_filter.setter
    def subject_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03dfadc490cf8fd104833b4fb7d69aa71b9253e6fbfa2a18e0266785f1a170ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectFilter", value)

    @builtins.property
    @jsii.member(jsii_name="subjectFormat")
    def subject_format(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subjectFormat"))

    @subject_format.setter
    def subject_format(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6ebea960f6ff9d5eb832ad4e95e53069f43a0c00216d60033e466c24a4c3f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectFormat", value)

    @builtins.property
    @jsii.member(jsii_name="subjectMatchAttribute")
    def subject_match_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectMatchAttribute"))

    @subject_match_attribute.setter
    def subject_match_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05204b6e4ab45049ce2dde3e7a1d57e391c57593df86be9083efe2b9e5eddb21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectMatchAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="subjectMatchType")
    def subject_match_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectMatchType"))

    @subject_match_type.setter
    def subject_match_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bef9bcf96c05357d8eb66eb90a1f41064a5bd1caf325c7dab6f189a87ab9dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectMatchType", value)

    @builtins.property
    @jsii.member(jsii_name="suspendedAction")
    def suspended_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suspendedAction"))

    @suspended_action.setter
    def suspended_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d375f345f32a028a6bb3fffe3211a8f135dbd3ebdf7839e8db79413cdcdec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendedAction", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad30054bdbf0b433661e0459bac7859954d09f5ebb6392b239b8e5dc0dd61b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.idpSaml.IdpSamlConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "issuer": "issuer",
        "kid": "kid",
        "name": "name",
        "sso_url": "ssoUrl",
        "account_link_action": "accountLinkAction",
        "account_link_group_include": "accountLinkGroupInclude",
        "acs_binding": "acsBinding",
        "acs_type": "acsType",
        "deprovisioned_action": "deprovisionedAction",
        "groups_action": "groupsAction",
        "groups_assignment": "groupsAssignment",
        "groups_attribute": "groupsAttribute",
        "groups_filter": "groupsFilter",
        "id": "id",
        "issuer_mode": "issuerMode",
        "max_clock_skew": "maxClockSkew",
        "name_format": "nameFormat",
        "profile_master": "profileMaster",
        "provisioning_action": "provisioningAction",
        "request_signature_algorithm": "requestSignatureAlgorithm",
        "request_signature_scope": "requestSignatureScope",
        "response_signature_algorithm": "responseSignatureAlgorithm",
        "response_signature_scope": "responseSignatureScope",
        "sso_binding": "ssoBinding",
        "sso_destination": "ssoDestination",
        "status": "status",
        "subject_filter": "subjectFilter",
        "subject_format": "subjectFormat",
        "subject_match_attribute": "subjectMatchAttribute",
        "subject_match_type": "subjectMatchType",
        "suspended_action": "suspendedAction",
        "username_template": "usernameTemplate",
    },
)
class IdpSamlConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        issuer: builtins.str,
        kid: builtins.str,
        name: builtins.str,
        sso_url: builtins.str,
        account_link_action: typing.Optional[builtins.str] = None,
        account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        acs_binding: typing.Optional[builtins.str] = None,
        acs_type: typing.Optional[builtins.str] = None,
        deprovisioned_action: typing.Optional[builtins.str] = None,
        groups_action: typing.Optional[builtins.str] = None,
        groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_attribute: typing.Optional[builtins.str] = None,
        groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        max_clock_skew: typing.Optional[jsii.Number] = None,
        name_format: typing.Optional[builtins.str] = None,
        profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_action: typing.Optional[builtins.str] = None,
        request_signature_algorithm: typing.Optional[builtins.str] = None,
        request_signature_scope: typing.Optional[builtins.str] = None,
        response_signature_algorithm: typing.Optional[builtins.str] = None,
        response_signature_scope: typing.Optional[builtins.str] = None,
        sso_binding: typing.Optional[builtins.str] = None,
        sso_destination: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        subject_filter: typing.Optional[builtins.str] = None,
        subject_format: typing.Optional[typing.Sequence[builtins.str]] = None,
        subject_match_attribute: typing.Optional[builtins.str] = None,
        subject_match_type: typing.Optional[builtins.str] = None,
        suspended_action: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param issuer: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#issuer IdpSaml#issuer}.
        :param kid: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#kid IdpSaml#kid}.
        :param name: Name of the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#name IdpSaml#name}
        :param sso_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#sso_url IdpSaml#sso_url}.
        :param account_link_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#account_link_action IdpSaml#account_link_action}.
        :param account_link_group_include: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#account_link_group_include IdpSaml#account_link_group_include}.
        :param acs_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#acs_binding IdpSaml#acs_binding}.
        :param acs_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#acs_type IdpSaml#acs_type}.
        :param deprovisioned_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#deprovisioned_action IdpSaml#deprovisioned_action}.
        :param groups_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_action IdpSaml#groups_action}.
        :param groups_assignment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_assignment IdpSaml#groups_assignment}.
        :param groups_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_attribute IdpSaml#groups_attribute}.
        :param groups_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_filter IdpSaml#groups_filter}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#id IdpSaml#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_mode: Indicates whether Okta uses the original Okta org domain URL, or a custom domain URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#issuer_mode IdpSaml#issuer_mode}
        :param max_clock_skew: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#max_clock_skew IdpSaml#max_clock_skew}.
        :param name_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#name_format IdpSaml#name_format}.
        :param profile_master: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#profile_master IdpSaml#profile_master}.
        :param provisioning_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#provisioning_action IdpSaml#provisioning_action}.
        :param request_signature_algorithm: The XML digital Signature Algorithm used when signing an message. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#request_signature_algorithm IdpSaml#request_signature_algorithm}
        :param request_signature_scope: Specifies whether to digitally sign messages to the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#request_signature_scope IdpSaml#request_signature_scope}
        :param response_signature_algorithm: The minimum XML digital Signature Algorithm allowed when verifying a message or element. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#response_signature_algorithm IdpSaml#response_signature_algorithm}
        :param response_signature_scope: Specifies whether to verify a message or element XML digital signature. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#response_signature_scope IdpSaml#response_signature_scope}
        :param sso_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#sso_binding IdpSaml#sso_binding}.
        :param sso_destination: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#sso_destination IdpSaml#sso_destination}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#status IdpSaml#status}.
        :param subject_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_filter IdpSaml#subject_filter}.
        :param subject_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_format IdpSaml#subject_format}.
        :param subject_match_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_match_attribute IdpSaml#subject_match_attribute}.
        :param subject_match_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_match_type IdpSaml#subject_match_type}.
        :param suspended_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#suspended_action IdpSaml#suspended_action}.
        :param username_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#username_template IdpSaml#username_template}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6e69ab8fdcae3bb4f1fd223a20189a10478a54d9b041745223211afc98d6a5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument kid", value=kid, expected_type=type_hints["kid"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sso_url", value=sso_url, expected_type=type_hints["sso_url"])
            check_type(argname="argument account_link_action", value=account_link_action, expected_type=type_hints["account_link_action"])
            check_type(argname="argument account_link_group_include", value=account_link_group_include, expected_type=type_hints["account_link_group_include"])
            check_type(argname="argument acs_binding", value=acs_binding, expected_type=type_hints["acs_binding"])
            check_type(argname="argument acs_type", value=acs_type, expected_type=type_hints["acs_type"])
            check_type(argname="argument deprovisioned_action", value=deprovisioned_action, expected_type=type_hints["deprovisioned_action"])
            check_type(argname="argument groups_action", value=groups_action, expected_type=type_hints["groups_action"])
            check_type(argname="argument groups_assignment", value=groups_assignment, expected_type=type_hints["groups_assignment"])
            check_type(argname="argument groups_attribute", value=groups_attribute, expected_type=type_hints["groups_attribute"])
            check_type(argname="argument groups_filter", value=groups_filter, expected_type=type_hints["groups_filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument issuer_mode", value=issuer_mode, expected_type=type_hints["issuer_mode"])
            check_type(argname="argument max_clock_skew", value=max_clock_skew, expected_type=type_hints["max_clock_skew"])
            check_type(argname="argument name_format", value=name_format, expected_type=type_hints["name_format"])
            check_type(argname="argument profile_master", value=profile_master, expected_type=type_hints["profile_master"])
            check_type(argname="argument provisioning_action", value=provisioning_action, expected_type=type_hints["provisioning_action"])
            check_type(argname="argument request_signature_algorithm", value=request_signature_algorithm, expected_type=type_hints["request_signature_algorithm"])
            check_type(argname="argument request_signature_scope", value=request_signature_scope, expected_type=type_hints["request_signature_scope"])
            check_type(argname="argument response_signature_algorithm", value=response_signature_algorithm, expected_type=type_hints["response_signature_algorithm"])
            check_type(argname="argument response_signature_scope", value=response_signature_scope, expected_type=type_hints["response_signature_scope"])
            check_type(argname="argument sso_binding", value=sso_binding, expected_type=type_hints["sso_binding"])
            check_type(argname="argument sso_destination", value=sso_destination, expected_type=type_hints["sso_destination"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument subject_filter", value=subject_filter, expected_type=type_hints["subject_filter"])
            check_type(argname="argument subject_format", value=subject_format, expected_type=type_hints["subject_format"])
            check_type(argname="argument subject_match_attribute", value=subject_match_attribute, expected_type=type_hints["subject_match_attribute"])
            check_type(argname="argument subject_match_type", value=subject_match_type, expected_type=type_hints["subject_match_type"])
            check_type(argname="argument suspended_action", value=suspended_action, expected_type=type_hints["suspended_action"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issuer": issuer,
            "kid": kid,
            "name": name,
            "sso_url": sso_url,
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
        if account_link_action is not None:
            self._values["account_link_action"] = account_link_action
        if account_link_group_include is not None:
            self._values["account_link_group_include"] = account_link_group_include
        if acs_binding is not None:
            self._values["acs_binding"] = acs_binding
        if acs_type is not None:
            self._values["acs_type"] = acs_type
        if deprovisioned_action is not None:
            self._values["deprovisioned_action"] = deprovisioned_action
        if groups_action is not None:
            self._values["groups_action"] = groups_action
        if groups_assignment is not None:
            self._values["groups_assignment"] = groups_assignment
        if groups_attribute is not None:
            self._values["groups_attribute"] = groups_attribute
        if groups_filter is not None:
            self._values["groups_filter"] = groups_filter
        if id is not None:
            self._values["id"] = id
        if issuer_mode is not None:
            self._values["issuer_mode"] = issuer_mode
        if max_clock_skew is not None:
            self._values["max_clock_skew"] = max_clock_skew
        if name_format is not None:
            self._values["name_format"] = name_format
        if profile_master is not None:
            self._values["profile_master"] = profile_master
        if provisioning_action is not None:
            self._values["provisioning_action"] = provisioning_action
        if request_signature_algorithm is not None:
            self._values["request_signature_algorithm"] = request_signature_algorithm
        if request_signature_scope is not None:
            self._values["request_signature_scope"] = request_signature_scope
        if response_signature_algorithm is not None:
            self._values["response_signature_algorithm"] = response_signature_algorithm
        if response_signature_scope is not None:
            self._values["response_signature_scope"] = response_signature_scope
        if sso_binding is not None:
            self._values["sso_binding"] = sso_binding
        if sso_destination is not None:
            self._values["sso_destination"] = sso_destination
        if status is not None:
            self._values["status"] = status
        if subject_filter is not None:
            self._values["subject_filter"] = subject_filter
        if subject_format is not None:
            self._values["subject_format"] = subject_format
        if subject_match_attribute is not None:
            self._values["subject_match_attribute"] = subject_match_attribute
        if subject_match_type is not None:
            self._values["subject_match_type"] = subject_match_type
        if suspended_action is not None:
            self._values["suspended_action"] = suspended_action
        if username_template is not None:
            self._values["username_template"] = username_template

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
    def issuer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#issuer IdpSaml#issuer}.'''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kid(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#kid IdpSaml#kid}.'''
        result = self._values.get("kid")
        assert result is not None, "Required property 'kid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the IdP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#name IdpSaml#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sso_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#sso_url IdpSaml#sso_url}.'''
        result = self._values.get("sso_url")
        assert result is not None, "Required property 'sso_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_link_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#account_link_action IdpSaml#account_link_action}.'''
        result = self._values.get("account_link_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_link_group_include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#account_link_group_include IdpSaml#account_link_group_include}.'''
        result = self._values.get("account_link_group_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def acs_binding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#acs_binding IdpSaml#acs_binding}.'''
        result = self._values.get("acs_binding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def acs_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#acs_type IdpSaml#acs_type}.'''
        result = self._values.get("acs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deprovisioned_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#deprovisioned_action IdpSaml#deprovisioned_action}.'''
        result = self._values.get("deprovisioned_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_action IdpSaml#groups_action}.'''
        result = self._values.get("groups_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_assignment(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_assignment IdpSaml#groups_assignment}.'''
        result = self._values.get("groups_assignment")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def groups_attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_attribute IdpSaml#groups_attribute}.'''
        result = self._values.get("groups_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#groups_filter IdpSaml#groups_filter}.'''
        result = self._values.get("groups_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#id IdpSaml#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer_mode(self) -> typing.Optional[builtins.str]:
        '''Indicates whether Okta uses the original Okta org domain URL, or a custom domain URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#issuer_mode IdpSaml#issuer_mode}
        '''
        result = self._values.get("issuer_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_clock_skew(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#max_clock_skew IdpSaml#max_clock_skew}.'''
        result = self._values.get("max_clock_skew")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#name_format IdpSaml#name_format}.'''
        result = self._values.get("name_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile_master(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#profile_master IdpSaml#profile_master}.'''
        result = self._values.get("profile_master")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def provisioning_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#provisioning_action IdpSaml#provisioning_action}.'''
        result = self._values.get("provisioning_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_signature_algorithm(self) -> typing.Optional[builtins.str]:
        '''The XML digital Signature Algorithm used when signing an  message.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#request_signature_algorithm IdpSaml#request_signature_algorithm}
        '''
        result = self._values.get("request_signature_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_signature_scope(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to digitally sign  messages to the IdP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#request_signature_scope IdpSaml#request_signature_scope}
        '''
        result = self._values.get("request_signature_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_signature_algorithm(self) -> typing.Optional[builtins.str]:
        '''The minimum XML digital Signature Algorithm allowed when verifying a  message or  element.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#response_signature_algorithm IdpSaml#response_signature_algorithm}
        '''
        result = self._values.get("response_signature_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_signature_scope(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to verify a  message or  element XML digital signature.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#response_signature_scope IdpSaml#response_signature_scope}
        '''
        result = self._values.get("response_signature_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sso_binding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#sso_binding IdpSaml#sso_binding}.'''
        result = self._values.get("sso_binding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sso_destination(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#sso_destination IdpSaml#sso_destination}.'''
        result = self._values.get("sso_destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#status IdpSaml#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_filter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_filter IdpSaml#subject_filter}.'''
        result = self._values.get("subject_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_format(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_format IdpSaml#subject_format}.'''
        result = self._values.get("subject_format")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subject_match_attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_match_attribute IdpSaml#subject_match_attribute}.'''
        result = self._values.get("subject_match_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_match_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#subject_match_type IdpSaml#subject_match_type}.'''
        result = self._values.get("subject_match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspended_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#suspended_action IdpSaml#suspended_action}.'''
        result = self._values.get("suspended_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_saml#username_template IdpSaml#username_template}.'''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdpSamlConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IdpSaml",
    "IdpSamlConfig",
]

publication.publish()

def _typecheckingstub__d56dfbe40e32b3dfef94dccffcf0bf422e48db9b7d4d4475385ed11e496281c3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    issuer: builtins.str,
    kid: builtins.str,
    name: builtins.str,
    sso_url: builtins.str,
    account_link_action: typing.Optional[builtins.str] = None,
    account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    acs_binding: typing.Optional[builtins.str] = None,
    acs_type: typing.Optional[builtins.str] = None,
    deprovisioned_action: typing.Optional[builtins.str] = None,
    groups_action: typing.Optional[builtins.str] = None,
    groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_attribute: typing.Optional[builtins.str] = None,
    groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    max_clock_skew: typing.Optional[jsii.Number] = None,
    name_format: typing.Optional[builtins.str] = None,
    profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    provisioning_action: typing.Optional[builtins.str] = None,
    request_signature_algorithm: typing.Optional[builtins.str] = None,
    request_signature_scope: typing.Optional[builtins.str] = None,
    response_signature_algorithm: typing.Optional[builtins.str] = None,
    response_signature_scope: typing.Optional[builtins.str] = None,
    sso_binding: typing.Optional[builtins.str] = None,
    sso_destination: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    subject_filter: typing.Optional[builtins.str] = None,
    subject_format: typing.Optional[typing.Sequence[builtins.str]] = None,
    subject_match_attribute: typing.Optional[builtins.str] = None,
    subject_match_type: typing.Optional[builtins.str] = None,
    suspended_action: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__832bc5f92e788fa37a757015cfdbb1c8dbcbb9018e1d1d938666cc2e4689db3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0965d47d48381e0ad5f8f5630069d89bb07634d2ad24e0631e81f9920f290bf3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3beb6bb76de916a535fa70905d9fc0dea8b2914cf984f5176691bb33633cf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59f44a4742ca9bbff964846d383df8b1f5424e859606ef42f9816d90f8ac031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b296692dc9cb0ed741e798920833b00225470cd7724e345d65675076d61e7107(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99fe29065f290f45749f00f7009855ccb87d16c3bf9db24cbd138a384d242fd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b16bb396ceea1ccde95b9f8e512fcff77937c6f90169e37d1b60dacaff543bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef729b43ec61f369639be3b1a9130ad252d620a3165ba85bb3b3c2ade1a8918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2427c6b788208aaa5aa3a7a26f902497b0c4d55114f2acd3ec31a5f3120edf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e479a41f5062f94e5494ce1a82e14faf3059f0420df8da02a7a6d30d0493fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d41a99bac902acf38f892e47c53cc3239764c92af28d2ded4ad00392bfe1751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7efff200d77fc6cdd016442a7fdbdb625f94b3c7a2b631351967cc23ebca2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60bb8dcc3814d8af249536690843310c1afeff751f9eb6a725288f0229384929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4f218e6be8c0dc6c2123dbda7a4f845d947d5765fee4dedbc35d62e66b9cab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe957fd25fbf6543260aac8b86fdbc8a4264907e53c82f2c30ce4bb9b97ca2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5d793991ea4b8c914f38e309628c399882af9a28488419461652c357f99184(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50217b68f32653f0e1459a6f5082dcf5463deb1accafb0318af51c6d887adaef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d7d3a4e76278da672e143b8796517193ea25143ba2ed2cba745692d432130b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5f76768310c65f9edf3fa0661af554e8e01922a3e7b8d05fa01297eae22021(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6d12f52380e40f1a38448bc94037dc8ad816b0585de9fc5ace8f52d1642bf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec250dc2a4ebde38c1dce820182e24f21cd6b4965734af49929cf9eb21be934(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebaf38480a7da2d81dff33c1d609e4814f0091f1e780d9054f93c8fa89971310(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17487e197bd3939f9e334dccd64a05c74b2d24bec722f99a72db0e44b34f72f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a38916194b959bddd32e5725c00b698092a7a0c01ff69e50071b9a59054e7dbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a902bac3e8b0726b0db2c334d8e3682304919e4f500d00cced0a70009eb97c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f325b91ed41f836d5c2fc1f16ce5ab81e8230f19829b00803a624761e1571e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03dfadc490cf8fd104833b4fb7d69aa71b9253e6fbfa2a18e0266785f1a170ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6ebea960f6ff9d5eb832ad4e95e53069f43a0c00216d60033e466c24a4c3f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05204b6e4ab45049ce2dde3e7a1d57e391c57593df86be9083efe2b9e5eddb21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bef9bcf96c05357d8eb66eb90a1f41064a5bd1caf325c7dab6f189a87ab9dca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d375f345f32a028a6bb3fffe3211a8f135dbd3ebdf7839e8db79413cdcdec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad30054bdbf0b433661e0459bac7859954d09f5ebb6392b239b8e5dc0dd61b39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6e69ab8fdcae3bb4f1fd223a20189a10478a54d9b041745223211afc98d6a5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    issuer: builtins.str,
    kid: builtins.str,
    name: builtins.str,
    sso_url: builtins.str,
    account_link_action: typing.Optional[builtins.str] = None,
    account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    acs_binding: typing.Optional[builtins.str] = None,
    acs_type: typing.Optional[builtins.str] = None,
    deprovisioned_action: typing.Optional[builtins.str] = None,
    groups_action: typing.Optional[builtins.str] = None,
    groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_attribute: typing.Optional[builtins.str] = None,
    groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    max_clock_skew: typing.Optional[jsii.Number] = None,
    name_format: typing.Optional[builtins.str] = None,
    profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    provisioning_action: typing.Optional[builtins.str] = None,
    request_signature_algorithm: typing.Optional[builtins.str] = None,
    request_signature_scope: typing.Optional[builtins.str] = None,
    response_signature_algorithm: typing.Optional[builtins.str] = None,
    response_signature_scope: typing.Optional[builtins.str] = None,
    sso_binding: typing.Optional[builtins.str] = None,
    sso_destination: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    subject_filter: typing.Optional[builtins.str] = None,
    subject_format: typing.Optional[typing.Sequence[builtins.str]] = None,
    subject_match_attribute: typing.Optional[builtins.str] = None,
    subject_match_type: typing.Optional[builtins.str] = None,
    suspended_action: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
