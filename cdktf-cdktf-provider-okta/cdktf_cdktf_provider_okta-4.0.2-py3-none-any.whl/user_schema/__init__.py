'''
# `okta_user_schema`

Refer to the Terraform Registory for docs: [`okta_user_schema`](https://www.terraform.io/docs/providers/okta/r/user_schema).
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


class UserSchema(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.userSchema.UserSchema",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/user_schema okta_user_schema}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        index: builtins.str,
        title: builtins.str,
        type: builtins.str,
        array_enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["UserSchemaArrayOneOf", typing.Dict[builtins.str, typing.Any]]]]] = None,
        array_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_name: typing.Optional[builtins.str] = None,
        external_namespace: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        master: typing.Optional[builtins.str] = None,
        master_override_priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["UserSchemaMasterOverridePriority", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_length: typing.Optional[jsii.Number] = None,
        min_length: typing.Optional[jsii.Number] = None,
        one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["UserSchemaOneOf", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pattern: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scope: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/user_schema okta_user_schema} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param index: Subschema unique string identifier. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#index UserSchema#index}
        :param title: Subschema title (display name). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#title UserSchema#title}
        :param type: Subschema type: string, boolean, number, integer, array, or object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#type UserSchema#type}
        :param array_enum: Custom Subschema enumerated value of a property of type array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#array_enum UserSchema#array_enum}
        :param array_one_of: array_one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#array_one_of UserSchema#array_one_of}
        :param array_type: Subschema array type: string, number, integer, reference. Type field must be an array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#array_type UserSchema#array_type}
        :param description: Custom Subschema description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#description UserSchema#description}
        :param enum: Custom Subschema enumerated value of the property. see: developer.okta.com/docs/api/resources/schemas#user-profile-schema-property-object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#enum UserSchema#enum}
        :param external_name: Subschema external name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#external_name UserSchema#external_name}
        :param external_namespace: Subschema external namespace. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#external_namespace UserSchema#external_namespace}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#id UserSchema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param master: SubSchema profile manager, if not set it will inherit its setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#master UserSchema#master}
        :param master_override_priority: master_override_priority block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#master_override_priority UserSchema#master_override_priority}
        :param max_length: Subschema of type string maximum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#max_length UserSchema#max_length}
        :param min_length: Subschema of type string minimum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#min_length UserSchema#min_length}
        :param one_of: one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#one_of UserSchema#one_of}
        :param pattern: The validation pattern to use for the subschema. Must be in form of '.+', or '[]+' if present.'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#pattern UserSchema#pattern}
        :param permissions: SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#permissions UserSchema#permissions}
        :param required: Whether the subschema is required. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#required UserSchema#required}
        :param scope: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#scope UserSchema#scope}.
        :param unique: Subschema unique restriction. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#unique UserSchema#unique}
        :param user_type: Custom subschema user type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#user_type UserSchema#user_type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4d2bc14d70bb10896991f71284aff0f9fa5fbe4fc58ba6cc9e2f19db973c6b)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = UserSchemaConfig(
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
            master_override_priority=master_override_priority,
            max_length=max_length,
            min_length=min_length,
            one_of=one_of,
            pattern=pattern,
            permissions=permissions,
            required=required,
            scope=scope,
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["UserSchemaArrayOneOf", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f7b92388e111bb31232086d26c91588c703deb7e845d41bfdb0ee766612389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArrayOneOf", [value]))

    @jsii.member(jsii_name="putMasterOverridePriority")
    def put_master_override_priority(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["UserSchemaMasterOverridePriority", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9bbcd9848863983d9b31e7a938cea6c430829cd1c92c9dd6a7d7872d62670b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMasterOverridePriority", [value]))

    @jsii.member(jsii_name="putOneOf")
    def put_one_of(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["UserSchemaOneOf", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415e0d6448978d92022f5c3e31720fea65f6e99b77830714aa8fd7f51c8eaf33)
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

    @jsii.member(jsii_name="resetMasterOverridePriority")
    def reset_master_override_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterOverridePriority", []))

    @jsii.member(jsii_name="resetMaxLength")
    def reset_max_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxLength", []))

    @jsii.member(jsii_name="resetMinLength")
    def reset_min_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLength", []))

    @jsii.member(jsii_name="resetOneOf")
    def reset_one_of(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOneOf", []))

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

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
    def array_one_of(self) -> "UserSchemaArrayOneOfList":
        return typing.cast("UserSchemaArrayOneOfList", jsii.get(self, "arrayOneOf"))

    @builtins.property
    @jsii.member(jsii_name="masterOverridePriority")
    def master_override_priority(self) -> "UserSchemaMasterOverridePriorityList":
        return typing.cast("UserSchemaMasterOverridePriorityList", jsii.get(self, "masterOverridePriority"))

    @builtins.property
    @jsii.member(jsii_name="oneOf")
    def one_of(self) -> "UserSchemaOneOfList":
        return typing.cast("UserSchemaOneOfList", jsii.get(self, "oneOf"))

    @builtins.property
    @jsii.member(jsii_name="arrayEnumInput")
    def array_enum_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "arrayEnumInput"))

    @builtins.property
    @jsii.member(jsii_name="arrayOneOfInput")
    def array_one_of_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserSchemaArrayOneOf"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserSchemaArrayOneOf"]]], jsii.get(self, "arrayOneOfInput"))

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
    @jsii.member(jsii_name="masterOverridePriorityInput")
    def master_override_priority_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserSchemaMasterOverridePriority"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserSchemaMasterOverridePriority"]]], jsii.get(self, "masterOverridePriorityInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserSchemaOneOf"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserSchemaOneOf"]]], jsii.get(self, "oneOfInput"))

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
    @jsii.member(jsii_name="uniqueInput")
    def unique_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uniqueInput"))

    @builtins.property
    @jsii.member(jsii_name="userTypeInput")
    def user_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="arrayEnum")
    def array_enum(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "arrayEnum"))

    @array_enum.setter
    def array_enum(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1269d37c855168d2baed40d7b7a5f7673729484a881c917dd09fd737f9bd6bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arrayEnum", value)

    @builtins.property
    @jsii.member(jsii_name="arrayType")
    def array_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arrayType"))

    @array_type.setter
    def array_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96d152b263f3bfd6c90965665afa9df09d83eb624b06ad55d6511b43122cd45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arrayType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae36b34cf6c6c86ac278821bc773916df2c7cd4298c63d68f3db8fc633e90c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enum")
    def enum(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enum"))

    @enum.setter
    def enum(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__738fcba3930d3a194dc9537755e240799fafa55f6e87c22b6442ac194aecfe4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enum", value)

    @builtins.property
    @jsii.member(jsii_name="externalName")
    def external_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalName"))

    @external_name.setter
    def external_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13fb85dcf8d486640b269fdd2fc485c6d4a44e8aac1780d4569a770e5399ef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalName", value)

    @builtins.property
    @jsii.member(jsii_name="externalNamespace")
    def external_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalNamespace"))

    @external_namespace.setter
    def external_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca25fc7fdb997cd6d015a1d2b4b5412f700b7064084fc7097bcee03d4a8c3a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalNamespace", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e08f7ac280e1ed4f2e4f839630b62605624afe5cbbcff54fe65fc0989f2dbab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2ad52b94641b093a15162780965859385b695afc933f465a476ccf1e4a543b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value)

    @builtins.property
    @jsii.member(jsii_name="master")
    def master(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "master"))

    @master.setter
    def master(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7886c47fe67a9847ad39b2a06f8f50ffd8a8ef498ae0776007a4370a3b6ac67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "master", value)

    @builtins.property
    @jsii.member(jsii_name="maxLength")
    def max_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLength"))

    @max_length.setter
    def max_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af115a9f26550af7889561883bdbab78a38b6cae095772d24a9f8c7dc0996f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLength", value)

    @builtins.property
    @jsii.member(jsii_name="minLength")
    def min_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLength"))

    @min_length.setter
    def min_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d4f047527c39e5af24b544ff46617188c027508476412c9080dc7a54dc240c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLength", value)

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89e7697fceb84b498634592f7eae915b9b8d371d0013bdea193a5e60f6480b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value)

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f7537f0b4cf0da3ac69f7a99e634e06f702d6c4268a1239ad7cc059c9f9341)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6276abd679ebe70f06d9174f868ef2f0f37f38faa5cd6fe82a9deb811baa7a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b83c00212a6e191d728d2072daa3d5c8d19438fb307048ba27aefe857df4774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42b01203c27021e5fc0aabebbbca0f61ea584ab7657dc97130c573c165b4da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58249edb79f00b3f44476bbf9af0b291f6b1d4146d610d3d58f497c77c7b1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="unique")
    def unique(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unique"))

    @unique.setter
    def unique(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c6656cba9c3d1577c18655ad0482520cc59654d271a499285af57dc92ca121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unique", value)

    @builtins.property
    @jsii.member(jsii_name="userType")
    def user_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userType"))

    @user_type.setter
    def user_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d93173b3d3899f8d6de15a7b497997026c12062df6e01bfcf15d99e434e94e2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.userSchema.UserSchemaArrayOneOf",
    jsii_struct_bases=[],
    name_mapping={"const": "const", "title": "title"},
)
class UserSchemaArrayOneOf:
    def __init__(self, *, const: builtins.str, title: builtins.str) -> None:
        '''
        :param const: Enum value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#const UserSchema#const}
        :param title: Enum title. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#title UserSchema#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e587a7ed2e1b0a0df41dd35ecbc111c44a8f359ca80943fe7e2d4f794f5b3095)
            check_type(argname="argument const", value=const, expected_type=type_hints["const"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "const": const,
            "title": title,
        }

    @builtins.property
    def const(self) -> builtins.str:
        '''Enum value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#const UserSchema#const}
        '''
        result = self._values.get("const")
        assert result is not None, "Required property 'const' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Enum title.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#title UserSchema#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserSchemaArrayOneOf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserSchemaArrayOneOfList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.userSchema.UserSchemaArrayOneOfList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42ced4e9b61192b34a052f817d9d32ab0e4a10d30f30268785cdf833ed7fc021)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserSchemaArrayOneOfOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076608f76e701d568b3dd2658f3185f3ab6b43f13a49dddfef744e85a6f19171)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserSchemaArrayOneOfOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cabcb6e33654a92881a853b3d77c56e8fd81dba014e1e2344aed3531e1d71bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab87bd8f972576fca04b7c736d51910aaca9da3c3f3eced052c7ee8a3807836e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e95c38defde5f09b17caa653146abb73413ad1243c1321aae6ffefe48ae3ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaArrayOneOf]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaArrayOneOf]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaArrayOneOf]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c4e1015b25553fc5f0f6349fba77f5d0d5014d3c0c64ff32ea1c40d4db1b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class UserSchemaArrayOneOfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.userSchema.UserSchemaArrayOneOfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d52f5015915ffa9518a0c2dbadec33f4d4d245179a4e081c18ee8383937cba4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b44ce6a07b0854b0019afaa98f84621896fe12d623ad849f20060e34e8538235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "const", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257083e554cd9c9a4667a72aa514aacce5763d1321a3f8527617166d4099479d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[UserSchemaArrayOneOf, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[UserSchemaArrayOneOf, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[UserSchemaArrayOneOf, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b7fa7b6cb09ff312d7cb0df7be2f291991bf8f7b52dcce8ecd08c62776b11ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.userSchema.UserSchemaConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
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
        "master_override_priority": "masterOverridePriority",
        "max_length": "maxLength",
        "min_length": "minLength",
        "one_of": "oneOf",
        "pattern": "pattern",
        "permissions": "permissions",
        "required": "required",
        "scope": "scope",
        "unique": "unique",
        "user_type": "userType",
    },
)
class UserSchemaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        index: builtins.str,
        title: builtins.str,
        type: builtins.str,
        array_enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserSchemaArrayOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
        array_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_name: typing.Optional[builtins.str] = None,
        external_namespace: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        master: typing.Optional[builtins.str] = None,
        master_override_priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["UserSchemaMasterOverridePriority", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_length: typing.Optional[jsii.Number] = None,
        min_length: typing.Optional[jsii.Number] = None,
        one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["UserSchemaOneOf", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pattern: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scope: typing.Optional[builtins.str] = None,
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
        :param index: Subschema unique string identifier. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#index UserSchema#index}
        :param title: Subschema title (display name). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#title UserSchema#title}
        :param type: Subschema type: string, boolean, number, integer, array, or object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#type UserSchema#type}
        :param array_enum: Custom Subschema enumerated value of a property of type array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#array_enum UserSchema#array_enum}
        :param array_one_of: array_one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#array_one_of UserSchema#array_one_of}
        :param array_type: Subschema array type: string, number, integer, reference. Type field must be an array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#array_type UserSchema#array_type}
        :param description: Custom Subschema description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#description UserSchema#description}
        :param enum: Custom Subschema enumerated value of the property. see: developer.okta.com/docs/api/resources/schemas#user-profile-schema-property-object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#enum UserSchema#enum}
        :param external_name: Subschema external name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#external_name UserSchema#external_name}
        :param external_namespace: Subschema external namespace. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#external_namespace UserSchema#external_namespace}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#id UserSchema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param master: SubSchema profile manager, if not set it will inherit its setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#master UserSchema#master}
        :param master_override_priority: master_override_priority block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#master_override_priority UserSchema#master_override_priority}
        :param max_length: Subschema of type string maximum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#max_length UserSchema#max_length}
        :param min_length: Subschema of type string minimum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#min_length UserSchema#min_length}
        :param one_of: one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#one_of UserSchema#one_of}
        :param pattern: The validation pattern to use for the subschema. Must be in form of '.+', or '[]+' if present.'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#pattern UserSchema#pattern}
        :param permissions: SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#permissions UserSchema#permissions}
        :param required: Whether the subschema is required. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#required UserSchema#required}
        :param scope: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#scope UserSchema#scope}.
        :param unique: Subschema unique restriction. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#unique UserSchema#unique}
        :param user_type: Custom subschema user type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#user_type UserSchema#user_type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c72fec2d180d3ad361607f0ae9ec6b55b6b84792e26e7847e745f54f9b5d064)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
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
            check_type(argname="argument master_override_priority", value=master_override_priority, expected_type=type_hints["master_override_priority"])
            check_type(argname="argument max_length", value=max_length, expected_type=type_hints["max_length"])
            check_type(argname="argument min_length", value=min_length, expected_type=type_hints["min_length"])
            check_type(argname="argument one_of", value=one_of, expected_type=type_hints["one_of"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument unique", value=unique, expected_type=type_hints["unique"])
            check_type(argname="argument user_type", value=user_type, expected_type=type_hints["user_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if master_override_priority is not None:
            self._values["master_override_priority"] = master_override_priority
        if max_length is not None:
            self._values["max_length"] = max_length
        if min_length is not None:
            self._values["min_length"] = min_length
        if one_of is not None:
            self._values["one_of"] = one_of
        if pattern is not None:
            self._values["pattern"] = pattern
        if permissions is not None:
            self._values["permissions"] = permissions
        if required is not None:
            self._values["required"] = required
        if scope is not None:
            self._values["scope"] = scope
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
    def index(self) -> builtins.str:
        '''Subschema unique string identifier.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#index UserSchema#index}
        '''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Subschema title (display name).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#title UserSchema#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Subschema type: string, boolean, number, integer, array, or object.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#type UserSchema#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def array_enum(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Custom Subschema enumerated value of a property of type array.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#array_enum UserSchema#array_enum}
        '''
        result = self._values.get("array_enum")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def array_one_of(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaArrayOneOf]]]:
        '''array_one_of block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#array_one_of UserSchema#array_one_of}
        '''
        result = self._values.get("array_one_of")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaArrayOneOf]]], result)

    @builtins.property
    def array_type(self) -> typing.Optional[builtins.str]:
        '''Subschema array type: string, number, integer, reference. Type field must be an array.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#array_type UserSchema#array_type}
        '''
        result = self._values.get("array_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Custom Subschema description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#description UserSchema#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enum(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Custom Subschema enumerated value of the property. see: developer.okta.com/docs/api/resources/schemas#user-profile-schema-property-object.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#enum UserSchema#enum}
        '''
        result = self._values.get("enum")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_name(self) -> typing.Optional[builtins.str]:
        '''Subschema external name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#external_name UserSchema#external_name}
        '''
        result = self._values.get("external_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_namespace(self) -> typing.Optional[builtins.str]:
        '''Subschema external namespace.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#external_namespace UserSchema#external_namespace}
        '''
        result = self._values.get("external_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#id UserSchema#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master(self) -> typing.Optional[builtins.str]:
        '''SubSchema profile manager, if not set it will inherit its setting.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#master UserSchema#master}
        '''
        result = self._values.get("master")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_override_priority(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserSchemaMasterOverridePriority"]]]:
        '''master_override_priority block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#master_override_priority UserSchema#master_override_priority}
        '''
        result = self._values.get("master_override_priority")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserSchemaMasterOverridePriority"]]], result)

    @builtins.property
    def max_length(self) -> typing.Optional[jsii.Number]:
        '''Subschema of type string maximum length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#max_length UserSchema#max_length}
        '''
        result = self._values.get("max_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        '''Subschema of type string minimum length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#min_length UserSchema#min_length}
        '''
        result = self._values.get("min_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def one_of(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserSchemaOneOf"]]]:
        '''one_of block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#one_of UserSchema#one_of}
        '''
        result = self._values.get("one_of")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["UserSchemaOneOf"]]], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''The validation pattern to use for the subschema. Must be in form of '.+', or '[]+' if present.'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#pattern UserSchema#pattern}
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#permissions UserSchema#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the subschema is required.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#required UserSchema#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#scope UserSchema#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unique(self) -> typing.Optional[builtins.str]:
        '''Subschema unique restriction.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#unique UserSchema#unique}
        '''
        result = self._values.get("unique")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_type(self) -> typing.Optional[builtins.str]:
        '''Custom subschema user type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#user_type UserSchema#user_type}
        '''
        result = self._values.get("user_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserSchemaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.userSchema.UserSchemaMasterOverridePriority",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "type": "type"},
)
class UserSchemaMasterOverridePriority:
    def __init__(
        self,
        *,
        value: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#value UserSchema#value}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#type UserSchema#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae01be0963ed26275d34825a4f0caae3b489f7420596f831a4e8b32710a20fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#value UserSchema#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#type UserSchema#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserSchemaMasterOverridePriority(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserSchemaMasterOverridePriorityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.userSchema.UserSchemaMasterOverridePriorityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0237e1484861423e557541f30779009787e4357b65aaf9dc5dd090548825e654)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserSchemaMasterOverridePriorityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25459cbb68f490ee2131a5e21bbc2e760fb994c29ec36a4d8fd6cf06034c1acd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserSchemaMasterOverridePriorityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f63dea98b0f1e1840b12024c1c35ae595d1ec5fd420af3c405af534610dcc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca55ee13a8ea8b51369f2bf2ea92eb914ceb4885c19f937c58942561a058ce16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b9bfe5d709544bcaf06170d0e4189dbe3ace9e3712a411affe73a151a3bc26c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaMasterOverridePriority]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaMasterOverridePriority]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaMasterOverridePriority]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37be82ffbbae6c74e2b20494ed1f975eb4048fb05a395685d2f9f4f37eab597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class UserSchemaMasterOverridePriorityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.userSchema.UserSchemaMasterOverridePriorityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bb9fd0afd08842f26f030f0690429c9ef4953361d9fa452b460a9c60feffb7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ab18a7d8e8c4e6b2ef01d8ae084ccc51e331855ce2a4fd826acea2ccc5e18e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b7a3846eeb8ddb4004f7e9af99e69b337576af75c51e74e8467e597fe80e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[UserSchemaMasterOverridePriority, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[UserSchemaMasterOverridePriority, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[UserSchemaMasterOverridePriority, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175a034125f4aebea1748a1065b69a1dc17686ba2fb0bc53bb32c0eae2a09892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.userSchema.UserSchemaOneOf",
    jsii_struct_bases=[],
    name_mapping={"const": "const", "title": "title"},
)
class UserSchemaOneOf:
    def __init__(self, *, const: builtins.str, title: builtins.str) -> None:
        '''
        :param const: Enum value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#const UserSchema#const}
        :param title: Enum title. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#title UserSchema#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f894aaa2fbe1aa2bff0cfd5ae35644ada09c99997c5f1025e4369b0da000abb1)
            check_type(argname="argument const", value=const, expected_type=type_hints["const"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "const": const,
            "title": title,
        }

    @builtins.property
    def const(self) -> builtins.str:
        '''Enum value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#const UserSchema#const}
        '''
        result = self._values.get("const")
        assert result is not None, "Required property 'const' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Enum title.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/user_schema#title UserSchema#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserSchemaOneOf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserSchemaOneOfList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.userSchema.UserSchemaOneOfList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e8f6ad2814652f92c1a5f409c2593629f62019c49b0ff552709f4f3d139113)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserSchemaOneOfOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4bd8f130cdce0d6d6061f4cf13fc390618ba6cfc38f29a83855a46b3eb7d89f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserSchemaOneOfOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e7999dd5f4a1e158bcb7315ad802792da52fe12f03a4553d1c9029ba53b7be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fdf1426a6c5e1e99d2a0018a4d7a2d366c3fd325c3fa7b5fa06ac4ec2f9223e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc518109ee4d114502d0f87eba33018bc6d8d905b879d899d23ec490d8388ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaOneOf]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaOneOf]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaOneOf]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efcbe372f0199e9c52d938bccc51f7e842899af44f10e560e1a34160dedd71ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class UserSchemaOneOfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.userSchema.UserSchemaOneOfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33ad638d60bf9dd936253335a619e95f0883dab4b444c08d0b68a5e4d02b9c4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28da1af049085fff0b82aa5f55d8fc5bfac44d06ac051fb6a628226c9c327a54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "const", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392eaad7673d290a881135408087b1905a2b40618578aeb538a9ddee0bce0e42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[UserSchemaOneOf, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[UserSchemaOneOf, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[UserSchemaOneOf, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377f34ea2c04b0c1822d98b39ff178c0912c4ccc4b06f48ae0317796e1edbbbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "UserSchema",
    "UserSchemaArrayOneOf",
    "UserSchemaArrayOneOfList",
    "UserSchemaArrayOneOfOutputReference",
    "UserSchemaConfig",
    "UserSchemaMasterOverridePriority",
    "UserSchemaMasterOverridePriorityList",
    "UserSchemaMasterOverridePriorityOutputReference",
    "UserSchemaOneOf",
    "UserSchemaOneOfList",
    "UserSchemaOneOfOutputReference",
]

publication.publish()

def _typecheckingstub__cd4d2bc14d70bb10896991f71284aff0f9fa5fbe4fc58ba6cc9e2f19db973c6b(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    index: builtins.str,
    title: builtins.str,
    type: builtins.str,
    array_enum: typing.Optional[typing.Sequence[builtins.str]] = None,
    array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserSchemaArrayOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    array_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enum: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_name: typing.Optional[builtins.str] = None,
    external_namespace: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    master: typing.Optional[builtins.str] = None,
    master_override_priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserSchemaMasterOverridePriority, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_length: typing.Optional[jsii.Number] = None,
    min_length: typing.Optional[jsii.Number] = None,
    one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserSchemaOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pattern: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scope: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__a5f7b92388e111bb31232086d26c91588c703deb7e845d41bfdb0ee766612389(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserSchemaArrayOneOf, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bbcd9848863983d9b31e7a938cea6c430829cd1c92c9dd6a7d7872d62670b2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserSchemaMasterOverridePriority, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415e0d6448978d92022f5c3e31720fea65f6e99b77830714aa8fd7f51c8eaf33(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserSchemaOneOf, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1269d37c855168d2baed40d7b7a5f7673729484a881c917dd09fd737f9bd6bdd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96d152b263f3bfd6c90965665afa9df09d83eb624b06ad55d6511b43122cd45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae36b34cf6c6c86ac278821bc773916df2c7cd4298c63d68f3db8fc633e90c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738fcba3930d3a194dc9537755e240799fafa55f6e87c22b6442ac194aecfe4c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13fb85dcf8d486640b269fdd2fc485c6d4a44e8aac1780d4569a770e5399ef3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca25fc7fdb997cd6d015a1d2b4b5412f700b7064084fc7097bcee03d4a8c3a9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e08f7ac280e1ed4f2e4f839630b62605624afe5cbbcff54fe65fc0989f2dbab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ad52b94641b093a15162780965859385b695afc933f465a476ccf1e4a543b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7886c47fe67a9847ad39b2a06f8f50ffd8a8ef498ae0776007a4370a3b6ac67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af115a9f26550af7889561883bdbab78a38b6cae095772d24a9f8c7dc0996f47(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d4f047527c39e5af24b544ff46617188c027508476412c9080dc7a54dc240c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89e7697fceb84b498634592f7eae915b9b8d371d0013bdea193a5e60f6480b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f7537f0b4cf0da3ac69f7a99e634e06f702d6c4268a1239ad7cc059c9f9341(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6276abd679ebe70f06d9174f868ef2f0f37f38faa5cd6fe82a9deb811baa7a52(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b83c00212a6e191d728d2072daa3d5c8d19438fb307048ba27aefe857df4774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42b01203c27021e5fc0aabebbbca0f61ea584ab7657dc97130c573c165b4da0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58249edb79f00b3f44476bbf9af0b291f6b1d4146d610d3d58f497c77c7b1ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c6656cba9c3d1577c18655ad0482520cc59654d271a499285af57dc92ca121(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93173b3d3899f8d6de15a7b497997026c12062df6e01bfcf15d99e434e94e2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e587a7ed2e1b0a0df41dd35ecbc111c44a8f359ca80943fe7e2d4f794f5b3095(
    *,
    const: builtins.str,
    title: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ced4e9b61192b34a052f817d9d32ab0e4a10d30f30268785cdf833ed7fc021(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076608f76e701d568b3dd2658f3185f3ab6b43f13a49dddfef744e85a6f19171(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cabcb6e33654a92881a853b3d77c56e8fd81dba014e1e2344aed3531e1d71bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab87bd8f972576fca04b7c736d51910aaca9da3c3f3eced052c7ee8a3807836e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e95c38defde5f09b17caa653146abb73413ad1243c1321aae6ffefe48ae3ba4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c4e1015b25553fc5f0f6349fba77f5d0d5014d3c0c64ff32ea1c40d4db1b0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaArrayOneOf]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d52f5015915ffa9518a0c2dbadec33f4d4d245179a4e081c18ee8383937cba4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44ce6a07b0854b0019afaa98f84621896fe12d623ad849f20060e34e8538235(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257083e554cd9c9a4667a72aa514aacce5763d1321a3f8527617166d4099479d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7fa7b6cb09ff312d7cb0df7be2f291991bf8f7b52dcce8ecd08c62776b11ac(
    value: typing.Optional[typing.Union[UserSchemaArrayOneOf, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c72fec2d180d3ad361607f0ae9ec6b55b6b84792e26e7847e745f54f9b5d064(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    index: builtins.str,
    title: builtins.str,
    type: builtins.str,
    array_enum: typing.Optional[typing.Sequence[builtins.str]] = None,
    array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserSchemaArrayOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    array_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enum: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_name: typing.Optional[builtins.str] = None,
    external_namespace: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    master: typing.Optional[builtins.str] = None,
    master_override_priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserSchemaMasterOverridePriority, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_length: typing.Optional[jsii.Number] = None,
    min_length: typing.Optional[jsii.Number] = None,
    one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[UserSchemaOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pattern: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scope: typing.Optional[builtins.str] = None,
    unique: typing.Optional[builtins.str] = None,
    user_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae01be0963ed26275d34825a4f0caae3b489f7420596f831a4e8b32710a20fe(
    *,
    value: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0237e1484861423e557541f30779009787e4357b65aaf9dc5dd090548825e654(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25459cbb68f490ee2131a5e21bbc2e760fb994c29ec36a4d8fd6cf06034c1acd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f63dea98b0f1e1840b12024c1c35ae595d1ec5fd420af3c405af534610dcc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca55ee13a8ea8b51369f2bf2ea92eb914ceb4885c19f937c58942561a058ce16(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9bfe5d709544bcaf06170d0e4189dbe3ace9e3712a411affe73a151a3bc26c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37be82ffbbae6c74e2b20494ed1f975eb4048fb05a395685d2f9f4f37eab597(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaMasterOverridePriority]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb9fd0afd08842f26f030f0690429c9ef4953361d9fa452b460a9c60feffb7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ab18a7d8e8c4e6b2ef01d8ae084ccc51e331855ce2a4fd826acea2ccc5e18e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b7a3846eeb8ddb4004f7e9af99e69b337576af75c51e74e8467e597fe80e75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175a034125f4aebea1748a1065b69a1dc17686ba2fb0bc53bb32c0eae2a09892(
    value: typing.Optional[typing.Union[UserSchemaMasterOverridePriority, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f894aaa2fbe1aa2bff0cfd5ae35644ada09c99997c5f1025e4369b0da000abb1(
    *,
    const: builtins.str,
    title: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e8f6ad2814652f92c1a5f409c2593629f62019c49b0ff552709f4f3d139113(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4bd8f130cdce0d6d6061f4cf13fc390618ba6cfc38f29a83855a46b3eb7d89f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e7999dd5f4a1e158bcb7315ad802792da52fe12f03a4553d1c9029ba53b7be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdf1426a6c5e1e99d2a0018a4d7a2d366c3fd325c3fa7b5fa06ac4ec2f9223e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc518109ee4d114502d0f87eba33018bc6d8d905b879d899d23ec490d8388ede(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efcbe372f0199e9c52d938bccc51f7e842899af44f10e560e1a34160dedd71ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[UserSchemaOneOf]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ad638d60bf9dd936253335a619e95f0883dab4b444c08d0b68a5e4d02b9c4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28da1af049085fff0b82aa5f55d8fc5bfac44d06ac051fb6a628226c9c327a54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392eaad7673d290a881135408087b1905a2b40618578aeb538a9ddee0bce0e42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377f34ea2c04b0c1822d98b39ff178c0912c4ccc4b06f48ae0317796e1edbbbc(
    value: typing.Optional[typing.Union[UserSchemaOneOf, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
