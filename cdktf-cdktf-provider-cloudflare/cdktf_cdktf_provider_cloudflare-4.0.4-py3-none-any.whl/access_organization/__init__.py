'''
# `cloudflare_access_organization`

Refer to the Terraform Registory for docs: [`cloudflare_access_organization`](https://www.terraform.io/docs/providers/cloudflare/r/access_organization).
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


class AccessOrganization(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessOrganization.AccessOrganization",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization cloudflare_access_organization}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        auth_domain: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_ui_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        login_design: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessOrganizationLoginDesign", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        zone_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization cloudflare_access_organization} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auth_domain: The unique subdomain assigned to your Zero Trust organization. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#auth_domain AccessOrganization#auth_domain}
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#account_id AccessOrganization#account_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#id AccessOrganization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_ui_read_only: When set to true, this will disable all editing of Access resources via the Zero Trust Dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#is_ui_read_only AccessOrganization#is_ui_read_only}
        :param login_design: login_design block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#login_design AccessOrganization#login_design}
        :param name: The name of your Zero Trust organization. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#name AccessOrganization#name}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#zone_id AccessOrganization#zone_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4003d5eb56ec4895276656aaa30bf15b778168f05ceb7c4b72c9c2af9e30ac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessOrganizationConfig(
            auth_domain=auth_domain,
            account_id=account_id,
            id=id,
            is_ui_read_only=is_ui_read_only,
            login_design=login_design,
            name=name,
            zone_id=zone_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putLoginDesign")
    def put_login_design(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessOrganizationLoginDesign", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7874483b525b8c4cdc5d7cfd332886ade642dee117f8efca5090e8b74ff12a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLoginDesign", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsUiReadOnly")
    def reset_is_ui_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsUiReadOnly", []))

    @jsii.member(jsii_name="resetLoginDesign")
    def reset_login_design(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginDesign", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetZoneId")
    def reset_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="loginDesign")
    def login_design(self) -> "AccessOrganizationLoginDesignList":
        return typing.cast("AccessOrganizationLoginDesignList", jsii.get(self, "loginDesign"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="authDomainInput")
    def auth_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isUiReadOnlyInput")
    def is_ui_read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isUiReadOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="loginDesignInput")
    def login_design_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessOrganizationLoginDesign"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessOrganizationLoginDesign"]]], jsii.get(self, "loginDesignInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9647d278f54408d06d4d9e86117600e5e886ec26646e698bdd8fe7cf19567b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="authDomain")
    def auth_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authDomain"))

    @auth_domain.setter
    def auth_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2239f643aaf26dbd471e26e6e540215167e7d8b4a348040e62d848e175c0f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authDomain", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fedaeab4d0e8ea7b9ae6ba9be571ca303d910f3301e216e9da49f6a897e53833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="isUiReadOnly")
    def is_ui_read_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isUiReadOnly"))

    @is_ui_read_only.setter
    def is_ui_read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2758bed2ae0188726c9ec87b079b40961d1402e6aef0a6a96d9ef9ef49220af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isUiReadOnly", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa9e5e397cf7872ba455b3c1c9637a5ca8d22baea43b9e27451d63c8984c72f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a895d95a4dd870744bca4ebfc4a031e356557c1288a9ed3d902a3d30d2cbf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessOrganization.AccessOrganizationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "auth_domain": "authDomain",
        "account_id": "accountId",
        "id": "id",
        "is_ui_read_only": "isUiReadOnly",
        "login_design": "loginDesign",
        "name": "name",
        "zone_id": "zoneId",
    },
)
class AccessOrganizationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auth_domain: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_ui_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        login_design: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessOrganizationLoginDesign", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param auth_domain: The unique subdomain assigned to your Zero Trust organization. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#auth_domain AccessOrganization#auth_domain}
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#account_id AccessOrganization#account_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#id AccessOrganization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_ui_read_only: When set to true, this will disable all editing of Access resources via the Zero Trust Dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#is_ui_read_only AccessOrganization#is_ui_read_only}
        :param login_design: login_design block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#login_design AccessOrganization#login_design}
        :param name: The name of your Zero Trust organization. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#name AccessOrganization#name}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#zone_id AccessOrganization#zone_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be385bf5ddeacdd65f04dfde3e57f74576550eb7b998877d95bd71177f1ffa9f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument auth_domain", value=auth_domain, expected_type=type_hints["auth_domain"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_ui_read_only", value=is_ui_read_only, expected_type=type_hints["is_ui_read_only"])
            check_type(argname="argument login_design", value=login_design, expected_type=type_hints["login_design"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_domain": auth_domain,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if id is not None:
            self._values["id"] = id
        if is_ui_read_only is not None:
            self._values["is_ui_read_only"] = is_ui_read_only
        if login_design is not None:
            self._values["login_design"] = login_design
        if name is not None:
            self._values["name"] = name
        if zone_id is not None:
            self._values["zone_id"] = zone_id

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
    def auth_domain(self) -> builtins.str:
        '''The unique subdomain assigned to your Zero Trust organization.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#auth_domain AccessOrganization#auth_domain}
        '''
        result = self._values.get("auth_domain")
        assert result is not None, "Required property 'auth_domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource. Conflicts with ``zone_id``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#account_id AccessOrganization#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#id AccessOrganization#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_ui_read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, this will disable all editing of Access resources via the Zero Trust Dashboard.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#is_ui_read_only AccessOrganization#is_ui_read_only}
        '''
        result = self._values.get("is_ui_read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def login_design(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessOrganizationLoginDesign"]]]:
        '''login_design block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#login_design AccessOrganization#login_design}
        '''
        result = self._values.get("login_design")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessOrganizationLoginDesign"]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of your Zero Trust organization.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#name AccessOrganization#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''The zone identifier to target for the resource. Conflicts with ``account_id``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#zone_id AccessOrganization#zone_id}
        '''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessOrganizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessOrganization.AccessOrganizationLoginDesign",
    jsii_struct_bases=[],
    name_mapping={
        "background_color": "backgroundColor",
        "footer_text": "footerText",
        "header_text": "headerText",
        "logo_path": "logoPath",
        "text_color": "textColor",
    },
)
class AccessOrganizationLoginDesign:
    def __init__(
        self,
        *,
        background_color: typing.Optional[builtins.str] = None,
        footer_text: typing.Optional[builtins.str] = None,
        header_text: typing.Optional[builtins.str] = None,
        logo_path: typing.Optional[builtins.str] = None,
        text_color: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param background_color: The background color on the login page. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#background_color AccessOrganization#background_color}
        :param footer_text: The text at the bottom of the login page. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#footer_text AccessOrganization#footer_text}
        :param header_text: The text at the top of the login page. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#header_text AccessOrganization#header_text}
        :param logo_path: The URL of the logo on the login page. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#logo_path AccessOrganization#logo_path}
        :param text_color: The text color on the login page. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#text_color AccessOrganization#text_color}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef193002b01da52dd850b64db28cacc0ea43954f1d43f2d9288ad09ebd5115b5)
            check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
            check_type(argname="argument footer_text", value=footer_text, expected_type=type_hints["footer_text"])
            check_type(argname="argument header_text", value=header_text, expected_type=type_hints["header_text"])
            check_type(argname="argument logo_path", value=logo_path, expected_type=type_hints["logo_path"])
            check_type(argname="argument text_color", value=text_color, expected_type=type_hints["text_color"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if background_color is not None:
            self._values["background_color"] = background_color
        if footer_text is not None:
            self._values["footer_text"] = footer_text
        if header_text is not None:
            self._values["header_text"] = header_text
        if logo_path is not None:
            self._values["logo_path"] = logo_path
        if text_color is not None:
            self._values["text_color"] = text_color

    @builtins.property
    def background_color(self) -> typing.Optional[builtins.str]:
        '''The background color on the login page.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#background_color AccessOrganization#background_color}
        '''
        result = self._values.get("background_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def footer_text(self) -> typing.Optional[builtins.str]:
        '''The text at the bottom of the login page.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#footer_text AccessOrganization#footer_text}
        '''
        result = self._values.get("footer_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_text(self) -> typing.Optional[builtins.str]:
        '''The text at the top of the login page.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#header_text AccessOrganization#header_text}
        '''
        result = self._values.get("header_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo_path(self) -> typing.Optional[builtins.str]:
        '''The URL of the logo on the login page.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#logo_path AccessOrganization#logo_path}
        '''
        result = self._values.get("logo_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text_color(self) -> typing.Optional[builtins.str]:
        '''The text color on the login page.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_organization#text_color AccessOrganization#text_color}
        '''
        result = self._values.get("text_color")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessOrganizationLoginDesign(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessOrganizationLoginDesignList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessOrganization.AccessOrganizationLoginDesignList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa053d649629ecf167d6cfe8f1948079d081fe232358b3a2b0246addfa166c7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessOrganizationLoginDesignOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2088f3eafa8c33180a2f8f029040cc0cc190db79f56ce08f016b8f8cc1aed040)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessOrganizationLoginDesignOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3c5eff8375f82501ddec406dc9187e7a250aff790f743458404001c9dd85ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dbbbe63f0aba77a199fd1d06746027dabb7ec58990f6839e687c039b2825c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a504d0b92ab403e12c69170c61db45f29ee2699ee0a60ad818e40bb0d7ca6cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessOrganizationLoginDesign]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessOrganizationLoginDesign]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessOrganizationLoginDesign]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea5fd5c2d7a52f92322ff53aaeb121c854e22a242c984df1f2ecb8d0752ef5e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessOrganizationLoginDesignOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessOrganization.AccessOrganizationLoginDesignOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a75da4bc4a8a712e76bd3759b6cf5b9d5dc897af095b7dd38c71745793f048)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBackgroundColor")
    def reset_background_color(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackgroundColor", []))

    @jsii.member(jsii_name="resetFooterText")
    def reset_footer_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFooterText", []))

    @jsii.member(jsii_name="resetHeaderText")
    def reset_header_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderText", []))

    @jsii.member(jsii_name="resetLogoPath")
    def reset_logo_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogoPath", []))

    @jsii.member(jsii_name="resetTextColor")
    def reset_text_color(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTextColor", []))

    @builtins.property
    @jsii.member(jsii_name="backgroundColorInput")
    def background_color_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backgroundColorInput"))

    @builtins.property
    @jsii.member(jsii_name="footerTextInput")
    def footer_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "footerTextInput"))

    @builtins.property
    @jsii.member(jsii_name="headerTextInput")
    def header_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerTextInput"))

    @builtins.property
    @jsii.member(jsii_name="logoPathInput")
    def logo_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoPathInput"))

    @builtins.property
    @jsii.member(jsii_name="textColorInput")
    def text_color_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textColorInput"))

    @builtins.property
    @jsii.member(jsii_name="backgroundColor")
    def background_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backgroundColor"))

    @background_color.setter
    def background_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78cf1da2251974d92603edaee69e70b49ee5e8956aec4756cbf46974cc50a694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backgroundColor", value)

    @builtins.property
    @jsii.member(jsii_name="footerText")
    def footer_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "footerText"))

    @footer_text.setter
    def footer_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d5d626a6bf712efc5196c8c03803e5aed0cd4340e3858803493956c117307a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "footerText", value)

    @builtins.property
    @jsii.member(jsii_name="headerText")
    def header_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerText"))

    @header_text.setter
    def header_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aadc1b403224fed9b16cc222648c9b0f0ce3ebc7f1b826c8d142578a593aa54a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerText", value)

    @builtins.property
    @jsii.member(jsii_name="logoPath")
    def logo_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoPath"))

    @logo_path.setter
    def logo_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fbb6d5bbfc80065079e08a641f72daef3cf8477f025a6500fc391e8f9c7d697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoPath", value)

    @builtins.property
    @jsii.member(jsii_name="textColor")
    def text_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textColor"))

    @text_color.setter
    def text_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b0249fd553fb37fce59a08c2fe06fac20ccd9d284464a3c199aea205c820d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textColor", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessOrganizationLoginDesign, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessOrganizationLoginDesign, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessOrganizationLoginDesign, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3688384439c6f28a4be5d1245391fe8067a6ad6a5fabae345435516d8d1b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AccessOrganization",
    "AccessOrganizationConfig",
    "AccessOrganizationLoginDesign",
    "AccessOrganizationLoginDesignList",
    "AccessOrganizationLoginDesignOutputReference",
]

publication.publish()

def _typecheckingstub__7b4003d5eb56ec4895276656aaa30bf15b778168f05ceb7c4b72c9c2af9e30ac(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    auth_domain: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_ui_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    login_design: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessOrganizationLoginDesign, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    zone_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__7874483b525b8c4cdc5d7cfd332886ade642dee117f8efca5090e8b74ff12a02(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessOrganizationLoginDesign, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9647d278f54408d06d4d9e86117600e5e886ec26646e698bdd8fe7cf19567b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2239f643aaf26dbd471e26e6e540215167e7d8b4a348040e62d848e175c0f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedaeab4d0e8ea7b9ae6ba9be571ca303d910f3301e216e9da49f6a897e53833(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2758bed2ae0188726c9ec87b079b40961d1402e6aef0a6a96d9ef9ef49220af(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa9e5e397cf7872ba455b3c1c9637a5ca8d22baea43b9e27451d63c8984c72f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a895d95a4dd870744bca4ebfc4a031e356557c1288a9ed3d902a3d30d2cbf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be385bf5ddeacdd65f04dfde3e57f74576550eb7b998877d95bd71177f1ffa9f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_domain: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_ui_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    login_design: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessOrganizationLoginDesign, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef193002b01da52dd850b64db28cacc0ea43954f1d43f2d9288ad09ebd5115b5(
    *,
    background_color: typing.Optional[builtins.str] = None,
    footer_text: typing.Optional[builtins.str] = None,
    header_text: typing.Optional[builtins.str] = None,
    logo_path: typing.Optional[builtins.str] = None,
    text_color: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa053d649629ecf167d6cfe8f1948079d081fe232358b3a2b0246addfa166c7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2088f3eafa8c33180a2f8f029040cc0cc190db79f56ce08f016b8f8cc1aed040(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3c5eff8375f82501ddec406dc9187e7a250aff790f743458404001c9dd85ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbbbe63f0aba77a199fd1d06746027dabb7ec58990f6839e687c039b2825c50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a504d0b92ab403e12c69170c61db45f29ee2699ee0a60ad818e40bb0d7ca6cb6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5fd5c2d7a52f92322ff53aaeb121c854e22a242c984df1f2ecb8d0752ef5e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessOrganizationLoginDesign]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a75da4bc4a8a712e76bd3759b6cf5b9d5dc897af095b7dd38c71745793f048(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78cf1da2251974d92603edaee69e70b49ee5e8956aec4756cbf46974cc50a694(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d5d626a6bf712efc5196c8c03803e5aed0cd4340e3858803493956c117307a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aadc1b403224fed9b16cc222648c9b0f0ce3ebc7f1b826c8d142578a593aa54a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fbb6d5bbfc80065079e08a641f72daef3cf8477f025a6500fc391e8f9c7d697(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b0249fd553fb37fce59a08c2fe06fac20ccd9d284464a3c199aea205c820d18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3688384439c6f28a4be5d1245391fe8067a6ad6a5fabae345435516d8d1b3e(
    value: typing.Optional[typing.Union[AccessOrganizationLoginDesign, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
