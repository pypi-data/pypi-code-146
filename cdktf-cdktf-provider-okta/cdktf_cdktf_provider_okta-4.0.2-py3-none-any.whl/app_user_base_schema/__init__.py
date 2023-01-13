'''
# `okta_app_user_base_schema`

Refer to the Terraform Registory for docs: [`okta_app_user_base_schema`](https://www.terraform.io/docs/providers/okta/r/app_user_base_schema).
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


class AppUserBaseSchema(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appUserBaseSchema.AppUserBaseSchema",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema okta_app_user_base_schema}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_id: builtins.str,
        index: builtins.str,
        title: builtins.str,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        master: typing.Optional[builtins.str] = None,
        pattern: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema okta_app_user_base_schema} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#app_id AppUserBaseSchema#app_id}.
        :param index: Subschema unique string identifier. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#index AppUserBaseSchema#index}
        :param title: Subschema title (display name). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#title AppUserBaseSchema#title}
        :param type: Subschema type: string, boolean, number, integer, array, or object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#type AppUserBaseSchema#type}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#id AppUserBaseSchema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param master: SubSchema profile manager, if not set it will inherit its setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#master AppUserBaseSchema#master}
        :param pattern: The validation pattern to use for the subschema. Must be in form of '.+', or '[]+' if present.'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#pattern AppUserBaseSchema#pattern}
        :param permissions: SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#permissions AppUserBaseSchema#permissions}
        :param required: Whether the subschema is required. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#required AppUserBaseSchema#required}
        :param user_type: Custom subschema user type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#user_type AppUserBaseSchema#user_type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d726209dc5028acc7bde9970c9bc73896e0df644d5e82a6c7e1dd9dc519b0bfa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppUserBaseSchemaConfig(
            app_id=app_id,
            index=index,
            title=title,
            type=type,
            id=id,
            master=master,
            pattern=pattern,
            permissions=permissions,
            required=required,
            user_type=user_type,
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

    @jsii.member(jsii_name="resetMaster")
    def reset_master(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaster", []))

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @jsii.member(jsii_name="resetUserType")
    def reset_user_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="appIdInput")
    def app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexInput")
    def index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexInput"))

    @builtins.property
    @jsii.member(jsii_name="masterInput")
    def master_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userTypeInput")
    def user_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacee5642c250a985e662b0a4452f5dffedd693cf61abca6e97d9da8a98607ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f47eda55ef60b6b97d1eed5e62b14c495ae26c1e06ef2846b588207aa808c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69e67b17257e35726451c8988732cd12165b627227d3811309f51bd3e23a0c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value)

    @builtins.property
    @jsii.member(jsii_name="master")
    def master(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "master"))

    @master.setter
    def master(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91bf8dc26dfa80ca8d94b0dd084ffa87e419c98a575c9a0e7209a52e170e7d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "master", value)

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dba0b1d7815a88ece4e7e42c3d6a60a7df8dcdbe607774c63b818a3d3acad390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value)

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d61d828e8ecf174bb9e1c27be9f392abf1e051deaf72b9906ab2c0ea68d1db43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissions", value)

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "required"))

    @required.setter
    def required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb18f7f5a6c3aa7d23e70366a20799ae7c28d20640bf93a96d265bcb51bc1fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f180c12bd664ebd750efdabf0f7d4de4fdfbc3f7d9053029ef799b28a2c8ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfa600216bcaaa46a19d92529cb1a37d59af3b52005c47716d7001af620bd58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userType")
    def user_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userType"))

    @user_type.setter
    def user_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33422dc23d4522b02f648fb77e504ab456c2ca78f2b2c7defeb93d4bfc5a306a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appUserBaseSchema.AppUserBaseSchemaConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_id": "appId",
        "index": "index",
        "title": "title",
        "type": "type",
        "id": "id",
        "master": "master",
        "pattern": "pattern",
        "permissions": "permissions",
        "required": "required",
        "user_type": "userType",
    },
)
class AppUserBaseSchemaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_id: builtins.str,
        index: builtins.str,
        title: builtins.str,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        master: typing.Optional[builtins.str] = None,
        pattern: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#app_id AppUserBaseSchema#app_id}.
        :param index: Subschema unique string identifier. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#index AppUserBaseSchema#index}
        :param title: Subschema title (display name). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#title AppUserBaseSchema#title}
        :param type: Subschema type: string, boolean, number, integer, array, or object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#type AppUserBaseSchema#type}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#id AppUserBaseSchema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param master: SubSchema profile manager, if not set it will inherit its setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#master AppUserBaseSchema#master}
        :param pattern: The validation pattern to use for the subschema. Must be in form of '.+', or '[]+' if present.'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#pattern AppUserBaseSchema#pattern}
        :param permissions: SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#permissions AppUserBaseSchema#permissions}
        :param required: Whether the subschema is required. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#required AppUserBaseSchema#required}
        :param user_type: Custom subschema user type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#user_type AppUserBaseSchema#user_type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39bc0d393239d4e2b4a3c03f9e3597722d9988260b90fb33e6c335a65fe419be)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument master", value=master, expected_type=type_hints["master"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument user_type", value=user_type, expected_type=type_hints["user_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
            "index": index,
            "title": title,
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
        if id is not None:
            self._values["id"] = id
        if master is not None:
            self._values["master"] = master
        if pattern is not None:
            self._values["pattern"] = pattern
        if permissions is not None:
            self._values["permissions"] = permissions
        if required is not None:
            self._values["required"] = required
        if user_type is not None:
            self._values["user_type"] = user_type

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
    def app_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#app_id AppUserBaseSchema#app_id}.'''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index(self) -> builtins.str:
        '''Subschema unique string identifier.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#index AppUserBaseSchema#index}
        '''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Subschema title (display name).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#title AppUserBaseSchema#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Subschema type: string, boolean, number, integer, array, or object.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#type AppUserBaseSchema#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#id AppUserBaseSchema#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master(self) -> typing.Optional[builtins.str]:
        '''SubSchema profile manager, if not set it will inherit its setting.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#master AppUserBaseSchema#master}
        '''
        result = self._values.get("master")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''The validation pattern to use for the subschema. Must be in form of '.+', or '[]+' if present.'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#pattern AppUserBaseSchema#pattern}
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#permissions AppUserBaseSchema#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the subschema is required.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#required AppUserBaseSchema#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user_type(self) -> typing.Optional[builtins.str]:
        '''Custom subschema user type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_base_schema#user_type AppUserBaseSchema#user_type}
        '''
        result = self._values.get("user_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppUserBaseSchemaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AppUserBaseSchema",
    "AppUserBaseSchemaConfig",
]

publication.publish()

def _typecheckingstub__d726209dc5028acc7bde9970c9bc73896e0df644d5e82a6c7e1dd9dc519b0bfa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_id: builtins.str,
    index: builtins.str,
    title: builtins.str,
    type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    master: typing.Optional[builtins.str] = None,
    pattern: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__bacee5642c250a985e662b0a4452f5dffedd693cf61abca6e97d9da8a98607ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f47eda55ef60b6b97d1eed5e62b14c495ae26c1e06ef2846b588207aa808c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69e67b17257e35726451c8988732cd12165b627227d3811309f51bd3e23a0c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91bf8dc26dfa80ca8d94b0dd084ffa87e419c98a575c9a0e7209a52e170e7d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba0b1d7815a88ece4e7e42c3d6a60a7df8dcdbe607774c63b818a3d3acad390(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61d828e8ecf174bb9e1c27be9f392abf1e051deaf72b9906ab2c0ea68d1db43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb18f7f5a6c3aa7d23e70366a20799ae7c28d20640bf93a96d265bcb51bc1fe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f180c12bd664ebd750efdabf0f7d4de4fdfbc3f7d9053029ef799b28a2c8ced(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfa600216bcaaa46a19d92529cb1a37d59af3b52005c47716d7001af620bd58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33422dc23d4522b02f648fb77e504ab456c2ca78f2b2c7defeb93d4bfc5a306a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39bc0d393239d4e2b4a3c03f9e3597722d9988260b90fb33e6c335a65fe419be(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_id: builtins.str,
    index: builtins.str,
    title: builtins.str,
    type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    master: typing.Optional[builtins.str] = None,
    pattern: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
