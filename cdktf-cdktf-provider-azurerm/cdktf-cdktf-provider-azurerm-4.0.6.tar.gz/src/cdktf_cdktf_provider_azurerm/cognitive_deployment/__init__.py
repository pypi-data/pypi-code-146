'''
# `azurerm_cognitive_deployment`

Refer to the Terraform Registory for docs: [`azurerm_cognitive_deployment`](https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment).
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


class CognitiveDeployment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cognitiveDeployment.CognitiveDeployment",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment azurerm_cognitive_deployment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cognitive_account_id: builtins.str,
        model: typing.Union["CognitiveDeploymentModel", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        scale: typing.Union["CognitiveDeploymentScale", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        rai_policy_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CognitiveDeploymentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment azurerm_cognitive_deployment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cognitive_account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#cognitive_account_id CognitiveDeployment#cognitive_account_id}.
        :param model: model block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#model CognitiveDeployment#model}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#name CognitiveDeployment#name}.
        :param scale: scale block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#scale CognitiveDeployment#scale}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#id CognitiveDeployment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rai_policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#rai_policy_name CognitiveDeployment#rai_policy_name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#timeouts CognitiveDeployment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc0df905395a4df7f17fc4c47db099cf93c96ead383502e535fe49a9f89260a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CognitiveDeploymentConfig(
            cognitive_account_id=cognitive_account_id,
            model=model,
            name=name,
            scale=scale,
            id=id,
            rai_policy_name=rai_policy_name,
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

    @jsii.member(jsii_name="putModel")
    def put_model(
        self,
        *,
        format: builtins.str,
        name: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#format CognitiveDeployment#format}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#name CognitiveDeployment#name}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#version CognitiveDeployment#version}.
        '''
        value = CognitiveDeploymentModel(format=format, name=name, version=version)

        return typing.cast(None, jsii.invoke(self, "putModel", [value]))

    @jsii.member(jsii_name="putScale")
    def put_scale(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#type CognitiveDeployment#type}.
        '''
        value = CognitiveDeploymentScale(type=type)

        return typing.cast(None, jsii.invoke(self, "putScale", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#create CognitiveDeployment#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#delete CognitiveDeployment#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#read CognitiveDeployment#read}.
        '''
        value = CognitiveDeploymentTimeouts(create=create, delete=delete, read=read)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRaiPolicyName")
    def reset_rai_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRaiPolicyName", []))

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
    @jsii.member(jsii_name="model")
    def model(self) -> "CognitiveDeploymentModelOutputReference":
        return typing.cast("CognitiveDeploymentModelOutputReference", jsii.get(self, "model"))

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> "CognitiveDeploymentScaleOutputReference":
        return typing.cast("CognitiveDeploymentScaleOutputReference", jsii.get(self, "scale"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CognitiveDeploymentTimeoutsOutputReference":
        return typing.cast("CognitiveDeploymentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cognitiveAccountIdInput")
    def cognitive_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cognitiveAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="modelInput")
    def model_input(self) -> typing.Optional["CognitiveDeploymentModel"]:
        return typing.cast(typing.Optional["CognitiveDeploymentModel"], jsii.get(self, "modelInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="raiPolicyNameInput")
    def rai_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "raiPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleInput")
    def scale_input(self) -> typing.Optional["CognitiveDeploymentScale"]:
        return typing.cast(typing.Optional["CognitiveDeploymentScale"], jsii.get(self, "scaleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["CognitiveDeploymentTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["CognitiveDeploymentTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cognitiveAccountId")
    def cognitive_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cognitiveAccountId"))

    @cognitive_account_id.setter
    def cognitive_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf09e34b76658e416eccfc1b860575d844057ace0eb30e1cfc34cee0227486c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cognitiveAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b78e52b2c2a97b702d97c8ec91b2ea206e4b752415cd02fbde48aeed57c91a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d89d588eeb958e537c873bca83e590bd41c14c671d84aad319ada5f2668092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="raiPolicyName")
    def rai_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "raiPolicyName"))

    @rai_policy_name.setter
    def rai_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf82805661f8f2b70ef46223cb3afd824549c009c811699b13b8f939dfb7c54e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "raiPolicyName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cognitiveDeployment.CognitiveDeploymentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cognitive_account_id": "cognitiveAccountId",
        "model": "model",
        "name": "name",
        "scale": "scale",
        "id": "id",
        "rai_policy_name": "raiPolicyName",
        "timeouts": "timeouts",
    },
)
class CognitiveDeploymentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cognitive_account_id: builtins.str,
        model: typing.Union["CognitiveDeploymentModel", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        scale: typing.Union["CognitiveDeploymentScale", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        rai_policy_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CognitiveDeploymentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cognitive_account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#cognitive_account_id CognitiveDeployment#cognitive_account_id}.
        :param model: model block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#model CognitiveDeployment#model}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#name CognitiveDeployment#name}.
        :param scale: scale block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#scale CognitiveDeployment#scale}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#id CognitiveDeployment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rai_policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#rai_policy_name CognitiveDeployment#rai_policy_name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#timeouts CognitiveDeployment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(model, dict):
            model = CognitiveDeploymentModel(**model)
        if isinstance(scale, dict):
            scale = CognitiveDeploymentScale(**scale)
        if isinstance(timeouts, dict):
            timeouts = CognitiveDeploymentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54baca5740a798f42b2f0780582d1d23b6d328b4af7d815eaf65ea5a55991dca)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cognitive_account_id", value=cognitive_account_id, expected_type=type_hints["cognitive_account_id"])
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument scale", value=scale, expected_type=type_hints["scale"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rai_policy_name", value=rai_policy_name, expected_type=type_hints["rai_policy_name"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cognitive_account_id": cognitive_account_id,
            "model": model,
            "name": name,
            "scale": scale,
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
        if rai_policy_name is not None:
            self._values["rai_policy_name"] = rai_policy_name
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
    def cognitive_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#cognitive_account_id CognitiveDeployment#cognitive_account_id}.'''
        result = self._values.get("cognitive_account_id")
        assert result is not None, "Required property 'cognitive_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def model(self) -> "CognitiveDeploymentModel":
        '''model block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#model CognitiveDeployment#model}
        '''
        result = self._values.get("model")
        assert result is not None, "Required property 'model' is missing"
        return typing.cast("CognitiveDeploymentModel", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#name CognitiveDeployment#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scale(self) -> "CognitiveDeploymentScale":
        '''scale block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#scale CognitiveDeployment#scale}
        '''
        result = self._values.get("scale")
        assert result is not None, "Required property 'scale' is missing"
        return typing.cast("CognitiveDeploymentScale", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#id CognitiveDeployment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rai_policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#rai_policy_name CognitiveDeployment#rai_policy_name}.'''
        result = self._values.get("rai_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CognitiveDeploymentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#timeouts CognitiveDeployment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CognitiveDeploymentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitiveDeploymentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cognitiveDeployment.CognitiveDeploymentModel",
    jsii_struct_bases=[],
    name_mapping={"format": "format", "name": "name", "version": "version"},
)
class CognitiveDeploymentModel:
    def __init__(
        self,
        *,
        format: builtins.str,
        name: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#format CognitiveDeployment#format}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#name CognitiveDeployment#name}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#version CognitiveDeployment#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04563fed4f3120562cfc7e7d5ab384db95d5075c21e3f7f061d3f7bf7d91685b)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "format": format,
            "name": name,
            "version": version,
        }

    @builtins.property
    def format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#format CognitiveDeployment#format}.'''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#name CognitiveDeployment#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#version CognitiveDeployment#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitiveDeploymentModel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitiveDeploymentModelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cognitiveDeployment.CognitiveDeploymentModelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0687fba75099900044fcbfb358fc28a37bed9c8807eed9078447e042cd4ea13f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c845da984c00a39006b2bb6a5849005670937a720196a71ed26e48e0fef1b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b62c0ceb03b938fc6dc29b6d3cd4f04da917abe2467146962732426f3bc43013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4077b79a162ba43875bb14e207e92283d4375a135f7a965262d6f86e71c426b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitiveDeploymentModel]:
        return typing.cast(typing.Optional[CognitiveDeploymentModel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CognitiveDeploymentModel]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed10e97bbf525c16afcb5bab00ac38dd63edd17b5afc25646473f99a6e89db0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cognitiveDeployment.CognitiveDeploymentScale",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class CognitiveDeploymentScale:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#type CognitiveDeployment#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5012a2d95fd24d694933764d6f41cc4559c0a2cee4a02ff14427b0e378a8851)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#type CognitiveDeployment#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitiveDeploymentScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitiveDeploymentScaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cognitiveDeployment.CognitiveDeploymentScaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42a16b99cf2a43db2430b1bc0ccc7c77d67bcf0266c5128ffcebb772fe4bdb28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb75087610f734a0e0480ab7a03a0ccd49bfe9f2ef7434b2f66637c194a3d08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CognitiveDeploymentScale]:
        return typing.cast(typing.Optional[CognitiveDeploymentScale], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CognitiveDeploymentScale]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b460bf3f643aa3c9a777e6cac603cf8aa20835782d8789cae97d062a1c651e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cognitiveDeployment.CognitiveDeploymentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class CognitiveDeploymentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#create CognitiveDeployment#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#delete CognitiveDeployment#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#read CognitiveDeployment#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d94199ea8083c5cb08d03da87fc49bfdeac3d4a97d5ad0dc23387b6677cf9c25)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#create CognitiveDeployment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#delete CognitiveDeployment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/cognitive_deployment#read CognitiveDeployment#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitiveDeploymentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CognitiveDeploymentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cognitiveDeployment.CognitiveDeploymentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3be21705c9d39cf8ca7697c181c194374bfdc16eaa9eaac2df9b9e81352ca5e)
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
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f5b26ba59a2e82aa98a55b6574870b302a173076ba71e3d2f681b76e0b48f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b62fa53f99b29ea76e549309937727196269d5c3bf609b3f34e983684ed4b49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77ba61e5353977cdef32f9f97a10345d6db2620efb452f31d1cb09cc0748c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CognitiveDeploymentTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CognitiveDeploymentTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CognitiveDeploymentTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9e25a839d131981a3809045f43256303c15db9803ea4094a208fd3a6ddd496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CognitiveDeployment",
    "CognitiveDeploymentConfig",
    "CognitiveDeploymentModel",
    "CognitiveDeploymentModelOutputReference",
    "CognitiveDeploymentScale",
    "CognitiveDeploymentScaleOutputReference",
    "CognitiveDeploymentTimeouts",
    "CognitiveDeploymentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4bc0df905395a4df7f17fc4c47db099cf93c96ead383502e535fe49a9f89260a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cognitive_account_id: builtins.str,
    model: typing.Union[CognitiveDeploymentModel, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    scale: typing.Union[CognitiveDeploymentScale, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    rai_policy_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CognitiveDeploymentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0bf09e34b76658e416eccfc1b860575d844057ace0eb30e1cfc34cee0227486c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b78e52b2c2a97b702d97c8ec91b2ea206e4b752415cd02fbde48aeed57c91a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d89d588eeb958e537c873bca83e590bd41c14c671d84aad319ada5f2668092(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf82805661f8f2b70ef46223cb3afd824549c009c811699b13b8f939dfb7c54e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54baca5740a798f42b2f0780582d1d23b6d328b4af7d815eaf65ea5a55991dca(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cognitive_account_id: builtins.str,
    model: typing.Union[CognitiveDeploymentModel, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    scale: typing.Union[CognitiveDeploymentScale, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    rai_policy_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CognitiveDeploymentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04563fed4f3120562cfc7e7d5ab384db95d5075c21e3f7f061d3f7bf7d91685b(
    *,
    format: builtins.str,
    name: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0687fba75099900044fcbfb358fc28a37bed9c8807eed9078447e042cd4ea13f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c845da984c00a39006b2bb6a5849005670937a720196a71ed26e48e0fef1b19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62c0ceb03b938fc6dc29b6d3cd4f04da917abe2467146962732426f3bc43013(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4077b79a162ba43875bb14e207e92283d4375a135f7a965262d6f86e71c426b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed10e97bbf525c16afcb5bab00ac38dd63edd17b5afc25646473f99a6e89db0(
    value: typing.Optional[CognitiveDeploymentModel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5012a2d95fd24d694933764d6f41cc4559c0a2cee4a02ff14427b0e378a8851(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a16b99cf2a43db2430b1bc0ccc7c77d67bcf0266c5128ffcebb772fe4bdb28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb75087610f734a0e0480ab7a03a0ccd49bfe9f2ef7434b2f66637c194a3d08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b460bf3f643aa3c9a777e6cac603cf8aa20835782d8789cae97d062a1c651e6(
    value: typing.Optional[CognitiveDeploymentScale],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94199ea8083c5cb08d03da87fc49bfdeac3d4a97d5ad0dc23387b6677cf9c25(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3be21705c9d39cf8ca7697c181c194374bfdc16eaa9eaac2df9b9e81352ca5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f5b26ba59a2e82aa98a55b6574870b302a173076ba71e3d2f681b76e0b48f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b62fa53f99b29ea76e549309937727196269d5c3bf609b3f34e983684ed4b49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77ba61e5353977cdef32f9f97a10345d6db2620efb452f31d1cb09cc0748c20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9e25a839d131981a3809045f43256303c15db9803ea4094a208fd3a6ddd496(
    value: typing.Optional[typing.Union[CognitiveDeploymentTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
