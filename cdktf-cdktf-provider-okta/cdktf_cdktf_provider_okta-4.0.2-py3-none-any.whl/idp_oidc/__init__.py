'''
# `okta_idp_oidc`

Refer to the Terraform Registory for docs: [`okta_idp_oidc`](https://www.terraform.io/docs/providers/okta/r/idp_oidc).
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


class IdpOidc(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.idpOidc.IdpOidc",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc okta_idp_oidc}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authorization_binding: builtins.str,
        authorization_url: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        issuer_url: builtins.str,
        jwks_binding: builtins.str,
        jwks_url: builtins.str,
        name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        token_binding: builtins.str,
        token_url: builtins.str,
        account_link_action: typing.Optional[builtins.str] = None,
        account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        deprovisioned_action: typing.Optional[builtins.str] = None,
        groups_action: typing.Optional[builtins.str] = None,
        groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_attribute: typing.Optional[builtins.str] = None,
        groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        max_clock_skew: typing.Optional[jsii.Number] = None,
        profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        provisioning_action: typing.Optional[builtins.str] = None,
        request_signature_algorithm: typing.Optional[builtins.str] = None,
        request_signature_scope: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        subject_match_attribute: typing.Optional[builtins.str] = None,
        subject_match_type: typing.Optional[builtins.str] = None,
        suspended_action: typing.Optional[builtins.str] = None,
        user_info_binding: typing.Optional[builtins.str] = None,
        user_info_url: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc okta_idp_oidc} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authorization_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#authorization_binding IdpOidc#authorization_binding}.
        :param authorization_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#authorization_url IdpOidc#authorization_url}.
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#client_id IdpOidc#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#client_secret IdpOidc#client_secret}.
        :param issuer_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#issuer_url IdpOidc#issuer_url}.
        :param jwks_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#jwks_binding IdpOidc#jwks_binding}.
        :param jwks_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#jwks_url IdpOidc#jwks_url}.
        :param name: Name of the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#name IdpOidc#name}
        :param scopes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#scopes IdpOidc#scopes}.
        :param token_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#token_binding IdpOidc#token_binding}.
        :param token_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#token_url IdpOidc#token_url}.
        :param account_link_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#account_link_action IdpOidc#account_link_action}.
        :param account_link_group_include: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#account_link_group_include IdpOidc#account_link_group_include}.
        :param deprovisioned_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#deprovisioned_action IdpOidc#deprovisioned_action}.
        :param groups_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_action IdpOidc#groups_action}.
        :param groups_assignment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_assignment IdpOidc#groups_assignment}.
        :param groups_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_attribute IdpOidc#groups_attribute}.
        :param groups_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_filter IdpOidc#groups_filter}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#id IdpOidc#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_mode: Indicates whether Okta uses the original Okta org domain URL, custom domain URL, or dynamic. See Identity Provider attributes - issuerMode - https://developer.okta.com/docs/reference/api/idps/#identity-provider-attributes Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#issuer_mode IdpOidc#issuer_mode}
        :param max_clock_skew: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#max_clock_skew IdpOidc#max_clock_skew}.
        :param profile_master: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#profile_master IdpOidc#profile_master}.
        :param protocol_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#protocol_type IdpOidc#protocol_type}.
        :param provisioning_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#provisioning_action IdpOidc#provisioning_action}.
        :param request_signature_algorithm: The HMAC Signature Algorithm used when signing an authorization request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#request_signature_algorithm IdpOidc#request_signature_algorithm}
        :param request_signature_scope: Specifies whether to digitally sign an authorization request to the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#request_signature_scope IdpOidc#request_signature_scope}
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#status IdpOidc#status}.
        :param subject_match_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#subject_match_attribute IdpOidc#subject_match_attribute}.
        :param subject_match_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#subject_match_type IdpOidc#subject_match_type}.
        :param suspended_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#suspended_action IdpOidc#suspended_action}.
        :param user_info_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#user_info_binding IdpOidc#user_info_binding}.
        :param user_info_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#user_info_url IdpOidc#user_info_url}.
        :param username_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#username_template IdpOidc#username_template}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bd9d4eb5ea05d74b8370593a598e630012444063098df2f229b8394b539a29f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IdpOidcConfig(
            authorization_binding=authorization_binding,
            authorization_url=authorization_url,
            client_id=client_id,
            client_secret=client_secret,
            issuer_url=issuer_url,
            jwks_binding=jwks_binding,
            jwks_url=jwks_url,
            name=name,
            scopes=scopes,
            token_binding=token_binding,
            token_url=token_url,
            account_link_action=account_link_action,
            account_link_group_include=account_link_group_include,
            deprovisioned_action=deprovisioned_action,
            groups_action=groups_action,
            groups_assignment=groups_assignment,
            groups_attribute=groups_attribute,
            groups_filter=groups_filter,
            id=id,
            issuer_mode=issuer_mode,
            max_clock_skew=max_clock_skew,
            profile_master=profile_master,
            protocol_type=protocol_type,
            provisioning_action=provisioning_action,
            request_signature_algorithm=request_signature_algorithm,
            request_signature_scope=request_signature_scope,
            status=status,
            subject_match_attribute=subject_match_attribute,
            subject_match_type=subject_match_type,
            suspended_action=suspended_action,
            user_info_binding=user_info_binding,
            user_info_url=user_info_url,
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

    @jsii.member(jsii_name="resetProfileMaster")
    def reset_profile_master(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileMaster", []))

    @jsii.member(jsii_name="resetProtocolType")
    def reset_protocol_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolType", []))

    @jsii.member(jsii_name="resetProvisioningAction")
    def reset_provisioning_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisioningAction", []))

    @jsii.member(jsii_name="resetRequestSignatureAlgorithm")
    def reset_request_signature_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestSignatureAlgorithm", []))

    @jsii.member(jsii_name="resetRequestSignatureScope")
    def reset_request_signature_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestSignatureScope", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetSubjectMatchAttribute")
    def reset_subject_match_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectMatchAttribute", []))

    @jsii.member(jsii_name="resetSubjectMatchType")
    def reset_subject_match_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectMatchType", []))

    @jsii.member(jsii_name="resetSuspendedAction")
    def reset_suspended_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspendedAction", []))

    @jsii.member(jsii_name="resetUserInfoBinding")
    def reset_user_info_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserInfoBinding", []))

    @jsii.member(jsii_name="resetUserInfoUrl")
    def reset_user_info_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserInfoUrl", []))

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
    @jsii.member(jsii_name="authorizationBindingInput")
    def authorization_binding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationUrlInput")
    def authorization_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

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
    @jsii.member(jsii_name="issuerModeInput")
    def issuer_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerModeInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerUrlInput")
    def issuer_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="jwksBindingInput")
    def jwks_binding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jwksBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="jwksUrlInput")
    def jwks_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jwksUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="maxClockSkewInput")
    def max_clock_skew_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxClockSkewInput"))

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
    @jsii.member(jsii_name="protocolTypeInput")
    def protocol_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolTypeInput"))

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
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

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
    @jsii.member(jsii_name="tokenBindingInput")
    def token_binding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenUrlInput")
    def token_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="userInfoBindingInput")
    def user_info_binding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInfoBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="userInfoUrlInput")
    def user_info_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInfoUrlInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__29e86f6b0339efd881049e74f132489faef57c1a2e28047014545de20c2bdb40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountLinkAction", value)

    @builtins.property
    @jsii.member(jsii_name="accountLinkGroupInclude")
    def account_link_group_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountLinkGroupInclude"))

    @account_link_group_include.setter
    def account_link_group_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45fdbbab326ced1e02c0df9d7e57d03822b98c6e9cea21dcc2990e48bfdbcc28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountLinkGroupInclude", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationBinding")
    def authorization_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationBinding"))

    @authorization_binding.setter
    def authorization_binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ebaccc6a7139a12b04d5a33bac9a114e2ace4d42696ca2311662e0a299b2347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationBinding", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationUrl")
    def authorization_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationUrl"))

    @authorization_url.setter
    def authorization_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db357deda8d21dce804bf391cf88dbf5707421736fd2cd92526ad94ec2f64020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationUrl", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4ddf110af9963a5256d83812099ad5d68c8c0a0d00bac6904b299dcd3942e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37e927d14f088ec24f14412765c4c7b7c704a5ab8fd39e0bbe3cbd24eb826af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="deprovisionedAction")
    def deprovisioned_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deprovisionedAction"))

    @deprovisioned_action.setter
    def deprovisioned_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a769357b41a12fb1ebebe7c33a971c52fb0464fd650eca97892452ba6c05870b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deprovisionedAction", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAction")
    def groups_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupsAction"))

    @groups_action.setter
    def groups_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf1113eb23c99c53523ea84e3160b6473dc89eaea98391e08a66a7680945717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAction", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAssignment")
    def groups_assignment(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsAssignment"))

    @groups_assignment.setter
    def groups_assignment(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d863da206536b7c8fd647afda084b213ae6b7e44403f15736e031b4e3191411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAssignment", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAttribute")
    def groups_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupsAttribute"))

    @groups_attribute.setter
    def groups_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f916a515dedfd631a621ba52e67433242ff5e9fe3263bd591a1554825e8f7f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="groupsFilter")
    def groups_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsFilter"))

    @groups_filter.setter
    def groups_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d201ff5af0d0b3c29220ca214966df1afd1a231f139a887170fd2c55970df420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsFilter", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5b9dba8dbe0655a0e15b9074b55171033044ff5f9b0512bb8fcc6038abf161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="issuerMode")
    def issuer_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerMode"))

    @issuer_mode.setter
    def issuer_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7741162284036d3c1538d2d75b284b8b0dedc2f265fdf30bccde3dd3a3f799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerMode", value)

    @builtins.property
    @jsii.member(jsii_name="issuerUrl")
    def issuer_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUrl"))

    @issuer_url.setter
    def issuer_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e304d346173d67f61173f593dc3372a62761a1b095186ec3b686fb812e50d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUrl", value)

    @builtins.property
    @jsii.member(jsii_name="jwksBinding")
    def jwks_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwksBinding"))

    @jwks_binding.setter
    def jwks_binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07f8944e15364843b26d2c63435cf146e6c0de5fb787ec7d8585f489925a594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwksBinding", value)

    @builtins.property
    @jsii.member(jsii_name="jwksUrl")
    def jwks_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwksUrl"))

    @jwks_url.setter
    def jwks_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b0dad5443ba377cbd7e4ca99aa8f9e176a302daaafc70377e96985dc991473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwksUrl", value)

    @builtins.property
    @jsii.member(jsii_name="maxClockSkew")
    def max_clock_skew(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClockSkew"))

    @max_clock_skew.setter
    def max_clock_skew(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3eac5d464295809bf034a31d1c8126e919019a491a73db93057c985071dd3e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxClockSkew", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e474777b5553cdc5a87e6cc51b3ef0edf1fd7d8b0108598378dad43a2bb9bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__073c8ca6de75e9e73bb551c86610a70e75ef1b384e1232b3d93306e45251cb12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileMaster", value)

    @builtins.property
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolType"))

    @protocol_type.setter
    def protocol_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c3d6b3b7693c62379d93c8481784205d2c56d611f3d8c8955292cf5dc52c2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolType", value)

    @builtins.property
    @jsii.member(jsii_name="provisioningAction")
    def provisioning_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisioningAction"))

    @provisioning_action.setter
    def provisioning_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475340f795780f59493946b7113f1a954ed1eb90eadcd4803c0ed00bf63f231d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningAction", value)

    @builtins.property
    @jsii.member(jsii_name="requestSignatureAlgorithm")
    def request_signature_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestSignatureAlgorithm"))

    @request_signature_algorithm.setter
    def request_signature_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec06d63747f1d8f667f19e8b22e454724db12eb27fc61c119cd9b8124111a799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestSignatureAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="requestSignatureScope")
    def request_signature_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestSignatureScope"))

    @request_signature_scope.setter
    def request_signature_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a09f87c5bc8c0cbccecaacd2b2d315130225012523416dc41f9a400813c55cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestSignatureScope", value)

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23bc66d82db4da2283853039b3a454cc41dbbd68dea61463ba2a02137d0043d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9c53d99c3f0d55466b5b5e6d260c9818c9c853aabac1bde3ee4e05de1364a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="subjectMatchAttribute")
    def subject_match_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectMatchAttribute"))

    @subject_match_attribute.setter
    def subject_match_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53889f4a5f5a14ccfb568385742dc7b46772e761af0f3a0fe3cf8f233d96fc50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectMatchAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="subjectMatchType")
    def subject_match_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectMatchType"))

    @subject_match_type.setter
    def subject_match_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea69370de1cdf51b13fd7d7f0e5b969ed3780cc9fd317f4539ec0f8b0069bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectMatchType", value)

    @builtins.property
    @jsii.member(jsii_name="suspendedAction")
    def suspended_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suspendedAction"))

    @suspended_action.setter
    def suspended_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ad0b1bd03fd53a5f47fe375654437a70175b00e8b5a246db12d693b70ccbc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendedAction", value)

    @builtins.property
    @jsii.member(jsii_name="tokenBinding")
    def token_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenBinding"))

    @token_binding.setter
    def token_binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f16061cd5fe5988c192b84b128e701c05e6726fdaf0b1c7ecbab37cca64192a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenBinding", value)

    @builtins.property
    @jsii.member(jsii_name="tokenUrl")
    def token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenUrl"))

    @token_url.setter
    def token_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5251a5c6304158400051139c771efbe15ae87f87e4230118b49a6b3d78b1c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUrl", value)

    @builtins.property
    @jsii.member(jsii_name="userInfoBinding")
    def user_info_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userInfoBinding"))

    @user_info_binding.setter
    def user_info_binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9df64975d26f159e0effdbebeff98dd5e8a5c0bb7b6a26d2b44d526965f5be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userInfoBinding", value)

    @builtins.property
    @jsii.member(jsii_name="userInfoUrl")
    def user_info_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userInfoUrl"))

    @user_info_url.setter
    def user_info_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc60d476b9bc49d81c68d851a263aae9c34e2e62d8ab05f80c3d7e74da87c758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userInfoUrl", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c088f2e61d2f422d17f89cc3f22a385a41cc3cc021f63e66d580308139cfb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.idpOidc.IdpOidcConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "authorization_binding": "authorizationBinding",
        "authorization_url": "authorizationUrl",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "issuer_url": "issuerUrl",
        "jwks_binding": "jwksBinding",
        "jwks_url": "jwksUrl",
        "name": "name",
        "scopes": "scopes",
        "token_binding": "tokenBinding",
        "token_url": "tokenUrl",
        "account_link_action": "accountLinkAction",
        "account_link_group_include": "accountLinkGroupInclude",
        "deprovisioned_action": "deprovisionedAction",
        "groups_action": "groupsAction",
        "groups_assignment": "groupsAssignment",
        "groups_attribute": "groupsAttribute",
        "groups_filter": "groupsFilter",
        "id": "id",
        "issuer_mode": "issuerMode",
        "max_clock_skew": "maxClockSkew",
        "profile_master": "profileMaster",
        "protocol_type": "protocolType",
        "provisioning_action": "provisioningAction",
        "request_signature_algorithm": "requestSignatureAlgorithm",
        "request_signature_scope": "requestSignatureScope",
        "status": "status",
        "subject_match_attribute": "subjectMatchAttribute",
        "subject_match_type": "subjectMatchType",
        "suspended_action": "suspendedAction",
        "user_info_binding": "userInfoBinding",
        "user_info_url": "userInfoUrl",
        "username_template": "usernameTemplate",
    },
)
class IdpOidcConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authorization_binding: builtins.str,
        authorization_url: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        issuer_url: builtins.str,
        jwks_binding: builtins.str,
        jwks_url: builtins.str,
        name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        token_binding: builtins.str,
        token_url: builtins.str,
        account_link_action: typing.Optional[builtins.str] = None,
        account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        deprovisioned_action: typing.Optional[builtins.str] = None,
        groups_action: typing.Optional[builtins.str] = None,
        groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_attribute: typing.Optional[builtins.str] = None,
        groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        max_clock_skew: typing.Optional[jsii.Number] = None,
        profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        provisioning_action: typing.Optional[builtins.str] = None,
        request_signature_algorithm: typing.Optional[builtins.str] = None,
        request_signature_scope: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        subject_match_attribute: typing.Optional[builtins.str] = None,
        subject_match_type: typing.Optional[builtins.str] = None,
        suspended_action: typing.Optional[builtins.str] = None,
        user_info_binding: typing.Optional[builtins.str] = None,
        user_info_url: typing.Optional[builtins.str] = None,
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
        :param authorization_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#authorization_binding IdpOidc#authorization_binding}.
        :param authorization_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#authorization_url IdpOidc#authorization_url}.
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#client_id IdpOidc#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#client_secret IdpOidc#client_secret}.
        :param issuer_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#issuer_url IdpOidc#issuer_url}.
        :param jwks_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#jwks_binding IdpOidc#jwks_binding}.
        :param jwks_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#jwks_url IdpOidc#jwks_url}.
        :param name: Name of the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#name IdpOidc#name}
        :param scopes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#scopes IdpOidc#scopes}.
        :param token_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#token_binding IdpOidc#token_binding}.
        :param token_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#token_url IdpOidc#token_url}.
        :param account_link_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#account_link_action IdpOidc#account_link_action}.
        :param account_link_group_include: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#account_link_group_include IdpOidc#account_link_group_include}.
        :param deprovisioned_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#deprovisioned_action IdpOidc#deprovisioned_action}.
        :param groups_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_action IdpOidc#groups_action}.
        :param groups_assignment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_assignment IdpOidc#groups_assignment}.
        :param groups_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_attribute IdpOidc#groups_attribute}.
        :param groups_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_filter IdpOidc#groups_filter}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#id IdpOidc#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_mode: Indicates whether Okta uses the original Okta org domain URL, custom domain URL, or dynamic. See Identity Provider attributes - issuerMode - https://developer.okta.com/docs/reference/api/idps/#identity-provider-attributes Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#issuer_mode IdpOidc#issuer_mode}
        :param max_clock_skew: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#max_clock_skew IdpOidc#max_clock_skew}.
        :param profile_master: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#profile_master IdpOidc#profile_master}.
        :param protocol_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#protocol_type IdpOidc#protocol_type}.
        :param provisioning_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#provisioning_action IdpOidc#provisioning_action}.
        :param request_signature_algorithm: The HMAC Signature Algorithm used when signing an authorization request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#request_signature_algorithm IdpOidc#request_signature_algorithm}
        :param request_signature_scope: Specifies whether to digitally sign an authorization request to the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#request_signature_scope IdpOidc#request_signature_scope}
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#status IdpOidc#status}.
        :param subject_match_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#subject_match_attribute IdpOidc#subject_match_attribute}.
        :param subject_match_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#subject_match_type IdpOidc#subject_match_type}.
        :param suspended_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#suspended_action IdpOidc#suspended_action}.
        :param user_info_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#user_info_binding IdpOidc#user_info_binding}.
        :param user_info_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#user_info_url IdpOidc#user_info_url}.
        :param username_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#username_template IdpOidc#username_template}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc94c1916f8716199387125aec1f7ef3af6fe9d29d4873b7e93352ce0d63693)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument authorization_binding", value=authorization_binding, expected_type=type_hints["authorization_binding"])
            check_type(argname="argument authorization_url", value=authorization_url, expected_type=type_hints["authorization_url"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument issuer_url", value=issuer_url, expected_type=type_hints["issuer_url"])
            check_type(argname="argument jwks_binding", value=jwks_binding, expected_type=type_hints["jwks_binding"])
            check_type(argname="argument jwks_url", value=jwks_url, expected_type=type_hints["jwks_url"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument token_binding", value=token_binding, expected_type=type_hints["token_binding"])
            check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
            check_type(argname="argument account_link_action", value=account_link_action, expected_type=type_hints["account_link_action"])
            check_type(argname="argument account_link_group_include", value=account_link_group_include, expected_type=type_hints["account_link_group_include"])
            check_type(argname="argument deprovisioned_action", value=deprovisioned_action, expected_type=type_hints["deprovisioned_action"])
            check_type(argname="argument groups_action", value=groups_action, expected_type=type_hints["groups_action"])
            check_type(argname="argument groups_assignment", value=groups_assignment, expected_type=type_hints["groups_assignment"])
            check_type(argname="argument groups_attribute", value=groups_attribute, expected_type=type_hints["groups_attribute"])
            check_type(argname="argument groups_filter", value=groups_filter, expected_type=type_hints["groups_filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument issuer_mode", value=issuer_mode, expected_type=type_hints["issuer_mode"])
            check_type(argname="argument max_clock_skew", value=max_clock_skew, expected_type=type_hints["max_clock_skew"])
            check_type(argname="argument profile_master", value=profile_master, expected_type=type_hints["profile_master"])
            check_type(argname="argument protocol_type", value=protocol_type, expected_type=type_hints["protocol_type"])
            check_type(argname="argument provisioning_action", value=provisioning_action, expected_type=type_hints["provisioning_action"])
            check_type(argname="argument request_signature_algorithm", value=request_signature_algorithm, expected_type=type_hints["request_signature_algorithm"])
            check_type(argname="argument request_signature_scope", value=request_signature_scope, expected_type=type_hints["request_signature_scope"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument subject_match_attribute", value=subject_match_attribute, expected_type=type_hints["subject_match_attribute"])
            check_type(argname="argument subject_match_type", value=subject_match_type, expected_type=type_hints["subject_match_type"])
            check_type(argname="argument suspended_action", value=suspended_action, expected_type=type_hints["suspended_action"])
            check_type(argname="argument user_info_binding", value=user_info_binding, expected_type=type_hints["user_info_binding"])
            check_type(argname="argument user_info_url", value=user_info_url, expected_type=type_hints["user_info_url"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization_binding": authorization_binding,
            "authorization_url": authorization_url,
            "client_id": client_id,
            "client_secret": client_secret,
            "issuer_url": issuer_url,
            "jwks_binding": jwks_binding,
            "jwks_url": jwks_url,
            "name": name,
            "scopes": scopes,
            "token_binding": token_binding,
            "token_url": token_url,
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
        if profile_master is not None:
            self._values["profile_master"] = profile_master
        if protocol_type is not None:
            self._values["protocol_type"] = protocol_type
        if provisioning_action is not None:
            self._values["provisioning_action"] = provisioning_action
        if request_signature_algorithm is not None:
            self._values["request_signature_algorithm"] = request_signature_algorithm
        if request_signature_scope is not None:
            self._values["request_signature_scope"] = request_signature_scope
        if status is not None:
            self._values["status"] = status
        if subject_match_attribute is not None:
            self._values["subject_match_attribute"] = subject_match_attribute
        if subject_match_type is not None:
            self._values["subject_match_type"] = subject_match_type
        if suspended_action is not None:
            self._values["suspended_action"] = suspended_action
        if user_info_binding is not None:
            self._values["user_info_binding"] = user_info_binding
        if user_info_url is not None:
            self._values["user_info_url"] = user_info_url
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
    def authorization_binding(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#authorization_binding IdpOidc#authorization_binding}.'''
        result = self._values.get("authorization_binding")
        assert result is not None, "Required property 'authorization_binding' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#authorization_url IdpOidc#authorization_url}.'''
        result = self._values.get("authorization_url")
        assert result is not None, "Required property 'authorization_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#client_id IdpOidc#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#client_secret IdpOidc#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issuer_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#issuer_url IdpOidc#issuer_url}.'''
        result = self._values.get("issuer_url")
        assert result is not None, "Required property 'issuer_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jwks_binding(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#jwks_binding IdpOidc#jwks_binding}.'''
        result = self._values.get("jwks_binding")
        assert result is not None, "Required property 'jwks_binding' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jwks_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#jwks_url IdpOidc#jwks_url}.'''
        result = self._values.get("jwks_url")
        assert result is not None, "Required property 'jwks_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the IdP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#name IdpOidc#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scopes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#scopes IdpOidc#scopes}.'''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def token_binding(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#token_binding IdpOidc#token_binding}.'''
        result = self._values.get("token_binding")
        assert result is not None, "Required property 'token_binding' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#token_url IdpOidc#token_url}.'''
        result = self._values.get("token_url")
        assert result is not None, "Required property 'token_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_link_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#account_link_action IdpOidc#account_link_action}.'''
        result = self._values.get("account_link_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_link_group_include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#account_link_group_include IdpOidc#account_link_group_include}.'''
        result = self._values.get("account_link_group_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deprovisioned_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#deprovisioned_action IdpOidc#deprovisioned_action}.'''
        result = self._values.get("deprovisioned_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_action IdpOidc#groups_action}.'''
        result = self._values.get("groups_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_assignment(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_assignment IdpOidc#groups_assignment}.'''
        result = self._values.get("groups_assignment")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def groups_attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_attribute IdpOidc#groups_attribute}.'''
        result = self._values.get("groups_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#groups_filter IdpOidc#groups_filter}.'''
        result = self._values.get("groups_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#id IdpOidc#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer_mode(self) -> typing.Optional[builtins.str]:
        '''Indicates whether Okta uses the original Okta org domain URL, custom domain URL, or dynamic.

        See Identity Provider attributes - issuerMode - https://developer.okta.com/docs/reference/api/idps/#identity-provider-attributes

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#issuer_mode IdpOidc#issuer_mode}
        '''
        result = self._values.get("issuer_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_clock_skew(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#max_clock_skew IdpOidc#max_clock_skew}.'''
        result = self._values.get("max_clock_skew")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profile_master(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#profile_master IdpOidc#profile_master}.'''
        result = self._values.get("profile_master")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def protocol_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#protocol_type IdpOidc#protocol_type}.'''
        result = self._values.get("protocol_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#provisioning_action IdpOidc#provisioning_action}.'''
        result = self._values.get("provisioning_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_signature_algorithm(self) -> typing.Optional[builtins.str]:
        '''The HMAC Signature Algorithm used when signing an authorization request.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#request_signature_algorithm IdpOidc#request_signature_algorithm}
        '''
        result = self._values.get("request_signature_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_signature_scope(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to digitally sign an authorization request to the IdP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#request_signature_scope IdpOidc#request_signature_scope}
        '''
        result = self._values.get("request_signature_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#status IdpOidc#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_match_attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#subject_match_attribute IdpOidc#subject_match_attribute}.'''
        result = self._values.get("subject_match_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_match_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#subject_match_type IdpOidc#subject_match_type}.'''
        result = self._values.get("subject_match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspended_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#suspended_action IdpOidc#suspended_action}.'''
        result = self._values.get("suspended_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_info_binding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#user_info_binding IdpOidc#user_info_binding}.'''
        result = self._values.get("user_info_binding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_info_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#user_info_url IdpOidc#user_info_url}.'''
        result = self._values.get("user_info_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp_oidc#username_template IdpOidc#username_template}.'''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdpOidcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IdpOidc",
    "IdpOidcConfig",
]

publication.publish()

def _typecheckingstub__4bd9d4eb5ea05d74b8370593a598e630012444063098df2f229b8394b539a29f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authorization_binding: builtins.str,
    authorization_url: builtins.str,
    client_id: builtins.str,
    client_secret: builtins.str,
    issuer_url: builtins.str,
    jwks_binding: builtins.str,
    jwks_url: builtins.str,
    name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    token_binding: builtins.str,
    token_url: builtins.str,
    account_link_action: typing.Optional[builtins.str] = None,
    account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    deprovisioned_action: typing.Optional[builtins.str] = None,
    groups_action: typing.Optional[builtins.str] = None,
    groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_attribute: typing.Optional[builtins.str] = None,
    groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    max_clock_skew: typing.Optional[jsii.Number] = None,
    profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protocol_type: typing.Optional[builtins.str] = None,
    provisioning_action: typing.Optional[builtins.str] = None,
    request_signature_algorithm: typing.Optional[builtins.str] = None,
    request_signature_scope: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    subject_match_attribute: typing.Optional[builtins.str] = None,
    subject_match_type: typing.Optional[builtins.str] = None,
    suspended_action: typing.Optional[builtins.str] = None,
    user_info_binding: typing.Optional[builtins.str] = None,
    user_info_url: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__29e86f6b0339efd881049e74f132489faef57c1a2e28047014545de20c2bdb40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fdbbab326ced1e02c0df9d7e57d03822b98c6e9cea21dcc2990e48bfdbcc28(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebaccc6a7139a12b04d5a33bac9a114e2ace4d42696ca2311662e0a299b2347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db357deda8d21dce804bf391cf88dbf5707421736fd2cd92526ad94ec2f64020(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4ddf110af9963a5256d83812099ad5d68c8c0a0d00bac6904b299dcd3942e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37e927d14f088ec24f14412765c4c7b7c704a5ab8fd39e0bbe3cbd24eb826af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a769357b41a12fb1ebebe7c33a971c52fb0464fd650eca97892452ba6c05870b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf1113eb23c99c53523ea84e3160b6473dc89eaea98391e08a66a7680945717(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d863da206536b7c8fd647afda084b213ae6b7e44403f15736e031b4e3191411(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f916a515dedfd631a621ba52e67433242ff5e9fe3263bd591a1554825e8f7f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d201ff5af0d0b3c29220ca214966df1afd1a231f139a887170fd2c55970df420(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5b9dba8dbe0655a0e15b9074b55171033044ff5f9b0512bb8fcc6038abf161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7741162284036d3c1538d2d75b284b8b0dedc2f265fdf30bccde3dd3a3f799(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e304d346173d67f61173f593dc3372a62761a1b095186ec3b686fb812e50d35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07f8944e15364843b26d2c63435cf146e6c0de5fb787ec7d8585f489925a594(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b0dad5443ba377cbd7e4ca99aa8f9e176a302daaafc70377e96985dc991473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3eac5d464295809bf034a31d1c8126e919019a491a73db93057c985071dd3e1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e474777b5553cdc5a87e6cc51b3ef0edf1fd7d8b0108598378dad43a2bb9bb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073c8ca6de75e9e73bb551c86610a70e75ef1b384e1232b3d93306e45251cb12(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c3d6b3b7693c62379d93c8481784205d2c56d611f3d8c8955292cf5dc52c2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475340f795780f59493946b7113f1a954ed1eb90eadcd4803c0ed00bf63f231d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec06d63747f1d8f667f19e8b22e454724db12eb27fc61c119cd9b8124111a799(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a09f87c5bc8c0cbccecaacd2b2d315130225012523416dc41f9a400813c55cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23bc66d82db4da2283853039b3a454cc41dbbd68dea61463ba2a02137d0043d1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9c53d99c3f0d55466b5b5e6d260c9818c9c853aabac1bde3ee4e05de1364a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53889f4a5f5a14ccfb568385742dc7b46772e761af0f3a0fe3cf8f233d96fc50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea69370de1cdf51b13fd7d7f0e5b969ed3780cc9fd317f4539ec0f8b0069bda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ad0b1bd03fd53a5f47fe375654437a70175b00e8b5a246db12d693b70ccbc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16061cd5fe5988c192b84b128e701c05e6726fdaf0b1c7ecbab37cca64192a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5251a5c6304158400051139c771efbe15ae87f87e4230118b49a6b3d78b1c09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9df64975d26f159e0effdbebeff98dd5e8a5c0bb7b6a26d2b44d526965f5be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc60d476b9bc49d81c68d851a263aae9c34e2e62d8ab05f80c3d7e74da87c758(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c088f2e61d2f422d17f89cc3f22a385a41cc3cc021f63e66d580308139cfb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc94c1916f8716199387125aec1f7ef3af6fe9d29d4873b7e93352ce0d63693(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authorization_binding: builtins.str,
    authorization_url: builtins.str,
    client_id: builtins.str,
    client_secret: builtins.str,
    issuer_url: builtins.str,
    jwks_binding: builtins.str,
    jwks_url: builtins.str,
    name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    token_binding: builtins.str,
    token_url: builtins.str,
    account_link_action: typing.Optional[builtins.str] = None,
    account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    deprovisioned_action: typing.Optional[builtins.str] = None,
    groups_action: typing.Optional[builtins.str] = None,
    groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_attribute: typing.Optional[builtins.str] = None,
    groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    max_clock_skew: typing.Optional[jsii.Number] = None,
    profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protocol_type: typing.Optional[builtins.str] = None,
    provisioning_action: typing.Optional[builtins.str] = None,
    request_signature_algorithm: typing.Optional[builtins.str] = None,
    request_signature_scope: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    subject_match_attribute: typing.Optional[builtins.str] = None,
    subject_match_type: typing.Optional[builtins.str] = None,
    suspended_action: typing.Optional[builtins.str] = None,
    user_info_binding: typing.Optional[builtins.str] = None,
    user_info_url: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
