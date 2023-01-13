'''
# `okta_org_configuration`

Refer to the Terraform Registory for docs: [`okta_org_configuration`](https://www.terraform.io/docs/providers/okta/r/org_configuration).
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


class OrgConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.orgConfiguration.OrgConfiguration",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/org_configuration okta_org_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        company_name: builtins.str,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        billing_contact_user: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        end_user_support_help_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        opt_out_communication_emails: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        phone_number: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        support_phone_number: typing.Optional[builtins.str] = None,
        technical_contact_user: typing.Optional[builtins.str] = None,
        website: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/org_configuration okta_org_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param company_name: Name of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#company_name OrgConfiguration#company_name}
        :param address1: Primary address of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#address_1 OrgConfiguration#address_1}
        :param address2: Secondary address of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#address_2 OrgConfiguration#address_2}
        :param billing_contact_user: User ID representing the billing contact. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#billing_contact_user OrgConfiguration#billing_contact_user}
        :param city: City of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#city OrgConfiguration#city}
        :param country: Country of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#country OrgConfiguration#country}
        :param end_user_support_help_url: Support link of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#end_user_support_help_url OrgConfiguration#end_user_support_help_url}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#id OrgConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo: Local path to logo of the org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#logo OrgConfiguration#logo}
        :param opt_out_communication_emails: Indicates whether the org's users receive Okta Communication emails. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#opt_out_communication_emails OrgConfiguration#opt_out_communication_emails}
        :param phone_number: Support help phone of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#phone_number OrgConfiguration#phone_number}
        :param postal_code: Postal code of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#postal_code OrgConfiguration#postal_code}
        :param state: State of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#state OrgConfiguration#state}
        :param support_phone_number: Support help phone of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#support_phone_number OrgConfiguration#support_phone_number}
        :param technical_contact_user: User ID representing the technical contact. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#technical_contact_user OrgConfiguration#technical_contact_user}
        :param website: The org's website. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#website OrgConfiguration#website}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b656c9985fedb7f276820ec533486b77ef879f5ef77716c039ba122d681d4865)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrgConfigurationConfig(
            company_name=company_name,
            address1=address1,
            address2=address2,
            billing_contact_user=billing_contact_user,
            city=city,
            country=country,
            end_user_support_help_url=end_user_support_help_url,
            id=id,
            logo=logo,
            opt_out_communication_emails=opt_out_communication_emails,
            phone_number=phone_number,
            postal_code=postal_code,
            state=state,
            support_phone_number=support_phone_number,
            technical_contact_user=technical_contact_user,
            website=website,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAddress1")
    def reset_address1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress1", []))

    @jsii.member(jsii_name="resetAddress2")
    def reset_address2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress2", []))

    @jsii.member(jsii_name="resetBillingContactUser")
    def reset_billing_contact_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingContactUser", []))

    @jsii.member(jsii_name="resetCity")
    def reset_city(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCity", []))

    @jsii.member(jsii_name="resetCountry")
    def reset_country(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountry", []))

    @jsii.member(jsii_name="resetEndUserSupportHelpUrl")
    def reset_end_user_support_help_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndUserSupportHelpUrl", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogo")
    def reset_logo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogo", []))

    @jsii.member(jsii_name="resetOptOutCommunicationEmails")
    def reset_opt_out_communication_emails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptOutCommunicationEmails", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @jsii.member(jsii_name="resetPostalCode")
    def reset_postal_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostalCode", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetSupportPhoneNumber")
    def reset_support_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportPhoneNumber", []))

    @jsii.member(jsii_name="resetTechnicalContactUser")
    def reset_technical_contact_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTechnicalContactUser", []))

    @jsii.member(jsii_name="resetWebsite")
    def reset_website(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebsite", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="expiresAt")
    def expires_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiresAt"))

    @builtins.property
    @jsii.member(jsii_name="subdomain")
    def subdomain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subdomain"))

    @builtins.property
    @jsii.member(jsii_name="address1Input")
    def address1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address1Input"))

    @builtins.property
    @jsii.member(jsii_name="address2Input")
    def address2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "address2Input"))

    @builtins.property
    @jsii.member(jsii_name="billingContactUserInput")
    def billing_contact_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingContactUserInput"))

    @builtins.property
    @jsii.member(jsii_name="cityInput")
    def city_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cityInput"))

    @builtins.property
    @jsii.member(jsii_name="companyNameInput")
    def company_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "companyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="countryInput")
    def country_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryInput"))

    @builtins.property
    @jsii.member(jsii_name="endUserSupportHelpUrlInput")
    def end_user_support_help_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endUserSupportHelpUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logoInput")
    def logo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoInput"))

    @builtins.property
    @jsii.member(jsii_name="optOutCommunicationEmailsInput")
    def opt_out_communication_emails_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optOutCommunicationEmailsInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="postalCodeInput")
    def postal_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postalCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="supportPhoneNumberInput")
    def support_phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportPhoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="technicalContactUserInput")
    def technical_contact_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "technicalContactUserInput"))

    @builtins.property
    @jsii.member(jsii_name="websiteInput")
    def website_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "websiteInput"))

    @builtins.property
    @jsii.member(jsii_name="address1")
    def address1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address1"))

    @address1.setter
    def address1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86fd38af5b1d6dc5e67feb77de3d8af79781c444ea96f9a5be3833474cb86610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address1", value)

    @builtins.property
    @jsii.member(jsii_name="address2")
    def address2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address2"))

    @address2.setter
    def address2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34c0685f9d287e416c9592586f227b0aaf9268a17c685e6edc2bb50f8d37fff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address2", value)

    @builtins.property
    @jsii.member(jsii_name="billingContactUser")
    def billing_contact_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingContactUser"))

    @billing_contact_user.setter
    def billing_contact_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d978ed4409e43f6cb2a468770d2f3bbc3233fab19df2befd1be793ca8306d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingContactUser", value)

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @city.setter
    def city(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557f224a2abee984c0002c22ebc4a9d7a0df0b87ba2dc6659c5d2342c28047d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "city", value)

    @builtins.property
    @jsii.member(jsii_name="companyName")
    def company_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "companyName"))

    @company_name.setter
    def company_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0395f0642b87c2315f320be397f24ca4f359fe7c6bd37ec3fbfe4cb307495a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "companyName", value)

    @builtins.property
    @jsii.member(jsii_name="country")
    def country(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "country"))

    @country.setter
    def country(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5715e2c04e791508e64e48ab05d52b778efc81fde3b273bccc1cc9187de5cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "country", value)

    @builtins.property
    @jsii.member(jsii_name="endUserSupportHelpUrl")
    def end_user_support_help_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endUserSupportHelpUrl"))

    @end_user_support_help_url.setter
    def end_user_support_help_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8e7dbfc6ac0b214bbe249c3214e08dfc4362286198e8f815cfbb834b397b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endUserSupportHelpUrl", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f89892863b8599a1bb9e2f721c5a975e41090d9e1e9952aabb799b408bb191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="logo")
    def logo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logo"))

    @logo.setter
    def logo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512762aad0365e5e9849262a0be843f65fcc250e0071c50ad0e0372211ca8490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logo", value)

    @builtins.property
    @jsii.member(jsii_name="optOutCommunicationEmails")
    def opt_out_communication_emails(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optOutCommunicationEmails"))

    @opt_out_communication_emails.setter
    def opt_out_communication_emails(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f497f7cad27ad9d6088ce9db16c2e70a4f9f4c70c59275acbaa03bd7bacdc69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optOutCommunicationEmails", value)

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a020ebcfb2d7c553e08c539829fcbac51ff93f8c581d939a4a9fda6793896b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value)

    @builtins.property
    @jsii.member(jsii_name="postalCode")
    def postal_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalCode"))

    @postal_code.setter
    def postal_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc953d7de3d86ecd8d018a36d853106f126bc75942713ba72cb08176113a877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postalCode", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14adae8011058e28de75c260fbe7ba46e87f91e36aadf3dbebac88511e12d30f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)

    @builtins.property
    @jsii.member(jsii_name="supportPhoneNumber")
    def support_phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportPhoneNumber"))

    @support_phone_number.setter
    def support_phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e1c9f356151e9761d7830f21b745b8498aea3e7cdf00463fcf9118ef4e6d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportPhoneNumber", value)

    @builtins.property
    @jsii.member(jsii_name="technicalContactUser")
    def technical_contact_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "technicalContactUser"))

    @technical_contact_user.setter
    def technical_contact_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5120e16d15787681601cac9ef92f17fd6f7d3ff3d1e8470a42931e5938ef8e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "technicalContactUser", value)

    @builtins.property
    @jsii.member(jsii_name="website")
    def website(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "website"))

    @website.setter
    def website(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dabf7b52da42d72d4f96b04978fe21acda8a159d94cb83272a2cbfd36a5ad7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "website", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.orgConfiguration.OrgConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "company_name": "companyName",
        "address1": "address1",
        "address2": "address2",
        "billing_contact_user": "billingContactUser",
        "city": "city",
        "country": "country",
        "end_user_support_help_url": "endUserSupportHelpUrl",
        "id": "id",
        "logo": "logo",
        "opt_out_communication_emails": "optOutCommunicationEmails",
        "phone_number": "phoneNumber",
        "postal_code": "postalCode",
        "state": "state",
        "support_phone_number": "supportPhoneNumber",
        "technical_contact_user": "technicalContactUser",
        "website": "website",
    },
)
class OrgConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        company_name: builtins.str,
        address1: typing.Optional[builtins.str] = None,
        address2: typing.Optional[builtins.str] = None,
        billing_contact_user: typing.Optional[builtins.str] = None,
        city: typing.Optional[builtins.str] = None,
        country: typing.Optional[builtins.str] = None,
        end_user_support_help_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        opt_out_communication_emails: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        phone_number: typing.Optional[builtins.str] = None,
        postal_code: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        support_phone_number: typing.Optional[builtins.str] = None,
        technical_contact_user: typing.Optional[builtins.str] = None,
        website: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param company_name: Name of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#company_name OrgConfiguration#company_name}
        :param address1: Primary address of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#address_1 OrgConfiguration#address_1}
        :param address2: Secondary address of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#address_2 OrgConfiguration#address_2}
        :param billing_contact_user: User ID representing the billing contact. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#billing_contact_user OrgConfiguration#billing_contact_user}
        :param city: City of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#city OrgConfiguration#city}
        :param country: Country of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#country OrgConfiguration#country}
        :param end_user_support_help_url: Support link of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#end_user_support_help_url OrgConfiguration#end_user_support_help_url}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#id OrgConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo: Local path to logo of the org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#logo OrgConfiguration#logo}
        :param opt_out_communication_emails: Indicates whether the org's users receive Okta Communication emails. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#opt_out_communication_emails OrgConfiguration#opt_out_communication_emails}
        :param phone_number: Support help phone of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#phone_number OrgConfiguration#phone_number}
        :param postal_code: Postal code of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#postal_code OrgConfiguration#postal_code}
        :param state: State of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#state OrgConfiguration#state}
        :param support_phone_number: Support help phone of org. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#support_phone_number OrgConfiguration#support_phone_number}
        :param technical_contact_user: User ID representing the technical contact. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#technical_contact_user OrgConfiguration#technical_contact_user}
        :param website: The org's website. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#website OrgConfiguration#website}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3e4c8b8ac9389a9897f051e77ee5fc4b66ca8a898039a16a5f309d6ec8142c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
            check_type(argname="argument address1", value=address1, expected_type=type_hints["address1"])
            check_type(argname="argument address2", value=address2, expected_type=type_hints["address2"])
            check_type(argname="argument billing_contact_user", value=billing_contact_user, expected_type=type_hints["billing_contact_user"])
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument country", value=country, expected_type=type_hints["country"])
            check_type(argname="argument end_user_support_help_url", value=end_user_support_help_url, expected_type=type_hints["end_user_support_help_url"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logo", value=logo, expected_type=type_hints["logo"])
            check_type(argname="argument opt_out_communication_emails", value=opt_out_communication_emails, expected_type=type_hints["opt_out_communication_emails"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument support_phone_number", value=support_phone_number, expected_type=type_hints["support_phone_number"])
            check_type(argname="argument technical_contact_user", value=technical_contact_user, expected_type=type_hints["technical_contact_user"])
            check_type(argname="argument website", value=website, expected_type=type_hints["website"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "company_name": company_name,
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
        if address1 is not None:
            self._values["address1"] = address1
        if address2 is not None:
            self._values["address2"] = address2
        if billing_contact_user is not None:
            self._values["billing_contact_user"] = billing_contact_user
        if city is not None:
            self._values["city"] = city
        if country is not None:
            self._values["country"] = country
        if end_user_support_help_url is not None:
            self._values["end_user_support_help_url"] = end_user_support_help_url
        if id is not None:
            self._values["id"] = id
        if logo is not None:
            self._values["logo"] = logo
        if opt_out_communication_emails is not None:
            self._values["opt_out_communication_emails"] = opt_out_communication_emails
        if phone_number is not None:
            self._values["phone_number"] = phone_number
        if postal_code is not None:
            self._values["postal_code"] = postal_code
        if state is not None:
            self._values["state"] = state
        if support_phone_number is not None:
            self._values["support_phone_number"] = support_phone_number
        if technical_contact_user is not None:
            self._values["technical_contact_user"] = technical_contact_user
        if website is not None:
            self._values["website"] = website

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
    def company_name(self) -> builtins.str:
        '''Name of org.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#company_name OrgConfiguration#company_name}
        '''
        result = self._values.get("company_name")
        assert result is not None, "Required property 'company_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address1(self) -> typing.Optional[builtins.str]:
        '''Primary address of org.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#address_1 OrgConfiguration#address_1}
        '''
        result = self._values.get("address1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address2(self) -> typing.Optional[builtins.str]:
        '''Secondary address of org.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#address_2 OrgConfiguration#address_2}
        '''
        result = self._values.get("address2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing_contact_user(self) -> typing.Optional[builtins.str]:
        '''User ID representing the billing contact.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#billing_contact_user OrgConfiguration#billing_contact_user}
        '''
        result = self._values.get("billing_contact_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def city(self) -> typing.Optional[builtins.str]:
        '''City of org.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#city OrgConfiguration#city}
        '''
        result = self._values.get("city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country(self) -> typing.Optional[builtins.str]:
        '''Country of org.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#country OrgConfiguration#country}
        '''
        result = self._values.get("country")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end_user_support_help_url(self) -> typing.Optional[builtins.str]:
        '''Support link of org.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#end_user_support_help_url OrgConfiguration#end_user_support_help_url}
        '''
        result = self._values.get("end_user_support_help_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#id OrgConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo(self) -> typing.Optional[builtins.str]:
        '''Local path to logo of the org.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#logo OrgConfiguration#logo}
        '''
        result = self._values.get("logo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def opt_out_communication_emails(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the org's users receive Okta Communication emails.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#opt_out_communication_emails OrgConfiguration#opt_out_communication_emails}
        '''
        result = self._values.get("opt_out_communication_emails")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def phone_number(self) -> typing.Optional[builtins.str]:
        '''Support help phone of org.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#phone_number OrgConfiguration#phone_number}
        '''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postal_code(self) -> typing.Optional[builtins.str]:
        '''Postal code of org.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#postal_code OrgConfiguration#postal_code}
        '''
        result = self._values.get("postal_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''State of org.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#state OrgConfiguration#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_phone_number(self) -> typing.Optional[builtins.str]:
        '''Support help phone of org.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#support_phone_number OrgConfiguration#support_phone_number}
        '''
        result = self._values.get("support_phone_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def technical_contact_user(self) -> typing.Optional[builtins.str]:
        '''User ID representing the technical contact.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#technical_contact_user OrgConfiguration#technical_contact_user}
        '''
        result = self._values.get("technical_contact_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def website(self) -> typing.Optional[builtins.str]:
        '''The org's website.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/org_configuration#website OrgConfiguration#website}
        '''
        result = self._values.get("website")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "OrgConfiguration",
    "OrgConfigurationConfig",
]

publication.publish()

def _typecheckingstub__b656c9985fedb7f276820ec533486b77ef879f5ef77716c039ba122d681d4865(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    company_name: builtins.str,
    address1: typing.Optional[builtins.str] = None,
    address2: typing.Optional[builtins.str] = None,
    billing_contact_user: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    end_user_support_help_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    opt_out_communication_emails: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    phone_number: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    support_phone_number: typing.Optional[builtins.str] = None,
    technical_contact_user: typing.Optional[builtins.str] = None,
    website: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__86fd38af5b1d6dc5e67feb77de3d8af79781c444ea96f9a5be3833474cb86610(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34c0685f9d287e416c9592586f227b0aaf9268a17c685e6edc2bb50f8d37fff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d978ed4409e43f6cb2a468770d2f3bbc3233fab19df2befd1be793ca8306d41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557f224a2abee984c0002c22ebc4a9d7a0df0b87ba2dc6659c5d2342c28047d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0395f0642b87c2315f320be397f24ca4f359fe7c6bd37ec3fbfe4cb307495a6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5715e2c04e791508e64e48ab05d52b778efc81fde3b273bccc1cc9187de5cea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8e7dbfc6ac0b214bbe249c3214e08dfc4362286198e8f815cfbb834b397b01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f89892863b8599a1bb9e2f721c5a975e41090d9e1e9952aabb799b408bb191(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512762aad0365e5e9849262a0be843f65fcc250e0071c50ad0e0372211ca8490(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f497f7cad27ad9d6088ce9db16c2e70a4f9f4c70c59275acbaa03bd7bacdc69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a020ebcfb2d7c553e08c539829fcbac51ff93f8c581d939a4a9fda6793896b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc953d7de3d86ecd8d018a36d853106f126bc75942713ba72cb08176113a877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14adae8011058e28de75c260fbe7ba46e87f91e36aadf3dbebac88511e12d30f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e1c9f356151e9761d7830f21b745b8498aea3e7cdf00463fcf9118ef4e6d44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5120e16d15787681601cac9ef92f17fd6f7d3ff3d1e8470a42931e5938ef8e0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dabf7b52da42d72d4f96b04978fe21acda8a159d94cb83272a2cbfd36a5ad7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3e4c8b8ac9389a9897f051e77ee5fc4b66ca8a898039a16a5f309d6ec8142c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    company_name: builtins.str,
    address1: typing.Optional[builtins.str] = None,
    address2: typing.Optional[builtins.str] = None,
    billing_contact_user: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    end_user_support_help_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    opt_out_communication_emails: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    phone_number: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    support_phone_number: typing.Optional[builtins.str] = None,
    technical_contact_user: typing.Optional[builtins.str] = None,
    website: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
