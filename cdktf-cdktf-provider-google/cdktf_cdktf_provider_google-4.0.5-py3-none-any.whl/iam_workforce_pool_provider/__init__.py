'''
# `google_iam_workforce_pool_provider`

Refer to the Terraform Registory for docs: [`google_iam_workforce_pool_provider`](https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider).
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


class IamWorkforcePoolProvider(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProvider",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider google_iam_workforce_pool_provider}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        provider_id: builtins.str,
        workforce_pool_id: builtins.str,
        attribute_condition: typing.Optional[builtins.str] = None,
        attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["IamWorkforcePoolProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        saml: typing.Optional[typing.Union["IamWorkforcePoolProviderSaml", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["IamWorkforcePoolProviderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider google_iam_workforce_pool_provider} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#location IamWorkforcePoolProvider#location}
        :param provider_id: The ID for the provider, which becomes the final component of the resource name. This value must be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#provider_id IamWorkforcePoolProvider#provider_id}
        :param workforce_pool_id: The ID to use for the pool, which becomes the final component of the resource name. The IDs must be a globally unique string of 6 to 63 lowercase letters, digits, or hyphens. It must start with a letter, and cannot have a trailing hyphen. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#workforce_pool_id IamWorkforcePoolProvider#workforce_pool_id}
        :param attribute_condition: A `Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted. The expression must output a boolean representing whether to allow the federation. The following keywords may be referenced in the expressions: 'assertion': JSON representing the authentication credential issued by the provider. 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'. 'google.profile_photo' and 'google.display_name' are not supported. 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'. The maximum length of the attribute condition expression is 4096 characters. If unspecified, all valid authentication credentials will be accepted. The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins':: "'admins' in google.groups" Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#attribute_condition IamWorkforcePoolProvider#attribute_condition}
        :param attribute_mapping: Maps attributes from the authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'. Each key must be a string specifying the Google Cloud IAM attribute to map to. The following keys are supported: 'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings. This is also the subject that appears in Cloud Logging logs. This is a required field and the mapped subject cannot exceed 127 bytes. 'google.groups': Groups the authenticating user belongs to. You can grant groups access to resources using an IAM 'principalSet' binding; access applies to all members of the group. 'google.display_name': The name of the authenticated user. This is an optional field and the mapped display name cannot exceed 100 bytes. If not set, 'google.subject' will be displayed instead. This attribute cannot be referenced in IAM bindings. 'google.profile_photo': The URL that specifies the authenticated user's thumbnail photo. This is an optional field. When set, the image will be visible as the user's profile picture. If not set, a generic user icon will be displayed instead. This attribute cannot be referenced in IAM bindings. You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where {custom_attribute} is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes. The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_]. You can reference these attributes in IAM policies to define fine-grained access for a workforce pool to Google Cloud resources. For example: 'google.subject': 'principal://iam.googleapis.com/locations/{location}/workforcePools/{pool}/subject/{value}' 'google.groups': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/group/{value}' 'attribute.{custom_attribute}': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/attribute.{custom_attribute}/{value}' Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_ function that maps an identity provider credential to the normalized attribute specified by the corresponding map key. You can use the 'assertion' keyword in the expression to access a JSON representation of the authentication credential issued by the provider. The maximum length of an attribute mapping expression is 2048 characters. When evaluated, the total size of all mapped attributes must not exceed 8KB. For OIDC providers, you must supply a custom mapping that includes the 'google.subject' attribute. For example, the following maps the sub claim of the incoming credential to the 'subject' attribute on a Google token:: {"google.subject": "assertion.sub"} An object containing a list of '"key": value' pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#attribute_mapping IamWorkforcePoolProvider#attribute_mapping}
        :param description: A user-specified description of the provider. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#description IamWorkforcePoolProvider#description}
        :param disabled: Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#disabled IamWorkforcePoolProvider#disabled}
        :param display_name: A user-specified display name for the provider. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#display_name IamWorkforcePoolProvider#display_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#id IamWorkforcePoolProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oidc: oidc block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#oidc IamWorkforcePoolProvider#oidc}
        :param saml: saml block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#saml IamWorkforcePoolProvider#saml}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#timeouts IamWorkforcePoolProvider#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a47478adbd3ec68f1330af2d6ff9e243c88aefadc8c47839af58a905b566e88)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IamWorkforcePoolProviderConfig(
            location=location,
            provider_id=provider_id,
            workforce_pool_id=workforce_pool_id,
            attribute_condition=attribute_condition,
            attribute_mapping=attribute_mapping,
            description=description,
            disabled=disabled,
            display_name=display_name,
            id=id,
            oidc=oidc,
            saml=saml,
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

    @jsii.member(jsii_name="putOidc")
    def put_oidc(self, *, client_id: builtins.str, issuer_uri: builtins.str) -> None:
        '''
        :param client_id: The client ID. Must match the audience claim of the JWT issued by the identity provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#client_id IamWorkforcePoolProvider#client_id}
        :param issuer_uri: The OIDC issuer URI. Must be a valid URI using the 'https' scheme. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#issuer_uri IamWorkforcePoolProvider#issuer_uri}
        '''
        value = IamWorkforcePoolProviderOidc(
            client_id=client_id, issuer_uri=issuer_uri
        )

        return typing.cast(None, jsii.invoke(self, "putOidc", [value]))

    @jsii.member(jsii_name="putSaml")
    def put_saml(self, *, idp_metadata_xml: builtins.str) -> None:
        '''
        :param idp_metadata_xml: SAML Identity provider configuration metadata xml doc. The xml document should comply with `SAML 2.0 specification <https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf>`_. The max size of the acceptable xml document will be bounded to 128k characters. The metadata xml document should satisfy the following constraints: 1. Must contain an Identity Provider Entity ID. 2. Must contain at least one non-expired signing key certificate. 3. For each signing key: a) Valid from should be no more than 7 days from now. b) Valid to should be no more than 10 years in the future. 4. Up to 3 IdP signing keys are allowed in the metadata xml. When updating the provider's metadata xml, at least one non-expired signing key must overlap with the existing metadata. This requirement is skipped if there are no non-expired signing keys present in the existing metadata. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#idp_metadata_xml IamWorkforcePoolProvider#idp_metadata_xml}
        '''
        value = IamWorkforcePoolProviderSaml(idp_metadata_xml=idp_metadata_xml)

        return typing.cast(None, jsii.invoke(self, "putSaml", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#create IamWorkforcePoolProvider#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#delete IamWorkforcePoolProvider#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#update IamWorkforcePoolProvider#update}.
        '''
        value = IamWorkforcePoolProviderTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAttributeCondition")
    def reset_attribute_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeCondition", []))

    @jsii.member(jsii_name="resetAttributeMapping")
    def reset_attribute_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeMapping", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOidc")
    def reset_oidc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidc", []))

    @jsii.member(jsii_name="resetSaml")
    def reset_saml(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="oidc")
    def oidc(self) -> "IamWorkforcePoolProviderOidcOutputReference":
        return typing.cast("IamWorkforcePoolProviderOidcOutputReference", jsii.get(self, "oidc"))

    @builtins.property
    @jsii.member(jsii_name="saml")
    def saml(self) -> "IamWorkforcePoolProviderSamlOutputReference":
        return typing.cast("IamWorkforcePoolProviderSamlOutputReference", jsii.get(self, "saml"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "IamWorkforcePoolProviderTimeoutsOutputReference":
        return typing.cast("IamWorkforcePoolProviderTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="attributeConditionInput")
    def attribute_condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeMappingInput")
    def attribute_mapping_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "attributeMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcInput")
    def oidc_input(self) -> typing.Optional["IamWorkforcePoolProviderOidc"]:
        return typing.cast(typing.Optional["IamWorkforcePoolProviderOidc"], jsii.get(self, "oidcInput"))

    @builtins.property
    @jsii.member(jsii_name="providerIdInput")
    def provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="samlInput")
    def saml_input(self) -> typing.Optional["IamWorkforcePoolProviderSaml"]:
        return typing.cast(typing.Optional["IamWorkforcePoolProviderSaml"], jsii.get(self, "samlInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["IamWorkforcePoolProviderTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["IamWorkforcePoolProviderTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workforcePoolIdInput")
    def workforce_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workforcePoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeCondition")
    def attribute_condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeCondition"))

    @attribute_condition.setter
    def attribute_condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e1b0db9ca7a173514277f73861e3dfd873c59964ee6338ad0a4906a6cebbce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeCondition", value)

    @builtins.property
    @jsii.member(jsii_name="attributeMapping")
    def attribute_mapping(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "attributeMapping"))

    @attribute_mapping.setter
    def attribute_mapping(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032d5f57919a0dfc9718cafb55f934de9c55c82469fb80402ecbf369459802f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeMapping", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a6014637e2e44c92d7b6cbc9ffbad3f777798c19b66112dc44bbcb3b7a7be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b6ded60fec5aaedbb912b33165d57e36531fab776a60c2e22fe9bb0d994e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__386113e0e07c0c0a537d8b22ff22d768e34c68e7b50816f571c2d60d92252c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d9c6b2ce89f1ce316a2c5ad15c5390711e96396764ca8e4d9477d74ad1476e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d72abca926c4f1ca51e47a654f1463d0e21f4cb93c7ffe12f2099650fdcc8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="providerId")
    def provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerId"))

    @provider_id.setter
    def provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388af3eaa352f6297a8884a49ae9dfce1f413b0e9a2599cc3f14c5e1fda2b334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerId", value)

    @builtins.property
    @jsii.member(jsii_name="workforcePoolId")
    def workforce_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workforcePoolId"))

    @workforce_pool_id.setter
    def workforce_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d27e9ab4e8f7fbbbf2f10fe70a3b72cc78729aa9dfa6ea785e194ccc3eba4fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workforcePoolId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "provider_id": "providerId",
        "workforce_pool_id": "workforcePoolId",
        "attribute_condition": "attributeCondition",
        "attribute_mapping": "attributeMapping",
        "description": "description",
        "disabled": "disabled",
        "display_name": "displayName",
        "id": "id",
        "oidc": "oidc",
        "saml": "saml",
        "timeouts": "timeouts",
    },
)
class IamWorkforcePoolProviderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        provider_id: builtins.str,
        workforce_pool_id: builtins.str,
        attribute_condition: typing.Optional[builtins.str] = None,
        attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union["IamWorkforcePoolProviderOidc", typing.Dict[builtins.str, typing.Any]]] = None,
        saml: typing.Optional[typing.Union["IamWorkforcePoolProviderSaml", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["IamWorkforcePoolProviderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#location IamWorkforcePoolProvider#location}
        :param provider_id: The ID for the provider, which becomes the final component of the resource name. This value must be 4-32 characters, and may contain the characters [a-z0-9-]. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#provider_id IamWorkforcePoolProvider#provider_id}
        :param workforce_pool_id: The ID to use for the pool, which becomes the final component of the resource name. The IDs must be a globally unique string of 6 to 63 lowercase letters, digits, or hyphens. It must start with a letter, and cannot have a trailing hyphen. The prefix 'gcp-' is reserved for use by Google, and may not be specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#workforce_pool_id IamWorkforcePoolProvider#workforce_pool_id}
        :param attribute_condition: A `Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted. The expression must output a boolean representing whether to allow the federation. The following keywords may be referenced in the expressions: 'assertion': JSON representing the authentication credential issued by the provider. 'google': The Google attributes mapped from the assertion in the 'attribute_mappings'. 'google.profile_photo' and 'google.display_name' are not supported. 'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'. The maximum length of the attribute condition expression is 4096 characters. If unspecified, all valid authentication credentials will be accepted. The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins':: "'admins' in google.groups" Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#attribute_condition IamWorkforcePoolProvider#attribute_condition}
        :param attribute_mapping: Maps attributes from the authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'. Each key must be a string specifying the Google Cloud IAM attribute to map to. The following keys are supported: 'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings. This is also the subject that appears in Cloud Logging logs. This is a required field and the mapped subject cannot exceed 127 bytes. 'google.groups': Groups the authenticating user belongs to. You can grant groups access to resources using an IAM 'principalSet' binding; access applies to all members of the group. 'google.display_name': The name of the authenticated user. This is an optional field and the mapped display name cannot exceed 100 bytes. If not set, 'google.subject' will be displayed instead. This attribute cannot be referenced in IAM bindings. 'google.profile_photo': The URL that specifies the authenticated user's thumbnail photo. This is an optional field. When set, the image will be visible as the user's profile picture. If not set, a generic user icon will be displayed instead. This attribute cannot be referenced in IAM bindings. You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where {custom_attribute} is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes. The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_]. You can reference these attributes in IAM policies to define fine-grained access for a workforce pool to Google Cloud resources. For example: 'google.subject': 'principal://iam.googleapis.com/locations/{location}/workforcePools/{pool}/subject/{value}' 'google.groups': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/group/{value}' 'attribute.{custom_attribute}': 'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/attribute.{custom_attribute}/{value}' Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_ function that maps an identity provider credential to the normalized attribute specified by the corresponding map key. You can use the 'assertion' keyword in the expression to access a JSON representation of the authentication credential issued by the provider. The maximum length of an attribute mapping expression is 2048 characters. When evaluated, the total size of all mapped attributes must not exceed 8KB. For OIDC providers, you must supply a custom mapping that includes the 'google.subject' attribute. For example, the following maps the sub claim of the incoming credential to the 'subject' attribute on a Google token:: {"google.subject": "assertion.sub"} An object containing a list of '"key": value' pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#attribute_mapping IamWorkforcePoolProvider#attribute_mapping}
        :param description: A user-specified description of the provider. Cannot exceed 256 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#description IamWorkforcePoolProvider#description}
        :param disabled: Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#disabled IamWorkforcePoolProvider#disabled}
        :param display_name: A user-specified display name for the provider. Cannot exceed 32 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#display_name IamWorkforcePoolProvider#display_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#id IamWorkforcePoolProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param oidc: oidc block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#oidc IamWorkforcePoolProvider#oidc}
        :param saml: saml block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#saml IamWorkforcePoolProvider#saml}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#timeouts IamWorkforcePoolProvider#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(oidc, dict):
            oidc = IamWorkforcePoolProviderOidc(**oidc)
        if isinstance(saml, dict):
            saml = IamWorkforcePoolProviderSaml(**saml)
        if isinstance(timeouts, dict):
            timeouts = IamWorkforcePoolProviderTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f319fe9e23ad84ae4ef94ab842d5a90db41a5bf6b0d42dd96ab49e0f574fb2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument provider_id", value=provider_id, expected_type=type_hints["provider_id"])
            check_type(argname="argument workforce_pool_id", value=workforce_pool_id, expected_type=type_hints["workforce_pool_id"])
            check_type(argname="argument attribute_condition", value=attribute_condition, expected_type=type_hints["attribute_condition"])
            check_type(argname="argument attribute_mapping", value=attribute_mapping, expected_type=type_hints["attribute_mapping"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument oidc", value=oidc, expected_type=type_hints["oidc"])
            check_type(argname="argument saml", value=saml, expected_type=type_hints["saml"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "provider_id": provider_id,
            "workforce_pool_id": workforce_pool_id,
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
        if attribute_condition is not None:
            self._values["attribute_condition"] = attribute_condition
        if attribute_mapping is not None:
            self._values["attribute_mapping"] = attribute_mapping
        if description is not None:
            self._values["description"] = description
        if disabled is not None:
            self._values["disabled"] = disabled
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if oidc is not None:
            self._values["oidc"] = oidc
        if saml is not None:
            self._values["saml"] = saml
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
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#location IamWorkforcePoolProvider#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_id(self) -> builtins.str:
        '''The ID for the provider, which becomes the final component of the resource name.

        This value must be 4-32 characters, and may contain the characters [a-z0-9-].
        The prefix 'gcp-' is reserved for use by Google, and may not be specified.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#provider_id IamWorkforcePoolProvider#provider_id}
        '''
        result = self._values.get("provider_id")
        assert result is not None, "Required property 'provider_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workforce_pool_id(self) -> builtins.str:
        '''The ID to use for the pool, which becomes the final component of the resource name.

        The IDs must be a globally unique string of 6 to 63 lowercase letters, digits, or hyphens.
        It must start with a letter, and cannot have a trailing hyphen.
        The prefix 'gcp-' is reserved for use by Google, and may not be specified.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#workforce_pool_id IamWorkforcePoolProvider#workforce_pool_id}
        '''
        result = self._values.get("workforce_pool_id")
        assert result is not None, "Required property 'workforce_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attribute_condition(self) -> typing.Optional[builtins.str]:
        '''A `Common Expression Language <https://opensource.google/projects/cel>`_ expression, in plain text, to restrict what otherwise valid authentication credentials issued by the provider should not be accepted.

        The expression must output a boolean representing whether to allow the federation.

        The following keywords may be referenced in the expressions:
        'assertion': JSON representing the authentication credential issued by the provider.
        'google': The Google attributes mapped from the assertion in the 'attribute_mappings'.
        'google.profile_photo' and 'google.display_name' are not supported.
        'attribute': The custom attributes mapped from the assertion in the 'attribute_mappings'.

        The maximum length of the attribute condition expression is 4096 characters.
        If unspecified, all valid authentication credentials will be accepted.

        The following example shows how to only allow credentials with a mapped 'google.groups' value of 'admins'::

           "'admins' in google.groups"

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#attribute_condition IamWorkforcePoolProvider#attribute_condition}
        '''
        result = self._values.get("attribute_condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attribute_mapping(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Maps attributes from the authentication credentials issued by an external identity provider to Google Cloud attributes, such as 'subject' and 'segment'.

        Each key must be a string specifying the Google Cloud IAM attribute to map to.

        The following keys are supported:
        'google.subject': The principal IAM is authenticating. You can reference this value in IAM bindings.
        This is also the subject that appears in Cloud Logging logs. This is a required field and
        the mapped subject cannot exceed 127 bytes.
        'google.groups': Groups the authenticating user belongs to. You can grant groups access to
        resources using an IAM 'principalSet' binding; access applies to all members of the group.
        'google.display_name': The name of the authenticated user. This is an optional field and
        the mapped display name cannot exceed 100 bytes. If not set, 'google.subject' will be displayed instead.
        This attribute cannot be referenced in IAM bindings.
        'google.profile_photo': The URL that specifies the authenticated user's thumbnail photo.
        This is an optional field. When set, the image will be visible as the user's profile picture.
        If not set, a generic user icon will be displayed instead.
        This attribute cannot be referenced in IAM bindings.

        You can also provide custom attributes by specifying 'attribute.{custom_attribute}', where {custom_attribute}
        is the name of the custom attribute to be mapped. You can define a maximum of 50 custom attributes.
        The maximum length of a mapped attribute key is 100 characters, and the key may only contain the characters [a-z0-9_].

        You can reference these attributes in IAM policies to define fine-grained access for a workforce pool
        to Google Cloud resources. For example:
        'google.subject':
        'principal://iam.googleapis.com/locations/{location}/workforcePools/{pool}/subject/{value}'
        'google.groups':
        'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/group/{value}'
        'attribute.{custom_attribute}':
        'principalSet://iam.googleapis.com/locations/{location}/workforcePools/{pool}/attribute.{custom_attribute}/{value}'

        Each value must be a `Common Expression Language <https://opensource.google/projects/cel>`_
        function that maps an identity provider credential to the normalized attribute specified
        by the corresponding map key.

        You can use the 'assertion' keyword in the expression to access a JSON representation of
        the authentication credential issued by the provider.

        The maximum length of an attribute mapping expression is 2048 characters. When evaluated,
        the total size of all mapped attributes must not exceed 8KB.

        For OIDC providers, you must supply a custom mapping that includes the 'google.subject' attribute.
        For example, the following maps the sub claim of the incoming credential to the 'subject' attribute
        on a Google token::

           {"google.subject": "assertion.sub"}

        An object containing a list of '"key": value' pairs.
        Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#attribute_mapping IamWorkforcePoolProvider#attribute_mapping}
        '''
        result = self._values.get("attribute_mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A user-specified description of the provider. Cannot exceed 256 characters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#description IamWorkforcePoolProvider#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the provider is disabled. You cannot use a disabled provider to exchange tokens. However, existing tokens still grant access.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#disabled IamWorkforcePoolProvider#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A user-specified display name for the provider. Cannot exceed 32 characters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#display_name IamWorkforcePoolProvider#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#id IamWorkforcePoolProvider#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc(self) -> typing.Optional["IamWorkforcePoolProviderOidc"]:
        '''oidc block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#oidc IamWorkforcePoolProvider#oidc}
        '''
        result = self._values.get("oidc")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderOidc"], result)

    @builtins.property
    def saml(self) -> typing.Optional["IamWorkforcePoolProviderSaml"]:
        '''saml block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#saml IamWorkforcePoolProvider#saml}
        '''
        result = self._values.get("saml")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderSaml"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["IamWorkforcePoolProviderTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#timeouts IamWorkforcePoolProvider#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IamWorkforcePoolProviderTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderOidc",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "issuer_uri": "issuerUri"},
)
class IamWorkforcePoolProviderOidc:
    def __init__(self, *, client_id: builtins.str, issuer_uri: builtins.str) -> None:
        '''
        :param client_id: The client ID. Must match the audience claim of the JWT issued by the identity provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#client_id IamWorkforcePoolProvider#client_id}
        :param issuer_uri: The OIDC issuer URI. Must be a valid URI using the 'https' scheme. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#issuer_uri IamWorkforcePoolProvider#issuer_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b57aaa92d517f373514b558e9cc6f1654c111ed189ba3e7dab7de33a273b8d)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument issuer_uri", value=issuer_uri, expected_type=type_hints["issuer_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "issuer_uri": issuer_uri,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The client ID. Must match the audience claim of the JWT issued by the identity provider.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#client_id IamWorkforcePoolProvider#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issuer_uri(self) -> builtins.str:
        '''The OIDC issuer URI. Must be a valid URI using the 'https' scheme.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#issuer_uri IamWorkforcePoolProvider#issuer_uri}
        '''
        result = self._values.get("issuer_uri")
        assert result is not None, "Required property 'issuer_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderOidc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkforcePoolProviderOidcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderOidcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b42d3b7aeea5ee572f6030330e1f1b5cf62fb08283c8a9f700ba570d3e8690e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerUriInput")
    def issuer_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb2f7a9636131c9602f6edcefb4503f80cc41c3770aea14294b34a71e5683cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @issuer_uri.setter
    def issuer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b8eb23291f94e3d0869295e320512d58f2bbcee379c85fb251420eea5139cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUri", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IamWorkforcePoolProviderOidc]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderOidc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkforcePoolProviderOidc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c991c2e18daaa9dc1507ebc0880ee0507856a86918241dd36c3d4048a6e9f853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderSaml",
    jsii_struct_bases=[],
    name_mapping={"idp_metadata_xml": "idpMetadataXml"},
)
class IamWorkforcePoolProviderSaml:
    def __init__(self, *, idp_metadata_xml: builtins.str) -> None:
        '''
        :param idp_metadata_xml: SAML Identity provider configuration metadata xml doc. The xml document should comply with `SAML 2.0 specification <https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf>`_. The max size of the acceptable xml document will be bounded to 128k characters. The metadata xml document should satisfy the following constraints: 1. Must contain an Identity Provider Entity ID. 2. Must contain at least one non-expired signing key certificate. 3. For each signing key: a) Valid from should be no more than 7 days from now. b) Valid to should be no more than 10 years in the future. 4. Up to 3 IdP signing keys are allowed in the metadata xml. When updating the provider's metadata xml, at least one non-expired signing key must overlap with the existing metadata. This requirement is skipped if there are no non-expired signing keys present in the existing metadata. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#idp_metadata_xml IamWorkforcePoolProvider#idp_metadata_xml}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e519f57d11a4b738970c9ad61882e8e98eda02415eff90e33ef126224f0fbc03)
            check_type(argname="argument idp_metadata_xml", value=idp_metadata_xml, expected_type=type_hints["idp_metadata_xml"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "idp_metadata_xml": idp_metadata_xml,
        }

    @builtins.property
    def idp_metadata_xml(self) -> builtins.str:
        '''SAML Identity provider configuration metadata xml doc.

        The xml document should comply with `SAML 2.0 specification <https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf>`_.
        The max size of the acceptable xml document will be bounded to 128k characters.

        The metadata xml document should satisfy the following constraints:

        1. Must contain an Identity Provider Entity ID.
        2. Must contain at least one non-expired signing key certificate.
        3. For each signing key:
           a) Valid from should be no more than 7 days from now.
           b) Valid to should be no more than 10 years in the future.
        4. Up to 3 IdP signing keys are allowed in the metadata xml.

        When updating the provider's metadata xml, at least one non-expired signing key
        must overlap with the existing metadata. This requirement is skipped if there are
        no non-expired signing keys present in the existing metadata.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#idp_metadata_xml IamWorkforcePoolProvider#idp_metadata_xml}
        '''
        result = self._values.get("idp_metadata_xml")
        assert result is not None, "Required property 'idp_metadata_xml' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderSaml(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkforcePoolProviderSamlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderSamlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7539fa8677369208017df4ee32617076ab14d63f1a94112b870c85b746b9667e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idpMetadataXmlInput")
    def idp_metadata_xml_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idpMetadataXmlInput"))

    @builtins.property
    @jsii.member(jsii_name="idpMetadataXml")
    def idp_metadata_xml(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idpMetadataXml"))

    @idp_metadata_xml.setter
    def idp_metadata_xml(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682d1793fc37e9d105e567cf00e866d526e59a47edb95f1f76d87f9d95d0024b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpMetadataXml", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IamWorkforcePoolProviderSaml]:
        return typing.cast(typing.Optional[IamWorkforcePoolProviderSaml], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamWorkforcePoolProviderSaml],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5b4f74df985063879999e1db387d034115cbe0cf7e0c9dd46e58cd1c41fa4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class IamWorkforcePoolProviderTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#create IamWorkforcePoolProvider#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#delete IamWorkforcePoolProvider#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#update IamWorkforcePoolProvider#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ed77d8e497aa0090daaeaaa1378646a510614ac6d6fdd4362c17821bb1e520)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#create IamWorkforcePoolProvider#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#delete IamWorkforcePoolProvider#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/iam_workforce_pool_provider#update IamWorkforcePoolProvider#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamWorkforcePoolProviderTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamWorkforcePoolProviderTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamWorkforcePoolProvider.IamWorkforcePoolProviderTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed20058fa6d8611ae68b3eec817a674e1ab095e83d87345f8dac066e8a6ce14f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e866f1d559c40b98a0344726da1871af6395716a180a333cc191b0e51f03698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25f4a6410396b49bf9b66778c0be592eefe71d92c73f6225207cb64a31c0bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c181453d31a5f272ea17b3b08bec20a68f76651cc143eb627abcb3e650d3ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[IamWorkforcePoolProviderTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[IamWorkforcePoolProviderTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[IamWorkforcePoolProviderTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6522b6ce950dc2403c9c5c75f226a0a547af862cdfe02d026a7d443d3c7b97e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "IamWorkforcePoolProvider",
    "IamWorkforcePoolProviderConfig",
    "IamWorkforcePoolProviderOidc",
    "IamWorkforcePoolProviderOidcOutputReference",
    "IamWorkforcePoolProviderSaml",
    "IamWorkforcePoolProviderSamlOutputReference",
    "IamWorkforcePoolProviderTimeouts",
    "IamWorkforcePoolProviderTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9a47478adbd3ec68f1330af2d6ff9e243c88aefadc8c47839af58a905b566e88(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    provider_id: builtins.str,
    workforce_pool_id: builtins.str,
    attribute_condition: typing.Optional[builtins.str] = None,
    attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[IamWorkforcePoolProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    saml: typing.Optional[typing.Union[IamWorkforcePoolProviderSaml, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[IamWorkforcePoolProviderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d4e1b0db9ca7a173514277f73861e3dfd873c59964ee6338ad0a4906a6cebbce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032d5f57919a0dfc9718cafb55f934de9c55c82469fb80402ecbf369459802f2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a6014637e2e44c92d7b6cbc9ffbad3f777798c19b66112dc44bbcb3b7a7be6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b6ded60fec5aaedbb912b33165d57e36531fab776a60c2e22fe9bb0d994e72(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386113e0e07c0c0a537d8b22ff22d768e34c68e7b50816f571c2d60d92252c26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d9c6b2ce89f1ce316a2c5ad15c5390711e96396764ca8e4d9477d74ad1476e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d72abca926c4f1ca51e47a654f1463d0e21f4cb93c7ffe12f2099650fdcc8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388af3eaa352f6297a8884a49ae9dfce1f413b0e9a2599cc3f14c5e1fda2b334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d27e9ab4e8f7fbbbf2f10fe70a3b72cc78729aa9dfa6ea785e194ccc3eba4fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f319fe9e23ad84ae4ef94ab842d5a90db41a5bf6b0d42dd96ab49e0f574fb2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    provider_id: builtins.str,
    workforce_pool_id: builtins.str,
    attribute_condition: typing.Optional[builtins.str] = None,
    attribute_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[IamWorkforcePoolProviderOidc, typing.Dict[builtins.str, typing.Any]]] = None,
    saml: typing.Optional[typing.Union[IamWorkforcePoolProviderSaml, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[IamWorkforcePoolProviderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b57aaa92d517f373514b558e9cc6f1654c111ed189ba3e7dab7de33a273b8d(
    *,
    client_id: builtins.str,
    issuer_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b42d3b7aeea5ee572f6030330e1f1b5cf62fb08283c8a9f700ba570d3e8690e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb2f7a9636131c9602f6edcefb4503f80cc41c3770aea14294b34a71e5683cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b8eb23291f94e3d0869295e320512d58f2bbcee379c85fb251420eea5139cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c991c2e18daaa9dc1507ebc0880ee0507856a86918241dd36c3d4048a6e9f853(
    value: typing.Optional[IamWorkforcePoolProviderOidc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e519f57d11a4b738970c9ad61882e8e98eda02415eff90e33ef126224f0fbc03(
    *,
    idp_metadata_xml: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7539fa8677369208017df4ee32617076ab14d63f1a94112b870c85b746b9667e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682d1793fc37e9d105e567cf00e866d526e59a47edb95f1f76d87f9d95d0024b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5b4f74df985063879999e1db387d034115cbe0cf7e0c9dd46e58cd1c41fa4d(
    value: typing.Optional[IamWorkforcePoolProviderSaml],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ed77d8e497aa0090daaeaaa1378646a510614ac6d6fdd4362c17821bb1e520(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed20058fa6d8611ae68b3eec817a674e1ab095e83d87345f8dac066e8a6ce14f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e866f1d559c40b98a0344726da1871af6395716a180a333cc191b0e51f03698(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25f4a6410396b49bf9b66778c0be592eefe71d92c73f6225207cb64a31c0bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c181453d31a5f272ea17b3b08bec20a68f76651cc143eb627abcb3e650d3ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6522b6ce950dc2403c9c5c75f226a0a547af862cdfe02d026a7d443d3c7b97e6(
    value: typing.Optional[typing.Union[IamWorkforcePoolProviderTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
