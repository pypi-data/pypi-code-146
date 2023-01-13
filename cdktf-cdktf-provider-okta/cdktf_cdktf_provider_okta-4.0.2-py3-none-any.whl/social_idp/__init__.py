'''
# `okta_social_idp`

Refer to the Terraform Registory for docs: [`okta_social_idp`](https://www.terraform.io/docs/providers/okta/r/social_idp).
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


class SocialIdp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.socialIdp.SocialIdp",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/social_idp okta_social_idp}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        type: builtins.str,
        account_link_action: typing.Optional[builtins.str] = None,
        account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        apple_kid: typing.Optional[builtins.str] = None,
        apple_private_key: typing.Optional[builtins.str] = None,
        apple_team_id: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        deprovisioned_action: typing.Optional[builtins.str] = None,
        groups_action: typing.Optional[builtins.str] = None,
        groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_attribute: typing.Optional[builtins.str] = None,
        groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        match_attribute: typing.Optional[builtins.str] = None,
        match_type: typing.Optional[builtins.str] = None,
        max_clock_skew: typing.Optional[jsii.Number] = None,
        profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        provisioning_action: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/social_idp okta_social_idp} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#name SocialIdp#name}
        :param scopes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#scopes SocialIdp#scopes}.
        :param type: Identity Provider Types: https://developer.okta.com/docs/reference/api/idps/#identity-provider-type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#type SocialIdp#type}
        :param account_link_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#account_link_action SocialIdp#account_link_action}.
        :param account_link_group_include: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#account_link_group_include SocialIdp#account_link_group_include}.
        :param apple_kid: The Key ID that you obtained from Apple when you created the private key for the client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#apple_kid SocialIdp#apple_kid}
        :param apple_private_key: The PKCS #8 encoded private key that you created for the client and downloaded from Apple. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#apple_private_key SocialIdp#apple_private_key}
        :param apple_team_id: The Team ID associated with your Apple developer account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#apple_team_id SocialIdp#apple_team_id}
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#client_id SocialIdp#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#client_secret SocialIdp#client_secret}.
        :param deprovisioned_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#deprovisioned_action SocialIdp#deprovisioned_action}.
        :param groups_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_action SocialIdp#groups_action}.
        :param groups_assignment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_assignment SocialIdp#groups_assignment}.
        :param groups_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_attribute SocialIdp#groups_attribute}.
        :param groups_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_filter SocialIdp#groups_filter}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#id SocialIdp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_mode: Indicates whether Okta uses the original Okta org domain URL, or a custom domain URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#issuer_mode SocialIdp#issuer_mode}
        :param match_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#match_attribute SocialIdp#match_attribute}.
        :param match_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#match_type SocialIdp#match_type}.
        :param max_clock_skew: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#max_clock_skew SocialIdp#max_clock_skew}.
        :param profile_master: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#profile_master SocialIdp#profile_master}.
        :param protocol_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#protocol_type SocialIdp#protocol_type}.
        :param provisioning_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#provisioning_action SocialIdp#provisioning_action}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#status SocialIdp#status}.
        :param subject_match_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#subject_match_attribute SocialIdp#subject_match_attribute}.
        :param subject_match_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#subject_match_type SocialIdp#subject_match_type}.
        :param suspended_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#suspended_action SocialIdp#suspended_action}.
        :param username_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#username_template SocialIdp#username_template}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b940cf2d7a514af55c5b5801bc7c820e6b72a3386aec84119e6215c71ee223)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SocialIdpConfig(
            name=name,
            scopes=scopes,
            type=type,
            account_link_action=account_link_action,
            account_link_group_include=account_link_group_include,
            apple_kid=apple_kid,
            apple_private_key=apple_private_key,
            apple_team_id=apple_team_id,
            client_id=client_id,
            client_secret=client_secret,
            deprovisioned_action=deprovisioned_action,
            groups_action=groups_action,
            groups_assignment=groups_assignment,
            groups_attribute=groups_attribute,
            groups_filter=groups_filter,
            id=id,
            issuer_mode=issuer_mode,
            match_attribute=match_attribute,
            match_type=match_type,
            max_clock_skew=max_clock_skew,
            profile_master=profile_master,
            protocol_type=protocol_type,
            provisioning_action=provisioning_action,
            status=status,
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

    @jsii.member(jsii_name="resetAppleKid")
    def reset_apple_kid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppleKid", []))

    @jsii.member(jsii_name="resetApplePrivateKey")
    def reset_apple_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplePrivateKey", []))

    @jsii.member(jsii_name="resetAppleTeamId")
    def reset_apple_team_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppleTeamId", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

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

    @jsii.member(jsii_name="resetMatchAttribute")
    def reset_match_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchAttribute", []))

    @jsii.member(jsii_name="resetMatchType")
    def reset_match_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchType", []))

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
    @jsii.member(jsii_name="authorizationBinding")
    def authorization_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationBinding"))

    @builtins.property
    @jsii.member(jsii_name="authorizationUrl")
    def authorization_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationUrl"))

    @builtins.property
    @jsii.member(jsii_name="tokenBinding")
    def token_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenBinding"))

    @builtins.property
    @jsii.member(jsii_name="tokenUrl")
    def token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenUrl"))

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
    @jsii.member(jsii_name="appleKidInput")
    def apple_kid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appleKidInput"))

    @builtins.property
    @jsii.member(jsii_name="applePrivateKeyInput")
    def apple_private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applePrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="appleTeamIdInput")
    def apple_team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appleTeamIdInput"))

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
    @jsii.member(jsii_name="matchAttributeInput")
    def match_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="matchTypeInput")
    def match_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchTypeInput"))

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
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3f0b78f563d0a3ff591eac902a8b3eb7fcbd9f86a5d7c3bd22f5da04c3b1437c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountLinkAction", value)

    @builtins.property
    @jsii.member(jsii_name="accountLinkGroupInclude")
    def account_link_group_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountLinkGroupInclude"))

    @account_link_group_include.setter
    def account_link_group_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff735853dd9e1a77ec586c2eb6b737252637e0ae1e37ab2f6964372dfd4d2b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountLinkGroupInclude", value)

    @builtins.property
    @jsii.member(jsii_name="appleKid")
    def apple_kid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appleKid"))

    @apple_kid.setter
    def apple_kid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df64594886ac6d4dfd18265fbe178d998add62435668edf6a5b082e1170315a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appleKid", value)

    @builtins.property
    @jsii.member(jsii_name="applePrivateKey")
    def apple_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applePrivateKey"))

    @apple_private_key.setter
    def apple_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64de221f15c5fa6bec5503f65ffdd72fa2afe6fa68692d9c4a990022e554cc5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applePrivateKey", value)

    @builtins.property
    @jsii.member(jsii_name="appleTeamId")
    def apple_team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appleTeamId"))

    @apple_team_id.setter
    def apple_team_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ffa7bc15d3a09638795507f3a18e5ac6f1e7fd093a9ed4adbe88baf3ac8bc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appleTeamId", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b831d3984bd7295864a65fc9e492ef49a51d02312d64266176a6589a92b6fcd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea05ea7568e7c6380fd80a20de8d7ea8c171d891f04fe2bcadc38c6d479a50e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="deprovisionedAction")
    def deprovisioned_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deprovisionedAction"))

    @deprovisioned_action.setter
    def deprovisioned_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41771740224d28be4cfd68599f5fa98f2bd6bd1cf58830654c1e5d0233bca8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deprovisionedAction", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAction")
    def groups_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupsAction"))

    @groups_action.setter
    def groups_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349efed929545e5718eaff4e405e6858318db18aae076def5652930d6d39eee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAction", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAssignment")
    def groups_assignment(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsAssignment"))

    @groups_assignment.setter
    def groups_assignment(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1052de86b23aa2b8b214d1780b60d5bc78ae53a192f6ea4070ecf1b88b5954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAssignment", value)

    @builtins.property
    @jsii.member(jsii_name="groupsAttribute")
    def groups_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupsAttribute"))

    @groups_attribute.setter
    def groups_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7eadb5111775cbf93b6bf0d0beac10ac2cd36c52e7be6aa1fbd2830579f11d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="groupsFilter")
    def groups_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsFilter"))

    @groups_filter.setter
    def groups_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ff760f2d54c16432aaeb0fb2cdb4c3fd7d71370a5d331ae3f8b19061a8b03f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsFilter", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dadf60db7c636741824f05854fb42590fa78040f8a3956f69cb0b718461dbe63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="issuerMode")
    def issuer_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerMode"))

    @issuer_mode.setter
    def issuer_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed22691454c66ef01a530c899621671da0134299404aec49d3264246a280787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerMode", value)

    @builtins.property
    @jsii.member(jsii_name="matchAttribute")
    def match_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchAttribute"))

    @match_attribute.setter
    def match_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e03f9f8dc0ee9fc03d9a8ac1c4c08a5ca5869c992cef01138de8084a6a19b07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="matchType")
    def match_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchType"))

    @match_type.setter
    def match_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9a03dfa2948956a40c2bc62a9c70960c19fb42760dbee7d448c3a72d670980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchType", value)

    @builtins.property
    @jsii.member(jsii_name="maxClockSkew")
    def max_clock_skew(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClockSkew"))

    @max_clock_skew.setter
    def max_clock_skew(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27778ade336ecbbb69fea018ed1a07092b3e1e0de218363e54aded7ea51424ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxClockSkew", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ae0f07742fdafd658db5821f5283d7026efeaf1281da74d17fa869d53efe30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb2fce9337e5415c69108ec476bde5c7dbcdd1f41e4503cad76dc7800a9e7a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profileMaster", value)

    @builtins.property
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolType"))

    @protocol_type.setter
    def protocol_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97e1ff99301a786c726aa394dd644cfc5a75f7a37b49033c1c5849728ab28036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolType", value)

    @builtins.property
    @jsii.member(jsii_name="provisioningAction")
    def provisioning_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisioningAction"))

    @provisioning_action.setter
    def provisioning_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4eaf8396085b609850cff219ab609456dd30151be1012fcd78cbd1b7f9d12f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningAction", value)

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b6dbabc40af19c89cce0831175099ae47662d0c089eed6bbb9cce7c288c2f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604fd3a67b5e9fcd4c9b907e22b5af26b055bcc05c9ff0ba0ebf759f660e822d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="subjectMatchAttribute")
    def subject_match_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectMatchAttribute"))

    @subject_match_attribute.setter
    def subject_match_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18933bc53084d8c9e52b1e24719ed7d17684c49027b8bbef88ee3057defe502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectMatchAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="subjectMatchType")
    def subject_match_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectMatchType"))

    @subject_match_type.setter
    def subject_match_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79df65e27b8f4442eb836d402c0624cc73c7b1dda05ad1d37de7e3cee5079379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectMatchType", value)

    @builtins.property
    @jsii.member(jsii_name="suspendedAction")
    def suspended_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suspendedAction"))

    @suspended_action.setter
    def suspended_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cbb1982fe9ac7e4a8ef1c90c8e6847b72cc260155eacc857fb3b2cac2d56e7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendedAction", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903ab3f78d2f438c827b19de33c6001df66ee1f62a747044d64413a5d777af06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dccb2c6be0e3df120433501239e10543c1e35b205eae620f474832691c84bdc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.socialIdp.SocialIdpConfig",
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
        "scopes": "scopes",
        "type": "type",
        "account_link_action": "accountLinkAction",
        "account_link_group_include": "accountLinkGroupInclude",
        "apple_kid": "appleKid",
        "apple_private_key": "applePrivateKey",
        "apple_team_id": "appleTeamId",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "deprovisioned_action": "deprovisionedAction",
        "groups_action": "groupsAction",
        "groups_assignment": "groupsAssignment",
        "groups_attribute": "groupsAttribute",
        "groups_filter": "groupsFilter",
        "id": "id",
        "issuer_mode": "issuerMode",
        "match_attribute": "matchAttribute",
        "match_type": "matchType",
        "max_clock_skew": "maxClockSkew",
        "profile_master": "profileMaster",
        "protocol_type": "protocolType",
        "provisioning_action": "provisioningAction",
        "status": "status",
        "subject_match_attribute": "subjectMatchAttribute",
        "subject_match_type": "subjectMatchType",
        "suspended_action": "suspendedAction",
        "username_template": "usernameTemplate",
    },
)
class SocialIdpConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        scopes: typing.Sequence[builtins.str],
        type: builtins.str,
        account_link_action: typing.Optional[builtins.str] = None,
        account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        apple_kid: typing.Optional[builtins.str] = None,
        apple_private_key: typing.Optional[builtins.str] = None,
        apple_team_id: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        deprovisioned_action: typing.Optional[builtins.str] = None,
        groups_action: typing.Optional[builtins.str] = None,
        groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_attribute: typing.Optional[builtins.str] = None,
        groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        match_attribute: typing.Optional[builtins.str] = None,
        match_type: typing.Optional[builtins.str] = None,
        max_clock_skew: typing.Optional[jsii.Number] = None,
        profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        provisioning_action: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
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
        :param name: Name of the IdP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#name SocialIdp#name}
        :param scopes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#scopes SocialIdp#scopes}.
        :param type: Identity Provider Types: https://developer.okta.com/docs/reference/api/idps/#identity-provider-type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#type SocialIdp#type}
        :param account_link_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#account_link_action SocialIdp#account_link_action}.
        :param account_link_group_include: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#account_link_group_include SocialIdp#account_link_group_include}.
        :param apple_kid: The Key ID that you obtained from Apple when you created the private key for the client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#apple_kid SocialIdp#apple_kid}
        :param apple_private_key: The PKCS #8 encoded private key that you created for the client and downloaded from Apple. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#apple_private_key SocialIdp#apple_private_key}
        :param apple_team_id: The Team ID associated with your Apple developer account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#apple_team_id SocialIdp#apple_team_id}
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#client_id SocialIdp#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#client_secret SocialIdp#client_secret}.
        :param deprovisioned_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#deprovisioned_action SocialIdp#deprovisioned_action}.
        :param groups_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_action SocialIdp#groups_action}.
        :param groups_assignment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_assignment SocialIdp#groups_assignment}.
        :param groups_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_attribute SocialIdp#groups_attribute}.
        :param groups_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_filter SocialIdp#groups_filter}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#id SocialIdp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_mode: Indicates whether Okta uses the original Okta org domain URL, or a custom domain URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#issuer_mode SocialIdp#issuer_mode}
        :param match_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#match_attribute SocialIdp#match_attribute}.
        :param match_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#match_type SocialIdp#match_type}.
        :param max_clock_skew: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#max_clock_skew SocialIdp#max_clock_skew}.
        :param profile_master: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#profile_master SocialIdp#profile_master}.
        :param protocol_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#protocol_type SocialIdp#protocol_type}.
        :param provisioning_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#provisioning_action SocialIdp#provisioning_action}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#status SocialIdp#status}.
        :param subject_match_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#subject_match_attribute SocialIdp#subject_match_attribute}.
        :param subject_match_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#subject_match_type SocialIdp#subject_match_type}.
        :param suspended_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#suspended_action SocialIdp#suspended_action}.
        :param username_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#username_template SocialIdp#username_template}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1afa9ad1e25c0f7d4d223e15df821c233d5b5939724018d07e3ddb5bb93d8925)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument account_link_action", value=account_link_action, expected_type=type_hints["account_link_action"])
            check_type(argname="argument account_link_group_include", value=account_link_group_include, expected_type=type_hints["account_link_group_include"])
            check_type(argname="argument apple_kid", value=apple_kid, expected_type=type_hints["apple_kid"])
            check_type(argname="argument apple_private_key", value=apple_private_key, expected_type=type_hints["apple_private_key"])
            check_type(argname="argument apple_team_id", value=apple_team_id, expected_type=type_hints["apple_team_id"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument deprovisioned_action", value=deprovisioned_action, expected_type=type_hints["deprovisioned_action"])
            check_type(argname="argument groups_action", value=groups_action, expected_type=type_hints["groups_action"])
            check_type(argname="argument groups_assignment", value=groups_assignment, expected_type=type_hints["groups_assignment"])
            check_type(argname="argument groups_attribute", value=groups_attribute, expected_type=type_hints["groups_attribute"])
            check_type(argname="argument groups_filter", value=groups_filter, expected_type=type_hints["groups_filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument issuer_mode", value=issuer_mode, expected_type=type_hints["issuer_mode"])
            check_type(argname="argument match_attribute", value=match_attribute, expected_type=type_hints["match_attribute"])
            check_type(argname="argument match_type", value=match_type, expected_type=type_hints["match_type"])
            check_type(argname="argument max_clock_skew", value=max_clock_skew, expected_type=type_hints["max_clock_skew"])
            check_type(argname="argument profile_master", value=profile_master, expected_type=type_hints["profile_master"])
            check_type(argname="argument protocol_type", value=protocol_type, expected_type=type_hints["protocol_type"])
            check_type(argname="argument provisioning_action", value=provisioning_action, expected_type=type_hints["provisioning_action"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument subject_match_attribute", value=subject_match_attribute, expected_type=type_hints["subject_match_attribute"])
            check_type(argname="argument subject_match_type", value=subject_match_type, expected_type=type_hints["subject_match_type"])
            check_type(argname="argument suspended_action", value=suspended_action, expected_type=type_hints["suspended_action"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "scopes": scopes,
            "type": type,
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
        if apple_kid is not None:
            self._values["apple_kid"] = apple_kid
        if apple_private_key is not None:
            self._values["apple_private_key"] = apple_private_key
        if apple_team_id is not None:
            self._values["apple_team_id"] = apple_team_id
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
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
        if match_attribute is not None:
            self._values["match_attribute"] = match_attribute
        if match_type is not None:
            self._values["match_type"] = match_type
        if max_clock_skew is not None:
            self._values["max_clock_skew"] = max_clock_skew
        if profile_master is not None:
            self._values["profile_master"] = profile_master
        if protocol_type is not None:
            self._values["protocol_type"] = protocol_type
        if provisioning_action is not None:
            self._values["provisioning_action"] = provisioning_action
        if status is not None:
            self._values["status"] = status
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
    def name(self) -> builtins.str:
        '''Name of the IdP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#name SocialIdp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scopes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#scopes SocialIdp#scopes}.'''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Identity Provider Types: https://developer.okta.com/docs/reference/api/idps/#identity-provider-type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#type SocialIdp#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_link_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#account_link_action SocialIdp#account_link_action}.'''
        result = self._values.get("account_link_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_link_group_include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#account_link_group_include SocialIdp#account_link_group_include}.'''
        result = self._values.get("account_link_group_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def apple_kid(self) -> typing.Optional[builtins.str]:
        '''The Key ID that you obtained from Apple when you created the private key for the client.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#apple_kid SocialIdp#apple_kid}
        '''
        result = self._values.get("apple_kid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apple_private_key(self) -> typing.Optional[builtins.str]:
        '''The PKCS #8 encoded private key that you created for the client and downloaded from Apple.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#apple_private_key SocialIdp#apple_private_key}
        '''
        result = self._values.get("apple_private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apple_team_id(self) -> typing.Optional[builtins.str]:
        '''The Team ID associated with your Apple developer account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#apple_team_id SocialIdp#apple_team_id}
        '''
        result = self._values.get("apple_team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#client_id SocialIdp#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#client_secret SocialIdp#client_secret}.'''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deprovisioned_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#deprovisioned_action SocialIdp#deprovisioned_action}.'''
        result = self._values.get("deprovisioned_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_action SocialIdp#groups_action}.'''
        result = self._values.get("groups_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_assignment(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_assignment SocialIdp#groups_assignment}.'''
        result = self._values.get("groups_assignment")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def groups_attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_attribute SocialIdp#groups_attribute}.'''
        result = self._values.get("groups_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#groups_filter SocialIdp#groups_filter}.'''
        result = self._values.get("groups_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#id SocialIdp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer_mode(self) -> typing.Optional[builtins.str]:
        '''Indicates whether Okta uses the original Okta org domain URL, or a custom domain URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#issuer_mode SocialIdp#issuer_mode}
        '''
        result = self._values.get("issuer_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#match_attribute SocialIdp#match_attribute}.'''
        result = self._values.get("match_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#match_type SocialIdp#match_type}.'''
        result = self._values.get("match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_clock_skew(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#max_clock_skew SocialIdp#max_clock_skew}.'''
        result = self._values.get("max_clock_skew")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profile_master(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#profile_master SocialIdp#profile_master}.'''
        result = self._values.get("profile_master")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def protocol_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#protocol_type SocialIdp#protocol_type}.'''
        result = self._values.get("protocol_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#provisioning_action SocialIdp#provisioning_action}.'''
        result = self._values.get("provisioning_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#status SocialIdp#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_match_attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#subject_match_attribute SocialIdp#subject_match_attribute}.'''
        result = self._values.get("subject_match_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_match_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#subject_match_type SocialIdp#subject_match_type}.'''
        result = self._values.get("subject_match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspended_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#suspended_action SocialIdp#suspended_action}.'''
        result = self._values.get("suspended_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/social_idp#username_template SocialIdp#username_template}.'''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SocialIdpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SocialIdp",
    "SocialIdpConfig",
]

publication.publish()

def _typecheckingstub__43b940cf2d7a514af55c5b5801bc7c820e6b72a3386aec84119e6215c71ee223(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    type: builtins.str,
    account_link_action: typing.Optional[builtins.str] = None,
    account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    apple_kid: typing.Optional[builtins.str] = None,
    apple_private_key: typing.Optional[builtins.str] = None,
    apple_team_id: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    deprovisioned_action: typing.Optional[builtins.str] = None,
    groups_action: typing.Optional[builtins.str] = None,
    groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_attribute: typing.Optional[builtins.str] = None,
    groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    match_attribute: typing.Optional[builtins.str] = None,
    match_type: typing.Optional[builtins.str] = None,
    max_clock_skew: typing.Optional[jsii.Number] = None,
    profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protocol_type: typing.Optional[builtins.str] = None,
    provisioning_action: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__3f0b78f563d0a3ff591eac902a8b3eb7fcbd9f86a5d7c3bd22f5da04c3b1437c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff735853dd9e1a77ec586c2eb6b737252637e0ae1e37ab2f6964372dfd4d2b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df64594886ac6d4dfd18265fbe178d998add62435668edf6a5b082e1170315a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64de221f15c5fa6bec5503f65ffdd72fa2afe6fa68692d9c4a990022e554cc5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ffa7bc15d3a09638795507f3a18e5ac6f1e7fd093a9ed4adbe88baf3ac8bc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b831d3984bd7295864a65fc9e492ef49a51d02312d64266176a6589a92b6fcd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea05ea7568e7c6380fd80a20de8d7ea8c171d891f04fe2bcadc38c6d479a50e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41771740224d28be4cfd68599f5fa98f2bd6bd1cf58830654c1e5d0233bca8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349efed929545e5718eaff4e405e6858318db18aae076def5652930d6d39eee1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1052de86b23aa2b8b214d1780b60d5bc78ae53a192f6ea4070ecf1b88b5954(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7eadb5111775cbf93b6bf0d0beac10ac2cd36c52e7be6aa1fbd2830579f11d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ff760f2d54c16432aaeb0fb2cdb4c3fd7d71370a5d331ae3f8b19061a8b03f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dadf60db7c636741824f05854fb42590fa78040f8a3956f69cb0b718461dbe63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed22691454c66ef01a530c899621671da0134299404aec49d3264246a280787(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e03f9f8dc0ee9fc03d9a8ac1c4c08a5ca5869c992cef01138de8084a6a19b07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9a03dfa2948956a40c2bc62a9c70960c19fb42760dbee7d448c3a72d670980(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27778ade336ecbbb69fea018ed1a07092b3e1e0de218363e54aded7ea51424ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ae0f07742fdafd658db5821f5283d7026efeaf1281da74d17fa869d53efe30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2fce9337e5415c69108ec476bde5c7dbcdd1f41e4503cad76dc7800a9e7a23(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e1ff99301a786c726aa394dd644cfc5a75f7a37b49033c1c5849728ab28036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4eaf8396085b609850cff219ab609456dd30151be1012fcd78cbd1b7f9d12f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b6dbabc40af19c89cce0831175099ae47662d0c089eed6bbb9cce7c288c2f9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604fd3a67b5e9fcd4c9b907e22b5af26b055bcc05c9ff0ba0ebf759f660e822d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18933bc53084d8c9e52b1e24719ed7d17684c49027b8bbef88ee3057defe502(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79df65e27b8f4442eb836d402c0624cc73c7b1dda05ad1d37de7e3cee5079379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cbb1982fe9ac7e4a8ef1c90c8e6847b72cc260155eacc857fb3b2cac2d56e7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903ab3f78d2f438c827b19de33c6001df66ee1f62a747044d64413a5d777af06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccb2c6be0e3df120433501239e10543c1e35b205eae620f474832691c84bdc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afa9ad1e25c0f7d4d223e15df821c233d5b5939724018d07e3ddb5bb93d8925(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    type: builtins.str,
    account_link_action: typing.Optional[builtins.str] = None,
    account_link_group_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    apple_kid: typing.Optional[builtins.str] = None,
    apple_private_key: typing.Optional[builtins.str] = None,
    apple_team_id: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    deprovisioned_action: typing.Optional[builtins.str] = None,
    groups_action: typing.Optional[builtins.str] = None,
    groups_assignment: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_attribute: typing.Optional[builtins.str] = None,
    groups_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    match_attribute: typing.Optional[builtins.str] = None,
    match_type: typing.Optional[builtins.str] = None,
    max_clock_skew: typing.Optional[jsii.Number] = None,
    profile_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protocol_type: typing.Optional[builtins.str] = None,
    provisioning_action: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    subject_match_attribute: typing.Optional[builtins.str] = None,
    subject_match_type: typing.Optional[builtins.str] = None,
    suspended_action: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
