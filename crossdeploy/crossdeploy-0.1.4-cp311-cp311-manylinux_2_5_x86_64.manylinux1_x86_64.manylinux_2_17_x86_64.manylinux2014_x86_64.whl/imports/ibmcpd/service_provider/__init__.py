'''
# `ibmcpd_service_provider`

Refer to the Terraform Registory for docs: [`ibmcpd_service_provider`](https://www.terraform.io/docs/providers/ibmcpd/r/service_provider).
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

import crossdeploy.cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ServiceProvider(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="ibmcpd.serviceProvider.ServiceProvider",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider ibmcpd_service_provider}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        operational_space_id: builtins.str,
        service_type: builtins.str,
        aws_access_key_id: typing.Optional[builtins.str] = None,
        aws_region: typing.Optional[builtins.str] = None,
        aws_secret_access_key: typing.Optional[builtins.str] = None,
        cpd_api_key: typing.Optional[builtins.str] = None,
        cpd_url: typing.Optional[builtins.str] = None,
        cpd_user_name: typing.Optional[builtins.str] = None,
        deployment_space_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider ibmcpd_service_provider} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#name ServiceProvider#name}.
        :param operational_space_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#operational_space_id ServiceProvider#operational_space_id}.
        :param service_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#service_type ServiceProvider#service_type}.
        :param aws_access_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#aws_access_key_id ServiceProvider#aws_access_key_id}.
        :param aws_region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#aws_region ServiceProvider#aws_region}.
        :param aws_secret_access_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#aws_secret_access_key ServiceProvider#aws_secret_access_key}.
        :param cpd_api_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#cpd_api_key ServiceProvider#cpd_api_key}.
        :param cpd_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#cpd_url ServiceProvider#cpd_url}.
        :param cpd_user_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#cpd_user_name ServiceProvider#cpd_user_name}.
        :param deployment_space_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#deployment_space_id ServiceProvider#deployment_space_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__920fcbda6914b7921ceef9564de59f7b2635e644be1d79d63674cc49447ca8f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ServiceProviderConfig(
            name=name,
            operational_space_id=operational_space_id,
            service_type=service_type,
            aws_access_key_id=aws_access_key_id,
            aws_region=aws_region,
            aws_secret_access_key=aws_secret_access_key,
            cpd_api_key=cpd_api_key,
            cpd_url=cpd_url,
            cpd_user_name=cpd_user_name,
            deployment_space_id=deployment_space_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAwsAccessKeyId")
    def reset_aws_access_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccessKeyId", []))

    @jsii.member(jsii_name="resetAwsRegion")
    def reset_aws_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegion", []))

    @jsii.member(jsii_name="resetAwsSecretAccessKey")
    def reset_aws_secret_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsSecretAccessKey", []))

    @jsii.member(jsii_name="resetCpdApiKey")
    def reset_cpd_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpdApiKey", []))

    @jsii.member(jsii_name="resetCpdUrl")
    def reset_cpd_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpdUrl", []))

    @jsii.member(jsii_name="resetCpdUserName")
    def reset_cpd_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpdUserName", []))

    @jsii.member(jsii_name="resetDeploymentSpaceId")
    def reset_deployment_space_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentSpaceId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="awsAccessKeyIdInput")
    def aws_access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegionInput")
    def aws_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="awsSecretAccessKeyInput")
    def aws_secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsSecretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="cpdApiKeyInput")
    def cpd_api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpdApiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="cpdUrlInput")
    def cpd_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpdUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="cpdUserNameInput")
    def cpd_user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpdUserNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentSpaceIdInput")
    def deployment_space_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentSpaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="operationalSpaceIdInput")
    def operational_space_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationalSpaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTypeInput")
    def service_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccessKeyId")
    def aws_access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccessKeyId"))

    @aws_access_key_id.setter
    def aws_access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8c8d392c40d868548fc5828b16d623687c9e8eb6526c72ee36b68fbc62a00e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccessKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ec2cfe79f0b682263e989748f59394617fb2b8b27ec64f288f8255b908ff78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value)

    @builtins.property
    @jsii.member(jsii_name="awsSecretAccessKey")
    def aws_secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsSecretAccessKey"))

    @aws_secret_access_key.setter
    def aws_secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407aeb5c9739e354be6546982238fffe584c0410c82ad5507b0e3c8c2b9ae570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsSecretAccessKey", value)

    @builtins.property
    @jsii.member(jsii_name="cpdApiKey")
    def cpd_api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpdApiKey"))

    @cpd_api_key.setter
    def cpd_api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db683066de4657f05be15645adda091c0be80b6e727331e0c6a71489089ba722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpdApiKey", value)

    @builtins.property
    @jsii.member(jsii_name="cpdUrl")
    def cpd_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpdUrl"))

    @cpd_url.setter
    def cpd_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db8ba486c647adb515f72d46c24941020fe97377ea8acee45478018790463b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpdUrl", value)

    @builtins.property
    @jsii.member(jsii_name="cpdUserName")
    def cpd_user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpdUserName"))

    @cpd_user_name.setter
    def cpd_user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2a5b36ba081175ad4862984d195ff4235c6def5487505636ca66e08502fdfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpdUserName", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentSpaceId")
    def deployment_space_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentSpaceId"))

    @deployment_space_id.setter
    def deployment_space_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7c882b022c695835a6435ddf07d95fcaffcba976603dd60b150854271e4466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentSpaceId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcc1e49142d1cc9500cf82ee7708fa776635cc3bbbf60f233107f3a9da8635a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="operationalSpaceId")
    def operational_space_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationalSpaceId"))

    @operational_space_id.setter
    def operational_space_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68d88c6eb63c2e04c7783b8004d58c8c934fa685e1fa39e4b8e35512f655aea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationalSpaceId", value)

    @builtins.property
    @jsii.member(jsii_name="serviceType")
    def service_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceType"))

    @service_type.setter
    def service_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cf08b190706a5b06b5309f7ce2c22c77d64fd4d3ee3d14caa1ecfb4a82f56fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceType", value)


@jsii.data_type(
    jsii_type="ibmcpd.serviceProvider.ServiceProviderConfig",
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
        "operational_space_id": "operationalSpaceId",
        "service_type": "serviceType",
        "aws_access_key_id": "awsAccessKeyId",
        "aws_region": "awsRegion",
        "aws_secret_access_key": "awsSecretAccessKey",
        "cpd_api_key": "cpdApiKey",
        "cpd_url": "cpdUrl",
        "cpd_user_name": "cpdUserName",
        "deployment_space_id": "deploymentSpaceId",
    },
)
class ServiceProviderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        operational_space_id: builtins.str,
        service_type: builtins.str,
        aws_access_key_id: typing.Optional[builtins.str] = None,
        aws_region: typing.Optional[builtins.str] = None,
        aws_secret_access_key: typing.Optional[builtins.str] = None,
        cpd_api_key: typing.Optional[builtins.str] = None,
        cpd_url: typing.Optional[builtins.str] = None,
        cpd_user_name: typing.Optional[builtins.str] = None,
        deployment_space_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#name ServiceProvider#name}.
        :param operational_space_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#operational_space_id ServiceProvider#operational_space_id}.
        :param service_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#service_type ServiceProvider#service_type}.
        :param aws_access_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#aws_access_key_id ServiceProvider#aws_access_key_id}.
        :param aws_region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#aws_region ServiceProvider#aws_region}.
        :param aws_secret_access_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#aws_secret_access_key ServiceProvider#aws_secret_access_key}.
        :param cpd_api_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#cpd_api_key ServiceProvider#cpd_api_key}.
        :param cpd_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#cpd_url ServiceProvider#cpd_url}.
        :param cpd_user_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#cpd_user_name ServiceProvider#cpd_user_name}.
        :param deployment_space_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#deployment_space_id ServiceProvider#deployment_space_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72430ed49090b77f4eaa28410fa45ba175f541d40b4c118338d6d464cc81e7a9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument operational_space_id", value=operational_space_id, expected_type=type_hints["operational_space_id"])
            check_type(argname="argument service_type", value=service_type, expected_type=type_hints["service_type"])
            check_type(argname="argument aws_access_key_id", value=aws_access_key_id, expected_type=type_hints["aws_access_key_id"])
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            check_type(argname="argument aws_secret_access_key", value=aws_secret_access_key, expected_type=type_hints["aws_secret_access_key"])
            check_type(argname="argument cpd_api_key", value=cpd_api_key, expected_type=type_hints["cpd_api_key"])
            check_type(argname="argument cpd_url", value=cpd_url, expected_type=type_hints["cpd_url"])
            check_type(argname="argument cpd_user_name", value=cpd_user_name, expected_type=type_hints["cpd_user_name"])
            check_type(argname="argument deployment_space_id", value=deployment_space_id, expected_type=type_hints["deployment_space_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "operational_space_id": operational_space_id,
            "service_type": service_type,
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
        if aws_access_key_id is not None:
            self._values["aws_access_key_id"] = aws_access_key_id
        if aws_region is not None:
            self._values["aws_region"] = aws_region
        if aws_secret_access_key is not None:
            self._values["aws_secret_access_key"] = aws_secret_access_key
        if cpd_api_key is not None:
            self._values["cpd_api_key"] = cpd_api_key
        if cpd_url is not None:
            self._values["cpd_url"] = cpd_url
        if cpd_user_name is not None:
            self._values["cpd_user_name"] = cpd_user_name
        if deployment_space_id is not None:
            self._values["deployment_space_id"] = deployment_space_id

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#name ServiceProvider#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operational_space_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#operational_space_id ServiceProvider#operational_space_id}.'''
        result = self._values.get("operational_space_id")
        assert result is not None, "Required property 'operational_space_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#service_type ServiceProvider#service_type}.'''
        result = self._values.get("service_type")
        assert result is not None, "Required property 'service_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_access_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#aws_access_key_id ServiceProvider#aws_access_key_id}.'''
        result = self._values.get("aws_access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#aws_region ServiceProvider#aws_region}.'''
        result = self._values.get("aws_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_secret_access_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#aws_secret_access_key ServiceProvider#aws_secret_access_key}.'''
        result = self._values.get("aws_secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpd_api_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#cpd_api_key ServiceProvider#cpd_api_key}.'''
        result = self._values.get("cpd_api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpd_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#cpd_url ServiceProvider#cpd_url}.'''
        result = self._values.get("cpd_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpd_user_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#cpd_user_name ServiceProvider#cpd_user_name}.'''
        result = self._values.get("cpd_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_space_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/ibmcpd/r/service_provider#deployment_space_id ServiceProvider#deployment_space_id}.'''
        result = self._values.get("deployment_space_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ServiceProvider",
    "ServiceProviderConfig",
]

publication.publish()

def _typecheckingstub__920fcbda6914b7921ceef9564de59f7b2635e644be1d79d63674cc49447ca8f8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    operational_space_id: builtins.str,
    service_type: builtins.str,
    aws_access_key_id: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
    aws_secret_access_key: typing.Optional[builtins.str] = None,
    cpd_api_key: typing.Optional[builtins.str] = None,
    cpd_url: typing.Optional[builtins.str] = None,
    cpd_user_name: typing.Optional[builtins.str] = None,
    deployment_space_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d8c8d392c40d868548fc5828b16d623687c9e8eb6526c72ee36b68fbc62a00e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ec2cfe79f0b682263e989748f59394617fb2b8b27ec64f288f8255b908ff78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407aeb5c9739e354be6546982238fffe584c0410c82ad5507b0e3c8c2b9ae570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db683066de4657f05be15645adda091c0be80b6e727331e0c6a71489089ba722(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db8ba486c647adb515f72d46c24941020fe97377ea8acee45478018790463b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2a5b36ba081175ad4862984d195ff4235c6def5487505636ca66e08502fdfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7c882b022c695835a6435ddf07d95fcaffcba976603dd60b150854271e4466(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcc1e49142d1cc9500cf82ee7708fa776635cc3bbbf60f233107f3a9da8635a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68d88c6eb63c2e04c7783b8004d58c8c934fa685e1fa39e4b8e35512f655aea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf08b190706a5b06b5309f7ce2c22c77d64fd4d3ee3d14caa1ecfb4a82f56fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72430ed49090b77f4eaa28410fa45ba175f541d40b4c118338d6d464cc81e7a9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    operational_space_id: builtins.str,
    service_type: builtins.str,
    aws_access_key_id: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
    aws_secret_access_key: typing.Optional[builtins.str] = None,
    cpd_api_key: typing.Optional[builtins.str] = None,
    cpd_url: typing.Optional[builtins.str] = None,
    cpd_user_name: typing.Optional[builtins.str] = None,
    deployment_space_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
