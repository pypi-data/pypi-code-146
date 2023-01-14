'''
# `azurerm_video_analyzer`

Refer to the Terraform Registory for docs: [`azurerm_video_analyzer`](https://www.terraform.io/docs/providers/azurerm/r/video_analyzer).
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


class VideoAnalyzer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.videoAnalyzer.VideoAnalyzer",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer azurerm_video_analyzer}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        identity: typing.Union["VideoAnalyzerIdentity", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        storage_account: typing.Union["VideoAnalyzerStorageAccount", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VideoAnalyzerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer azurerm_video_analyzer} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param identity: identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#identity VideoAnalyzer#identity}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#location VideoAnalyzer#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#name VideoAnalyzer#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#resource_group_name VideoAnalyzer#resource_group_name}.
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#storage_account VideoAnalyzer#storage_account}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#id VideoAnalyzer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#tags VideoAnalyzer#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#timeouts VideoAnalyzer#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ea5c6d0bc4c37144b7407db899482cf147f9450f997f822c40de248b17efe1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VideoAnalyzerConfig(
            identity=identity,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            storage_account=storage_account,
            id=id,
            tags=tags,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#identity_ids VideoAnalyzer#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#type VideoAnalyzer#type}.
        '''
        value = VideoAnalyzerIdentity(identity_ids=identity_ids, type=type)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putStorageAccount")
    def put_storage_account(
        self,
        *,
        id: builtins.str,
        user_assigned_identity_id: builtins.str,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#id VideoAnalyzer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#user_assigned_identity_id VideoAnalyzer#user_assigned_identity_id}.
        '''
        value = VideoAnalyzerStorageAccount(
            id=id, user_assigned_identity_id=user_assigned_identity_id
        )

        return typing.cast(None, jsii.invoke(self, "putStorageAccount", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#create VideoAnalyzer#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#delete VideoAnalyzer#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#read VideoAnalyzer#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#update VideoAnalyzer#update}.
        '''
        value = VideoAnalyzerTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "VideoAnalyzerIdentityOutputReference":
        return typing.cast("VideoAnalyzerIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> "VideoAnalyzerStorageAccountOutputReference":
        return typing.cast("VideoAnalyzerStorageAccountOutputReference", jsii.get(self, "storageAccount"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VideoAnalyzerTimeoutsOutputReference":
        return typing.cast("VideoAnalyzerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["VideoAnalyzerIdentity"]:
        return typing.cast(typing.Optional["VideoAnalyzerIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(self) -> typing.Optional["VideoAnalyzerStorageAccount"]:
        return typing.cast(typing.Optional["VideoAnalyzerStorageAccount"], jsii.get(self, "storageAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["VideoAnalyzerTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VideoAnalyzerTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7005c90f01f194f13105c91fd0f18efd89895964ca62d9e79b631a056c083cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90691b3f1e1e13d23a4f0d633a69e567467640d5f64b4f9a2147ce0991a8a281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64203634a84aecde34fb13dcc3b7aca4738732b5399d19f9b75bf613f9e13013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee58ec5d2b47357006b42cc3dfad3750c173f4483ba193a927b19c21212ed790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12456ffded36049ff9f55ec466fe52c32c956cfa8de201ab5beb6858d61190af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.videoAnalyzer.VideoAnalyzerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "identity": "identity",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "storage_account": "storageAccount",
        "id": "id",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class VideoAnalyzerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        identity: typing.Union["VideoAnalyzerIdentity", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        storage_account: typing.Union["VideoAnalyzerStorageAccount", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VideoAnalyzerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param identity: identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#identity VideoAnalyzer#identity}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#location VideoAnalyzer#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#name VideoAnalyzer#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#resource_group_name VideoAnalyzer#resource_group_name}.
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#storage_account VideoAnalyzer#storage_account}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#id VideoAnalyzer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#tags VideoAnalyzer#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#timeouts VideoAnalyzer#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity, dict):
            identity = VideoAnalyzerIdentity(**identity)
        if isinstance(storage_account, dict):
            storage_account = VideoAnalyzerStorageAccount(**storage_account)
        if isinstance(timeouts, dict):
            timeouts = VideoAnalyzerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60fa59692c150f0f70b82a4104091992d0f206ed99d5287b5a3056a46d25b745)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity": identity,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "storage_account": storage_account,
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
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def identity(self) -> "VideoAnalyzerIdentity":
        '''identity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#identity VideoAnalyzer#identity}
        '''
        result = self._values.get("identity")
        assert result is not None, "Required property 'identity' is missing"
        return typing.cast("VideoAnalyzerIdentity", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#location VideoAnalyzer#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#name VideoAnalyzer#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#resource_group_name VideoAnalyzer#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account(self) -> "VideoAnalyzerStorageAccount":
        '''storage_account block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#storage_account VideoAnalyzer#storage_account}
        '''
        result = self._values.get("storage_account")
        assert result is not None, "Required property 'storage_account' is missing"
        return typing.cast("VideoAnalyzerStorageAccount", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#id VideoAnalyzer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#tags VideoAnalyzer#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VideoAnalyzerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#timeouts VideoAnalyzer#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VideoAnalyzerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VideoAnalyzerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.videoAnalyzer.VideoAnalyzerIdentity",
    jsii_struct_bases=[],
    name_mapping={"identity_ids": "identityIds", "type": "type"},
)
class VideoAnalyzerIdentity:
    def __init__(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#identity_ids VideoAnalyzer#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#type VideoAnalyzer#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b68e3774b3f001a6b46d309f106b2f9a33309fe5cce60f7449c7bcdbf1b793)
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_ids": identity_ids,
            "type": type,
        }

    @builtins.property
    def identity_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#identity_ids VideoAnalyzer#identity_ids}.'''
        result = self._values.get("identity_ids")
        assert result is not None, "Required property 'identity_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#type VideoAnalyzer#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VideoAnalyzerIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VideoAnalyzerIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.videoAnalyzer.VideoAnalyzerIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8830700fda8c0abc2a6f7d8ffd895947a0c0ad949dbc81208bc9b22cd6398f90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a6a7a58df1e013dbbb8e1a659eb09abaa3187343eef5d1a282d6f5cc86ed3b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8f05a77e407136d5286543af74c8dc396608f70f6721262a6e662f546db7c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VideoAnalyzerIdentity]:
        return typing.cast(typing.Optional[VideoAnalyzerIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VideoAnalyzerIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d26af2372141173cc518ef4eedb5f902ac8b82ef34725a5548bf0df2366adb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.videoAnalyzer.VideoAnalyzerStorageAccount",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "user_assigned_identity_id": "userAssignedIdentityId"},
)
class VideoAnalyzerStorageAccount:
    def __init__(
        self,
        *,
        id: builtins.str,
        user_assigned_identity_id: builtins.str,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#id VideoAnalyzer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#user_assigned_identity_id VideoAnalyzer#user_assigned_identity_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83dc1604f8e8f85a8709c204d0634824b05aea60c5d31043b314a279fcaf5970)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument user_assigned_identity_id", value=user_assigned_identity_id, expected_type=type_hints["user_assigned_identity_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "user_assigned_identity_id": user_assigned_identity_id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#id VideoAnalyzer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_assigned_identity_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#user_assigned_identity_id VideoAnalyzer#user_assigned_identity_id}.'''
        result = self._values.get("user_assigned_identity_id")
        assert result is not None, "Required property 'user_assigned_identity_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VideoAnalyzerStorageAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VideoAnalyzerStorageAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.videoAnalyzer.VideoAnalyzerStorageAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ea6091960ccdd277fefd4598d47828219553242171446b25193099c9a40eee2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityIdInput")
    def user_assigned_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAssignedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f44f26317cd64e33e8a53a60801182d70867b93b8ae9fd082620a2449800a17d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentityId"))

    @user_assigned_identity_id.setter
    def user_assigned_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1d9a432219ee92bf661257f7fe4dddcbeb7549f1f02316205adcd84d102bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentityId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VideoAnalyzerStorageAccount]:
        return typing.cast(typing.Optional[VideoAnalyzerStorageAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VideoAnalyzerStorageAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc900f2606c3211d75b595056223cb67011e8352e1744cdbeca97789628af0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.videoAnalyzer.VideoAnalyzerTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class VideoAnalyzerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#create VideoAnalyzer#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#delete VideoAnalyzer#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#read VideoAnalyzer#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#update VideoAnalyzer#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cc3ddc62b52b48d70775452bc05723d3f76db3009162d257c86953b53f5769)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#create VideoAnalyzer#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#delete VideoAnalyzer#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#read VideoAnalyzer#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/video_analyzer#update VideoAnalyzer#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VideoAnalyzerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VideoAnalyzerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.videoAnalyzer.VideoAnalyzerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ceaa02a04ec93448015e87e94c16c3cdafc8a015a3a716423a5567c3ae2d281)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0f803cbbc2462d80c8fa7bbd56c5365aadb1a14defeaba31c602281b443c2d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ec4234a9c94f6c1cf547dae7c11c0e0b9fb9aadcd1a31f2694ae809249aeaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bb8905d39324d94dd7df2b246396c2cdef2ec8d3449a1e466d7d45cc246439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55863650a81620149fe933014a9e8f715dec2ef972efb6c5ca79b13507634073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VideoAnalyzerTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VideoAnalyzerTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VideoAnalyzerTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ab95a0d6bdd7da0e5147f2334466ae70495992e7b247d895ddca40984b8384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "VideoAnalyzer",
    "VideoAnalyzerConfig",
    "VideoAnalyzerIdentity",
    "VideoAnalyzerIdentityOutputReference",
    "VideoAnalyzerStorageAccount",
    "VideoAnalyzerStorageAccountOutputReference",
    "VideoAnalyzerTimeouts",
    "VideoAnalyzerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__51ea5c6d0bc4c37144b7407db899482cf147f9450f997f822c40de248b17efe1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    identity: typing.Union[VideoAnalyzerIdentity, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    storage_account: typing.Union[VideoAnalyzerStorageAccount, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VideoAnalyzerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c7005c90f01f194f13105c91fd0f18efd89895964ca62d9e79b631a056c083cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90691b3f1e1e13d23a4f0d633a69e567467640d5f64b4f9a2147ce0991a8a281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64203634a84aecde34fb13dcc3b7aca4738732b5399d19f9b75bf613f9e13013(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee58ec5d2b47357006b42cc3dfad3750c173f4483ba193a927b19c21212ed790(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12456ffded36049ff9f55ec466fe52c32c956cfa8de201ab5beb6858d61190af(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60fa59692c150f0f70b82a4104091992d0f206ed99d5287b5a3056a46d25b745(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    identity: typing.Union[VideoAnalyzerIdentity, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    storage_account: typing.Union[VideoAnalyzerStorageAccount, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VideoAnalyzerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b68e3774b3f001a6b46d309f106b2f9a33309fe5cce60f7449c7bcdbf1b793(
    *,
    identity_ids: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8830700fda8c0abc2a6f7d8ffd895947a0c0ad949dbc81208bc9b22cd6398f90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6a7a58df1e013dbbb8e1a659eb09abaa3187343eef5d1a282d6f5cc86ed3b5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8f05a77e407136d5286543af74c8dc396608f70f6721262a6e662f546db7c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d26af2372141173cc518ef4eedb5f902ac8b82ef34725a5548bf0df2366adb9(
    value: typing.Optional[VideoAnalyzerIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83dc1604f8e8f85a8709c204d0634824b05aea60c5d31043b314a279fcaf5970(
    *,
    id: builtins.str,
    user_assigned_identity_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea6091960ccdd277fefd4598d47828219553242171446b25193099c9a40eee2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44f26317cd64e33e8a53a60801182d70867b93b8ae9fd082620a2449800a17d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1d9a432219ee92bf661257f7fe4dddcbeb7549f1f02316205adcd84d102bf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc900f2606c3211d75b595056223cb67011e8352e1744cdbeca97789628af0d(
    value: typing.Optional[VideoAnalyzerStorageAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cc3ddc62b52b48d70775452bc05723d3f76db3009162d257c86953b53f5769(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ceaa02a04ec93448015e87e94c16c3cdafc8a015a3a716423a5567c3ae2d281(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f803cbbc2462d80c8fa7bbd56c5365aadb1a14defeaba31c602281b443c2d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ec4234a9c94f6c1cf547dae7c11c0e0b9fb9aadcd1a31f2694ae809249aeaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bb8905d39324d94dd7df2b246396c2cdef2ec8d3449a1e466d7d45cc246439(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55863650a81620149fe933014a9e8f715dec2ef972efb6c5ca79b13507634073(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ab95a0d6bdd7da0e5147f2334466ae70495992e7b247d895ddca40984b8384(
    value: typing.Optional[typing.Union[VideoAnalyzerTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
