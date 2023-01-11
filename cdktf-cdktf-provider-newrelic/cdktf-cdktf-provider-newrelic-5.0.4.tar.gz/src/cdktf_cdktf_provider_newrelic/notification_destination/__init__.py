'''
# `newrelic_notification_destination`

Refer to the Terraform Registory for docs: [`newrelic_notification_destination`](https://www.terraform.io/docs/providers/newrelic/r/notification_destination).
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


class NotificationDestination(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.notificationDestination.NotificationDestination",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination newrelic_notification_destination}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        property: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NotificationDestinationProperty", typing.Dict[builtins.str, typing.Any]]]],
        type: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auth_basic: typing.Optional[typing.Union["NotificationDestinationAuthBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        auth_token: typing.Optional[typing.Union["NotificationDestinationAuthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination newrelic_notification_destination} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: (Required) The name of the destination. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#name NotificationDestination#name}
        :param property: property block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#property NotificationDestination#property}
        :param type: (Required) The type of the destination. One of: (WEBHOOK, EMAIL, SERVICE_NOW, PAGERDUTY_ACCOUNT_INTEGRATION, PAGERDUTY_SERVICE_INTEGRATION, JIRA, SLACK, SLACK_COLLABORATION, SLACK_LEGACY, MOBILE_PUSH, EVENT_BRIDGE). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#type NotificationDestination#type}
        :param account_id: The account ID under which to put the destination. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#account_id NotificationDestination#account_id}
        :param active: Indicates whether the destination is active. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#active NotificationDestination#active}
        :param auth_basic: auth_basic block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#auth_basic NotificationDestination#auth_basic}
        :param auth_token: auth_token block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#auth_token NotificationDestination#auth_token}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#id NotificationDestination#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5310edbc85bfacddc7ae11aa833bd774e8e55d8b676be0562f714c97c38dfdc1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NotificationDestinationConfig(
            name=name,
            property=property,
            type=type,
            account_id=account_id,
            active=active,
            auth_basic=auth_basic,
            auth_token=auth_token,
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

    @jsii.member(jsii_name="putAuthBasic")
    def put_auth_basic(self, *, password: builtins.str, user: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#password NotificationDestination#password}.
        :param user: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#user NotificationDestination#user}.
        '''
        value = NotificationDestinationAuthBasic(password=password, user=user)

        return typing.cast(None, jsii.invoke(self, "putAuthBasic", [value]))

    @jsii.member(jsii_name="putAuthToken")
    def put_auth_token(
        self,
        *,
        token: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#token NotificationDestination#token}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#prefix NotificationDestination#prefix}.
        '''
        value = NotificationDestinationAuthToken(token=token, prefix=prefix)

        return typing.cast(None, jsii.invoke(self, "putAuthToken", [value]))

    @jsii.member(jsii_name="putProperty")
    def put_property(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NotificationDestinationProperty", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c976f7808fd7465d82a2cc87c7de4cff59f5745365b33ea3bfb0a3fc4e13f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperty", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetActive")
    def reset_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActive", []))

    @jsii.member(jsii_name="resetAuthBasic")
    def reset_auth_basic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthBasic", []))

    @jsii.member(jsii_name="resetAuthToken")
    def reset_auth_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthToken", []))

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
    @jsii.member(jsii_name="authBasic")
    def auth_basic(self) -> "NotificationDestinationAuthBasicOutputReference":
        return typing.cast("NotificationDestinationAuthBasicOutputReference", jsii.get(self, "authBasic"))

    @builtins.property
    @jsii.member(jsii_name="authToken")
    def auth_token(self) -> "NotificationDestinationAuthTokenOutputReference":
        return typing.cast("NotificationDestinationAuthTokenOutputReference", jsii.get(self, "authToken"))

    @builtins.property
    @jsii.member(jsii_name="lastSent")
    def last_sent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastSent"))

    @builtins.property
    @jsii.member(jsii_name="property")
    def property(self) -> "NotificationDestinationPropertyList":
        return typing.cast("NotificationDestinationPropertyList", jsii.get(self, "property"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="activeInput")
    def active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activeInput"))

    @builtins.property
    @jsii.member(jsii_name="authBasicInput")
    def auth_basic_input(self) -> typing.Optional["NotificationDestinationAuthBasic"]:
        return typing.cast(typing.Optional["NotificationDestinationAuthBasic"], jsii.get(self, "authBasicInput"))

    @builtins.property
    @jsii.member(jsii_name="authTokenInput")
    def auth_token_input(self) -> typing.Optional["NotificationDestinationAuthToken"]:
        return typing.cast(typing.Optional["NotificationDestinationAuthToken"], jsii.get(self, "authTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="propertyInput")
    def property_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NotificationDestinationProperty"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NotificationDestinationProperty"]]], jsii.get(self, "propertyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d131d3b299527b2129d619f8dcfe5ee91e8f193fcbcf81d13ddc06d8ed2dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "active"))

    @active.setter
    def active(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb5c4ee3f1c6e59190cb310367fd56dabbb5029977983f91fdd6b2e638ae70d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "active", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a258aeb522ad1962a8a194196dda96485641f04d7f472ec746266b03c96ff558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd0b89d2f6110b33f564d21ba80deb25e81bf0a2ef4e5b62f5785d674f9e7ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c2113bd342327a910fe9c08091c77a12ff96752b0e9ce534448b746bd140e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.notificationDestination.NotificationDestinationAuthBasic",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "user": "user"},
)
class NotificationDestinationAuthBasic:
    def __init__(self, *, password: builtins.str, user: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#password NotificationDestination#password}.
        :param user: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#user NotificationDestination#user}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc45d2b8cd8d06f89a9fe520c08098701f9593e22d9c7dab749c31b8c030e6e6)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "user": user,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#password NotificationDestination#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#user NotificationDestination#user}.'''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationDestinationAuthBasic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotificationDestinationAuthBasicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.notificationDestination.NotificationDestinationAuthBasicOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23091e4568298dbc4db97cec63acf6c2b0950343431dfd6c78639aa1d8b27916)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0811aca4ec1e5ee5a4d0c0934ddbe3b944cb02a6c0625074f10cbd5a9e4a5a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61392bdb5fea18c1249465121755ba17ad26206942802351c2295aef68c9bb0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NotificationDestinationAuthBasic]:
        return typing.cast(typing.Optional[NotificationDestinationAuthBasic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotificationDestinationAuthBasic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39fc7286c41ad0190ecf10d1cbed6a23f9d26ce81131b8394199137a97f9b9a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.notificationDestination.NotificationDestinationAuthToken",
    jsii_struct_bases=[],
    name_mapping={"token": "token", "prefix": "prefix"},
)
class NotificationDestinationAuthToken:
    def __init__(
        self,
        *,
        token: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#token NotificationDestination#token}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#prefix NotificationDestination#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52fd9c85d44541a751b81222b3d572e6b5de194ece9774d4f5963b68ddb95bfe)
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "token": token,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def token(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#token NotificationDestination#token}.'''
        result = self._values.get("token")
        assert result is not None, "Required property 'token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#prefix NotificationDestination#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationDestinationAuthToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotificationDestinationAuthTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.notificationDestination.NotificationDestinationAuthTokenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acd314329b3a9050fef4ee226f12913223b7f90f904f4875ada41ad5b66acb78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f60ff897c87e45ca9cc9937d88186827dff2a03de8c2ccdc65768e04aad3700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c4042316cd47c77c2832b30f684c52e24b8165c9a4b0554da36378eaa0e861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NotificationDestinationAuthToken]:
        return typing.cast(typing.Optional[NotificationDestinationAuthToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotificationDestinationAuthToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79767d7d779d37bcfd7303cf8ecf9330d4a897df5688cafbf3bc68c9050a1a76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.notificationDestination.NotificationDestinationConfig",
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
        "property": "property",
        "type": "type",
        "account_id": "accountId",
        "active": "active",
        "auth_basic": "authBasic",
        "auth_token": "authToken",
        "id": "id",
    },
)
class NotificationDestinationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        property: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NotificationDestinationProperty", typing.Dict[builtins.str, typing.Any]]]],
        type: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auth_basic: typing.Optional[typing.Union[NotificationDestinationAuthBasic, typing.Dict[builtins.str, typing.Any]]] = None,
        auth_token: typing.Optional[typing.Union[NotificationDestinationAuthToken, typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: (Required) The name of the destination. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#name NotificationDestination#name}
        :param property: property block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#property NotificationDestination#property}
        :param type: (Required) The type of the destination. One of: (WEBHOOK, EMAIL, SERVICE_NOW, PAGERDUTY_ACCOUNT_INTEGRATION, PAGERDUTY_SERVICE_INTEGRATION, JIRA, SLACK, SLACK_COLLABORATION, SLACK_LEGACY, MOBILE_PUSH, EVENT_BRIDGE). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#type NotificationDestination#type}
        :param account_id: The account ID under which to put the destination. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#account_id NotificationDestination#account_id}
        :param active: Indicates whether the destination is active. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#active NotificationDestination#active}
        :param auth_basic: auth_basic block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#auth_basic NotificationDestination#auth_basic}
        :param auth_token: auth_token block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#auth_token NotificationDestination#auth_token}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#id NotificationDestination#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auth_basic, dict):
            auth_basic = NotificationDestinationAuthBasic(**auth_basic)
        if isinstance(auth_token, dict):
            auth_token = NotificationDestinationAuthToken(**auth_token)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96af390d97bf9c38f2100232e7e3349344258a4a1e10cc56a52f9f105e8c7e1f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            check_type(argname="argument auth_basic", value=auth_basic, expected_type=type_hints["auth_basic"])
            check_type(argname="argument auth_token", value=auth_token, expected_type=type_hints["auth_token"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "property": property,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if active is not None:
            self._values["active"] = active
        if auth_basic is not None:
            self._values["auth_basic"] = auth_basic
        if auth_token is not None:
            self._values["auth_token"] = auth_token
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
    def name(self) -> builtins.str:
        '''(Required) The name of the destination.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#name NotificationDestination#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def property(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NotificationDestinationProperty"]]:
        '''property block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#property NotificationDestination#property}
        '''
        result = self._values.get("property")
        assert result is not None, "Required property 'property' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NotificationDestinationProperty"]], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''(Required) The type of the destination. One of: (WEBHOOK, EMAIL, SERVICE_NOW, PAGERDUTY_ACCOUNT_INTEGRATION, PAGERDUTY_SERVICE_INTEGRATION, JIRA, SLACK, SLACK_COLLABORATION, SLACK_LEGACY, MOBILE_PUSH, EVENT_BRIDGE).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#type NotificationDestination#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account ID under which to put the destination.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#account_id NotificationDestination#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the destination is active.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#active NotificationDestination#active}
        '''
        result = self._values.get("active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auth_basic(self) -> typing.Optional[NotificationDestinationAuthBasic]:
        '''auth_basic block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#auth_basic NotificationDestination#auth_basic}
        '''
        result = self._values.get("auth_basic")
        return typing.cast(typing.Optional[NotificationDestinationAuthBasic], result)

    @builtins.property
    def auth_token(self) -> typing.Optional[NotificationDestinationAuthToken]:
        '''auth_token block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#auth_token NotificationDestination#auth_token}
        '''
        result = self._values.get("auth_token")
        return typing.cast(typing.Optional[NotificationDestinationAuthToken], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#id NotificationDestination#id}.

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
        return "NotificationDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.notificationDestination.NotificationDestinationProperty",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "value": "value",
        "display_value": "displayValue",
        "label": "label",
    },
)
class NotificationDestinationProperty:
    def __init__(
        self,
        *,
        key: builtins.str,
        value: builtins.str,
        display_value: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Notification property key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#key NotificationDestination#key}
        :param value: Notification property value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#value NotificationDestination#value}
        :param display_value: Notification property display key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#display_value NotificationDestination#display_value}
        :param label: Notification property label. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#label NotificationDestination#label}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acab913c865189c87c22695776e1fd576c1ab1eec898462f48894a37619f858c)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument display_value", value=display_value, expected_type=type_hints["display_value"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }
        if display_value is not None:
            self._values["display_value"] = display_value
        if label is not None:
            self._values["label"] = label

    @builtins.property
    def key(self) -> builtins.str:
        '''Notification property key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#key NotificationDestination#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Notification property value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#value NotificationDestination#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_value(self) -> typing.Optional[builtins.str]:
        '''Notification property display key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#display_value NotificationDestination#display_value}
        '''
        result = self._values.get("display_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Notification property label.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/notification_destination#label NotificationDestination#label}
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationDestinationProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotificationDestinationPropertyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.notificationDestination.NotificationDestinationPropertyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9173552e118c00bbf4c4134aa9edaaf6ab7b6a1d850ab3ddfce3fe4789e9b55a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NotificationDestinationPropertyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76714b5b606a11317e3a6acc2bbb5c884cc83a87d2fb97c79dc1ea723268b54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NotificationDestinationPropertyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282e70f0f7f970838f72b0d7e7899f0a0807e0abf2fc0541fe039f24f1152869)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da30a7b45328ac6fd995cf691c63155812f70fb511abea3db762137706a3bdde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a884044760c43f42a18102d7007753a99db97089f4a7dd05b48385934b8f82b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotificationDestinationProperty]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotificationDestinationProperty]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotificationDestinationProperty]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002d3ce80c9585a437122a95674757ec424345bceb66fee181e9c492e39bf16d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NotificationDestinationPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.notificationDestination.NotificationDestinationPropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbd7636d69fb8393bd78925a9f0dee0e9674c202c900928dc5923e8b0d67a5fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDisplayValue")
    def reset_display_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayValue", []))

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @builtins.property
    @jsii.member(jsii_name="displayValueInput")
    def display_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayValueInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="displayValue")
    def display_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayValue"))

    @display_value.setter
    def display_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90430b3b25353c12dbffcd89fe0703b07c76bd6d0fdc05edb59ba509f75b3607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayValue", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e2b5d7992a98c94ee332061970dd3a1a3710b52c17c3a4f99369b3d6a14a8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a702f764220e12c0e7db7af266b534fb4497d87d6b6f5e66cfee14b8a43b1a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd1a7080400157fc76b3949ca3cd6d6700c296762b044cb5b3bcb4fd011e67e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[NotificationDestinationProperty, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[NotificationDestinationProperty, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[NotificationDestinationProperty, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca1772727bd952f9f8524b6fdad86b21df73fa96a9aad25d876687b60fdb0a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NotificationDestination",
    "NotificationDestinationAuthBasic",
    "NotificationDestinationAuthBasicOutputReference",
    "NotificationDestinationAuthToken",
    "NotificationDestinationAuthTokenOutputReference",
    "NotificationDestinationConfig",
    "NotificationDestinationProperty",
    "NotificationDestinationPropertyList",
    "NotificationDestinationPropertyOutputReference",
]

publication.publish()

def _typecheckingstub__5310edbc85bfacddc7ae11aa833bd774e8e55d8b676be0562f714c97c38dfdc1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    property: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NotificationDestinationProperty, typing.Dict[builtins.str, typing.Any]]]],
    type: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auth_basic: typing.Optional[typing.Union[NotificationDestinationAuthBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_token: typing.Optional[typing.Union[NotificationDestinationAuthToken, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0c976f7808fd7465d82a2cc87c7de4cff59f5745365b33ea3bfb0a3fc4e13f7f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NotificationDestinationProperty, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d131d3b299527b2129d619f8dcfe5ee91e8f193fcbcf81d13ddc06d8ed2dc5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb5c4ee3f1c6e59190cb310367fd56dabbb5029977983f91fdd6b2e638ae70d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a258aeb522ad1962a8a194196dda96485641f04d7f472ec746266b03c96ff558(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd0b89d2f6110b33f564d21ba80deb25e81bf0a2ef4e5b62f5785d674f9e7ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c2113bd342327a910fe9c08091c77a12ff96752b0e9ce534448b746bd140e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc45d2b8cd8d06f89a9fe520c08098701f9593e22d9c7dab749c31b8c030e6e6(
    *,
    password: builtins.str,
    user: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23091e4568298dbc4db97cec63acf6c2b0950343431dfd6c78639aa1d8b27916(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0811aca4ec1e5ee5a4d0c0934ddbe3b944cb02a6c0625074f10cbd5a9e4a5a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61392bdb5fea18c1249465121755ba17ad26206942802351c2295aef68c9bb0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39fc7286c41ad0190ecf10d1cbed6a23f9d26ce81131b8394199137a97f9b9a3(
    value: typing.Optional[NotificationDestinationAuthBasic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fd9c85d44541a751b81222b3d572e6b5de194ece9774d4f5963b68ddb95bfe(
    *,
    token: builtins.str,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd314329b3a9050fef4ee226f12913223b7f90f904f4875ada41ad5b66acb78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f60ff897c87e45ca9cc9937d88186827dff2a03de8c2ccdc65768e04aad3700(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c4042316cd47c77c2832b30f684c52e24b8165c9a4b0554da36378eaa0e861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79767d7d779d37bcfd7303cf8ecf9330d4a897df5688cafbf3bc68c9050a1a76(
    value: typing.Optional[NotificationDestinationAuthToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96af390d97bf9c38f2100232e7e3349344258a4a1e10cc56a52f9f105e8c7e1f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    property: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NotificationDestinationProperty, typing.Dict[builtins.str, typing.Any]]]],
    type: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auth_basic: typing.Optional[typing.Union[NotificationDestinationAuthBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_token: typing.Optional[typing.Union[NotificationDestinationAuthToken, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acab913c865189c87c22695776e1fd576c1ab1eec898462f48894a37619f858c(
    *,
    key: builtins.str,
    value: builtins.str,
    display_value: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9173552e118c00bbf4c4134aa9edaaf6ab7b6a1d850ab3ddfce3fe4789e9b55a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76714b5b606a11317e3a6acc2bbb5c884cc83a87d2fb97c79dc1ea723268b54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282e70f0f7f970838f72b0d7e7899f0a0807e0abf2fc0541fe039f24f1152869(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da30a7b45328ac6fd995cf691c63155812f70fb511abea3db762137706a3bdde(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a884044760c43f42a18102d7007753a99db97089f4a7dd05b48385934b8f82b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002d3ce80c9585a437122a95674757ec424345bceb66fee181e9c492e39bf16d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NotificationDestinationProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd7636d69fb8393bd78925a9f0dee0e9674c202c900928dc5923e8b0d67a5fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90430b3b25353c12dbffcd89fe0703b07c76bd6d0fdc05edb59ba509f75b3607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e2b5d7992a98c94ee332061970dd3a1a3710b52c17c3a4f99369b3d6a14a8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a702f764220e12c0e7db7af266b534fb4497d87d6b6f5e66cfee14b8a43b1a84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd1a7080400157fc76b3949ca3cd6d6700c296762b044cb5b3bcb4fd011e67e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1772727bd952f9f8524b6fdad86b21df73fa96a9aad25d876687b60fdb0a0c(
    value: typing.Optional[typing.Union[NotificationDestinationProperty, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
