'''
# `aws_api_gateway_rest_api`

Refer to the Terraform Registory for docs: [`aws_api_gateway_rest_api`](https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api).
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


class ApiGatewayRestApi(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.apiGatewayRestApi.ApiGatewayRestApi",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api aws_api_gateway_rest_api}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        api_key_source: typing.Optional[builtins.str] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        body: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_configuration: typing.Optional[typing.Union["ApiGatewayRestApiEndpointConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        policy: typing.Optional[builtins.str] = None,
        put_rest_api_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api aws_api_gateway_rest_api} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#name ApiGatewayRestApi#name}.
        :param api_key_source: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#api_key_source ApiGatewayRestApi#api_key_source}.
        :param binary_media_types: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#binary_media_types ApiGatewayRestApi#binary_media_types}.
        :param body: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#body ApiGatewayRestApi#body}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#description ApiGatewayRestApi#description}.
        :param disable_execute_api_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#disable_execute_api_endpoint ApiGatewayRestApi#disable_execute_api_endpoint}.
        :param endpoint_configuration: endpoint_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#endpoint_configuration ApiGatewayRestApi#endpoint_configuration}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#id ApiGatewayRestApi#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimum_compression_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#minimum_compression_size ApiGatewayRestApi#minimum_compression_size}.
        :param parameters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#parameters ApiGatewayRestApi#parameters}.
        :param policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#policy ApiGatewayRestApi#policy}.
        :param put_rest_api_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#put_rest_api_mode ApiGatewayRestApi#put_rest_api_mode}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#tags ApiGatewayRestApi#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#tags_all ApiGatewayRestApi#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047ddcdb661a9ebf8512356870681d53a887f5ef5e806abdced5be2bc2176a88)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiGatewayRestApiConfig(
            name=name,
            api_key_source=api_key_source,
            binary_media_types=binary_media_types,
            body=body,
            description=description,
            disable_execute_api_endpoint=disable_execute_api_endpoint,
            endpoint_configuration=endpoint_configuration,
            id=id,
            minimum_compression_size=minimum_compression_size,
            parameters=parameters,
            policy=policy,
            put_rest_api_mode=put_rest_api_mode,
            tags=tags,
            tags_all=tags_all,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putEndpointConfiguration")
    def put_endpoint_configuration(
        self,
        *,
        types: typing.Sequence[builtins.str],
        vpc_endpoint_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param types: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#types ApiGatewayRestApi#types}.
        :param vpc_endpoint_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#vpc_endpoint_ids ApiGatewayRestApi#vpc_endpoint_ids}.
        '''
        value = ApiGatewayRestApiEndpointConfiguration(
            types=types, vpc_endpoint_ids=vpc_endpoint_ids
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointConfiguration", [value]))

    @jsii.member(jsii_name="resetApiKeySource")
    def reset_api_key_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKeySource", []))

    @jsii.member(jsii_name="resetBinaryMediaTypes")
    def reset_binary_media_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryMediaTypes", []))

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisableExecuteApiEndpoint")
    def reset_disable_execute_api_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableExecuteApiEndpoint", []))

    @jsii.member(jsii_name="resetEndpointConfiguration")
    def reset_endpoint_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinimumCompressionSize")
    def reset_minimum_compression_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumCompressionSize", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @jsii.member(jsii_name="resetPutRestApiMode")
    def reset_put_rest_api_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPutRestApiMode", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="createdDate")
    def created_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdDate"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfiguration")
    def endpoint_configuration(
        self,
    ) -> "ApiGatewayRestApiEndpointConfigurationOutputReference":
        return typing.cast("ApiGatewayRestApiEndpointConfigurationOutputReference", jsii.get(self, "endpointConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="executionArn")
    def execution_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionArn"))

    @builtins.property
    @jsii.member(jsii_name="rootResourceId")
    def root_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootResourceId"))

    @builtins.property
    @jsii.member(jsii_name="apiKeySourceInput")
    def api_key_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryMediaTypesInput")
    def binary_media_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "binaryMediaTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableExecuteApiEndpointInput")
    def disable_execute_api_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableExecuteApiEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfigurationInput")
    def endpoint_configuration_input(
        self,
    ) -> typing.Optional["ApiGatewayRestApiEndpointConfiguration"]:
        return typing.cast(typing.Optional["ApiGatewayRestApiEndpointConfiguration"], jsii.get(self, "endpointConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumCompressionSizeInput")
    def minimum_compression_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumCompressionSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="putRestApiModeInput")
    def put_rest_api_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "putRestApiModeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKeySource")
    def api_key_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKeySource"))

    @api_key_source.setter
    def api_key_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391a8afc3392c54a1ef1c084b3bcff4ff36414206f5b70a5d12826f13e744152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeySource", value)

    @builtins.property
    @jsii.member(jsii_name="binaryMediaTypes")
    def binary_media_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "binaryMediaTypes"))

    @binary_media_types.setter
    def binary_media_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f8a7d536d56b7c1a6f177f8bde53329182ee58c49d225c0a936eed6a93959f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryMediaTypes", value)

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @body.setter
    def body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d4cd988cb5426e469fab7ff5316fcafdd5372baaeea4ae752e93bc996b30e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3cf016b67fd974e6b62345a3399dc1eaf4c5417009233491409b9730aaefbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="disableExecuteApiEndpoint")
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableExecuteApiEndpoint"))

    @disable_execute_api_endpoint.setter
    def disable_execute_api_endpoint(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b420538fae927046b9eae6e82b6b1f668c16f1ebd5a27f20015cc356a8afedb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableExecuteApiEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65751b36c3f99a2e3deceebdf9613c9dc2c82efd70b3d53632dbf66d853bf58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="minimumCompressionSize")
    def minimum_compression_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumCompressionSize"))

    @minimum_compression_size.setter
    def minimum_compression_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb28c68bf887a2b7f2d19807ca165fb4224246514e7a235471498a0545ae46f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumCompressionSize", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2640b8f28723d4da9eeca458d84e9d702ca4b9ee4b357d7d9be645bcc2ff9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbf4b99d8bfcb7559e4c9eeaa5a502f4b84e023b7d6d3b6b6c6c2b6759fc445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2905f0f85a0c3808a82ff95e5761ec164bc009e644c654aa2680868c44edaf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="putRestApiMode")
    def put_rest_api_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "putRestApiMode"))

    @put_rest_api_mode.setter
    def put_rest_api_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f22ebdb1cf88d8b71000f83ea6d79ecd71b5d17948ef8cd2ccfaa70591f09c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "putRestApiMode", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009e9a98eb92260d94450fc1f4d29dc763d77b52b5ca17bbeae3be3fd6b28f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887e33814e96af0ae6cd7e727b292c64849b5db79036bef015fc8eb3382ac367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.apiGatewayRestApi.ApiGatewayRestApiConfig",
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
        "api_key_source": "apiKeySource",
        "binary_media_types": "binaryMediaTypes",
        "body": "body",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
        "endpoint_configuration": "endpointConfiguration",
        "id": "id",
        "minimum_compression_size": "minimumCompressionSize",
        "parameters": "parameters",
        "policy": "policy",
        "put_rest_api_mode": "putRestApiMode",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class ApiGatewayRestApiConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_key_source: typing.Optional[builtins.str] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        body: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_configuration: typing.Optional[typing.Union["ApiGatewayRestApiEndpointConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        policy: typing.Optional[builtins.str] = None,
        put_rest_api_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#name ApiGatewayRestApi#name}.
        :param api_key_source: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#api_key_source ApiGatewayRestApi#api_key_source}.
        :param binary_media_types: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#binary_media_types ApiGatewayRestApi#binary_media_types}.
        :param body: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#body ApiGatewayRestApi#body}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#description ApiGatewayRestApi#description}.
        :param disable_execute_api_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#disable_execute_api_endpoint ApiGatewayRestApi#disable_execute_api_endpoint}.
        :param endpoint_configuration: endpoint_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#endpoint_configuration ApiGatewayRestApi#endpoint_configuration}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#id ApiGatewayRestApi#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimum_compression_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#minimum_compression_size ApiGatewayRestApi#minimum_compression_size}.
        :param parameters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#parameters ApiGatewayRestApi#parameters}.
        :param policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#policy ApiGatewayRestApi#policy}.
        :param put_rest_api_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#put_rest_api_mode ApiGatewayRestApi#put_rest_api_mode}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#tags ApiGatewayRestApi#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#tags_all ApiGatewayRestApi#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(endpoint_configuration, dict):
            endpoint_configuration = ApiGatewayRestApiEndpointConfiguration(**endpoint_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8920a9f5ae1485fedff245d3431c6e963b66abd259547b85c1220d89791f59ca)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument api_key_source", value=api_key_source, expected_type=type_hints["api_key_source"])
            check_type(argname="argument binary_media_types", value=binary_media_types, expected_type=type_hints["binary_media_types"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_execute_api_endpoint", value=disable_execute_api_endpoint, expected_type=type_hints["disable_execute_api_endpoint"])
            check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument minimum_compression_size", value=minimum_compression_size, expected_type=type_hints["minimum_compression_size"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument put_rest_api_mode", value=put_rest_api_mode, expected_type=type_hints["put_rest_api_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if api_key_source is not None:
            self._values["api_key_source"] = api_key_source
        if binary_media_types is not None:
            self._values["binary_media_types"] = binary_media_types
        if body is not None:
            self._values["body"] = body
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint
        if endpoint_configuration is not None:
            self._values["endpoint_configuration"] = endpoint_configuration
        if id is not None:
            self._values["id"] = id
        if minimum_compression_size is not None:
            self._values["minimum_compression_size"] = minimum_compression_size
        if parameters is not None:
            self._values["parameters"] = parameters
        if policy is not None:
            self._values["policy"] = policy
        if put_rest_api_mode is not None:
            self._values["put_rest_api_mode"] = put_rest_api_mode
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#name ApiGatewayRestApi#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key_source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#api_key_source ApiGatewayRestApi#api_key_source}.'''
        result = self._values.get("api_key_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#binary_media_types ApiGatewayRestApi#binary_media_types}.'''
        result = self._values.get("binary_media_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def body(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#body ApiGatewayRestApi#body}.'''
        result = self._values.get("body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#description ApiGatewayRestApi#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#disable_execute_api_endpoint ApiGatewayRestApi#disable_execute_api_endpoint}.'''
        result = self._values.get("disable_execute_api_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def endpoint_configuration(
        self,
    ) -> typing.Optional["ApiGatewayRestApiEndpointConfiguration"]:
        '''endpoint_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#endpoint_configuration ApiGatewayRestApi#endpoint_configuration}
        '''
        result = self._values.get("endpoint_configuration")
        return typing.cast(typing.Optional["ApiGatewayRestApiEndpointConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#id ApiGatewayRestApi#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#minimum_compression_size ApiGatewayRestApi#minimum_compression_size}.'''
        result = self._values.get("minimum_compression_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#parameters ApiGatewayRestApi#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#policy ApiGatewayRestApi#policy}.'''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def put_rest_api_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#put_rest_api_mode ApiGatewayRestApi#put_rest_api_mode}.'''
        result = self._values.get("put_rest_api_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#tags ApiGatewayRestApi#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#tags_all ApiGatewayRestApi#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiGatewayRestApiConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.apiGatewayRestApi.ApiGatewayRestApiEndpointConfiguration",
    jsii_struct_bases=[],
    name_mapping={"types": "types", "vpc_endpoint_ids": "vpcEndpointIds"},
)
class ApiGatewayRestApiEndpointConfiguration:
    def __init__(
        self,
        *,
        types: typing.Sequence[builtins.str],
        vpc_endpoint_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param types: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#types ApiGatewayRestApi#types}.
        :param vpc_endpoint_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#vpc_endpoint_ids ApiGatewayRestApi#vpc_endpoint_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1207fa11d7cc06172cc3eeefbbe7b0919ccffce843f6a3f2aba3f0079b5caf39)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
            check_type(argname="argument vpc_endpoint_ids", value=vpc_endpoint_ids, expected_type=type_hints["vpc_endpoint_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "types": types,
        }
        if vpc_endpoint_ids is not None:
            self._values["vpc_endpoint_ids"] = vpc_endpoint_ids

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#types ApiGatewayRestApi#types}.'''
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc_endpoint_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/api_gateway_rest_api#vpc_endpoint_ids ApiGatewayRestApi#vpc_endpoint_ids}.'''
        result = self._values.get("vpc_endpoint_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiGatewayRestApiEndpointConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiGatewayRestApiEndpointConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.apiGatewayRestApi.ApiGatewayRestApiEndpointConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b7ed6091a726b114b303ee359aaabaabc7db5c1d0456acd913ea23a1afc3f76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVpcEndpointIds")
    def reset_vpc_endpoint_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcEndpointIds", []))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointIdsInput")
    def vpc_endpoint_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vpcEndpointIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @types.setter
    def types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13f4de7d4de0034b764d7e4488170dd01ad778bcc894e3583511251ab5bacf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value)

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointIds")
    def vpc_endpoint_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vpcEndpointIds"))

    @vpc_endpoint_ids.setter
    def vpc_endpoint_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ae5f28e0cbdb49e8fe717e9226e33c97dad39b1397cb31e41ba3d95cc163a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcEndpointIds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiGatewayRestApiEndpointConfiguration]:
        return typing.cast(typing.Optional[ApiGatewayRestApiEndpointConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiGatewayRestApiEndpointConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4caf3a11f6fce9c8257efd88ff1e95aafbf57f41927d50f5308fa1e03227d96b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ApiGatewayRestApi",
    "ApiGatewayRestApiConfig",
    "ApiGatewayRestApiEndpointConfiguration",
    "ApiGatewayRestApiEndpointConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__047ddcdb661a9ebf8512356870681d53a887f5ef5e806abdced5be2bc2176a88(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    api_key_source: typing.Optional[builtins.str] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    body: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_configuration: typing.Optional[typing.Union[ApiGatewayRestApiEndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    policy: typing.Optional[builtins.str] = None,
    put_rest_api_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__391a8afc3392c54a1ef1c084b3bcff4ff36414206f5b70a5d12826f13e744152(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f8a7d536d56b7c1a6f177f8bde53329182ee58c49d225c0a936eed6a93959f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4cd988cb5426e469fab7ff5316fcafdd5372baaeea4ae752e93bc996b30e17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3cf016b67fd974e6b62345a3399dc1eaf4c5417009233491409b9730aaefbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b420538fae927046b9eae6e82b6b1f668c16f1ebd5a27f20015cc356a8afedb7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65751b36c3f99a2e3deceebdf9613c9dc2c82efd70b3d53632dbf66d853bf58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb28c68bf887a2b7f2d19807ca165fb4224246514e7a235471498a0545ae46f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2640b8f28723d4da9eeca458d84e9d702ca4b9ee4b357d7d9be645bcc2ff9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbf4b99d8bfcb7559e4c9eeaa5a502f4b84e023b7d6d3b6b6c6c2b6759fc445(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2905f0f85a0c3808a82ff95e5761ec164bc009e644c654aa2680868c44edaf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f22ebdb1cf88d8b71000f83ea6d79ecd71b5d17948ef8cd2ccfaa70591f09c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009e9a98eb92260d94450fc1f4d29dc763d77b52b5ca17bbeae3be3fd6b28f40(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887e33814e96af0ae6cd7e727b292c64849b5db79036bef015fc8eb3382ac367(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8920a9f5ae1485fedff245d3431c6e963b66abd259547b85c1220d89791f59ca(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    api_key_source: typing.Optional[builtins.str] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    body: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_configuration: typing.Optional[typing.Union[ApiGatewayRestApiEndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    policy: typing.Optional[builtins.str] = None,
    put_rest_api_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1207fa11d7cc06172cc3eeefbbe7b0919ccffce843f6a3f2aba3f0079b5caf39(
    *,
    types: typing.Sequence[builtins.str],
    vpc_endpoint_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7ed6091a726b114b303ee359aaabaabc7db5c1d0456acd913ea23a1afc3f76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13f4de7d4de0034b764d7e4488170dd01ad778bcc894e3583511251ab5bacf9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ae5f28e0cbdb49e8fe717e9226e33c97dad39b1397cb31e41ba3d95cc163a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4caf3a11f6fce9c8257efd88ff1e95aafbf57f41927d50f5308fa1e03227d96b(
    value: typing.Optional[ApiGatewayRestApiEndpointConfiguration],
) -> None:
    """Type checking stubs"""
    pass
