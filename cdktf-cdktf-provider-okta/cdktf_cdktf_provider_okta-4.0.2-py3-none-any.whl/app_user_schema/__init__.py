'''
# `okta_app_user_schema`

Refer to the Terraform Registory for docs: [`okta_app_user_schema`](https://www.terraform.io/docs/providers/okta/r/app_user_schema).
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


class AppUserSchema(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appUserSchema.AppUserSchema",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema okta_app_user_schema}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_id: builtins.str,
        index: builtins.str,
        title: builtins.str,
        type: builtins.str,
        array_enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppUserSchemaArrayOneOf", typing.Dict[builtins.str, typing.Any]]]]] = None,
        array_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_name: typing.Optional[builtins.str] = None,
        external_namespace: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        master: typing.Optional[builtins.str] = None,
        max_length: typing.Optional[jsii.Number] = None,
        min_length: typing.Optional[jsii.Number] = None,
        one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppUserSchemaOneOf", typing.Dict[builtins.str, typing.Any]]]]] = None,
        permissions: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scope: typing.Optional[builtins.str] = None,
        union: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unique: typing.Optional[builtins.str] = None,
        user_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema okta_app_user_schema} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#app_id AppUserSchema#app_id}.
        :param index: Subschema unique string identifier. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#index AppUserSchema#index}
        :param title: Subschema title (display name). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#title AppUserSchema#title}
        :param type: Subschema type: string, boolean, number, integer, array, or object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#type AppUserSchema#type}
        :param array_enum: Custom Subschema enumerated value of a property of type array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#array_enum AppUserSchema#array_enum}
        :param array_one_of: array_one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#array_one_of AppUserSchema#array_one_of}
        :param array_type: Subschema array type: string, number, integer, reference. Type field must be an array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#array_type AppUserSchema#array_type}
        :param description: Custom Subschema description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#description AppUserSchema#description}
        :param enum: Custom Subschema enumerated value of the property. see: developer.okta.com/docs/api/resources/schemas#user-profile-schema-property-object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#enum AppUserSchema#enum}
        :param external_name: Subschema external name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#external_name AppUserSchema#external_name}
        :param external_namespace: Subschema external namespace. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#external_namespace AppUserSchema#external_namespace}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#id AppUserSchema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param master: SubSchema profile manager, if not set it will inherit its setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#master AppUserSchema#master}
        :param max_length: Subschema of type string maximum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#max_length AppUserSchema#max_length}
        :param min_length: Subschema of type string minimum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#min_length AppUserSchema#min_length}
        :param one_of: one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#one_of AppUserSchema#one_of}
        :param permissions: SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#permissions AppUserSchema#permissions}
        :param required: Whether the subschema is required. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#required AppUserSchema#required}
        :param scope: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#scope AppUserSchema#scope}.
        :param union: Allows to assign attribute's group priority. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#union AppUserSchema#union}
        :param unique: Subschema unique restriction. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#unique AppUserSchema#unique}
        :param user_type: Custom subschema user type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#user_type AppUserSchema#user_type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c21df91fa9a5fe480c1246d28c43afcfe5d8298bc51f27b6aa7570e324de5ee3)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppUserSchemaConfig(
            app_id=app_id,
            index=index,
            title=title,
            type=type,
            array_enum=array_enum,
            array_one_of=array_one_of,
            array_type=array_type,
            description=description,
            enum=enum,
            external_name=external_name,
            external_namespace=external_namespace,
            id=id,
            master=master,
            max_length=max_length,
            min_length=min_length,
            one_of=one_of,
            permissions=permissions,
            required=required,
            scope=scope,
            union=union,
            unique=unique,
            user_type=user_type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="putArrayOneOf")
    def put_array_one_of(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppUserSchemaArrayOneOf", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29db4e6073ff80ba4a60d4ea0e57aabaa9582f9f46a3f9836bc27428151642e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArrayOneOf", [value]))

    @jsii.member(jsii_name="putOneOf")
    def put_one_of(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppUserSchemaOneOf", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde443898f66e03ad627a3529b5088a577a40fbfa5ad9bba25a0ecd00548fd5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOneOf", [value]))

    @jsii.member(jsii_name="resetArrayEnum")
    def reset_array_enum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArrayEnum", []))

    @jsii.member(jsii_name="resetArrayOneOf")
    def reset_array_one_of(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArrayOneOf", []))

    @jsii.member(jsii_name="resetArrayType")
    def reset_array_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArrayType", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnum")
    def reset_enum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnum", []))

    @jsii.member(jsii_name="resetExternalName")
    def reset_external_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalName", []))

    @jsii.member(jsii_name="resetExternalNamespace")
    def reset_external_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalNamespace", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaster")
    def reset_master(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaster", []))

    @jsii.member(jsii_name="resetMaxLength")
    def reset_max_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxLength", []))

    @jsii.member(jsii_name="resetMinLength")
    def reset_min_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLength", []))

    @jsii.member(jsii_name="resetOneOf")
    def reset_one_of(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOneOf", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetUnion")
    def reset_union(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnion", []))

    @jsii.member(jsii_name="resetUnique")
    def reset_unique(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnique", []))

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
    @jsii.member(jsii_name="arrayOneOf")
    def array_one_of(self) -> "AppUserSchemaArrayOneOfList":
        return typing.cast("AppUserSchemaArrayOneOfList", jsii.get(self, "arrayOneOf"))

    @builtins.property
    @jsii.member(jsii_name="oneOf")
    def one_of(self) -> "AppUserSchemaOneOfList":
        return typing.cast("AppUserSchemaOneOfList", jsii.get(self, "oneOf"))

    @builtins.property
    @jsii.member(jsii_name="appIdInput")
    def app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdInput"))

    @builtins.property
    @jsii.member(jsii_name="arrayEnumInput")
    def array_enum_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "arrayEnumInput"))

    @builtins.property
    @jsii.member(jsii_name="arrayOneOfInput")
    def array_one_of_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppUserSchemaArrayOneOf"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppUserSchemaArrayOneOf"]]], jsii.get(self, "arrayOneOfInput"))

    @builtins.property
    @jsii.member(jsii_name="arrayTypeInput")
    def array_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arrayTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enumInput")
    def enum_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enumInput"))

    @builtins.property
    @jsii.member(jsii_name="externalNameInput")
    def external_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalNameInput"))

    @builtins.property
    @jsii.member(jsii_name="externalNamespaceInput")
    def external_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalNamespaceInput"))

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
    @jsii.member(jsii_name="maxLengthInput")
    def max_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="minLengthInput")
    def min_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="oneOfInput")
    def one_of_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppUserSchemaOneOf"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppUserSchemaOneOf"]]], jsii.get(self, "oneOfInput"))

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
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="unionInput")
    def union_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "unionInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueInput")
    def unique_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uniqueInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3a492cf95e884da2c76b14f191cfb538ee4a6b0adf4de88deaa45d75bc4e7a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value)

    @builtins.property
    @jsii.member(jsii_name="arrayEnum")
    def array_enum(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "arrayEnum"))

    @array_enum.setter
    def array_enum(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6f36b090b3bc126280e2f7629620a03936f86aa2f4dedcbaabb865438b7527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arrayEnum", value)

    @builtins.property
    @jsii.member(jsii_name="arrayType")
    def array_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arrayType"))

    @array_type.setter
    def array_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9772d20f29ee41834926073ff17a7828287bc36b9e2f7224433a9f1b26ef679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arrayType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbdf124d445a3a7a9cc0cfa9efde79906bc0e7882c4eb1c1cca9e2ffdd4b0a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enum")
    def enum(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enum"))

    @enum.setter
    def enum(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75108d174f75f26ba6d98ba01e4a13bb1918e93b994e1fd6f51b3ed63ba47f3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enum", value)

    @builtins.property
    @jsii.member(jsii_name="externalName")
    def external_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalName"))

    @external_name.setter
    def external_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4a6b653b6b2df4f875c64475df7bfaa594b05d5e4adc3dbfa26ba110e4d30f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalName", value)

    @builtins.property
    @jsii.member(jsii_name="externalNamespace")
    def external_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalNamespace"))

    @external_namespace.setter
    def external_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e115796ad69f85071c41e533e30bb338d49519164298d0fef5eadba4130b069f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalNamespace", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002c6934cc9e6f25dd7483c4553a2ff760a18f85775d1d90f93e17d95a107250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30e435710b832867d09d4fe3a02c15b5ba44126c481471f46999740d58d13a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value)

    @builtins.property
    @jsii.member(jsii_name="master")
    def master(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "master"))

    @master.setter
    def master(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776d00e2dd7fc77b951d229713d73e6fb0029550ad68ff8c2f964eb451df71dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "master", value)

    @builtins.property
    @jsii.member(jsii_name="maxLength")
    def max_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLength"))

    @max_length.setter
    def max_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d7e2f9336be70361b25d5c504cb76f136d386d8e7e505b689a32f6c2204d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLength", value)

    @builtins.property
    @jsii.member(jsii_name="minLength")
    def min_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLength"))

    @min_length.setter
    def min_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d3a81cf53539f71672b88b10f3c961d96e3e0a67620647f8c03ce6f0924635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLength", value)

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d6eb941b25b5f1bcd6ec8b6a126c0104485123aa354639cd70f1bd9209f695)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44e11b6c68480adcfbeb384929d4a6f22b010627b05afa5a212a55cdc90a0093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978b6b28ce72a15f120e5e5d4e0c51a0c6de0c4002133a18cabd5af0df423c9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6fce17f11a225f51f77641c087dbc5028436300cc63e9e2092eed05eda82cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ede3f7f2ef51bd7035dc59831c301b6d7b04583ca43d65dc667e679be4426b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="union")
    def union(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "union"))

    @union.setter
    def union(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0c8650e832de625a3f89b9686bfd23025a4fd87e765e87d41a558054f529878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "union", value)

    @builtins.property
    @jsii.member(jsii_name="unique")
    def unique(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unique"))

    @unique.setter
    def unique(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6183274cb07c3348a19b9fdcb9126a33496abf3c77ac15b1d9b6873f0813c3bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unique", value)

    @builtins.property
    @jsii.member(jsii_name="userType")
    def user_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userType"))

    @user_type.setter
    def user_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4de1b183ae27b509d56c7f88bc88d3aaea2ed2c58eb30e4e7be5ee663fd30e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appUserSchema.AppUserSchemaArrayOneOf",
    jsii_struct_bases=[],
    name_mapping={"const": "const", "title": "title"},
)
class AppUserSchemaArrayOneOf:
    def __init__(self, *, const: builtins.str, title: builtins.str) -> None:
        '''
        :param const: Enum value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#const AppUserSchema#const}
        :param title: Enum title. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#title AppUserSchema#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61f79a6f69383c55bd374592e988190a5354c9caf1403f85f865c6518554fc0)
            check_type(argname="argument const", value=const, expected_type=type_hints["const"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "const": const,
            "title": title,
        }

    @builtins.property
    def const(self) -> builtins.str:
        '''Enum value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#const AppUserSchema#const}
        '''
        result = self._values.get("const")
        assert result is not None, "Required property 'const' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Enum title.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#title AppUserSchema#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppUserSchemaArrayOneOf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppUserSchemaArrayOneOfList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appUserSchema.AppUserSchemaArrayOneOfList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8c68607275e521f2e13ff52d2f4993f009c7036cbc78ac07d4d084335d71365)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppUserSchemaArrayOneOfOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7be2b0db5a48ff606d4ed6af9f1eae43b9d25678a65e8a7dbaba7481bc02372)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppUserSchemaArrayOneOfOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b9ed4474ce8a59ef1459ad4b297afd09f72ea6b49c62b852e25233b9b041d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d222701de1055714d56e6ed7a4e16471c89829f0443bb3b3520a84e9031b83a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1293135b77055d3c52b8af0373b83c87d3db428a2d11fbf8f27c3110e592f593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppUserSchemaArrayOneOf]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppUserSchemaArrayOneOf]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppUserSchemaArrayOneOf]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b17d8490a411c9fc14df298d1d4a775397e3cf59013aaa1ec3cfc40a7991cefc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppUserSchemaArrayOneOfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appUserSchema.AppUserSchemaArrayOneOfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a282132e350f6aa3576679c13f7cccb216bdc9b13f7ec95566f610ae9353362)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="constInput")
    def const_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "constInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="const")
    def const(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "const"))

    @const.setter
    def const(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad436d1d26d984f5c98b7ac91419cba57a64373f63037f12eb01012f2f7a742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "const", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45de9c117a2207fee69778e95603a627136415b552bb0b193c6bd664fc0d8a85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppUserSchemaArrayOneOf, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppUserSchemaArrayOneOf, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppUserSchemaArrayOneOf, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc83f27a4b5a183fb3e97ffa27383c80e228b73b06be4d95b2a66c33e2455678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appUserSchema.AppUserSchemaConfig",
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
        "array_enum": "arrayEnum",
        "array_one_of": "arrayOneOf",
        "array_type": "arrayType",
        "description": "description",
        "enum": "enum",
        "external_name": "externalName",
        "external_namespace": "externalNamespace",
        "id": "id",
        "master": "master",
        "max_length": "maxLength",
        "min_length": "minLength",
        "one_of": "oneOf",
        "permissions": "permissions",
        "required": "required",
        "scope": "scope",
        "union": "union",
        "unique": "unique",
        "user_type": "userType",
    },
)
class AppUserSchemaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        array_enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppUserSchemaArrayOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
        array_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_name: typing.Optional[builtins.str] = None,
        external_namespace: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        master: typing.Optional[builtins.str] = None,
        max_length: typing.Optional[jsii.Number] = None,
        min_length: typing.Optional[jsii.Number] = None,
        one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppUserSchemaOneOf", typing.Dict[builtins.str, typing.Any]]]]] = None,
        permissions: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scope: typing.Optional[builtins.str] = None,
        union: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unique: typing.Optional[builtins.str] = None,
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
        :param app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#app_id AppUserSchema#app_id}.
        :param index: Subschema unique string identifier. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#index AppUserSchema#index}
        :param title: Subschema title (display name). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#title AppUserSchema#title}
        :param type: Subschema type: string, boolean, number, integer, array, or object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#type AppUserSchema#type}
        :param array_enum: Custom Subschema enumerated value of a property of type array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#array_enum AppUserSchema#array_enum}
        :param array_one_of: array_one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#array_one_of AppUserSchema#array_one_of}
        :param array_type: Subschema array type: string, number, integer, reference. Type field must be an array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#array_type AppUserSchema#array_type}
        :param description: Custom Subschema description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#description AppUserSchema#description}
        :param enum: Custom Subschema enumerated value of the property. see: developer.okta.com/docs/api/resources/schemas#user-profile-schema-property-object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#enum AppUserSchema#enum}
        :param external_name: Subschema external name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#external_name AppUserSchema#external_name}
        :param external_namespace: Subschema external namespace. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#external_namespace AppUserSchema#external_namespace}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#id AppUserSchema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param master: SubSchema profile manager, if not set it will inherit its setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#master AppUserSchema#master}
        :param max_length: Subschema of type string maximum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#max_length AppUserSchema#max_length}
        :param min_length: Subschema of type string minimum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#min_length AppUserSchema#min_length}
        :param one_of: one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#one_of AppUserSchema#one_of}
        :param permissions: SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#permissions AppUserSchema#permissions}
        :param required: Whether the subschema is required. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#required AppUserSchema#required}
        :param scope: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#scope AppUserSchema#scope}.
        :param union: Allows to assign attribute's group priority. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#union AppUserSchema#union}
        :param unique: Subschema unique restriction. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#unique AppUserSchema#unique}
        :param user_type: Custom subschema user type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#user_type AppUserSchema#user_type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd919e3c5666da879179b7fdf78b3f16c9715b62083546c3ab1cf8bfd2840a5)
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
            check_type(argname="argument array_enum", value=array_enum, expected_type=type_hints["array_enum"])
            check_type(argname="argument array_one_of", value=array_one_of, expected_type=type_hints["array_one_of"])
            check_type(argname="argument array_type", value=array_type, expected_type=type_hints["array_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enum", value=enum, expected_type=type_hints["enum"])
            check_type(argname="argument external_name", value=external_name, expected_type=type_hints["external_name"])
            check_type(argname="argument external_namespace", value=external_namespace, expected_type=type_hints["external_namespace"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument master", value=master, expected_type=type_hints["master"])
            check_type(argname="argument max_length", value=max_length, expected_type=type_hints["max_length"])
            check_type(argname="argument min_length", value=min_length, expected_type=type_hints["min_length"])
            check_type(argname="argument one_of", value=one_of, expected_type=type_hints["one_of"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument union", value=union, expected_type=type_hints["union"])
            check_type(argname="argument unique", value=unique, expected_type=type_hints["unique"])
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
        if array_enum is not None:
            self._values["array_enum"] = array_enum
        if array_one_of is not None:
            self._values["array_one_of"] = array_one_of
        if array_type is not None:
            self._values["array_type"] = array_type
        if description is not None:
            self._values["description"] = description
        if enum is not None:
            self._values["enum"] = enum
        if external_name is not None:
            self._values["external_name"] = external_name
        if external_namespace is not None:
            self._values["external_namespace"] = external_namespace
        if id is not None:
            self._values["id"] = id
        if master is not None:
            self._values["master"] = master
        if max_length is not None:
            self._values["max_length"] = max_length
        if min_length is not None:
            self._values["min_length"] = min_length
        if one_of is not None:
            self._values["one_of"] = one_of
        if permissions is not None:
            self._values["permissions"] = permissions
        if required is not None:
            self._values["required"] = required
        if scope is not None:
            self._values["scope"] = scope
        if union is not None:
            self._values["union"] = union
        if unique is not None:
            self._values["unique"] = unique
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#app_id AppUserSchema#app_id}.'''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index(self) -> builtins.str:
        '''Subschema unique string identifier.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#index AppUserSchema#index}
        '''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Subschema title (display name).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#title AppUserSchema#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Subschema type: string, boolean, number, integer, array, or object.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#type AppUserSchema#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def array_enum(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Custom Subschema enumerated value of a property of type array.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#array_enum AppUserSchema#array_enum}
        '''
        result = self._values.get("array_enum")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def array_one_of(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppUserSchemaArrayOneOf]]]:
        '''array_one_of block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#array_one_of AppUserSchema#array_one_of}
        '''
        result = self._values.get("array_one_of")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppUserSchemaArrayOneOf]]], result)

    @builtins.property
    def array_type(self) -> typing.Optional[builtins.str]:
        '''Subschema array type: string, number, integer, reference. Type field must be an array.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#array_type AppUserSchema#array_type}
        '''
        result = self._values.get("array_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Custom Subschema description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#description AppUserSchema#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enum(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Custom Subschema enumerated value of the property. see: developer.okta.com/docs/api/resources/schemas#user-profile-schema-property-object.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#enum AppUserSchema#enum}
        '''
        result = self._values.get("enum")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_name(self) -> typing.Optional[builtins.str]:
        '''Subschema external name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#external_name AppUserSchema#external_name}
        '''
        result = self._values.get("external_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_namespace(self) -> typing.Optional[builtins.str]:
        '''Subschema external namespace.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#external_namespace AppUserSchema#external_namespace}
        '''
        result = self._values.get("external_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#id AppUserSchema#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master(self) -> typing.Optional[builtins.str]:
        '''SubSchema profile manager, if not set it will inherit its setting.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#master AppUserSchema#master}
        '''
        result = self._values.get("master")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_length(self) -> typing.Optional[jsii.Number]:
        '''Subschema of type string maximum length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#max_length AppUserSchema#max_length}
        '''
        result = self._values.get("max_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        '''Subschema of type string minimum length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#min_length AppUserSchema#min_length}
        '''
        result = self._values.get("min_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def one_of(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppUserSchemaOneOf"]]]:
        '''one_of block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#one_of AppUserSchema#one_of}
        '''
        result = self._values.get("one_of")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppUserSchemaOneOf"]]], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#permissions AppUserSchema#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the subschema is required.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#required AppUserSchema#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#scope AppUserSchema#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def union(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows to assign attribute's group priority.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#union AppUserSchema#union}
        '''
        result = self._values.get("union")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def unique(self) -> typing.Optional[builtins.str]:
        '''Subschema unique restriction.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#unique AppUserSchema#unique}
        '''
        result = self._values.get("unique")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_type(self) -> typing.Optional[builtins.str]:
        '''Custom subschema user type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#user_type AppUserSchema#user_type}
        '''
        result = self._values.get("user_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppUserSchemaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appUserSchema.AppUserSchemaOneOf",
    jsii_struct_bases=[],
    name_mapping={"const": "const", "title": "title"},
)
class AppUserSchemaOneOf:
    def __init__(self, *, const: builtins.str, title: builtins.str) -> None:
        '''
        :param const: Enum value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#const AppUserSchema#const}
        :param title: Enum title. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#title AppUserSchema#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc5fb8b68fee334b78a42d8ca5fac8f917f8a67450896e97f0e113dd376f9f9)
            check_type(argname="argument const", value=const, expected_type=type_hints["const"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "const": const,
            "title": title,
        }

    @builtins.property
    def const(self) -> builtins.str:
        '''Enum value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#const AppUserSchema#const}
        '''
        result = self._values.get("const")
        assert result is not None, "Required property 'const' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Enum title.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_user_schema#title AppUserSchema#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppUserSchemaOneOf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppUserSchemaOneOfList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appUserSchema.AppUserSchemaOneOfList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22c0281d57ed37139c1d8b90c085d6a7a258dbc43ccbc25f4e97f234da407e4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppUserSchemaOneOfOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4685fb0300178965d8942fa321485f58e9ca055f00bbf031d2999151ca290615)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppUserSchemaOneOfOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dda752706d2519f4bca06e9ecb392f573bfb5adf26dc877f0ae156f8bb0434e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfe37a1eb6ff1ebfb8bce18f9b7d9b43403c743c66f3b1c73d5d8cfda1cb97c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a839562e273880bcacaa6e7f88f7aaf8cd8972241baca66ba397cc7ee5aac86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppUserSchemaOneOf]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppUserSchemaOneOf]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppUserSchemaOneOf]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62cdbc840e30bcd22b1a94eb700eff2d77b5e99602873b6ed402f3282df67eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppUserSchemaOneOfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appUserSchema.AppUserSchemaOneOfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cca754903cbcb88f82c19b9c9cdb94d177628743732039dfaa50937c48c1dc88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="constInput")
    def const_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "constInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="const")
    def const(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "const"))

    @const.setter
    def const(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b541986a15d186e4b7e41ef2ef587bb0e82900b7ccb64fd7740e6197d5727341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "const", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e341ab485dcb95c2dc3136706775671456847e4a1b5bb9bbd495b61e3d78873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppUserSchemaOneOf, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppUserSchemaOneOf, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppUserSchemaOneOf, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8baa33443fb52ebbc1a092fc9efa8aa9c884a875fd665ff259f0d510822e22b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AppUserSchema",
    "AppUserSchemaArrayOneOf",
    "AppUserSchemaArrayOneOfList",
    "AppUserSchemaArrayOneOfOutputReference",
    "AppUserSchemaConfig",
    "AppUserSchemaOneOf",
    "AppUserSchemaOneOfList",
    "AppUserSchemaOneOfOutputReference",
]

publication.publish()

def _typecheckingstub__c21df91fa9a5fe480c1246d28c43afcfe5d8298bc51f27b6aa7570e324de5ee3(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_id: builtins.str,
    index: builtins.str,
    title: builtins.str,
    type: builtins.str,
    array_enum: typing.Optional[typing.Sequence[builtins.str]] = None,
    array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppUserSchemaArrayOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    array_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enum: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_name: typing.Optional[builtins.str] = None,
    external_namespace: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    master: typing.Optional[builtins.str] = None,
    max_length: typing.Optional[jsii.Number] = None,
    min_length: typing.Optional[jsii.Number] = None,
    one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppUserSchemaOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    permissions: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scope: typing.Optional[builtins.str] = None,
    union: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unique: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__29db4e6073ff80ba4a60d4ea0e57aabaa9582f9f46a3f9836bc27428151642e4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppUserSchemaArrayOneOf, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde443898f66e03ad627a3529b5088a577a40fbfa5ad9bba25a0ecd00548fd5a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppUserSchemaOneOf, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a492cf95e884da2c76b14f191cfb538ee4a6b0adf4de88deaa45d75bc4e7a8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6f36b090b3bc126280e2f7629620a03936f86aa2f4dedcbaabb865438b7527(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9772d20f29ee41834926073ff17a7828287bc36b9e2f7224433a9f1b26ef679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbdf124d445a3a7a9cc0cfa9efde79906bc0e7882c4eb1c1cca9e2ffdd4b0a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75108d174f75f26ba6d98ba01e4a13bb1918e93b994e1fd6f51b3ed63ba47f3d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4a6b653b6b2df4f875c64475df7bfaa594b05d5e4adc3dbfa26ba110e4d30f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e115796ad69f85071c41e533e30bb338d49519164298d0fef5eadba4130b069f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002c6934cc9e6f25dd7483c4553a2ff760a18f85775d1d90f93e17d95a107250(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30e435710b832867d09d4fe3a02c15b5ba44126c481471f46999740d58d13a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776d00e2dd7fc77b951d229713d73e6fb0029550ad68ff8c2f964eb451df71dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d7e2f9336be70361b25d5c504cb76f136d386d8e7e505b689a32f6c2204d27(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d3a81cf53539f71672b88b10f3c961d96e3e0a67620647f8c03ce6f0924635(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d6eb941b25b5f1bcd6ec8b6a126c0104485123aa354639cd70f1bd9209f695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e11b6c68480adcfbeb384929d4a6f22b010627b05afa5a212a55cdc90a0093(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978b6b28ce72a15f120e5e5d4e0c51a0c6de0c4002133a18cabd5af0df423c9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6fce17f11a225f51f77641c087dbc5028436300cc63e9e2092eed05eda82cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ede3f7f2ef51bd7035dc59831c301b6d7b04583ca43d65dc667e679be4426b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c8650e832de625a3f89b9686bfd23025a4fd87e765e87d41a558054f529878(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6183274cb07c3348a19b9fdcb9126a33496abf3c77ac15b1d9b6873f0813c3bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4de1b183ae27b509d56c7f88bc88d3aaea2ed2c58eb30e4e7be5ee663fd30e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61f79a6f69383c55bd374592e988190a5354c9caf1403f85f865c6518554fc0(
    *,
    const: builtins.str,
    title: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c68607275e521f2e13ff52d2f4993f009c7036cbc78ac07d4d084335d71365(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7be2b0db5a48ff606d4ed6af9f1eae43b9d25678a65e8a7dbaba7481bc02372(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b9ed4474ce8a59ef1459ad4b297afd09f72ea6b49c62b852e25233b9b041d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d222701de1055714d56e6ed7a4e16471c89829f0443bb3b3520a84e9031b83a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1293135b77055d3c52b8af0373b83c87d3db428a2d11fbf8f27c3110e592f593(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b17d8490a411c9fc14df298d1d4a775397e3cf59013aaa1ec3cfc40a7991cefc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppUserSchemaArrayOneOf]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a282132e350f6aa3576679c13f7cccb216bdc9b13f7ec95566f610ae9353362(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad436d1d26d984f5c98b7ac91419cba57a64373f63037f12eb01012f2f7a742(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45de9c117a2207fee69778e95603a627136415b552bb0b193c6bd664fc0d8a85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc83f27a4b5a183fb3e97ffa27383c80e228b73b06be4d95b2a66c33e2455678(
    value: typing.Optional[typing.Union[AppUserSchemaArrayOneOf, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd919e3c5666da879179b7fdf78b3f16c9715b62083546c3ab1cf8bfd2840a5(
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
    array_enum: typing.Optional[typing.Sequence[builtins.str]] = None,
    array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppUserSchemaArrayOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    array_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enum: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_name: typing.Optional[builtins.str] = None,
    external_namespace: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    master: typing.Optional[builtins.str] = None,
    max_length: typing.Optional[jsii.Number] = None,
    min_length: typing.Optional[jsii.Number] = None,
    one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppUserSchemaOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    permissions: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scope: typing.Optional[builtins.str] = None,
    union: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unique: typing.Optional[builtins.str] = None,
    user_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc5fb8b68fee334b78a42d8ca5fac8f917f8a67450896e97f0e113dd376f9f9(
    *,
    const: builtins.str,
    title: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c0281d57ed37139c1d8b90c085d6a7a258dbc43ccbc25f4e97f234da407e4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4685fb0300178965d8942fa321485f58e9ca055f00bbf031d2999151ca290615(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dda752706d2519f4bca06e9ecb392f573bfb5adf26dc877f0ae156f8bb0434e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe37a1eb6ff1ebfb8bce18f9b7d9b43403c743c66f3b1c73d5d8cfda1cb97c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a839562e273880bcacaa6e7f88f7aaf8cd8972241baca66ba397cc7ee5aac86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cdbc840e30bcd22b1a94eb700eff2d77b5e99602873b6ed402f3282df67eca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppUserSchemaOneOf]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca754903cbcb88f82c19b9c9cdb94d177628743732039dfaa50937c48c1dc88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b541986a15d186e4b7e41ef2ef587bb0e82900b7ccb64fd7740e6197d5727341(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e341ab485dcb95c2dc3136706775671456847e4a1b5bb9bbd495b61e3d78873(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8baa33443fb52ebbc1a092fc9efa8aa9c884a875fd665ff259f0d510822e22b5(
    value: typing.Optional[typing.Union[AppUserSchemaOneOf, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
