'''
# `okta_group_schema_property`

Refer to the Terraform Registory for docs: [`okta_group_schema_property`](https://www.terraform.io/docs/providers/okta/r/group_schema_property).
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


class GroupSchemaProperty(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.groupSchemaProperty.GroupSchemaProperty",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property okta_group_schema_property}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        index: builtins.str,
        title: builtins.str,
        type: builtins.str,
        array_enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupSchemaPropertyArrayOneOf", typing.Dict[builtins.str, typing.Any]]]]] = None,
        array_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_name: typing.Optional[builtins.str] = None,
        external_namespace: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        master: typing.Optional[builtins.str] = None,
        master_override_priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupSchemaPropertyMasterOverridePriority", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_length: typing.Optional[jsii.Number] = None,
        min_length: typing.Optional[jsii.Number] = None,
        one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupSchemaPropertyOneOf", typing.Dict[builtins.str, typing.Any]]]]] = None,
        permissions: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scope: typing.Optional[builtins.str] = None,
        unique: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property okta_group_schema_property} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param index: Subschema unique string identifier. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#index GroupSchemaProperty#index}
        :param title: Subschema title (display name). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#title GroupSchemaProperty#title}
        :param type: Subschema type: string, boolean, number, integer, array, or object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#type GroupSchemaProperty#type}
        :param array_enum: Custom Subschema enumerated value of a property of type array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#array_enum GroupSchemaProperty#array_enum}
        :param array_one_of: array_one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#array_one_of GroupSchemaProperty#array_one_of}
        :param array_type: Subschema array type: string, number, integer, reference. Type field must be an array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#array_type GroupSchemaProperty#array_type}
        :param description: Custom Subschema description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#description GroupSchemaProperty#description}
        :param enum: Custom Subschema enumerated value of the property. see: developer.okta.com/docs/api/resources/schemas#user-profile-schema-property-object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#enum GroupSchemaProperty#enum}
        :param external_name: Subschema external name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#external_name GroupSchemaProperty#external_name}
        :param external_namespace: Subschema external namespace. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#external_namespace GroupSchemaProperty#external_namespace}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#id GroupSchemaProperty#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param master: SubSchema profile manager, if not set it will inherit its setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#master GroupSchemaProperty#master}
        :param master_override_priority: master_override_priority block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#master_override_priority GroupSchemaProperty#master_override_priority}
        :param max_length: Subschema of type string maximum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#max_length GroupSchemaProperty#max_length}
        :param min_length: Subschema of type string minimum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#min_length GroupSchemaProperty#min_length}
        :param one_of: one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#one_of GroupSchemaProperty#one_of}
        :param permissions: SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#permissions GroupSchemaProperty#permissions}
        :param required: Whether the subschema is required. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#required GroupSchemaProperty#required}
        :param scope: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#scope GroupSchemaProperty#scope}.
        :param unique: Subschema unique restriction. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#unique GroupSchemaProperty#unique}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db885696896d373bd1f0a3dafa20bf31356b98004f3f8817976ddd1a75b02b7)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GroupSchemaPropertyConfig(
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
            permissions=permissions,
            required=required,
            scope=scope,
            unique=unique,
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupSchemaPropertyArrayOneOf", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffef050feaff7fd33396b386c60b7187b1f4b181919a62f876fb0548b650cb09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArrayOneOf", [value]))

    @jsii.member(jsii_name="putMasterOverridePriority")
    def put_master_override_priority(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupSchemaPropertyMasterOverridePriority", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234d1ee45413972a1919a45850045864bd874bc5be01b8e1c709d885c4a17ed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMasterOverridePriority", [value]))

    @jsii.member(jsii_name="putOneOf")
    def put_one_of(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupSchemaPropertyOneOf", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f216df9ffa202ff755f7178dbfeb8eea6c884b74981f4adc0c61db3f117c1e)
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

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arrayOneOf")
    def array_one_of(self) -> "GroupSchemaPropertyArrayOneOfList":
        return typing.cast("GroupSchemaPropertyArrayOneOfList", jsii.get(self, "arrayOneOf"))

    @builtins.property
    @jsii.member(jsii_name="masterOverridePriority")
    def master_override_priority(
        self,
    ) -> "GroupSchemaPropertyMasterOverridePriorityList":
        return typing.cast("GroupSchemaPropertyMasterOverridePriorityList", jsii.get(self, "masterOverridePriority"))

    @builtins.property
    @jsii.member(jsii_name="oneOf")
    def one_of(self) -> "GroupSchemaPropertyOneOfList":
        return typing.cast("GroupSchemaPropertyOneOfList", jsii.get(self, "oneOf"))

    @builtins.property
    @jsii.member(jsii_name="arrayEnumInput")
    def array_enum_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "arrayEnumInput"))

    @builtins.property
    @jsii.member(jsii_name="arrayOneOfInput")
    def array_one_of_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupSchemaPropertyArrayOneOf"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupSchemaPropertyArrayOneOf"]]], jsii.get(self, "arrayOneOfInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupSchemaPropertyMasterOverridePriority"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupSchemaPropertyMasterOverridePriority"]]], jsii.get(self, "masterOverridePriorityInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupSchemaPropertyOneOf"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupSchemaPropertyOneOf"]]], jsii.get(self, "oneOfInput"))

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
    @jsii.member(jsii_name="arrayEnum")
    def array_enum(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "arrayEnum"))

    @array_enum.setter
    def array_enum(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed919e95e7a8e8177c50f9e275fe303386640d3f6ba0bea10b0137251d2db77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arrayEnum", value)

    @builtins.property
    @jsii.member(jsii_name="arrayType")
    def array_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arrayType"))

    @array_type.setter
    def array_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b1f54f24c6c89d4427fed82d2034ae0e3ae9016955ab3bd54c4bd55e94b903d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arrayType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff5e123d4b22fb64dcd0482e751ca1d51526cddc7e4b6c9d19427db27c67f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enum")
    def enum(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enum"))

    @enum.setter
    def enum(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267e586f9e423aad2c2ff655eadb79db428c7a49c3e6f40de817332a53b537e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enum", value)

    @builtins.property
    @jsii.member(jsii_name="externalName")
    def external_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalName"))

    @external_name.setter
    def external_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd00286b78e2c0bb6770b2d9a3f29d71a0cae7a27a346b2f1dceebd662725cfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalName", value)

    @builtins.property
    @jsii.member(jsii_name="externalNamespace")
    def external_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalNamespace"))

    @external_namespace.setter
    def external_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae3a66e920b29705d125718fde323994d476a91e17171883b15f8fe6a1f51af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalNamespace", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861d4c807de8a733f2b1f20cae0689729b6242acb68453139698c245666dd1cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69240ee3f9a674e862b90f59e24acfdbc2a96e0295b9bbdd74a96ff86625fcc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value)

    @builtins.property
    @jsii.member(jsii_name="master")
    def master(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "master"))

    @master.setter
    def master(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff7907a5f4ba116a23dfe3ea624784d11baf4dd07a54883ecd567a94836cf78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "master", value)

    @builtins.property
    @jsii.member(jsii_name="maxLength")
    def max_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLength"))

    @max_length.setter
    def max_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7eab827837225e0a43c4cb8dd79969692af40cf156c0c755c6a6ff23f4b1c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLength", value)

    @builtins.property
    @jsii.member(jsii_name="minLength")
    def min_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLength"))

    @min_length.setter
    def min_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ed69ee8cd9ab9c51fe98143a3687c1440f82c60b0ead601cd1b078f466aa21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLength", value)

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267a7bd8d0bd784a2ddc3d9461a2a57b83183ae694d4f1f22341fe53895ec29e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7769a8d7502f5fe0aa6972998320d7a8763969599e18506644bbb3f98bcdc268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb4672993af86ddd64a8571009c8cf8b3042c41052e0ad46ce50323e109fd17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271212446cbfcff6a1b8c1e12f65fe0c541d143608b982b93b8a581f3e5b0592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31f6515d0e885f9fe140f42751774f9905c659fbd6531f9076d8547eacde0f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="unique")
    def unique(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unique"))

    @unique.setter
    def unique(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9d7d25ef68f08e7e05bc2ff5814b7dadfcfe4dd8476da99ec98e0047f4cfb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unique", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.groupSchemaProperty.GroupSchemaPropertyArrayOneOf",
    jsii_struct_bases=[],
    name_mapping={"const": "const", "title": "title"},
)
class GroupSchemaPropertyArrayOneOf:
    def __init__(self, *, const: builtins.str, title: builtins.str) -> None:
        '''
        :param const: Enum value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#const GroupSchemaProperty#const}
        :param title: Enum title. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#title GroupSchemaProperty#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01bf05f4c2ff702c5d0560d7818d6c38476d0dc5796e67e816813b10f20a37da)
            check_type(argname="argument const", value=const, expected_type=type_hints["const"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "const": const,
            "title": title,
        }

    @builtins.property
    def const(self) -> builtins.str:
        '''Enum value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#const GroupSchemaProperty#const}
        '''
        result = self._values.get("const")
        assert result is not None, "Required property 'const' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Enum title.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#title GroupSchemaProperty#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupSchemaPropertyArrayOneOf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupSchemaPropertyArrayOneOfList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.groupSchemaProperty.GroupSchemaPropertyArrayOneOfList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__836d415ba36b5e6bf6d291a747b443d4ae4ba62bb1b6a397cd7e8f303513d34e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GroupSchemaPropertyArrayOneOfOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb0901b61a698c827d30c934d4d51e1b49108ae48a61cbb043750743b3f4c3a0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GroupSchemaPropertyArrayOneOfOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9851bd3cde3a5d1f4ffe62e9daeac7dcfc2cb465b0a3a33d00300c26c3b7d652)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9d96041341bdfd057a47a55f0482a4ec566dfb8fef4bc42b33e71c0fa256df0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1020598695d50b48a03669f65bf5ca91395b87400a282dafcca85b254de7fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyArrayOneOf]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyArrayOneOf]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyArrayOneOf]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18086adaff1d9935121411d605193b8a4b88c7bbd91892d33a7c9fcf831a7d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GroupSchemaPropertyArrayOneOfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.groupSchemaProperty.GroupSchemaPropertyArrayOneOfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c540cbf43ebc7b25136ee9f612b4b80a9a5e3c54839a4001f965cdf0e490ca25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07a1a47d8840c2e54b21748a0d20742ed0a7148a8b33d15f3077fac60f5d1ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "const", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f837451c019c40dfecc3d1cdb9f9ddd00e29a99cf3a85b3e7754756ebaf65da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GroupSchemaPropertyArrayOneOf, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GroupSchemaPropertyArrayOneOf, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GroupSchemaPropertyArrayOneOf, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e9dafaa4055dc0140ade41a8ee1eb1980af32eace2c9597cdf89a666a9bac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.groupSchemaProperty.GroupSchemaPropertyConfig",
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
        "permissions": "permissions",
        "required": "required",
        "scope": "scope",
        "unique": "unique",
    },
)
class GroupSchemaPropertyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupSchemaPropertyArrayOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
        array_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_name: typing.Optional[builtins.str] = None,
        external_namespace: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        master: typing.Optional[builtins.str] = None,
        master_override_priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupSchemaPropertyMasterOverridePriority", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_length: typing.Optional[jsii.Number] = None,
        min_length: typing.Optional[jsii.Number] = None,
        one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupSchemaPropertyOneOf", typing.Dict[builtins.str, typing.Any]]]]] = None,
        permissions: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scope: typing.Optional[builtins.str] = None,
        unique: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param index: Subschema unique string identifier. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#index GroupSchemaProperty#index}
        :param title: Subschema title (display name). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#title GroupSchemaProperty#title}
        :param type: Subschema type: string, boolean, number, integer, array, or object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#type GroupSchemaProperty#type}
        :param array_enum: Custom Subschema enumerated value of a property of type array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#array_enum GroupSchemaProperty#array_enum}
        :param array_one_of: array_one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#array_one_of GroupSchemaProperty#array_one_of}
        :param array_type: Subschema array type: string, number, integer, reference. Type field must be an array. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#array_type GroupSchemaProperty#array_type}
        :param description: Custom Subschema description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#description GroupSchemaProperty#description}
        :param enum: Custom Subschema enumerated value of the property. see: developer.okta.com/docs/api/resources/schemas#user-profile-schema-property-object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#enum GroupSchemaProperty#enum}
        :param external_name: Subschema external name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#external_name GroupSchemaProperty#external_name}
        :param external_namespace: Subschema external namespace. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#external_namespace GroupSchemaProperty#external_namespace}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#id GroupSchemaProperty#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param master: SubSchema profile manager, if not set it will inherit its setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#master GroupSchemaProperty#master}
        :param master_override_priority: master_override_priority block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#master_override_priority GroupSchemaProperty#master_override_priority}
        :param max_length: Subschema of type string maximum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#max_length GroupSchemaProperty#max_length}
        :param min_length: Subschema of type string minimum length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#min_length GroupSchemaProperty#min_length}
        :param one_of: one_of block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#one_of GroupSchemaProperty#one_of}
        :param permissions: SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#permissions GroupSchemaProperty#permissions}
        :param required: Whether the subschema is required. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#required GroupSchemaProperty#required}
        :param scope: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#scope GroupSchemaProperty#scope}.
        :param unique: Subschema unique restriction. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#unique GroupSchemaProperty#unique}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc395cb9a2ecdc4ef3f7db3852c20e93c00d8a7d2477b005f057bf91fad5b34)
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
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument unique", value=unique, expected_type=type_hints["unique"])
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
        if permissions is not None:
            self._values["permissions"] = permissions
        if required is not None:
            self._values["required"] = required
        if scope is not None:
            self._values["scope"] = scope
        if unique is not None:
            self._values["unique"] = unique

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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#index GroupSchemaProperty#index}
        '''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Subschema title (display name).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#title GroupSchemaProperty#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Subschema type: string, boolean, number, integer, array, or object.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#type GroupSchemaProperty#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def array_enum(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Custom Subschema enumerated value of a property of type array.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#array_enum GroupSchemaProperty#array_enum}
        '''
        result = self._values.get("array_enum")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def array_one_of(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyArrayOneOf]]]:
        '''array_one_of block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#array_one_of GroupSchemaProperty#array_one_of}
        '''
        result = self._values.get("array_one_of")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyArrayOneOf]]], result)

    @builtins.property
    def array_type(self) -> typing.Optional[builtins.str]:
        '''Subschema array type: string, number, integer, reference. Type field must be an array.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#array_type GroupSchemaProperty#array_type}
        '''
        result = self._values.get("array_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Custom Subschema description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#description GroupSchemaProperty#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enum(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Custom Subschema enumerated value of the property. see: developer.okta.com/docs/api/resources/schemas#user-profile-schema-property-object.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#enum GroupSchemaProperty#enum}
        '''
        result = self._values.get("enum")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_name(self) -> typing.Optional[builtins.str]:
        '''Subschema external name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#external_name GroupSchemaProperty#external_name}
        '''
        result = self._values.get("external_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_namespace(self) -> typing.Optional[builtins.str]:
        '''Subschema external namespace.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#external_namespace GroupSchemaProperty#external_namespace}
        '''
        result = self._values.get("external_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#id GroupSchemaProperty#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master(self) -> typing.Optional[builtins.str]:
        '''SubSchema profile manager, if not set it will inherit its setting.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#master GroupSchemaProperty#master}
        '''
        result = self._values.get("master")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_override_priority(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupSchemaPropertyMasterOverridePriority"]]]:
        '''master_override_priority block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#master_override_priority GroupSchemaProperty#master_override_priority}
        '''
        result = self._values.get("master_override_priority")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupSchemaPropertyMasterOverridePriority"]]], result)

    @builtins.property
    def max_length(self) -> typing.Optional[jsii.Number]:
        '''Subschema of type string maximum length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#max_length GroupSchemaProperty#max_length}
        '''
        result = self._values.get("max_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        '''Subschema of type string minimum length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#min_length GroupSchemaProperty#min_length}
        '''
        result = self._values.get("min_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def one_of(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupSchemaPropertyOneOf"]]]:
        '''one_of block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#one_of GroupSchemaProperty#one_of}
        '''
        result = self._values.get("one_of")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupSchemaPropertyOneOf"]]], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''SubSchema permissions: HIDE, READ_ONLY, or READ_WRITE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#permissions GroupSchemaProperty#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the subschema is required.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#required GroupSchemaProperty#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#scope GroupSchemaProperty#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unique(self) -> typing.Optional[builtins.str]:
        '''Subschema unique restriction.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#unique GroupSchemaProperty#unique}
        '''
        result = self._values.get("unique")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupSchemaPropertyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.groupSchemaProperty.GroupSchemaPropertyMasterOverridePriority",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "type": "type"},
)
class GroupSchemaPropertyMasterOverridePriority:
    def __init__(
        self,
        *,
        value: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#value GroupSchemaProperty#value}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#type GroupSchemaProperty#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0323d3dc83da1da90e973ccdcd9ca8232063d294d3c2bcdec1e678d47af52067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#value GroupSchemaProperty#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#type GroupSchemaProperty#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupSchemaPropertyMasterOverridePriority(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupSchemaPropertyMasterOverridePriorityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.groupSchemaProperty.GroupSchemaPropertyMasterOverridePriorityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cb0a02946c459ca3a79e7625cca9f2f68fe868beb1ab5efca1042203d37c93c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GroupSchemaPropertyMasterOverridePriorityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b70a086c759313af01e289abf891103fa21a02c4f0c4606a7f0330b61f9b66f6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GroupSchemaPropertyMasterOverridePriorityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a5846a180735267bdad4d6a442c4afb9a4a325cdf9c1366fb45619cffc6e62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__661d683b01964bbf069c3f3bbf420fc00c3ce5dae393d5c711593a19c972c4be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3472032d4cb9b09915221c6a4373f65ed1257bbd242b186ae95f33a00bf663d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyMasterOverridePriority]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyMasterOverridePriority]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyMasterOverridePriority]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b7b38a007c4d05e6cac872543e3cb599ecf65c784eaa24b565e27421dd73762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GroupSchemaPropertyMasterOverridePriorityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.groupSchemaProperty.GroupSchemaPropertyMasterOverridePriorityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21c5895f17806cc488750a3e2ea404c0730e168961e75440e71ddb03d0e6df0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f55c77b88da76bdd8cb72e5736e2e9baf49b517c248434b0b44bf994b48da25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb891670e840fc87448562dd83f64804f0afe5563d681409ce3b7474ae5978e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GroupSchemaPropertyMasterOverridePriority, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GroupSchemaPropertyMasterOverridePriority, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GroupSchemaPropertyMasterOverridePriority, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc9f6b1baacd756e53ab295a0c5340da7ca8d019e9c6de59aa840e78cda9a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.groupSchemaProperty.GroupSchemaPropertyOneOf",
    jsii_struct_bases=[],
    name_mapping={"const": "const", "title": "title"},
)
class GroupSchemaPropertyOneOf:
    def __init__(self, *, const: builtins.str, title: builtins.str) -> None:
        '''
        :param const: Enum value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#const GroupSchemaProperty#const}
        :param title: Enum title. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#title GroupSchemaProperty#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24dd6b63ea0f0b2cd595bac1e691ec69044c47446750689e04a3141f9168984)
            check_type(argname="argument const", value=const, expected_type=type_hints["const"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "const": const,
            "title": title,
        }

    @builtins.property
    def const(self) -> builtins.str:
        '''Enum value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#const GroupSchemaProperty#const}
        '''
        result = self._values.get("const")
        assert result is not None, "Required property 'const' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Enum title.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_schema_property#title GroupSchemaProperty#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupSchemaPropertyOneOf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupSchemaPropertyOneOfList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.groupSchemaProperty.GroupSchemaPropertyOneOfList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0c40243d7779c5a79e63e834baf3200ef491f0b283c57357dbb86036358e69d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GroupSchemaPropertyOneOfOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d23371771041e143d7c0adcfc0bc5aee5ead58baab22bf1f49a3a5b6442a63d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GroupSchemaPropertyOneOfOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce53a138e57100bf18b3d7e096e296561e24050b6b44227fbc02c9188e5436fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52158f8dbe5834a230e35d2e6c9775e462cc927514507cfb84550c4703ca4e15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87a5a6320f6e9e7bc3720cd14d97825ef599fe0557068f83a9235e10c2e47f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyOneOf]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyOneOf]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyOneOf]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e343b7cfd3f225e720907e0a4ac47af068face3dcce58d8ea79d8f783c9092c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GroupSchemaPropertyOneOfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.groupSchemaProperty.GroupSchemaPropertyOneOfOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dee0cb5db6e6684b32d7c8c0c38083bae6b59479642487327e8363a397b5a8dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2ee2fb48feac2efd38a0ac891787c14e5c9febd6ee844842de48f906c4b977b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "const", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2546f2cc2b729b0ff7116c8fe2862c1c8db34a81998d49350000ca1c99bf2063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GroupSchemaPropertyOneOf, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GroupSchemaPropertyOneOf, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GroupSchemaPropertyOneOf, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e04b4bea60a2c28b3c0367a2b4caddc160558066e6cd6a1941fe3cbfa63b099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GroupSchemaProperty",
    "GroupSchemaPropertyArrayOneOf",
    "GroupSchemaPropertyArrayOneOfList",
    "GroupSchemaPropertyArrayOneOfOutputReference",
    "GroupSchemaPropertyConfig",
    "GroupSchemaPropertyMasterOverridePriority",
    "GroupSchemaPropertyMasterOverridePriorityList",
    "GroupSchemaPropertyMasterOverridePriorityOutputReference",
    "GroupSchemaPropertyOneOf",
    "GroupSchemaPropertyOneOfList",
    "GroupSchemaPropertyOneOfOutputReference",
]

publication.publish()

def _typecheckingstub__8db885696896d373bd1f0a3dafa20bf31356b98004f3f8817976ddd1a75b02b7(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    index: builtins.str,
    title: builtins.str,
    type: builtins.str,
    array_enum: typing.Optional[typing.Sequence[builtins.str]] = None,
    array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupSchemaPropertyArrayOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    array_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enum: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_name: typing.Optional[builtins.str] = None,
    external_namespace: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    master: typing.Optional[builtins.str] = None,
    master_override_priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupSchemaPropertyMasterOverridePriority, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_length: typing.Optional[jsii.Number] = None,
    min_length: typing.Optional[jsii.Number] = None,
    one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupSchemaPropertyOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    permissions: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scope: typing.Optional[builtins.str] = None,
    unique: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ffef050feaff7fd33396b386c60b7187b1f4b181919a62f876fb0548b650cb09(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupSchemaPropertyArrayOneOf, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234d1ee45413972a1919a45850045864bd874bc5be01b8e1c709d885c4a17ed3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupSchemaPropertyMasterOverridePriority, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f216df9ffa202ff755f7178dbfeb8eea6c884b74981f4adc0c61db3f117c1e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupSchemaPropertyOneOf, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed919e95e7a8e8177c50f9e275fe303386640d3f6ba0bea10b0137251d2db77b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1f54f24c6c89d4427fed82d2034ae0e3ae9016955ab3bd54c4bd55e94b903d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff5e123d4b22fb64dcd0482e751ca1d51526cddc7e4b6c9d19427db27c67f42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267e586f9e423aad2c2ff655eadb79db428c7a49c3e6f40de817332a53b537e0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd00286b78e2c0bb6770b2d9a3f29d71a0cae7a27a346b2f1dceebd662725cfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae3a66e920b29705d125718fde323994d476a91e17171883b15f8fe6a1f51af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861d4c807de8a733f2b1f20cae0689729b6242acb68453139698c245666dd1cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69240ee3f9a674e862b90f59e24acfdbc2a96e0295b9bbdd74a96ff86625fcc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff7907a5f4ba116a23dfe3ea624784d11baf4dd07a54883ecd567a94836cf78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7eab827837225e0a43c4cb8dd79969692af40cf156c0c755c6a6ff23f4b1c15(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ed69ee8cd9ab9c51fe98143a3687c1440f82c60b0ead601cd1b078f466aa21(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267a7bd8d0bd784a2ddc3d9461a2a57b83183ae694d4f1f22341fe53895ec29e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7769a8d7502f5fe0aa6972998320d7a8763969599e18506644bbb3f98bcdc268(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb4672993af86ddd64a8571009c8cf8b3042c41052e0ad46ce50323e109fd17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271212446cbfcff6a1b8c1e12f65fe0c541d143608b982b93b8a581f3e5b0592(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31f6515d0e885f9fe140f42751774f9905c659fbd6531f9076d8547eacde0f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9d7d25ef68f08e7e05bc2ff5814b7dadfcfe4dd8476da99ec98e0047f4cfb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01bf05f4c2ff702c5d0560d7818d6c38476d0dc5796e67e816813b10f20a37da(
    *,
    const: builtins.str,
    title: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836d415ba36b5e6bf6d291a747b443d4ae4ba62bb1b6a397cd7e8f303513d34e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0901b61a698c827d30c934d4d51e1b49108ae48a61cbb043750743b3f4c3a0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9851bd3cde3a5d1f4ffe62e9daeac7dcfc2cb465b0a3a33d00300c26c3b7d652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d96041341bdfd057a47a55f0482a4ec566dfb8fef4bc42b33e71c0fa256df0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1020598695d50b48a03669f65bf5ca91395b87400a282dafcca85b254de7fe3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18086adaff1d9935121411d605193b8a4b88c7bbd91892d33a7c9fcf831a7d10(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyArrayOneOf]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c540cbf43ebc7b25136ee9f612b4b80a9a5e3c54839a4001f965cdf0e490ca25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a1a47d8840c2e54b21748a0d20742ed0a7148a8b33d15f3077fac60f5d1ce0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f837451c019c40dfecc3d1cdb9f9ddd00e29a99cf3a85b3e7754756ebaf65da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e9dafaa4055dc0140ade41a8ee1eb1980af32eace2c9597cdf89a666a9bac7(
    value: typing.Optional[typing.Union[GroupSchemaPropertyArrayOneOf, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc395cb9a2ecdc4ef3f7db3852c20e93c00d8a7d2477b005f057bf91fad5b34(
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
    array_one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupSchemaPropertyArrayOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    array_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enum: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_name: typing.Optional[builtins.str] = None,
    external_namespace: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    master: typing.Optional[builtins.str] = None,
    master_override_priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupSchemaPropertyMasterOverridePriority, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_length: typing.Optional[jsii.Number] = None,
    min_length: typing.Optional[jsii.Number] = None,
    one_of: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupSchemaPropertyOneOf, typing.Dict[builtins.str, typing.Any]]]]] = None,
    permissions: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scope: typing.Optional[builtins.str] = None,
    unique: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0323d3dc83da1da90e973ccdcd9ca8232063d294d3c2bcdec1e678d47af52067(
    *,
    value: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb0a02946c459ca3a79e7625cca9f2f68fe868beb1ab5efca1042203d37c93c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70a086c759313af01e289abf891103fa21a02c4f0c4606a7f0330b61f9b66f6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a5846a180735267bdad4d6a442c4afb9a4a325cdf9c1366fb45619cffc6e62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661d683b01964bbf069c3f3bbf420fc00c3ce5dae393d5c711593a19c972c4be(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3472032d4cb9b09915221c6a4373f65ed1257bbd242b186ae95f33a00bf663d4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7b38a007c4d05e6cac872543e3cb599ecf65c784eaa24b565e27421dd73762(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyMasterOverridePriority]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c5895f17806cc488750a3e2ea404c0730e168961e75440e71ddb03d0e6df0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f55c77b88da76bdd8cb72e5736e2e9baf49b517c248434b0b44bf994b48da25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb891670e840fc87448562dd83f64804f0afe5563d681409ce3b7474ae5978e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc9f6b1baacd756e53ab295a0c5340da7ca8d019e9c6de59aa840e78cda9a1a(
    value: typing.Optional[typing.Union[GroupSchemaPropertyMasterOverridePriority, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24dd6b63ea0f0b2cd595bac1e691ec69044c47446750689e04a3141f9168984(
    *,
    const: builtins.str,
    title: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c40243d7779c5a79e63e834baf3200ef491f0b283c57357dbb86036358e69d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d23371771041e143d7c0adcfc0bc5aee5ead58baab22bf1f49a3a5b6442a63d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce53a138e57100bf18b3d7e096e296561e24050b6b44227fbc02c9188e5436fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52158f8dbe5834a230e35d2e6c9775e462cc927514507cfb84550c4703ca4e15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a5a6320f6e9e7bc3720cd14d97825ef599fe0557068f83a9235e10c2e47f63(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e343b7cfd3f225e720907e0a4ac47af068face3dcce58d8ea79d8f783c9092c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupSchemaPropertyOneOf]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee0cb5db6e6684b32d7c8c0c38083bae6b59479642487327e8363a397b5a8dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ee2fb48feac2efd38a0ac891787c14e5c9febd6ee844842de48f906c4b977b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2546f2cc2b729b0ff7116c8fe2862c1c8db34a81998d49350000ca1c99bf2063(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e04b4bea60a2c28b3c0367a2b4caddc160558066e6cd6a1941fe3cbfa63b099(
    value: typing.Optional[typing.Union[GroupSchemaPropertyOneOf, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
