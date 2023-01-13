'''
# `okta_email_customization`

Refer to the Terraform Registory for docs: [`okta_email_customization`](https://www.terraform.io/docs/providers/okta/r/email_customization).
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


class EmailCustomization(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.emailCustomization.EmailCustomization",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/email_customization okta_email_customization}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        brand_id: builtins.str,
        template_name: builtins.str,
        body: typing.Optional[builtins.str] = None,
        force_is_default: typing.Optional[builtins.str] = None,
        is_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/email_customization okta_email_customization} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param brand_id: Brand ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#brand_id EmailCustomization#brand_id}
        :param template_name: Template Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#template_name EmailCustomization#template_name}
        :param body: The body of the customization. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#body EmailCustomization#body}
        :param force_is_default: Force is_default on the create and delete by deleting all email customizations. Comma separated string with values of 'create' or 'destroy' or both `create,destroy'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#force_is_default EmailCustomization#force_is_default}
        :param is_default: Whether the customization is the default. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#is_default EmailCustomization#is_default}
        :param language: The language supported by the customization. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#language EmailCustomization#language}
        :param subject: The subject of the customization. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#subject EmailCustomization#subject}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a109b9f80bcde4ad17b85b9cb0edada0be6a86e1eda7e17dea3610a7bbd66609)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = EmailCustomizationConfig(
            brand_id=brand_id,
            template_name=template_name,
            body=body,
            force_is_default=force_is_default,
            is_default=is_default,
            language=language,
            subject=subject,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetForceIsDefault")
    def reset_force_is_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceIsDefault", []))

    @jsii.member(jsii_name="resetIsDefault")
    def reset_is_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsDefault", []))

    @jsii.member(jsii_name="resetLanguage")
    def reset_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguage", []))

    @jsii.member(jsii_name="resetSubject")
    def reset_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubject", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="brandIdInput")
    def brand_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "brandIdInput"))

    @builtins.property
    @jsii.member(jsii_name="forceIsDefaultInput")
    def force_is_default_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forceIsDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="isDefaultInput")
    def is_default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="languageInput")
    def language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="templateNameInput")
    def template_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333560cf92276a439c47f242bb4607fba0b4c5fef82ef49daa48708aaffe518d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="brandId")
    def brand_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "brandId"))

    @brand_id.setter
    def brand_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cfd6f68d8bbd9ea826ba9c7c985bbdad594ecdd79aec874d1f7e266f90b7775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "brandId", value)

    @builtins.property
    @jsii.member(jsii_name="forceIsDefault")
    def force_is_default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forceIsDefault"))

    @force_is_default.setter
    def force_is_default(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48b5859610d93dc64ade6b5836b9d95b2eb9f6aa7be6cffc27d309c9b5dae4b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceIsDefault", value)

    @builtins.property
    @jsii.member(jsii_name="isDefault")
    def is_default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isDefault"))

    @is_default.setter
    def is_default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cbf536e5d1fb97a06b900919137d52be327cae0334f6c2b5f6b49837d9fb0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefault", value)

    @builtins.property
    @jsii.member(jsii_name="language")
    def language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "language"))

    @language.setter
    def language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ee23e0e51c478b3fc42057844bf10b3a1c75bfa528a7d0e0c57d8118bd5576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "language", value)

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e93cf59f43c18489a4700509ce8dc1549cb456bd726c0bcce301643e448f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5ddc5694b7456dbcd1ec6300e66cd0dc3ebf3f0fe149b057e9e41a85128618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.emailCustomization.EmailCustomizationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "brand_id": "brandId",
        "template_name": "templateName",
        "body": "body",
        "force_is_default": "forceIsDefault",
        "is_default": "isDefault",
        "language": "language",
        "subject": "subject",
    },
)
class EmailCustomizationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        brand_id: builtins.str,
        template_name: builtins.str,
        body: typing.Optional[builtins.str] = None,
        force_is_default: typing.Optional[builtins.str] = None,
        is_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param brand_id: Brand ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#brand_id EmailCustomization#brand_id}
        :param template_name: Template Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#template_name EmailCustomization#template_name}
        :param body: The body of the customization. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#body EmailCustomization#body}
        :param force_is_default: Force is_default on the create and delete by deleting all email customizations. Comma separated string with values of 'create' or 'destroy' or both `create,destroy'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#force_is_default EmailCustomization#force_is_default}
        :param is_default: Whether the customization is the default. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#is_default EmailCustomization#is_default}
        :param language: The language supported by the customization. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#language EmailCustomization#language}
        :param subject: The subject of the customization. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#subject EmailCustomization#subject}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c27fc250fac7e54188fe83bdce9b313e9de65314941636c70c3678b3b186753)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument brand_id", value=brand_id, expected_type=type_hints["brand_id"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument force_is_default", value=force_is_default, expected_type=type_hints["force_is_default"])
            check_type(argname="argument is_default", value=is_default, expected_type=type_hints["is_default"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "brand_id": brand_id,
            "template_name": template_name,
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
        if body is not None:
            self._values["body"] = body
        if force_is_default is not None:
            self._values["force_is_default"] = force_is_default
        if is_default is not None:
            self._values["is_default"] = is_default
        if language is not None:
            self._values["language"] = language
        if subject is not None:
            self._values["subject"] = subject

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
    def brand_id(self) -> builtins.str:
        '''Brand ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#brand_id EmailCustomization#brand_id}
        '''
        result = self._values.get("brand_id")
        assert result is not None, "Required property 'brand_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_name(self) -> builtins.str:
        '''Template Name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#template_name EmailCustomization#template_name}
        '''
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''The body of the customization.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#body EmailCustomization#body}
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_is_default(self) -> typing.Optional[builtins.str]:
        '''Force is_default on the create and delete by deleting all email customizations.

        Comma separated string with values of 'create' or 'destroy' or both `create,destroy'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#force_is_default EmailCustomization#force_is_default}
        '''
        result = self._values.get("force_is_default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the customization is the default.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#is_default EmailCustomization#is_default}
        '''
        result = self._values.get("is_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''The language supported by the customization.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#language EmailCustomization#language}
        '''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        '''The subject of the customization.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/email_customization#subject EmailCustomization#subject}
        '''
        result = self._values.get("subject")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailCustomizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EmailCustomization",
    "EmailCustomizationConfig",
]

publication.publish()

def _typecheckingstub__a109b9f80bcde4ad17b85b9cb0edada0be6a86e1eda7e17dea3610a7bbd66609(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    brand_id: builtins.str,
    template_name: builtins.str,
    body: typing.Optional[builtins.str] = None,
    force_is_default: typing.Optional[builtins.str] = None,
    is_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    language: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__333560cf92276a439c47f242bb4607fba0b4c5fef82ef49daa48708aaffe518d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cfd6f68d8bbd9ea826ba9c7c985bbdad594ecdd79aec874d1f7e266f90b7775(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b5859610d93dc64ade6b5836b9d95b2eb9f6aa7be6cffc27d309c9b5dae4b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cbf536e5d1fb97a06b900919137d52be327cae0334f6c2b5f6b49837d9fb0a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ee23e0e51c478b3fc42057844bf10b3a1c75bfa528a7d0e0c57d8118bd5576(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e93cf59f43c18489a4700509ce8dc1549cb456bd726c0bcce301643e448f30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5ddc5694b7456dbcd1ec6300e66cd0dc3ebf3f0fe149b057e9e41a85128618(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c27fc250fac7e54188fe83bdce9b313e9de65314941636c70c3678b3b186753(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    brand_id: builtins.str,
    template_name: builtins.str,
    body: typing.Optional[builtins.str] = None,
    force_is_default: typing.Optional[builtins.str] = None,
    is_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    language: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
