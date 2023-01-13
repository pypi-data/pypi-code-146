'''
# `okta_idp`

Refer to the Terraform Registory for docs: [`okta_idp`](https://www.terraform.io/docs/providers/okta/r/idp).
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


class Idp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.idp.Idp",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/idp okta_idp}.'''

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
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/idp okta_idp} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authorization_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#authorization_binding Idp#authorization_binding}.
        :param authorization_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#authorization_url Idp#authorization_url}.
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#client_id Idp#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#client_secret Idp#client_secret}.
        :param issuer_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#issuer_url Idp#issuer_url}.
        :param jwks_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#jwks_binding Idp#jwks_binding}.
        :param jwks_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#jwks_url Idp#jwks_url}.
        :param name: Name of the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#name Idp#name}
        :param scopes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#scopes Idp#scopes}.
        :param token_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#token_binding Idp#token_binding}.
        :param token_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#token_url Idp#token_url}.
        :param account_link_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#account_link_action Idp#account_link_action}.
        :param account_link_group_include: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#account_link_group_include Idp#account_link_group_include}.
        :param deprovisioned_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#deprovisioned_action Idp#deprovisioned_action}.
        :param groups_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_action Idp#groups_action}.
        :param groups_assignment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_assignment Idp#groups_assignment}.
        :param groups_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_attribute Idp#groups_attribute}.
        :param groups_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_filter Idp#groups_filter}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#id Idp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_mode: Indicates whether Okta uses the original Okta org domain URL, custom domain URL, or dynamic. See Identity Provider attributes - issuerMode - https://developer.okta.com/docs/reference/api/idps/#identity-provider-attributes Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#issuer_mode Idp#issuer_mode}
        :param max_clock_skew: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#max_clock_skew Idp#max_clock_skew}.
        :param profile_master: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#profile_master Idp#profile_master}.
        :param protocol_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#protocol_type Idp#protocol_type}.
        :param provisioning_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#provisioning_action Idp#provisioning_action}.
        :param request_signature_algorithm: The HMAC Signature Algorithm used when signing an authorization request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#request_signature_algorithm Idp#request_signature_algorithm}
        :param request_signature_scope: Specifies whether to digitally sign an authorization request to the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#request_signature_scope Idp#request_signature_scope}
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#status Idp#status}.
        :param subject_match_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#subject_match_attribute Idp#subject_match_attribute}.
        :param subject_match_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#subject_match_type Idp#subject_match_type}.
        :param suspended_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#suspended_action Idp#suspended_action}.
        :param user_info_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#user_info_binding Idp#user_info_binding}.
        :param user_info_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#user_info_url Idp#user_info_url}.
        :param username_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#username_template Idp#username_template}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319a3fa33c3a3b5fd612b603672644fd7bcfaaaae85e6b99adecc4d2bc818ddc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IdpConfig(
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
            type_hints = typing.get_type_hints(_typecheckingstub__6debe195b7eda68131da8e3ebb32e956015554e996221131bc4b93c36c24bbc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountLinkAction", value)

    @builtins.property
    @jsii.member(jsii_name="accountLinkGroupInclude")
    def account_link_group_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountLinkGroupInclude"))

    @account_link_group_include.setter
    def account_link_group_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4f86802865d4c713bbcf14ea6c49805e51e5ca2679eb7276b47d8d57353f37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountLinkGroupInclude", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationBinding")
    def authorization_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationBinding"))

    @authorization_binding.setter
    def authorization_binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5aae5045154360fd920806d4052cecc40d309f0765497fe0acf9d1156e5b32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationBinding", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationUrl")
    def authorization_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationUrl"))

    @authorization_url.setter
    def authorization_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fa1dd2f5bb88e65abe49fe994a0176be34380bc52a34751747289b20a15b7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationUrl", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2acc192bddfdcd2e92a40231fec4459e2858c0193946977900127b126d036c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8710c7489bb610b2e22f9226bd87ef1a8a8d5ab43ea70cd23aa48862b65cbb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="deprovisionedAction")
    def deprovisioned_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deprovisionedAction"))

    @deprovisioned_action.setter
    def deprovisioned_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64fdb22251ac482d35e04a9eaacd2900527e791d7412a433d1cd25e464d8863b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deprovisionedAction", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAction")
    def groups_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupsAction"))

    @groups_action.setter
    def groups_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a32d54c7021dd6bdc095c80b5261074e6eda5edfb0e31c2528a5db76610324d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAction", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAssignment")
    def groups_assignment(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsAssignment"))

    @groups_assignment.setter
    def groups_assignment(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72de9de8f3f88fd7e013d0daa47077fbab6ce726ceb1eb2053274f1809c7fed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAssignment", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAttribute")
    def groups_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupsAttribute"))

    @groups_attribute.setter
    def groups_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9afe3600fda4ea90c6d4468dcdde9e2dafb8f1d2b5701cc0d27d3e40288bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="groupsFilter")
    def groups_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsFilter"))

    @groups_filter.setter
    def groups_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029ccf0a490a30a9a9c144eb9e40bf05b3d82c34ed7f497415ad9ed89dea9bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsFilter", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746419750dcda563957d48d5dcf95bd80f0e498320343daf344166bbf6315dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="issuerMode")
    def issuer_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerMode"))

    @issuer_mode.setter
    def issuer_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3589903e0d8640578b7e9ee0e8627378589c4193d28b11cb95671cf0ea628f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerMode", value)

    @builtins.property
    @jsii.member(jsii_name="issuerUrl")
    def issuer_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUrl"))

    @issuer_url.setter
    def issuer_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feeae783382fc931c2a1fe05a19521b712c404367127ddc1a1bf4a63cb63ce50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUrl", value)

    @builtins.property
    @jsii.member(jsii_name="jwksBinding")
    def jwks_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwksBinding"))

    @jwks_binding.setter
    def jwks_binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113410a2a1b6e6086f3435abca81d371b828a8c9840c47dcdd34ac44a7deb217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwksBinding", value)

    @builtins.property
    @jsii.member(jsii_name="jwksUrl")
    def jwks_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jwksUrl"))

    @jwks_url.setter
    def jwks_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f89a52fcf8f73f591c05acac5eb72899cbebc86f453755357a2a1711bb72a210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwksUrl", value)

    @builtins.property
    @jsii.member(jsii_name="maxClockSkew")
    def max_clock_skew(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClockSkew"))

    @max_clock_skew.setter
    def max_clock_skew(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10fe44735f7601882989058f89e17e78e44276d89a5c473e8c1334a2d2ac1e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxClockSkew", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fee7def14a990617acc9176859893fb722ef966be238ab01a4eb2bbcf5dd899)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f357d0fb816920bacd0f1699e403ad4a6c2d995798a72f97052ebf877acb882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileMaster", value)

    @builtins.property
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolType"))

    @protocol_type.setter
    def protocol_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6082fb3de89c60a5b3b1d22c0cd94198cdfb9d6d268127478286ce5ac0241015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolType", value)

    @builtins.property
    @jsii.member(jsii_name="provisioningAction")
    def provisioning_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisioningAction"))

    @provisioning_action.setter
    def provisioning_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5a82e40061a340bf2392ab7b1d696e5684bbf2a3e16481cac84bd8eee0c246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningAction", value)

    @builtins.property
    @jsii.member(jsii_name="requestSignatureAlgorithm")
    def request_signature_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestSignatureAlgorithm"))

    @request_signature_algorithm.setter
    def request_signature_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aeb5e7686744d938312ea90e40a130a7a4c3ede8d9f3d9ed2dc27d8d1aa283b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestSignatureAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="requestSignatureScope")
    def request_signature_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestSignatureScope"))

    @request_signature_scope.setter
    def request_signature_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddabfaf41eaef8ca6414ccdb0afe3b3424b2c51c891e40a911c116bbd915d1e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestSignatureScope", value)

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b603e6ba4046991029c395351e5650adb4f2637b8bf8a86038dcb8d62cdbc6a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774cfec2b8e4eb13b91d042d22d09f5bb93d306e7e3b82fd0cf343c943a789a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="subjectMatchAttribute")
    def subject_match_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectMatchAttribute"))

    @subject_match_attribute.setter
    def subject_match_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d417db886e9adc1e2ca521d80a23df74a9dd4396f35f2277057aa17b1d0ac34c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectMatchAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="subjectMatchType")
    def subject_match_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectMatchType"))

    @subject_match_type.setter
    def subject_match_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47b45ce0dcb630535f8665bb4c5d987f89c0d2c1a14142f3e4cf01299768269f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectMatchType", value)

    @builtins.property
    @jsii.member(jsii_name="suspendedAction")
    def suspended_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suspendedAction"))

    @suspended_action.setter
    def suspended_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a0596f548ea0706f00e03424c772591bfa5deb0977c255aabc73bc29f3b889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendedAction", value)

    @builtins.property
    @jsii.member(jsii_name="tokenBinding")
    def token_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenBinding"))

    @token_binding.setter
    def token_binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8754e4c5e2d54c144e4e2c8d41ada1df2a9dc2dd2f2239c60ecac164dedc473c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenBinding", value)

    @builtins.property
    @jsii.member(jsii_name="tokenUrl")
    def token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenUrl"))

    @token_url.setter
    def token_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d78b51da4eadcd3652ac5ffd74b99f7b874eedc8d629e163ef1b51c3cf4c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUrl", value)

    @builtins.property
    @jsii.member(jsii_name="userInfoBinding")
    def user_info_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userInfoBinding"))

    @user_info_binding.setter
    def user_info_binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832bdd85f93ed0041df8f593fd18304309a7db88e321c0c9652e270b74f837db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userInfoBinding", value)

    @builtins.property
    @jsii.member(jsii_name="userInfoUrl")
    def user_info_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userInfoUrl"))

    @user_info_url.setter
    def user_info_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea44c8fefb80eb12d64e8c6df188ad7a4c4cc3f1efcc457aed7143c55c00e0a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userInfoUrl", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3200a3ad82b60179f948d50e3972f1cb28ef2621722e66eaee67b3a25c4f881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.idp.IdpConfig",
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
class IdpConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        :param authorization_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#authorization_binding Idp#authorization_binding}.
        :param authorization_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#authorization_url Idp#authorization_url}.
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#client_id Idp#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#client_secret Idp#client_secret}.
        :param issuer_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#issuer_url Idp#issuer_url}.
        :param jwks_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#jwks_binding Idp#jwks_binding}.
        :param jwks_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#jwks_url Idp#jwks_url}.
        :param name: Name of the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#name Idp#name}
        :param scopes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#scopes Idp#scopes}.
        :param token_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#token_binding Idp#token_binding}.
        :param token_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#token_url Idp#token_url}.
        :param account_link_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#account_link_action Idp#account_link_action}.
        :param account_link_group_include: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#account_link_group_include Idp#account_link_group_include}.
        :param deprovisioned_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#deprovisioned_action Idp#deprovisioned_action}.
        :param groups_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_action Idp#groups_action}.
        :param groups_assignment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_assignment Idp#groups_assignment}.
        :param groups_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_attribute Idp#groups_attribute}.
        :param groups_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_filter Idp#groups_filter}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#id Idp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_mode: Indicates whether Okta uses the original Okta org domain URL, custom domain URL, or dynamic. See Identity Provider attributes - issuerMode - https://developer.okta.com/docs/reference/api/idps/#identity-provider-attributes Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#issuer_mode Idp#issuer_mode}
        :param max_clock_skew: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#max_clock_skew Idp#max_clock_skew}.
        :param profile_master: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#profile_master Idp#profile_master}.
        :param protocol_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#protocol_type Idp#protocol_type}.
        :param provisioning_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#provisioning_action Idp#provisioning_action}.
        :param request_signature_algorithm: The HMAC Signature Algorithm used when signing an authorization request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#request_signature_algorithm Idp#request_signature_algorithm}
        :param request_signature_scope: Specifies whether to digitally sign an authorization request to the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#request_signature_scope Idp#request_signature_scope}
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#status Idp#status}.
        :param subject_match_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#subject_match_attribute Idp#subject_match_attribute}.
        :param subject_match_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#subject_match_type Idp#subject_match_type}.
        :param suspended_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#suspended_action Idp#suspended_action}.
        :param user_info_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#user_info_binding Idp#user_info_binding}.
        :param user_info_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#user_info_url Idp#user_info_url}.
        :param username_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#username_template Idp#username_template}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759339cad8e9fa64718502484e6ec54108609779c31dda32a8678985fd0205e7)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#authorization_binding Idp#authorization_binding}.'''
        result = self._values.get("authorization_binding")
        assert result is not None, "Required property 'authorization_binding' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#authorization_url Idp#authorization_url}.'''
        result = self._values.get("authorization_url")
        assert result is not None, "Required property 'authorization_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#client_id Idp#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#client_secret Idp#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issuer_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#issuer_url Idp#issuer_url}.'''
        result = self._values.get("issuer_url")
        assert result is not None, "Required property 'issuer_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jwks_binding(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#jwks_binding Idp#jwks_binding}.'''
        result = self._values.get("jwks_binding")
        assert result is not None, "Required property 'jwks_binding' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jwks_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#jwks_url Idp#jwks_url}.'''
        result = self._values.get("jwks_url")
        assert result is not None, "Required property 'jwks_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the IdP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#name Idp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scopes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#scopes Idp#scopes}.'''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def token_binding(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#token_binding Idp#token_binding}.'''
        result = self._values.get("token_binding")
        assert result is not None, "Required property 'token_binding' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#token_url Idp#token_url}.'''
        result = self._values.get("token_url")
        assert result is not None, "Required property 'token_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_link_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#account_link_action Idp#account_link_action}.'''
        result = self._values.get("account_link_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_link_group_include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#account_link_group_include Idp#account_link_group_include}.'''
        result = self._values.get("account_link_group_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deprovisioned_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#deprovisioned_action Idp#deprovisioned_action}.'''
        result = self._values.get("deprovisioned_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_action Idp#groups_action}.'''
        result = self._values.get("groups_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_assignment(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_assignment Idp#groups_assignment}.'''
        result = self._values.get("groups_assignment")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def groups_attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_attribute Idp#groups_attribute}.'''
        result = self._values.get("groups_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#groups_filter Idp#groups_filter}.'''
        result = self._values.get("groups_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#id Idp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer_mode(self) -> typing.Optional[builtins.str]:
        '''Indicates whether Okta uses the original Okta org domain URL, custom domain URL, or dynamic.

        See Identity Provider attributes - issuerMode - https://developer.okta.com/docs/reference/api/idps/#identity-provider-attributes

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#issuer_mode Idp#issuer_mode}
        '''
        result = self._values.get("issuer_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_clock_skew(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#max_clock_skew Idp#max_clock_skew}.'''
        result = self._values.get("max_clock_skew")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profile_master(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#profile_master Idp#profile_master}.'''
        result = self._values.get("profile_master")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def protocol_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#protocol_type Idp#protocol_type}.'''
        result = self._values.get("protocol_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#provisioning_action Idp#provisioning_action}.'''
        result = self._values.get("provisioning_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_signature_algorithm(self) -> typing.Optional[builtins.str]:
        '''The HMAC Signature Algorithm used when signing an authorization request.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#request_signature_algorithm Idp#request_signature_algorithm}
        '''
        result = self._values.get("request_signature_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_signature_scope(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to digitally sign an authorization request to the IdP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#request_signature_scope Idp#request_signature_scope}
        '''
        result = self._values.get("request_signature_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#status Idp#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_match_attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#subject_match_attribute Idp#subject_match_attribute}.'''
        result = self._values.get("subject_match_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_match_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#subject_match_type Idp#subject_match_type}.'''
        result = self._values.get("subject_match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspended_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#suspended_action Idp#suspended_action}.'''
        result = self._values.get("suspended_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_info_binding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#user_info_binding Idp#user_info_binding}.'''
        result = self._values.get("user_info_binding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_info_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#user_info_url Idp#user_info_url}.'''
        result = self._values.get("user_info_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/idp#username_template Idp#username_template}.'''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Idp",
    "IdpConfig",
]

publication.publish()

def _typecheckingstub__319a3fa33c3a3b5fd612b603672644fd7bcfaaaae85e6b99adecc4d2bc818ddc(
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

def _typecheckingstub__6debe195b7eda68131da8e3ebb32e956015554e996221131bc4b93c36c24bbc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4f86802865d4c713bbcf14ea6c49805e51e5ca2679eb7276b47d8d57353f37(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5aae5045154360fd920806d4052cecc40d309f0765497fe0acf9d1156e5b32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fa1dd2f5bb88e65abe49fe994a0176be34380bc52a34751747289b20a15b7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2acc192bddfdcd2e92a40231fec4459e2858c0193946977900127b126d036c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8710c7489bb610b2e22f9226bd87ef1a8a8d5ab43ea70cd23aa48862b65cbb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64fdb22251ac482d35e04a9eaacd2900527e791d7412a433d1cd25e464d8863b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a32d54c7021dd6bdc095c80b5261074e6eda5edfb0e31c2528a5db76610324d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72de9de8f3f88fd7e013d0daa47077fbab6ce726ceb1eb2053274f1809c7fed5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9afe3600fda4ea90c6d4468dcdde9e2dafb8f1d2b5701cc0d27d3e40288bc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029ccf0a490a30a9a9c144eb9e40bf05b3d82c34ed7f497415ad9ed89dea9bea(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746419750dcda563957d48d5dcf95bd80f0e498320343daf344166bbf6315dbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3589903e0d8640578b7e9ee0e8627378589c4193d28b11cb95671cf0ea628f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feeae783382fc931c2a1fe05a19521b712c404367127ddc1a1bf4a63cb63ce50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113410a2a1b6e6086f3435abca81d371b828a8c9840c47dcdd34ac44a7deb217(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89a52fcf8f73f591c05acac5eb72899cbebc86f453755357a2a1711bb72a210(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10fe44735f7601882989058f89e17e78e44276d89a5c473e8c1334a2d2ac1e22(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fee7def14a990617acc9176859893fb722ef966be238ab01a4eb2bbcf5dd899(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f357d0fb816920bacd0f1699e403ad4a6c2d995798a72f97052ebf877acb882(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6082fb3de89c60a5b3b1d22c0cd94198cdfb9d6d268127478286ce5ac0241015(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5a82e40061a340bf2392ab7b1d696e5684bbf2a3e16481cac84bd8eee0c246(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aeb5e7686744d938312ea90e40a130a7a4c3ede8d9f3d9ed2dc27d8d1aa283b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddabfaf41eaef8ca6414ccdb0afe3b3424b2c51c891e40a911c116bbd915d1e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b603e6ba4046991029c395351e5650adb4f2637b8bf8a86038dcb8d62cdbc6a0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774cfec2b8e4eb13b91d042d22d09f5bb93d306e7e3b82fd0cf343c943a789a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d417db886e9adc1e2ca521d80a23df74a9dd4396f35f2277057aa17b1d0ac34c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b45ce0dcb630535f8665bb4c5d987f89c0d2c1a14142f3e4cf01299768269f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a0596f548ea0706f00e03424c772591bfa5deb0977c255aabc73bc29f3b889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8754e4c5e2d54c144e4e2c8d41ada1df2a9dc2dd2f2239c60ecac164dedc473c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d78b51da4eadcd3652ac5ffd74b99f7b874eedc8d629e163ef1b51c3cf4c3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832bdd85f93ed0041df8f593fd18304309a7db88e321c0c9652e270b74f837db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea44c8fefb80eb12d64e8c6df188ad7a4c4cc3f1efcc457aed7143c55c00e0a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3200a3ad82b60179f948d50e3972f1cb28ef2621722e66eaee67b3a25c4f881(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759339cad8e9fa64718502484e6ec54108609779c31dda32a8678985fd0205e7(
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
