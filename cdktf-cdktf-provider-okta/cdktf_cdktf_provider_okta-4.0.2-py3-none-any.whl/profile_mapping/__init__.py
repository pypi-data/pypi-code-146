'''
# `okta_profile_mapping`

Refer to the Terraform Registory for docs: [`okta_profile_mapping`](https://www.terraform.io/docs/providers/okta/r/profile_mapping).
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


class ProfileMapping(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.profileMapping.ProfileMapping",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping okta_profile_mapping}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        source_id: builtins.str,
        target_id: builtins.str,
        always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_when_absent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        mappings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProfileMappingMappings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping okta_profile_mapping} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param source_id: The source id of the mapping to manage. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#source_id ProfileMapping#source_id}
        :param target_id: The target id of the mapping to manage. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#target_id ProfileMapping#target_id}
        :param always_apply: Whether apply the changes to all users with this profile after updating or creating the these mappings. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#always_apply ProfileMapping#always_apply}
        :param delete_when_absent: When turned on this flag will trigger the provider to delete mapping properties that are not defined in config. By default, we do not delete missing properties. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#delete_when_absent ProfileMapping#delete_when_absent}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#id ProfileMapping#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mappings: mappings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#mappings ProfileMapping#mappings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b69d8a5ecc16ae474abbdfc5febe57f8bbfdf636240fea77f92bfbd377f4d04)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProfileMappingConfig(
            source_id=source_id,
            target_id=target_id,
            always_apply=always_apply,
            delete_when_absent=delete_when_absent,
            id=id,
            mappings=mappings,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putMappings")
    def put_mappings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProfileMappingMappings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8a9345e859bd9d00cc71a372fa21d3046bbf1beaaed68fcb5109005c0bdbc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMappings", [value]))

    @jsii.member(jsii_name="resetAlwaysApply")
    def reset_always_apply(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlwaysApply", []))

    @jsii.member(jsii_name="resetDeleteWhenAbsent")
    def reset_delete_when_absent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteWhenAbsent", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMappings")
    def reset_mappings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappings", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="mappings")
    def mappings(self) -> "ProfileMappingMappingsList":
        return typing.cast("ProfileMappingMappingsList", jsii.get(self, "mappings"))

    @builtins.property
    @jsii.member(jsii_name="sourceName")
    def source_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceName"))

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @builtins.property
    @jsii.member(jsii_name="targetName")
    def target_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetName"))

    @builtins.property
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetType"))

    @builtins.property
    @jsii.member(jsii_name="alwaysApplyInput")
    def always_apply_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "alwaysApplyInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteWhenAbsentInput")
    def delete_when_absent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteWhenAbsentInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingsInput")
    def mappings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProfileMappingMappings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProfileMappingMappings"]]], jsii.get(self, "mappingsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIdInput")
    def source_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetIdInput")
    def target_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="alwaysApply")
    def always_apply(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "alwaysApply"))

    @always_apply.setter
    def always_apply(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77fed582e82ae4abc58fb063318488511a5825afe8b44d8bfc6af2df9fadad0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysApply", value)

    @builtins.property
    @jsii.member(jsii_name="deleteWhenAbsent")
    def delete_when_absent(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteWhenAbsent"))

    @delete_when_absent.setter
    def delete_when_absent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf137659151ae0b945a78b212b99dc3705c5430bc9233121e3c06ffd721949a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteWhenAbsent", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__132c48e41fc8178a2eaadc986b99031579cbcbb5852b98d95bf6eb3125f5d776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="sourceId")
    def source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceId"))

    @source_id.setter
    def source_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d46e2069a79d5d87a9747c9e00497d75884e9b90ff0ea247fd5a96511a79f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceId", value)

    @builtins.property
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetId"))

    @target_id.setter
    def target_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6721e7b1a06d46d9d2e0a57d05ef10d808a2a5ca105e5fd6d345e80a15aee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.profileMapping.ProfileMappingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "source_id": "sourceId",
        "target_id": "targetId",
        "always_apply": "alwaysApply",
        "delete_when_absent": "deleteWhenAbsent",
        "id": "id",
        "mappings": "mappings",
    },
)
class ProfileMappingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        source_id: builtins.str,
        target_id: builtins.str,
        always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_when_absent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        mappings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProfileMappingMappings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param source_id: The source id of the mapping to manage. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#source_id ProfileMapping#source_id}
        :param target_id: The target id of the mapping to manage. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#target_id ProfileMapping#target_id}
        :param always_apply: Whether apply the changes to all users with this profile after updating or creating the these mappings. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#always_apply ProfileMapping#always_apply}
        :param delete_when_absent: When turned on this flag will trigger the provider to delete mapping properties that are not defined in config. By default, we do not delete missing properties. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#delete_when_absent ProfileMapping#delete_when_absent}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#id ProfileMapping#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mappings: mappings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#mappings ProfileMapping#mappings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207326b3068c4a4da06f5b026a81b01129cbb132c7aab3921e37a010770c4af8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
            check_type(argname="argument target_id", value=target_id, expected_type=type_hints["target_id"])
            check_type(argname="argument always_apply", value=always_apply, expected_type=type_hints["always_apply"])
            check_type(argname="argument delete_when_absent", value=delete_when_absent, expected_type=type_hints["delete_when_absent"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mappings", value=mappings, expected_type=type_hints["mappings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_id": source_id,
            "target_id": target_id,
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
        if always_apply is not None:
            self._values["always_apply"] = always_apply
        if delete_when_absent is not None:
            self._values["delete_when_absent"] = delete_when_absent
        if id is not None:
            self._values["id"] = id
        if mappings is not None:
            self._values["mappings"] = mappings

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
    def source_id(self) -> builtins.str:
        '''The source id of the mapping to manage.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#source_id ProfileMapping#source_id}
        '''
        result = self._values.get("source_id")
        assert result is not None, "Required property 'source_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_id(self) -> builtins.str:
        '''The target id of the mapping to manage.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#target_id ProfileMapping#target_id}
        '''
        result = self._values.get("target_id")
        assert result is not None, "Required property 'target_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def always_apply(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether apply the changes to all users with this profile after updating or creating the these mappings.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#always_apply ProfileMapping#always_apply}
        '''
        result = self._values.get("always_apply")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete_when_absent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When turned on this flag will trigger the provider to delete mapping properties that are not defined in config.

        By default, we do not delete missing properties.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#delete_when_absent ProfileMapping#delete_when_absent}
        '''
        result = self._values.get("delete_when_absent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#id ProfileMapping#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mappings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProfileMappingMappings"]]]:
        '''mappings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#mappings ProfileMapping#mappings}
        '''
        result = self._values.get("mappings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProfileMappingMappings"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProfileMappingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.profileMapping.ProfileMappingMappings",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression", "id": "id", "push_status": "pushStatus"},
)
class ProfileMappingMappings:
    def __init__(
        self,
        *,
        expression: builtins.str,
        id: builtins.str,
        push_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#expression ProfileMapping#expression}.
        :param id: The mapping property key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#id ProfileMapping#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param push_status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#push_status ProfileMapping#push_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d20787fce6403bde8e610860a6cb36119c471002b763caeba41fc497e0b462b)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument push_status", value=push_status, expected_type=type_hints["push_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
            "id": id,
        }
        if push_status is not None:
            self._values["push_status"] = push_status

    @builtins.property
    def expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#expression ProfileMapping#expression}.'''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The mapping property key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#id ProfileMapping#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def push_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/profile_mapping#push_status ProfileMapping#push_status}.'''
        result = self._values.get("push_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProfileMappingMappings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProfileMappingMappingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.profileMapping.ProfileMappingMappingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3140f7fc78b8403141c1d9b25b397b681ce298acb16a6a7ef434684540c35f3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProfileMappingMappingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__461897273dd4638d4b60f53d4efc63fe97e12feb6552d512cea34db8ccd8b09b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProfileMappingMappingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72776606476618d275ba73835958a171e7df667c9618e412959711dcfed19dad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b509a8fbcdd0571573a7cd8685553b3cbdaffa56780b7ea101faadc9e66649b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af8b4dfd7f828f6ded4a8320277421bd6583b840c8572d98c17e4c356ca04838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProfileMappingMappings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProfileMappingMappings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProfileMappingMappings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5820d71d9e8d08d8fb801c4c237267e5ad8051aa1a24347422e38cf312104e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ProfileMappingMappingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.profileMapping.ProfileMappingMappingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56659b809ba5596303729c15492b78ca51a48b4aee94513ba4e75eac5b5cca11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPushStatus")
    def reset_push_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushStatus", []))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="pushStatusInput")
    def push_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pushStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0438aa834b742aeaa904af1f4e4e59ef336b60b05fe3d50c096450ebfbd1207c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5691b4812b4501a74a030192cfd70a91d61b75e0d138dfdda925c27230762b4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="pushStatus")
    def push_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pushStatus"))

    @push_status.setter
    def push_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967649f1aedd59a817bc964a7618d5f32f76c20c31751b2b8db6608f0a8e07c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushStatus", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ProfileMappingMappings, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ProfileMappingMappings, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ProfileMappingMappings, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb13abf9040962af04d90eba8886fb1ad5f7327af9c262465a356d31a8f45fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ProfileMapping",
    "ProfileMappingConfig",
    "ProfileMappingMappings",
    "ProfileMappingMappingsList",
    "ProfileMappingMappingsOutputReference",
]

publication.publish()

def _typecheckingstub__0b69d8a5ecc16ae474abbdfc5febe57f8bbfdf636240fea77f92bfbd377f4d04(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    source_id: builtins.str,
    target_id: builtins.str,
    always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_when_absent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    mappings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProfileMappingMappings, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__ba8a9345e859bd9d00cc71a372fa21d3046bbf1beaaed68fcb5109005c0bdbc3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProfileMappingMappings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fed582e82ae4abc58fb063318488511a5825afe8b44d8bfc6af2df9fadad0b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf137659151ae0b945a78b212b99dc3705c5430bc9233121e3c06ffd721949a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132c48e41fc8178a2eaadc986b99031579cbcbb5852b98d95bf6eb3125f5d776(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d46e2069a79d5d87a9747c9e00497d75884e9b90ff0ea247fd5a96511a79f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6721e7b1a06d46d9d2e0a57d05ef10d808a2a5ca105e5fd6d345e80a15aee6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207326b3068c4a4da06f5b026a81b01129cbb132c7aab3921e37a010770c4af8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_id: builtins.str,
    target_id: builtins.str,
    always_apply: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_when_absent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    mappings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProfileMappingMappings, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d20787fce6403bde8e610860a6cb36119c471002b763caeba41fc497e0b462b(
    *,
    expression: builtins.str,
    id: builtins.str,
    push_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3140f7fc78b8403141c1d9b25b397b681ce298acb16a6a7ef434684540c35f3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461897273dd4638d4b60f53d4efc63fe97e12feb6552d512cea34db8ccd8b09b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72776606476618d275ba73835958a171e7df667c9618e412959711dcfed19dad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b509a8fbcdd0571573a7cd8685553b3cbdaffa56780b7ea101faadc9e66649b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8b4dfd7f828f6ded4a8320277421bd6583b840c8572d98c17e4c356ca04838(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5820d71d9e8d08d8fb801c4c237267e5ad8051aa1a24347422e38cf312104e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProfileMappingMappings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56659b809ba5596303729c15492b78ca51a48b4aee94513ba4e75eac5b5cca11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0438aa834b742aeaa904af1f4e4e59ef336b60b05fe3d50c096450ebfbd1207c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5691b4812b4501a74a030192cfd70a91d61b75e0d138dfdda925c27230762b4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967649f1aedd59a817bc964a7618d5f32f76c20c31751b2b8db6608f0a8e07c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb13abf9040962af04d90eba8886fb1ad5f7327af9c262465a356d31a8f45fc3(
    value: typing.Optional[typing.Union[ProfileMappingMappings, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
