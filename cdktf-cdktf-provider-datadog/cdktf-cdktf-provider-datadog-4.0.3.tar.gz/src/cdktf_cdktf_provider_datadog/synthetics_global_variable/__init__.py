'''
# `datadog_synthetics_global_variable`

Refer to the Terraform Registory for docs: [`datadog_synthetics_global_variable`](https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable).
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


class SyntheticsGlobalVariable(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariable",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable datadog_synthetics_global_variable}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        value: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        parse_test_id: typing.Optional[builtins.str] = None,
        parse_test_options: typing.Optional[typing.Union["SyntheticsGlobalVariableParseTestOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable datadog_synthetics_global_variable} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Synthetics global variable name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#name SyntheticsGlobalVariable#name}
        :param value: The value of the global variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#value SyntheticsGlobalVariable#value}
        :param description: Description of the global variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#description SyntheticsGlobalVariable#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#id SyntheticsGlobalVariable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parse_test_id: Id of the Synthetics test to use for a variable from test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#parse_test_id SyntheticsGlobalVariable#parse_test_id}
        :param parse_test_options: parse_test_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#parse_test_options SyntheticsGlobalVariable#parse_test_options}
        :param restricted_roles: A list of role identifiers to associate with the Synthetics global variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#restricted_roles SyntheticsGlobalVariable#restricted_roles}
        :param secure: If set to true, the value of the global variable is hidden. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#secure SyntheticsGlobalVariable#secure}
        :param tags: A list of tags to associate with your synthetics global variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#tags SyntheticsGlobalVariable#tags}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8130ffd11a0e21ba65645d2942d6d24827dd309902720b48e6aa8bb09898234a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SyntheticsGlobalVariableConfig(
            name=name,
            value=value,
            description=description,
            id=id,
            parse_test_id=parse_test_id,
            parse_test_options=parse_test_options,
            restricted_roles=restricted_roles,
            secure=secure,
            tags=tags,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putParseTestOptions")
    def put_parse_test_options(
        self,
        *,
        type: builtins.str,
        field: typing.Optional[builtins.str] = None,
        local_variable_name: typing.Optional[builtins.str] = None,
        parser: typing.Optional[typing.Union["SyntheticsGlobalVariableParseTestOptionsParser", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Defines the source to use to extract the value. Valid values are ``http_body``, ``http_header``, ``local_variable``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#type SyntheticsGlobalVariable#type}
        :param field: Required when type = ``http_header``. Defines the header to use to extract the value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#field SyntheticsGlobalVariable#field}
        :param local_variable_name: When type is ``local_variable``, name of the local variable to use to extract the value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#local_variable_name SyntheticsGlobalVariable#local_variable_name}
        :param parser: parser block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#parser SyntheticsGlobalVariable#parser}
        '''
        value = SyntheticsGlobalVariableParseTestOptions(
            type=type,
            field=field,
            local_variable_name=local_variable_name,
            parser=parser,
        )

        return typing.cast(None, jsii.invoke(self, "putParseTestOptions", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetParseTestId")
    def reset_parse_test_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseTestId", []))

    @jsii.member(jsii_name="resetParseTestOptions")
    def reset_parse_test_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseTestOptions", []))

    @jsii.member(jsii_name="resetRestrictedRoles")
    def reset_restricted_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedRoles", []))

    @jsii.member(jsii_name="resetSecure")
    def reset_secure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecure", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="parseTestOptions")
    def parse_test_options(
        self,
    ) -> "SyntheticsGlobalVariableParseTestOptionsOutputReference":
        return typing.cast("SyntheticsGlobalVariableParseTestOptionsOutputReference", jsii.get(self, "parseTestOptions"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parseTestIdInput")
    def parse_test_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parseTestIdInput"))

    @builtins.property
    @jsii.member(jsii_name="parseTestOptionsInput")
    def parse_test_options_input(
        self,
    ) -> typing.Optional["SyntheticsGlobalVariableParseTestOptions"]:
        return typing.cast(typing.Optional["SyntheticsGlobalVariableParseTestOptions"], jsii.get(self, "parseTestOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedRolesInput")
    def restricted_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="secureInput")
    def secure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secureInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5788193d85c608e53229844e5d474d6e97671a3940f445d70fab418f64b97f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee281aba529a743bf87bc0dded4f6e58d24568b8a45c3a6e453411c2cfda6f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8db3cbcbc12a692c9b8cab94ba6b62216d49b6ba4890ea3dec5bfa6930e5215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="parseTestId")
    def parse_test_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parseTestId"))

    @parse_test_id.setter
    def parse_test_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a18607594b6da1ebaefc8ea8de385f4b5316de535be739bb45a0bc0a2e4e92a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parseTestId", value)

    @builtins.property
    @jsii.member(jsii_name="restrictedRoles")
    def restricted_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedRoles"))

    @restricted_roles.setter
    def restricted_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e791098824659489ff80e0e78f970432bc4199c9faa83ce76ec52776c7a803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="secure")
    def secure(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secure"))

    @secure.setter
    def secure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a40ce9bc785d30740d27aab35e01f9767684fb47d64e4741a0dba881efbfa36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secure", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a521fa7e1d9afa8e6d7062b6f1f25b1380ff83e25d6cab06040e1aaf3dc10b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4ab1a6261c0a0805944bb08aa51411a235c7968e7a04fa2e3bffb62ad10ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableConfig",
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
        "value": "value",
        "description": "description",
        "id": "id",
        "parse_test_id": "parseTestId",
        "parse_test_options": "parseTestOptions",
        "restricted_roles": "restrictedRoles",
        "secure": "secure",
        "tags": "tags",
    },
)
class SyntheticsGlobalVariableConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        value: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        parse_test_id: typing.Optional[builtins.str] = None,
        parse_test_options: typing.Optional[typing.Union["SyntheticsGlobalVariableParseTestOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Synthetics global variable name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#name SyntheticsGlobalVariable#name}
        :param value: The value of the global variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#value SyntheticsGlobalVariable#value}
        :param description: Description of the global variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#description SyntheticsGlobalVariable#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#id SyntheticsGlobalVariable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parse_test_id: Id of the Synthetics test to use for a variable from test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#parse_test_id SyntheticsGlobalVariable#parse_test_id}
        :param parse_test_options: parse_test_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#parse_test_options SyntheticsGlobalVariable#parse_test_options}
        :param restricted_roles: A list of role identifiers to associate with the Synthetics global variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#restricted_roles SyntheticsGlobalVariable#restricted_roles}
        :param secure: If set to true, the value of the global variable is hidden. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#secure SyntheticsGlobalVariable#secure}
        :param tags: A list of tags to associate with your synthetics global variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#tags SyntheticsGlobalVariable#tags}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(parse_test_options, dict):
            parse_test_options = SyntheticsGlobalVariableParseTestOptions(**parse_test_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcfac2b6f5d731f178d31b130a243e4236cc921180c897ee746b90bd6be142b0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parse_test_id", value=parse_test_id, expected_type=type_hints["parse_test_id"])
            check_type(argname="argument parse_test_options", value=parse_test_options, expected_type=type_hints["parse_test_options"])
            check_type(argname="argument restricted_roles", value=restricted_roles, expected_type=type_hints["restricted_roles"])
            check_type(argname="argument secure", value=secure, expected_type=type_hints["secure"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if parse_test_id is not None:
            self._values["parse_test_id"] = parse_test_id
        if parse_test_options is not None:
            self._values["parse_test_options"] = parse_test_options
        if restricted_roles is not None:
            self._values["restricted_roles"] = restricted_roles
        if secure is not None:
            self._values["secure"] = secure
        if tags is not None:
            self._values["tags"] = tags

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
        '''Synthetics global variable name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#name SyntheticsGlobalVariable#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the global variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#value SyntheticsGlobalVariable#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the global variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#description SyntheticsGlobalVariable#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#id SyntheticsGlobalVariable#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parse_test_id(self) -> typing.Optional[builtins.str]:
        '''Id of the Synthetics test to use for a variable from test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#parse_test_id SyntheticsGlobalVariable#parse_test_id}
        '''
        result = self._values.get("parse_test_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parse_test_options(
        self,
    ) -> typing.Optional["SyntheticsGlobalVariableParseTestOptions"]:
        '''parse_test_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#parse_test_options SyntheticsGlobalVariable#parse_test_options}
        '''
        result = self._values.get("parse_test_options")
        return typing.cast(typing.Optional["SyntheticsGlobalVariableParseTestOptions"], result)

    @builtins.property
    def restricted_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of role identifiers to associate with the Synthetics global variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#restricted_roles SyntheticsGlobalVariable#restricted_roles}
        '''
        result = self._values.get("restricted_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the value of the global variable is hidden. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#secure SyntheticsGlobalVariable#secure}
        '''
        result = self._values.get("secure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tags to associate with your synthetics global variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#tags SyntheticsGlobalVariable#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsGlobalVariableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableParseTestOptions",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "field": "field",
        "local_variable_name": "localVariableName",
        "parser": "parser",
    },
)
class SyntheticsGlobalVariableParseTestOptions:
    def __init__(
        self,
        *,
        type: builtins.str,
        field: typing.Optional[builtins.str] = None,
        local_variable_name: typing.Optional[builtins.str] = None,
        parser: typing.Optional[typing.Union["SyntheticsGlobalVariableParseTestOptionsParser", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Defines the source to use to extract the value. Valid values are ``http_body``, ``http_header``, ``local_variable``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#type SyntheticsGlobalVariable#type}
        :param field: Required when type = ``http_header``. Defines the header to use to extract the value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#field SyntheticsGlobalVariable#field}
        :param local_variable_name: When type is ``local_variable``, name of the local variable to use to extract the value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#local_variable_name SyntheticsGlobalVariable#local_variable_name}
        :param parser: parser block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#parser SyntheticsGlobalVariable#parser}
        '''
        if isinstance(parser, dict):
            parser = SyntheticsGlobalVariableParseTestOptionsParser(**parser)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c891479c2ff58d4c7ee95c32ffb1c6e8113a005dc333ae5da8f69c0969c47b60)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument local_variable_name", value=local_variable_name, expected_type=type_hints["local_variable_name"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if field is not None:
            self._values["field"] = field
        if local_variable_name is not None:
            self._values["local_variable_name"] = local_variable_name
        if parser is not None:
            self._values["parser"] = parser

    @builtins.property
    def type(self) -> builtins.str:
        '''Defines the source to use to extract the value. Valid values are ``http_body``, ``http_header``, ``local_variable``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#type SyntheticsGlobalVariable#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def field(self) -> typing.Optional[builtins.str]:
        '''Required when type = ``http_header``. Defines the header to use to extract the value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#field SyntheticsGlobalVariable#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_variable_name(self) -> typing.Optional[builtins.str]:
        '''When type is ``local_variable``, name of the local variable to use to extract the value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#local_variable_name SyntheticsGlobalVariable#local_variable_name}
        '''
        result = self._values.get("local_variable_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parser(
        self,
    ) -> typing.Optional["SyntheticsGlobalVariableParseTestOptionsParser"]:
        '''parser block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#parser SyntheticsGlobalVariable#parser}
        '''
        result = self._values.get("parser")
        return typing.cast(typing.Optional["SyntheticsGlobalVariableParseTestOptionsParser"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsGlobalVariableParseTestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsGlobalVariableParseTestOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableParseTestOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49e304cd61031eb012f85dc389d715dab5646e5be0fc1b52a4098852c058b886)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putParser")
    def put_parser(
        self,
        *,
        type: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of parser to extract the value. Valid values are ``raw``, ``json_path``, ``regex``, ``x_path``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#type SyntheticsGlobalVariable#type}
        :param value: Value for the parser to use, required for type ``json_path`` or ``regex``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#value SyntheticsGlobalVariable#value}
        '''
        value_ = SyntheticsGlobalVariableParseTestOptionsParser(type=type, value=value)

        return typing.cast(None, jsii.invoke(self, "putParser", [value_]))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @jsii.member(jsii_name="resetLocalVariableName")
    def reset_local_variable_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalVariableName", []))

    @jsii.member(jsii_name="resetParser")
    def reset_parser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParser", []))

    @builtins.property
    @jsii.member(jsii_name="parser")
    def parser(self) -> "SyntheticsGlobalVariableParseTestOptionsParserOutputReference":
        return typing.cast("SyntheticsGlobalVariableParseTestOptionsParserOutputReference", jsii.get(self, "parser"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="localVariableNameInput")
    def local_variable_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localVariableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parserInput")
    def parser_input(
        self,
    ) -> typing.Optional["SyntheticsGlobalVariableParseTestOptionsParser"]:
        return typing.cast(typing.Optional["SyntheticsGlobalVariableParseTestOptionsParser"], jsii.get(self, "parserInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d37da09cc9857df35cd0946bfa45b5e4e12683e5923f19a5e692d91b73f0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value)

    @builtins.property
    @jsii.member(jsii_name="localVariableName")
    def local_variable_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localVariableName"))

    @local_variable_name.setter
    def local_variable_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e7109537e74bdfd501f10f03c1f502ce6c18942c3b3073d9b7c317a6d88e592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localVariableName", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fcb33507c22dda355b535155a97c5fa71182c7976751e5da076d1ecbebc2c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsGlobalVariableParseTestOptions]:
        return typing.cast(typing.Optional[SyntheticsGlobalVariableParseTestOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsGlobalVariableParseTestOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e81295eb53b8224ba71ccf8ee6615a25d6b64568e6f3ff0acffe34023964c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableParseTestOptionsParser",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SyntheticsGlobalVariableParseTestOptionsParser:
    def __init__(
        self,
        *,
        type: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of parser to extract the value. Valid values are ``raw``, ``json_path``, ``regex``, ``x_path``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#type SyntheticsGlobalVariable#type}
        :param value: Value for the parser to use, required for type ``json_path`` or ``regex``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#value SyntheticsGlobalVariable#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b61d4325df063e55e3376869c11f80e380138b0acca80b527a4305e8f7d8ecc)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of parser to extract the value. Valid values are ``raw``, ``json_path``, ``regex``, ``x_path``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#type SyntheticsGlobalVariable#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value for the parser to use, required for type ``json_path`` or ``regex``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/synthetics_global_variable#value SyntheticsGlobalVariable#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsGlobalVariableParseTestOptionsParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsGlobalVariableParseTestOptionsParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableParseTestOptionsParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96bcd2e362738eefe8344df96f9a9200c207516349d2dc84181f2a9e5eecf12d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__44a15579b79d6b9770670b36ff07ab0a7ce1b18e90c84eff2600a99f86213997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7fdb27bdaf55f5734fb702d771a6426f0f5a5424d46bd6ae956b59a956e59f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SyntheticsGlobalVariableParseTestOptionsParser]:
        return typing.cast(typing.Optional[SyntheticsGlobalVariableParseTestOptionsParser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SyntheticsGlobalVariableParseTestOptionsParser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5003b27fa89627b796fe64d0eae72b4cf2af2013b8fcf4accede4a4ba31ac55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SyntheticsGlobalVariable",
    "SyntheticsGlobalVariableConfig",
    "SyntheticsGlobalVariableParseTestOptions",
    "SyntheticsGlobalVariableParseTestOptionsOutputReference",
    "SyntheticsGlobalVariableParseTestOptionsParser",
    "SyntheticsGlobalVariableParseTestOptionsParserOutputReference",
]

publication.publish()

def _typecheckingstub__8130ffd11a0e21ba65645d2942d6d24827dd309902720b48e6aa8bb09898234a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    value: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    parse_test_id: typing.Optional[builtins.str] = None,
    parse_test_options: typing.Optional[typing.Union[SyntheticsGlobalVariableParseTestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__5788193d85c608e53229844e5d474d6e97671a3940f445d70fab418f64b97f1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee281aba529a743bf87bc0dded4f6e58d24568b8a45c3a6e453411c2cfda6f84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8db3cbcbc12a692c9b8cab94ba6b62216d49b6ba4890ea3dec5bfa6930e5215(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a18607594b6da1ebaefc8ea8de385f4b5316de535be739bb45a0bc0a2e4e92a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e791098824659489ff80e0e78f970432bc4199c9faa83ce76ec52776c7a803(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a40ce9bc785d30740d27aab35e01f9767684fb47d64e4741a0dba881efbfa36(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a521fa7e1d9afa8e6d7062b6f1f25b1380ff83e25d6cab06040e1aaf3dc10b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4ab1a6261c0a0805944bb08aa51411a235c7968e7a04fa2e3bffb62ad10ddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcfac2b6f5d731f178d31b130a243e4236cc921180c897ee746b90bd6be142b0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    value: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    parse_test_id: typing.Optional[builtins.str] = None,
    parse_test_options: typing.Optional[typing.Union[SyntheticsGlobalVariableParseTestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c891479c2ff58d4c7ee95c32ffb1c6e8113a005dc333ae5da8f69c0969c47b60(
    *,
    type: builtins.str,
    field: typing.Optional[builtins.str] = None,
    local_variable_name: typing.Optional[builtins.str] = None,
    parser: typing.Optional[typing.Union[SyntheticsGlobalVariableParseTestOptionsParser, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e304cd61031eb012f85dc389d715dab5646e5be0fc1b52a4098852c058b886(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d37da09cc9857df35cd0946bfa45b5e4e12683e5923f19a5e692d91b73f0c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7109537e74bdfd501f10f03c1f502ce6c18942c3b3073d9b7c317a6d88e592(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fcb33507c22dda355b535155a97c5fa71182c7976751e5da076d1ecbebc2c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e81295eb53b8224ba71ccf8ee6615a25d6b64568e6f3ff0acffe34023964c88(
    value: typing.Optional[SyntheticsGlobalVariableParseTestOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b61d4325df063e55e3376869c11f80e380138b0acca80b527a4305e8f7d8ecc(
    *,
    type: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96bcd2e362738eefe8344df96f9a9200c207516349d2dc84181f2a9e5eecf12d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a15579b79d6b9770670b36ff07ab0a7ce1b18e90c84eff2600a99f86213997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7fdb27bdaf55f5734fb702d771a6426f0f5a5424d46bd6ae956b59a956e59f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5003b27fa89627b796fe64d0eae72b4cf2af2013b8fcf4accede4a4ba31ac55(
    value: typing.Optional[SyntheticsGlobalVariableParseTestOptionsParser],
) -> None:
    """Type checking stubs"""
    pass
