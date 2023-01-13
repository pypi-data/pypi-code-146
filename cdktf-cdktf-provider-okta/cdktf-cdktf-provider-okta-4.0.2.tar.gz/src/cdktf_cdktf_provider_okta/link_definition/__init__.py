'''
# `okta_link_definition`

Refer to the Terraform Registory for docs: [`okta_link_definition`](https://www.terraform.io/docs/providers/okta/r/link_definition).
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


class LinkDefinition(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.linkDefinition.LinkDefinition",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/link_definition okta_link_definition}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        associated_description: builtins.str,
        associated_name: builtins.str,
        associated_title: builtins.str,
        primary_description: builtins.str,
        primary_name: builtins.str,
        primary_title: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/link_definition okta_link_definition} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param associated_description: Description of the associated relationship. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#associated_description LinkDefinition#associated_description}
        :param associated_name: API name of the associated link. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#associated_name LinkDefinition#associated_name}
        :param associated_title: Display name of the associated link. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#associated_title LinkDefinition#associated_title}
        :param primary_description: Description of the primary relationship. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#primary_description LinkDefinition#primary_description}
        :param primary_name: API name of the primary link. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#primary_name LinkDefinition#primary_name}
        :param primary_title: Display name of the primary link. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#primary_title LinkDefinition#primary_title}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#id LinkDefinition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2d6bbcf61fdffc42d76ee78c8784e21ec6b82a3805b54ad7fe839d4965d4cf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LinkDefinitionConfig(
            associated_description=associated_description,
            associated_name=associated_name,
            associated_title=associated_title,
            primary_description=primary_description,
            primary_name=primary_name,
            primary_title=primary_title,
            id=id,
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

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="associatedDescriptionInput")
    def associated_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "associatedDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="associatedNameInput")
    def associated_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "associatedNameInput"))

    @builtins.property
    @jsii.member(jsii_name="associatedTitleInput")
    def associated_title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "associatedTitleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryDescriptionInput")
    def primary_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryNameInput")
    def primary_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryNameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryTitleInput")
    def primary_title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryTitleInput"))

    @builtins.property
    @jsii.member(jsii_name="associatedDescription")
    def associated_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "associatedDescription"))

    @associated_description.setter
    def associated_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f91d9ca5d397086c820ad8b8b73afcfbffc6353a4a60610eca10db07d3bf80c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedDescription", value)

    @builtins.property
    @jsii.member(jsii_name="associatedName")
    def associated_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "associatedName"))

    @associated_name.setter
    def associated_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1f01ac0bc3c20926e936f2b78e5b7f3396fab4ba4b27ceccf6427d23f522e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedName", value)

    @builtins.property
    @jsii.member(jsii_name="associatedTitle")
    def associated_title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "associatedTitle"))

    @associated_title.setter
    def associated_title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07710735f46c2b1077ee237a97db930c83209b540efd5c70a4a934993fa718d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedTitle", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673b488b87ed5697ee5b6155b1fe1a6e09057da3d8d9d09302630d059d71deb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="primaryDescription")
    def primary_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryDescription"))

    @primary_description.setter
    def primary_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8561cb62791fbeb2c4efdb679f11a5a5927b2c7a0883adbe27dec3664c377154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryDescription", value)

    @builtins.property
    @jsii.member(jsii_name="primaryName")
    def primary_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryName"))

    @primary_name.setter
    def primary_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00032a4e25c927c84917e92370b1eccfb0d4a65e7c6b2339b6286fe3016209b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryName", value)

    @builtins.property
    @jsii.member(jsii_name="primaryTitle")
    def primary_title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryTitle"))

    @primary_title.setter
    def primary_title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea98a9788cce5806c6b1d85b7261162b14e41b534776b015ceceb6b563d1be55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryTitle", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.linkDefinition.LinkDefinitionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "associated_description": "associatedDescription",
        "associated_name": "associatedName",
        "associated_title": "associatedTitle",
        "primary_description": "primaryDescription",
        "primary_name": "primaryName",
        "primary_title": "primaryTitle",
        "id": "id",
    },
)
class LinkDefinitionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        associated_description: builtins.str,
        associated_name: builtins.str,
        associated_title: builtins.str,
        primary_description: builtins.str,
        primary_name: builtins.str,
        primary_title: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param associated_description: Description of the associated relationship. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#associated_description LinkDefinition#associated_description}
        :param associated_name: API name of the associated link. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#associated_name LinkDefinition#associated_name}
        :param associated_title: Display name of the associated link. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#associated_title LinkDefinition#associated_title}
        :param primary_description: Description of the primary relationship. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#primary_description LinkDefinition#primary_description}
        :param primary_name: API name of the primary link. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#primary_name LinkDefinition#primary_name}
        :param primary_title: Display name of the primary link. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#primary_title LinkDefinition#primary_title}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#id LinkDefinition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216d62386f6163bf701ccdca38718e4915c93201d57dcc2711c89651544b1357)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument associated_description", value=associated_description, expected_type=type_hints["associated_description"])
            check_type(argname="argument associated_name", value=associated_name, expected_type=type_hints["associated_name"])
            check_type(argname="argument associated_title", value=associated_title, expected_type=type_hints["associated_title"])
            check_type(argname="argument primary_description", value=primary_description, expected_type=type_hints["primary_description"])
            check_type(argname="argument primary_name", value=primary_name, expected_type=type_hints["primary_name"])
            check_type(argname="argument primary_title", value=primary_title, expected_type=type_hints["primary_title"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "associated_description": associated_description,
            "associated_name": associated_name,
            "associated_title": associated_title,
            "primary_description": primary_description,
            "primary_name": primary_name,
            "primary_title": primary_title,
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
        if id is not None:
            self._values["id"] = id

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
    def associated_description(self) -> builtins.str:
        '''Description of the associated relationship.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#associated_description LinkDefinition#associated_description}
        '''
        result = self._values.get("associated_description")
        assert result is not None, "Required property 'associated_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def associated_name(self) -> builtins.str:
        '''API name of the associated link.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#associated_name LinkDefinition#associated_name}
        '''
        result = self._values.get("associated_name")
        assert result is not None, "Required property 'associated_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def associated_title(self) -> builtins.str:
        '''Display name of the associated link.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#associated_title LinkDefinition#associated_title}
        '''
        result = self._values.get("associated_title")
        assert result is not None, "Required property 'associated_title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_description(self) -> builtins.str:
        '''Description of the primary relationship.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#primary_description LinkDefinition#primary_description}
        '''
        result = self._values.get("primary_description")
        assert result is not None, "Required property 'primary_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_name(self) -> builtins.str:
        '''API name of the primary link.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#primary_name LinkDefinition#primary_name}
        '''
        result = self._values.get("primary_name")
        assert result is not None, "Required property 'primary_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_title(self) -> builtins.str:
        '''Display name of the primary link.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#primary_title LinkDefinition#primary_title}
        '''
        result = self._values.get("primary_title")
        assert result is not None, "Required property 'primary_title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/link_definition#id LinkDefinition#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinkDefinitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LinkDefinition",
    "LinkDefinitionConfig",
]

publication.publish()

def _typecheckingstub__ac2d6bbcf61fdffc42d76ee78c8784e21ec6b82a3805b54ad7fe839d4965d4cf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    associated_description: builtins.str,
    associated_name: builtins.str,
    associated_title: builtins.str,
    primary_description: builtins.str,
    primary_name: builtins.str,
    primary_title: builtins.str,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__3f91d9ca5d397086c820ad8b8b73afcfbffc6353a4a60610eca10db07d3bf80c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1f01ac0bc3c20926e936f2b78e5b7f3396fab4ba4b27ceccf6427d23f522e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07710735f46c2b1077ee237a97db930c83209b540efd5c70a4a934993fa718d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673b488b87ed5697ee5b6155b1fe1a6e09057da3d8d9d09302630d059d71deb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8561cb62791fbeb2c4efdb679f11a5a5927b2c7a0883adbe27dec3664c377154(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00032a4e25c927c84917e92370b1eccfb0d4a65e7c6b2339b6286fe3016209b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea98a9788cce5806c6b1d85b7261162b14e41b534776b015ceceb6b563d1be55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216d62386f6163bf701ccdca38718e4915c93201d57dcc2711c89651544b1357(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    associated_description: builtins.str,
    associated_name: builtins.str,
    associated_title: builtins.str,
    primary_description: builtins.str,
    primary_name: builtins.str,
    primary_title: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
