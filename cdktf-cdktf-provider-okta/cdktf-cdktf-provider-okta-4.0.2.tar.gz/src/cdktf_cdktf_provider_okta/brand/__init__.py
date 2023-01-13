'''
# `okta_brand`

Refer to the Terraform Registory for docs: [`okta_brand`](https://www.terraform.io/docs/providers/okta/r/brand).
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


class Brand(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.brand.Brand",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/brand okta_brand}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        agree_to_custom_privacy_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        brand_id: typing.Optional[builtins.str] = None,
        custom_privacy_policy_url: typing.Optional[builtins.str] = None,
        remove_powered_by_okta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/brand okta_brand} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param agree_to_custom_privacy_policy: Consent for updating the custom privacy policy URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#agree_to_custom_privacy_policy Brand#agree_to_custom_privacy_policy}
        :param brand_id: Brand ID - Note: Okta API for brands only reads and updates therefore the okta_brand resource needs to act as a quasi data source. Do this by setting brand_id. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#brand_id Brand#brand_id}
        :param custom_privacy_policy_url: Custom privacy policy URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#custom_privacy_policy_url Brand#custom_privacy_policy_url}
        :param remove_powered_by_okta: Removes "Powered by Okta" from the Okta-hosted sign-in page and "© 2021 Okta, Inc." from the Okta End-User Dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#remove_powered_by_okta Brand#remove_powered_by_okta}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d7e18230a9679bcb2d8a4bbb20ecd6c5e549abeb5b80dc2a6b55e3908bbda9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = BrandConfig(
            agree_to_custom_privacy_policy=agree_to_custom_privacy_policy,
            brand_id=brand_id,
            custom_privacy_policy_url=custom_privacy_policy_url,
            remove_powered_by_okta=remove_powered_by_okta,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAgreeToCustomPrivacyPolicy")
    def reset_agree_to_custom_privacy_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgreeToCustomPrivacyPolicy", []))

    @jsii.member(jsii_name="resetBrandId")
    def reset_brand_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrandId", []))

    @jsii.member(jsii_name="resetCustomPrivacyPolicyUrl")
    def reset_custom_privacy_policy_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPrivacyPolicyUrl", []))

    @jsii.member(jsii_name="resetRemovePoweredByOkta")
    def reset_remove_powered_by_okta(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemovePoweredByOkta", []))

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
    @jsii.member(jsii_name="agreeToCustomPrivacyPolicyInput")
    def agree_to_custom_privacy_policy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "agreeToCustomPrivacyPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="brandIdInput")
    def brand_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "brandIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customPrivacyPolicyUrlInput")
    def custom_privacy_policy_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customPrivacyPolicyUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="removePoweredByOktaInput")
    def remove_powered_by_okta_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "removePoweredByOktaInput"))

    @builtins.property
    @jsii.member(jsii_name="agreeToCustomPrivacyPolicy")
    def agree_to_custom_privacy_policy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "agreeToCustomPrivacyPolicy"))

    @agree_to_custom_privacy_policy.setter
    def agree_to_custom_privacy_policy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a188989f1e2e1a421b119f34b3755fa4cbbdf28ee4bdbf022bf334dbfab994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agreeToCustomPrivacyPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="brandId")
    def brand_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "brandId"))

    @brand_id.setter
    def brand_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a01a0159a0126332e6826636dd10ceb76194ff7b2f42e67f6090e3ef270efc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "brandId", value)

    @builtins.property
    @jsii.member(jsii_name="customPrivacyPolicyUrl")
    def custom_privacy_policy_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customPrivacyPolicyUrl"))

    @custom_privacy_policy_url.setter
    def custom_privacy_policy_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d340b3c630f3f9dcc058631e47292e4b46f1fade342f4eab5001597e0dbe5df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPrivacyPolicyUrl", value)

    @builtins.property
    @jsii.member(jsii_name="removePoweredByOkta")
    def remove_powered_by_okta(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "removePoweredByOkta"))

    @remove_powered_by_okta.setter
    def remove_powered_by_okta(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f9c7af21a10a5e0e69b1de043527cde1622f8eadcf459f5f6d0f1e60ca1b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "removePoweredByOkta", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.brand.BrandConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "agree_to_custom_privacy_policy": "agreeToCustomPrivacyPolicy",
        "brand_id": "brandId",
        "custom_privacy_policy_url": "customPrivacyPolicyUrl",
        "remove_powered_by_okta": "removePoweredByOkta",
    },
)
class BrandConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        agree_to_custom_privacy_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        brand_id: typing.Optional[builtins.str] = None,
        custom_privacy_policy_url: typing.Optional[builtins.str] = None,
        remove_powered_by_okta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param agree_to_custom_privacy_policy: Consent for updating the custom privacy policy URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#agree_to_custom_privacy_policy Brand#agree_to_custom_privacy_policy}
        :param brand_id: Brand ID - Note: Okta API for brands only reads and updates therefore the okta_brand resource needs to act as a quasi data source. Do this by setting brand_id. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#brand_id Brand#brand_id}
        :param custom_privacy_policy_url: Custom privacy policy URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#custom_privacy_policy_url Brand#custom_privacy_policy_url}
        :param remove_powered_by_okta: Removes "Powered by Okta" from the Okta-hosted sign-in page and "© 2021 Okta, Inc." from the Okta End-User Dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#remove_powered_by_okta Brand#remove_powered_by_okta}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdaa068f352d0f9814bd9f7105de41a5097c77622ef2727ebe72bb393e61d86d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument agree_to_custom_privacy_policy", value=agree_to_custom_privacy_policy, expected_type=type_hints["agree_to_custom_privacy_policy"])
            check_type(argname="argument brand_id", value=brand_id, expected_type=type_hints["brand_id"])
            check_type(argname="argument custom_privacy_policy_url", value=custom_privacy_policy_url, expected_type=type_hints["custom_privacy_policy_url"])
            check_type(argname="argument remove_powered_by_okta", value=remove_powered_by_okta, expected_type=type_hints["remove_powered_by_okta"])
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
        if agree_to_custom_privacy_policy is not None:
            self._values["agree_to_custom_privacy_policy"] = agree_to_custom_privacy_policy
        if brand_id is not None:
            self._values["brand_id"] = brand_id
        if custom_privacy_policy_url is not None:
            self._values["custom_privacy_policy_url"] = custom_privacy_policy_url
        if remove_powered_by_okta is not None:
            self._values["remove_powered_by_okta"] = remove_powered_by_okta

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
    def agree_to_custom_privacy_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Consent for updating the custom privacy policy URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#agree_to_custom_privacy_policy Brand#agree_to_custom_privacy_policy}
        '''
        result = self._values.get("agree_to_custom_privacy_policy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def brand_id(self) -> typing.Optional[builtins.str]:
        '''Brand ID - Note: Okta API for brands only reads and updates therefore the okta_brand resource needs to act as a quasi data source.

        Do this by setting brand_id.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#brand_id Brand#brand_id}
        '''
        result = self._values.get("brand_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_privacy_policy_url(self) -> typing.Optional[builtins.str]:
        '''Custom privacy policy URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#custom_privacy_policy_url Brand#custom_privacy_policy_url}
        '''
        result = self._values.get("custom_privacy_policy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove_powered_by_okta(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Removes "Powered by Okta" from the Okta-hosted sign-in page and "© 2021 Okta, Inc." from the Okta End-User Dashboard.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/brand#remove_powered_by_okta Brand#remove_powered_by_okta}
        '''
        result = self._values.get("remove_powered_by_okta")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BrandConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Brand",
    "BrandConfig",
]

publication.publish()

def _typecheckingstub__f2d7e18230a9679bcb2d8a4bbb20ecd6c5e549abeb5b80dc2a6b55e3908bbda9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    agree_to_custom_privacy_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    brand_id: typing.Optional[builtins.str] = None,
    custom_privacy_policy_url: typing.Optional[builtins.str] = None,
    remove_powered_by_okta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__38a188989f1e2e1a421b119f34b3755fa4cbbdf28ee4bdbf022bf334dbfab994(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a01a0159a0126332e6826636dd10ceb76194ff7b2f42e67f6090e3ef270efc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d340b3c630f3f9dcc058631e47292e4b46f1fade342f4eab5001597e0dbe5df3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f9c7af21a10a5e0e69b1de043527cde1622f8eadcf459f5f6d0f1e60ca1b8b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdaa068f352d0f9814bd9f7105de41a5097c77622ef2727ebe72bb393e61d86d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    agree_to_custom_privacy_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    brand_id: typing.Optional[builtins.str] = None,
    custom_privacy_policy_url: typing.Optional[builtins.str] = None,
    remove_powered_by_okta: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
