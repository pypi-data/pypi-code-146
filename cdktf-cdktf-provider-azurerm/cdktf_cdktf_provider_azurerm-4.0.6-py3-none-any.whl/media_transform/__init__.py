'''
# `azurerm_media_transform`

Refer to the Terraform Registory for docs: [`azurerm_media_transform`](https://www.terraform.io/docs/providers/azurerm/r/media_transform).
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


class MediaTransform(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransform",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform azurerm_media_transform}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        media_services_account_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        output: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaTransformOutput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["MediaTransformTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform azurerm_media_transform} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param media_services_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#media_services_account_name MediaTransform#media_services_account_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#name MediaTransform#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#resource_group_name MediaTransform#resource_group_name}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#description MediaTransform#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#id MediaTransform#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param output: output block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#output MediaTransform#output}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#timeouts MediaTransform#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c41f75eff24819994958b09a36c6e201c83521a2f56558da9c72e6c1092fecb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MediaTransformConfig(
            media_services_account_name=media_services_account_name,
            name=name,
            resource_group_name=resource_group_name,
            description=description,
            id=id,
            output=output,
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

    @jsii.member(jsii_name="putOutput")
    def put_output(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaTransformOutput", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac089d9982f230f82d95ebdb742b3102b62365a83b3986aecb192666f5605a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOutput", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#create MediaTransform#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#delete MediaTransform#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#read MediaTransform#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#update MediaTransform#update}.
        '''
        value = MediaTransformTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOutput")
    def reset_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutput", []))

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
    @jsii.member(jsii_name="output")
    def output(self) -> "MediaTransformOutputList":
        return typing.cast("MediaTransformOutputList", jsii.get(self, "output"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MediaTransformTimeoutsOutputReference":
        return typing.cast("MediaTransformTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mediaServicesAccountNameInput")
    def media_services_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mediaServicesAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="outputInput")
    def output_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaTransformOutput"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaTransformOutput"]]], jsii.get(self, "outputInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MediaTransformTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MediaTransformTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c484f553fe83e00cc7ebf3d19380c26db01278d40912d3122273cf5d87a4ef98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765acf3267073be26589e651f5abc8aa1b9ebe6f00d0c2dd01fee2598ac8decb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="mediaServicesAccountName")
    def media_services_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mediaServicesAccountName"))

    @media_services_account_name.setter
    def media_services_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a64d0fd84d7e7cdb13bbbf9a77362ca775919c44e5f389baff7604ff496577f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mediaServicesAccountName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612d790c370ef7c1243727283235dc5de0f8207e4ac50898580bcdf405a06082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16de48379a7915c82c056609e94f7730f02cc6b10d0405f0db65a2579af36cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "media_services_account_name": "mediaServicesAccountName",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "description": "description",
        "id": "id",
        "output": "output",
        "timeouts": "timeouts",
    },
)
class MediaTransformConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        media_services_account_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        output: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaTransformOutput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["MediaTransformTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param media_services_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#media_services_account_name MediaTransform#media_services_account_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#name MediaTransform#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#resource_group_name MediaTransform#resource_group_name}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#description MediaTransform#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#id MediaTransform#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param output: output block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#output MediaTransform#output}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#timeouts MediaTransform#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = MediaTransformTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d209c9d3caa58f11af5ecf8bd18ddc9bff1f3ac46948505b039466b853b75d7c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument media_services_account_name", value=media_services_account_name, expected_type=type_hints["media_services_account_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "media_services_account_name": media_services_account_name,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if output is not None:
            self._values["output"] = output
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
    def media_services_account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#media_services_account_name MediaTransform#media_services_account_name}.'''
        result = self._values.get("media_services_account_name")
        assert result is not None, "Required property 'media_services_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#name MediaTransform#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#resource_group_name MediaTransform#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#description MediaTransform#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#id MediaTransform#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaTransformOutput"]]]:
        '''output block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#output MediaTransform#output}
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaTransformOutput"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MediaTransformTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#timeouts MediaTransform#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MediaTransformTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaTransformConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformOutput",
    jsii_struct_bases=[],
    name_mapping={
        "audio_analyzer_preset": "audioAnalyzerPreset",
        "builtin_preset": "builtinPreset",
        "face_detector_preset": "faceDetectorPreset",
        "on_error_action": "onErrorAction",
        "relative_priority": "relativePriority",
        "video_analyzer_preset": "videoAnalyzerPreset",
    },
)
class MediaTransformOutput:
    def __init__(
        self,
        *,
        audio_analyzer_preset: typing.Optional[typing.Union["MediaTransformOutputAudioAnalyzerPreset", typing.Dict[builtins.str, typing.Any]]] = None,
        builtin_preset: typing.Optional[typing.Union["MediaTransformOutputBuiltinPreset", typing.Dict[builtins.str, typing.Any]]] = None,
        face_detector_preset: typing.Optional[typing.Union["MediaTransformOutputFaceDetectorPreset", typing.Dict[builtins.str, typing.Any]]] = None,
        on_error_action: typing.Optional[builtins.str] = None,
        relative_priority: typing.Optional[builtins.str] = None,
        video_analyzer_preset: typing.Optional[typing.Union["MediaTransformOutputVideoAnalyzerPreset", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_analyzer_preset: audio_analyzer_preset block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_analyzer_preset MediaTransform#audio_analyzer_preset}
        :param builtin_preset: builtin_preset block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#builtin_preset MediaTransform#builtin_preset}
        :param face_detector_preset: face_detector_preset block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#face_detector_preset MediaTransform#face_detector_preset}
        :param on_error_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#on_error_action MediaTransform#on_error_action}.
        :param relative_priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#relative_priority MediaTransform#relative_priority}.
        :param video_analyzer_preset: video_analyzer_preset block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#video_analyzer_preset MediaTransform#video_analyzer_preset}
        '''
        if isinstance(audio_analyzer_preset, dict):
            audio_analyzer_preset = MediaTransformOutputAudioAnalyzerPreset(**audio_analyzer_preset)
        if isinstance(builtin_preset, dict):
            builtin_preset = MediaTransformOutputBuiltinPreset(**builtin_preset)
        if isinstance(face_detector_preset, dict):
            face_detector_preset = MediaTransformOutputFaceDetectorPreset(**face_detector_preset)
        if isinstance(video_analyzer_preset, dict):
            video_analyzer_preset = MediaTransformOutputVideoAnalyzerPreset(**video_analyzer_preset)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666c2c9da913938700dc7a27642e2ad57f50a195b5bb94a8c837c8d76bb13caa)
            check_type(argname="argument audio_analyzer_preset", value=audio_analyzer_preset, expected_type=type_hints["audio_analyzer_preset"])
            check_type(argname="argument builtin_preset", value=builtin_preset, expected_type=type_hints["builtin_preset"])
            check_type(argname="argument face_detector_preset", value=face_detector_preset, expected_type=type_hints["face_detector_preset"])
            check_type(argname="argument on_error_action", value=on_error_action, expected_type=type_hints["on_error_action"])
            check_type(argname="argument relative_priority", value=relative_priority, expected_type=type_hints["relative_priority"])
            check_type(argname="argument video_analyzer_preset", value=video_analyzer_preset, expected_type=type_hints["video_analyzer_preset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audio_analyzer_preset is not None:
            self._values["audio_analyzer_preset"] = audio_analyzer_preset
        if builtin_preset is not None:
            self._values["builtin_preset"] = builtin_preset
        if face_detector_preset is not None:
            self._values["face_detector_preset"] = face_detector_preset
        if on_error_action is not None:
            self._values["on_error_action"] = on_error_action
        if relative_priority is not None:
            self._values["relative_priority"] = relative_priority
        if video_analyzer_preset is not None:
            self._values["video_analyzer_preset"] = video_analyzer_preset

    @builtins.property
    def audio_analyzer_preset(
        self,
    ) -> typing.Optional["MediaTransformOutputAudioAnalyzerPreset"]:
        '''audio_analyzer_preset block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_analyzer_preset MediaTransform#audio_analyzer_preset}
        '''
        result = self._values.get("audio_analyzer_preset")
        return typing.cast(typing.Optional["MediaTransformOutputAudioAnalyzerPreset"], result)

    @builtins.property
    def builtin_preset(self) -> typing.Optional["MediaTransformOutputBuiltinPreset"]:
        '''builtin_preset block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#builtin_preset MediaTransform#builtin_preset}
        '''
        result = self._values.get("builtin_preset")
        return typing.cast(typing.Optional["MediaTransformOutputBuiltinPreset"], result)

    @builtins.property
    def face_detector_preset(
        self,
    ) -> typing.Optional["MediaTransformOutputFaceDetectorPreset"]:
        '''face_detector_preset block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#face_detector_preset MediaTransform#face_detector_preset}
        '''
        result = self._values.get("face_detector_preset")
        return typing.cast(typing.Optional["MediaTransformOutputFaceDetectorPreset"], result)

    @builtins.property
    def on_error_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#on_error_action MediaTransform#on_error_action}.'''
        result = self._values.get("on_error_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def relative_priority(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#relative_priority MediaTransform#relative_priority}.'''
        result = self._values.get("relative_priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def video_analyzer_preset(
        self,
    ) -> typing.Optional["MediaTransformOutputVideoAnalyzerPreset"]:
        '''video_analyzer_preset block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#video_analyzer_preset MediaTransform#video_analyzer_preset}
        '''
        result = self._values.get("video_analyzer_preset")
        return typing.cast(typing.Optional["MediaTransformOutputVideoAnalyzerPreset"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaTransformOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformOutputAudioAnalyzerPreset",
    jsii_struct_bases=[],
    name_mapping={
        "audio_analysis_mode": "audioAnalysisMode",
        "audio_language": "audioLanguage",
    },
)
class MediaTransformOutputAudioAnalyzerPreset:
    def __init__(
        self,
        *,
        audio_analysis_mode: typing.Optional[builtins.str] = None,
        audio_language: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audio_analysis_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_analysis_mode MediaTransform#audio_analysis_mode}.
        :param audio_language: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_language MediaTransform#audio_language}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86be4a547b7de35e3afda494aa38b62e654677fcdff205b65dff86815f012de5)
            check_type(argname="argument audio_analysis_mode", value=audio_analysis_mode, expected_type=type_hints["audio_analysis_mode"])
            check_type(argname="argument audio_language", value=audio_language, expected_type=type_hints["audio_language"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audio_analysis_mode is not None:
            self._values["audio_analysis_mode"] = audio_analysis_mode
        if audio_language is not None:
            self._values["audio_language"] = audio_language

    @builtins.property
    def audio_analysis_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_analysis_mode MediaTransform#audio_analysis_mode}.'''
        result = self._values.get("audio_analysis_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def audio_language(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_language MediaTransform#audio_language}.'''
        result = self._values.get("audio_language")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaTransformOutputAudioAnalyzerPreset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaTransformOutputAudioAnalyzerPresetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformOutputAudioAnalyzerPresetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33b7d395d1b3f01cb790ac467032c53ffa9ec5ce4c5d360da4f2b991b3a8b77d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudioAnalysisMode")
    def reset_audio_analysis_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioAnalysisMode", []))

    @jsii.member(jsii_name="resetAudioLanguage")
    def reset_audio_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioLanguage", []))

    @builtins.property
    @jsii.member(jsii_name="audioAnalysisModeInput")
    def audio_analysis_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audioAnalysisModeInput"))

    @builtins.property
    @jsii.member(jsii_name="audioLanguageInput")
    def audio_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audioLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="audioAnalysisMode")
    def audio_analysis_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioAnalysisMode"))

    @audio_analysis_mode.setter
    def audio_analysis_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65612928c10a6dca460daef87ccf949b480be7328a992cce94e160dcc5f4c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioAnalysisMode", value)

    @builtins.property
    @jsii.member(jsii_name="audioLanguage")
    def audio_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioLanguage"))

    @audio_language.setter
    def audio_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b9492548862da82bd8cb63c7d8f31f8dae74ec2c02438e53905504a40b8364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaTransformOutputAudioAnalyzerPreset]:
        return typing.cast(typing.Optional[MediaTransformOutputAudioAnalyzerPreset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaTransformOutputAudioAnalyzerPreset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebfb78476aa46c3af4b31d0c08f0f4906badb1955918d4992296705c51407255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformOutputBuiltinPreset",
    jsii_struct_bases=[],
    name_mapping={"preset_name": "presetName"},
)
class MediaTransformOutputBuiltinPreset:
    def __init__(self, *, preset_name: builtins.str) -> None:
        '''
        :param preset_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#preset_name MediaTransform#preset_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0cfa8e191093b2699a78d5eacb297553ab56fbcd29a7002d0f47feefac77b2)
            check_type(argname="argument preset_name", value=preset_name, expected_type=type_hints["preset_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "preset_name": preset_name,
        }

    @builtins.property
    def preset_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#preset_name MediaTransform#preset_name}.'''
        result = self._values.get("preset_name")
        assert result is not None, "Required property 'preset_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaTransformOutputBuiltinPreset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaTransformOutputBuiltinPresetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformOutputBuiltinPresetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fc02c10b96f92dbd42b1e4867b5445b62a5f082b94a254aad7de93633cb3e9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="presetNameInput")
    def preset_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "presetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="presetName")
    def preset_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "presetName"))

    @preset_name.setter
    def preset_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca46e3a1a2b119a67fd3a9df7a632485257928812a7eb25e1bf2eda4eec9be6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presetName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MediaTransformOutputBuiltinPreset]:
        return typing.cast(typing.Optional[MediaTransformOutputBuiltinPreset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaTransformOutputBuiltinPreset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2c5f4d0cb36a7ef6df80284babe5ce85a6bb15f2343aa9be57a287a12090476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformOutputFaceDetectorPreset",
    jsii_struct_bases=[],
    name_mapping={"analysis_resolution": "analysisResolution"},
)
class MediaTransformOutputFaceDetectorPreset:
    def __init__(
        self,
        *,
        analysis_resolution: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param analysis_resolution: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#analysis_resolution MediaTransform#analysis_resolution}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c59bd284086270465237bf3fd3a92dcc4058494fffeee893f3de6bade87935c)
            check_type(argname="argument analysis_resolution", value=analysis_resolution, expected_type=type_hints["analysis_resolution"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if analysis_resolution is not None:
            self._values["analysis_resolution"] = analysis_resolution

    @builtins.property
    def analysis_resolution(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#analysis_resolution MediaTransform#analysis_resolution}.'''
        result = self._values.get("analysis_resolution")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaTransformOutputFaceDetectorPreset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaTransformOutputFaceDetectorPresetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformOutputFaceDetectorPresetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a0c631f840d38c32d0e610f614c22be53a7272a95389d831392f2fa43ddffd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAnalysisResolution")
    def reset_analysis_resolution(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalysisResolution", []))

    @builtins.property
    @jsii.member(jsii_name="analysisResolutionInput")
    def analysis_resolution_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "analysisResolutionInput"))

    @builtins.property
    @jsii.member(jsii_name="analysisResolution")
    def analysis_resolution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "analysisResolution"))

    @analysis_resolution.setter
    def analysis_resolution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1db3e523de183b9f9fa92fb1205b76ea7168ed14ed188ef3c002688eedb783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analysisResolution", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MediaTransformOutputFaceDetectorPreset]:
        return typing.cast(typing.Optional[MediaTransformOutputFaceDetectorPreset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaTransformOutputFaceDetectorPreset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb4155e3f3339515d1ccf85655135e9c64762332528a9ef97fa82ac3371abdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaTransformOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9317d382df1ad8258ff57d6871121b80fb035c98bd4801c9b19a27204f83a2e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MediaTransformOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1441d9de76bfa2c71300f6f681987187350e3cc8a8964886d7b039986a6ca5e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MediaTransformOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26285451211fb4312004f4c366e60eba513d2cac63e7f94d5d0848a78066b300)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1e0a546320d11a4b1e336ba244ce3ef08c04d643dfca8dc2c9a0f525c1ca0a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9495279790ab8749bc4f493ea18cb893f7cfb80f5fa56125c3d18f7e394f5842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaTransformOutput]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaTransformOutput]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaTransformOutput]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238c880f727f4e248192e062f420d9b65f16c8eeecee50297408cde591f7bf1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaTransformOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91bd6a33c37bb09f019110b2d711d588d130f4ff4aa13d9ae44bb8f7fa19af48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAudioAnalyzerPreset")
    def put_audio_analyzer_preset(
        self,
        *,
        audio_analysis_mode: typing.Optional[builtins.str] = None,
        audio_language: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audio_analysis_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_analysis_mode MediaTransform#audio_analysis_mode}.
        :param audio_language: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_language MediaTransform#audio_language}.
        '''
        value = MediaTransformOutputAudioAnalyzerPreset(
            audio_analysis_mode=audio_analysis_mode, audio_language=audio_language
        )

        return typing.cast(None, jsii.invoke(self, "putAudioAnalyzerPreset", [value]))

    @jsii.member(jsii_name="putBuiltinPreset")
    def put_builtin_preset(self, *, preset_name: builtins.str) -> None:
        '''
        :param preset_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#preset_name MediaTransform#preset_name}.
        '''
        value = MediaTransformOutputBuiltinPreset(preset_name=preset_name)

        return typing.cast(None, jsii.invoke(self, "putBuiltinPreset", [value]))

    @jsii.member(jsii_name="putFaceDetectorPreset")
    def put_face_detector_preset(
        self,
        *,
        analysis_resolution: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param analysis_resolution: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#analysis_resolution MediaTransform#analysis_resolution}.
        '''
        value = MediaTransformOutputFaceDetectorPreset(
            analysis_resolution=analysis_resolution
        )

        return typing.cast(None, jsii.invoke(self, "putFaceDetectorPreset", [value]))

    @jsii.member(jsii_name="putVideoAnalyzerPreset")
    def put_video_analyzer_preset(
        self,
        *,
        audio_analysis_mode: typing.Optional[builtins.str] = None,
        audio_language: typing.Optional[builtins.str] = None,
        insights_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audio_analysis_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_analysis_mode MediaTransform#audio_analysis_mode}.
        :param audio_language: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_language MediaTransform#audio_language}.
        :param insights_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#insights_type MediaTransform#insights_type}.
        '''
        value = MediaTransformOutputVideoAnalyzerPreset(
            audio_analysis_mode=audio_analysis_mode,
            audio_language=audio_language,
            insights_type=insights_type,
        )

        return typing.cast(None, jsii.invoke(self, "putVideoAnalyzerPreset", [value]))

    @jsii.member(jsii_name="resetAudioAnalyzerPreset")
    def reset_audio_analyzer_preset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioAnalyzerPreset", []))

    @jsii.member(jsii_name="resetBuiltinPreset")
    def reset_builtin_preset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuiltinPreset", []))

    @jsii.member(jsii_name="resetFaceDetectorPreset")
    def reset_face_detector_preset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFaceDetectorPreset", []))

    @jsii.member(jsii_name="resetOnErrorAction")
    def reset_on_error_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnErrorAction", []))

    @jsii.member(jsii_name="resetRelativePriority")
    def reset_relative_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelativePriority", []))

    @jsii.member(jsii_name="resetVideoAnalyzerPreset")
    def reset_video_analyzer_preset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVideoAnalyzerPreset", []))

    @builtins.property
    @jsii.member(jsii_name="audioAnalyzerPreset")
    def audio_analyzer_preset(
        self,
    ) -> MediaTransformOutputAudioAnalyzerPresetOutputReference:
        return typing.cast(MediaTransformOutputAudioAnalyzerPresetOutputReference, jsii.get(self, "audioAnalyzerPreset"))

    @builtins.property
    @jsii.member(jsii_name="builtinPreset")
    def builtin_preset(self) -> MediaTransformOutputBuiltinPresetOutputReference:
        return typing.cast(MediaTransformOutputBuiltinPresetOutputReference, jsii.get(self, "builtinPreset"))

    @builtins.property
    @jsii.member(jsii_name="faceDetectorPreset")
    def face_detector_preset(
        self,
    ) -> MediaTransformOutputFaceDetectorPresetOutputReference:
        return typing.cast(MediaTransformOutputFaceDetectorPresetOutputReference, jsii.get(self, "faceDetectorPreset"))

    @builtins.property
    @jsii.member(jsii_name="videoAnalyzerPreset")
    def video_analyzer_preset(
        self,
    ) -> "MediaTransformOutputVideoAnalyzerPresetOutputReference":
        return typing.cast("MediaTransformOutputVideoAnalyzerPresetOutputReference", jsii.get(self, "videoAnalyzerPreset"))

    @builtins.property
    @jsii.member(jsii_name="audioAnalyzerPresetInput")
    def audio_analyzer_preset_input(
        self,
    ) -> typing.Optional[MediaTransformOutputAudioAnalyzerPreset]:
        return typing.cast(typing.Optional[MediaTransformOutputAudioAnalyzerPreset], jsii.get(self, "audioAnalyzerPresetInput"))

    @builtins.property
    @jsii.member(jsii_name="builtinPresetInput")
    def builtin_preset_input(
        self,
    ) -> typing.Optional[MediaTransformOutputBuiltinPreset]:
        return typing.cast(typing.Optional[MediaTransformOutputBuiltinPreset], jsii.get(self, "builtinPresetInput"))

    @builtins.property
    @jsii.member(jsii_name="faceDetectorPresetInput")
    def face_detector_preset_input(
        self,
    ) -> typing.Optional[MediaTransformOutputFaceDetectorPreset]:
        return typing.cast(typing.Optional[MediaTransformOutputFaceDetectorPreset], jsii.get(self, "faceDetectorPresetInput"))

    @builtins.property
    @jsii.member(jsii_name="onErrorActionInput")
    def on_error_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onErrorActionInput"))

    @builtins.property
    @jsii.member(jsii_name="relativePriorityInput")
    def relative_priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "relativePriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="videoAnalyzerPresetInput")
    def video_analyzer_preset_input(
        self,
    ) -> typing.Optional["MediaTransformOutputVideoAnalyzerPreset"]:
        return typing.cast(typing.Optional["MediaTransformOutputVideoAnalyzerPreset"], jsii.get(self, "videoAnalyzerPresetInput"))

    @builtins.property
    @jsii.member(jsii_name="onErrorAction")
    def on_error_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onErrorAction"))

    @on_error_action.setter
    def on_error_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e2b52788bfb52c59c765e93837dd3322f5b6385f2acb62c10e7417eb1621019)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onErrorAction", value)

    @builtins.property
    @jsii.member(jsii_name="relativePriority")
    def relative_priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "relativePriority"))

    @relative_priority.setter
    def relative_priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0f09cd0fcfd254e31c1e3dee7525a0411b00cbd866d45828cf85383fc67c7b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relativePriority", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaTransformOutput, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaTransformOutput, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaTransformOutput, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f4e0b3413e107129052b78146364562f08f8efbd59c8a649d1f81919a0795f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformOutputVideoAnalyzerPreset",
    jsii_struct_bases=[],
    name_mapping={
        "audio_analysis_mode": "audioAnalysisMode",
        "audio_language": "audioLanguage",
        "insights_type": "insightsType",
    },
)
class MediaTransformOutputVideoAnalyzerPreset:
    def __init__(
        self,
        *,
        audio_analysis_mode: typing.Optional[builtins.str] = None,
        audio_language: typing.Optional[builtins.str] = None,
        insights_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audio_analysis_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_analysis_mode MediaTransform#audio_analysis_mode}.
        :param audio_language: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_language MediaTransform#audio_language}.
        :param insights_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#insights_type MediaTransform#insights_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21d4da6e7f3bdf0c69bad3f28be58309cea877c7882b3ea9c5c9aaddbab0cf3)
            check_type(argname="argument audio_analysis_mode", value=audio_analysis_mode, expected_type=type_hints["audio_analysis_mode"])
            check_type(argname="argument audio_language", value=audio_language, expected_type=type_hints["audio_language"])
            check_type(argname="argument insights_type", value=insights_type, expected_type=type_hints["insights_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audio_analysis_mode is not None:
            self._values["audio_analysis_mode"] = audio_analysis_mode
        if audio_language is not None:
            self._values["audio_language"] = audio_language
        if insights_type is not None:
            self._values["insights_type"] = insights_type

    @builtins.property
    def audio_analysis_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_analysis_mode MediaTransform#audio_analysis_mode}.'''
        result = self._values.get("audio_analysis_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def audio_language(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#audio_language MediaTransform#audio_language}.'''
        result = self._values.get("audio_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insights_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#insights_type MediaTransform#insights_type}.'''
        result = self._values.get("insights_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaTransformOutputVideoAnalyzerPreset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaTransformOutputVideoAnalyzerPresetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformOutputVideoAnalyzerPresetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f7b71787ab213f88aeb08caebb759ba4d0f4294809be57ede57b675db5a966b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudioAnalysisMode")
    def reset_audio_analysis_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioAnalysisMode", []))

    @jsii.member(jsii_name="resetAudioLanguage")
    def reset_audio_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioLanguage", []))

    @jsii.member(jsii_name="resetInsightsType")
    def reset_insights_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsightsType", []))

    @builtins.property
    @jsii.member(jsii_name="audioAnalysisModeInput")
    def audio_analysis_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audioAnalysisModeInput"))

    @builtins.property
    @jsii.member(jsii_name="audioLanguageInput")
    def audio_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audioLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsTypeInput")
    def insights_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="audioAnalysisMode")
    def audio_analysis_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioAnalysisMode"))

    @audio_analysis_mode.setter
    def audio_analysis_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd082d360b16eaf74b374b0253738554ac685bc145d88aa402d656590efd47b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioAnalysisMode", value)

    @builtins.property
    @jsii.member(jsii_name="audioLanguage")
    def audio_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioLanguage"))

    @audio_language.setter
    def audio_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a57824460c1121ea78e5d8968903fcc20738f54e058af73d6f0ff4fdcacce6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="insightsType")
    def insights_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insightsType"))

    @insights_type.setter
    def insights_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b059fe9fac3b9147ece6eac4638aa137dbec22b481310e4707a0f97ea9cf9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaTransformOutputVideoAnalyzerPreset]:
        return typing.cast(typing.Optional[MediaTransformOutputVideoAnalyzerPreset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaTransformOutputVideoAnalyzerPreset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881c3d50817b9e2442aed3ae97a01f7998ebcffd13b2200569e06c177352c83a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MediaTransformTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#create MediaTransform#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#delete MediaTransform#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#read MediaTransform#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#update MediaTransform#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e43fd1b703a56fc20bc768a0e7bce6dea3287e74430531f0e92c599aeddb818)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#create MediaTransform#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#delete MediaTransform#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#read MediaTransform#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_transform#update MediaTransform#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaTransformTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaTransformTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaTransform.MediaTransformTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44d1510a9dad2d32571f2a0a58a967146d7ca8a5e44a1196823c610994557a37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d840edc49ea910bbe1c70bca8273605df6f1f1181a00d3f967d9e3cb453e8db2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8199f8eb674c4e565702cd4419fc3289f16065c22c1a2877d6600c85ec469407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e0b423cdf9c4e5831c0ebc9012e376762dbd9fb012e0ef446b6c0e65d07cd51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ebd1d73f32d40163f1fe5d7b1f9a32f163b322085eb417766e9979973cac2a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaTransformTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaTransformTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaTransformTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8c5f7043957b5b658727509151c81a1bfe14f11d2020ef9a582f5bbe84fda4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MediaTransform",
    "MediaTransformConfig",
    "MediaTransformOutput",
    "MediaTransformOutputAudioAnalyzerPreset",
    "MediaTransformOutputAudioAnalyzerPresetOutputReference",
    "MediaTransformOutputBuiltinPreset",
    "MediaTransformOutputBuiltinPresetOutputReference",
    "MediaTransformOutputFaceDetectorPreset",
    "MediaTransformOutputFaceDetectorPresetOutputReference",
    "MediaTransformOutputList",
    "MediaTransformOutputOutputReference",
    "MediaTransformOutputVideoAnalyzerPreset",
    "MediaTransformOutputVideoAnalyzerPresetOutputReference",
    "MediaTransformTimeouts",
    "MediaTransformTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4c41f75eff24819994958b09a36c6e201c83521a2f56558da9c72e6c1092fecb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    media_services_account_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    output: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaTransformOutput, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[MediaTransformTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__aac089d9982f230f82d95ebdb742b3102b62365a83b3986aecb192666f5605a0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaTransformOutput, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c484f553fe83e00cc7ebf3d19380c26db01278d40912d3122273cf5d87a4ef98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765acf3267073be26589e651f5abc8aa1b9ebe6f00d0c2dd01fee2598ac8decb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a64d0fd84d7e7cdb13bbbf9a77362ca775919c44e5f389baff7604ff496577f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612d790c370ef7c1243727283235dc5de0f8207e4ac50898580bcdf405a06082(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16de48379a7915c82c056609e94f7730f02cc6b10d0405f0db65a2579af36cc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d209c9d3caa58f11af5ecf8bd18ddc9bff1f3ac46948505b039466b853b75d7c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    media_services_account_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    output: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaTransformOutput, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[MediaTransformTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666c2c9da913938700dc7a27642e2ad57f50a195b5bb94a8c837c8d76bb13caa(
    *,
    audio_analyzer_preset: typing.Optional[typing.Union[MediaTransformOutputAudioAnalyzerPreset, typing.Dict[builtins.str, typing.Any]]] = None,
    builtin_preset: typing.Optional[typing.Union[MediaTransformOutputBuiltinPreset, typing.Dict[builtins.str, typing.Any]]] = None,
    face_detector_preset: typing.Optional[typing.Union[MediaTransformOutputFaceDetectorPreset, typing.Dict[builtins.str, typing.Any]]] = None,
    on_error_action: typing.Optional[builtins.str] = None,
    relative_priority: typing.Optional[builtins.str] = None,
    video_analyzer_preset: typing.Optional[typing.Union[MediaTransformOutputVideoAnalyzerPreset, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86be4a547b7de35e3afda494aa38b62e654677fcdff205b65dff86815f012de5(
    *,
    audio_analysis_mode: typing.Optional[builtins.str] = None,
    audio_language: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b7d395d1b3f01cb790ac467032c53ffa9ec5ce4c5d360da4f2b991b3a8b77d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65612928c10a6dca460daef87ccf949b480be7328a992cce94e160dcc5f4c4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b9492548862da82bd8cb63c7d8f31f8dae74ec2c02438e53905504a40b8364(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebfb78476aa46c3af4b31d0c08f0f4906badb1955918d4992296705c51407255(
    value: typing.Optional[MediaTransformOutputAudioAnalyzerPreset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0cfa8e191093b2699a78d5eacb297553ab56fbcd29a7002d0f47feefac77b2(
    *,
    preset_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc02c10b96f92dbd42b1e4867b5445b62a5f082b94a254aad7de93633cb3e9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca46e3a1a2b119a67fd3a9df7a632485257928812a7eb25e1bf2eda4eec9be6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c5f4d0cb36a7ef6df80284babe5ce85a6bb15f2343aa9be57a287a12090476(
    value: typing.Optional[MediaTransformOutputBuiltinPreset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c59bd284086270465237bf3fd3a92dcc4058494fffeee893f3de6bade87935c(
    *,
    analysis_resolution: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0c631f840d38c32d0e610f614c22be53a7272a95389d831392f2fa43ddffd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1db3e523de183b9f9fa92fb1205b76ea7168ed14ed188ef3c002688eedb783(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb4155e3f3339515d1ccf85655135e9c64762332528a9ef97fa82ac3371abdc(
    value: typing.Optional[MediaTransformOutputFaceDetectorPreset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9317d382df1ad8258ff57d6871121b80fb035c98bd4801c9b19a27204f83a2e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1441d9de76bfa2c71300f6f681987187350e3cc8a8964886d7b039986a6ca5e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26285451211fb4312004f4c366e60eba513d2cac63e7f94d5d0848a78066b300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e0a546320d11a4b1e336ba244ce3ef08c04d643dfca8dc2c9a0f525c1ca0a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9495279790ab8749bc4f493ea18cb893f7cfb80f5fa56125c3d18f7e394f5842(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238c880f727f4e248192e062f420d9b65f16c8eeecee50297408cde591f7bf1f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaTransformOutput]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91bd6a33c37bb09f019110b2d711d588d130f4ff4aa13d9ae44bb8f7fa19af48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2b52788bfb52c59c765e93837dd3322f5b6385f2acb62c10e7417eb1621019(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f09cd0fcfd254e31c1e3dee7525a0411b00cbd866d45828cf85383fc67c7b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f4e0b3413e107129052b78146364562f08f8efbd59c8a649d1f81919a0795f(
    value: typing.Optional[typing.Union[MediaTransformOutput, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21d4da6e7f3bdf0c69bad3f28be58309cea877c7882b3ea9c5c9aaddbab0cf3(
    *,
    audio_analysis_mode: typing.Optional[builtins.str] = None,
    audio_language: typing.Optional[builtins.str] = None,
    insights_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7b71787ab213f88aeb08caebb759ba4d0f4294809be57ede57b675db5a966b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd082d360b16eaf74b374b0253738554ac685bc145d88aa402d656590efd47b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a57824460c1121ea78e5d8968903fcc20738f54e058af73d6f0ff4fdcacce6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b059fe9fac3b9147ece6eac4638aa137dbec22b481310e4707a0f97ea9cf9bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881c3d50817b9e2442aed3ae97a01f7998ebcffd13b2200569e06c177352c83a(
    value: typing.Optional[MediaTransformOutputVideoAnalyzerPreset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e43fd1b703a56fc20bc768a0e7bce6dea3287e74430531f0e92c599aeddb818(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d1510a9dad2d32571f2a0a58a967146d7ca8a5e44a1196823c610994557a37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d840edc49ea910bbe1c70bca8273605df6f1f1181a00d3f967d9e3cb453e8db2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8199f8eb674c4e565702cd4419fc3289f16065c22c1a2877d6600c85ec469407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0b423cdf9c4e5831c0ebc9012e376762dbd9fb012e0ef446b6c0e65d07cd51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebd1d73f32d40163f1fe5d7b1f9a32f163b322085eb417766e9979973cac2a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8c5f7043957b5b658727509151c81a1bfe14f11d2020ef9a582f5bbe84fda4(
    value: typing.Optional[typing.Union[MediaTransformTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
