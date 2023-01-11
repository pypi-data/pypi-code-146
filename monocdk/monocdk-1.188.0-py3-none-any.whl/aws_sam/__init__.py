'''
# AWS Serverless Application Model Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as serverless
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Serverless construct libraries](https://constructs.dev/search?q=serverless)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Serverless resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Serverless.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Serverless](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Serverless.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnApi(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sam.CfnApi",
):
    '''A CloudFormation ``AWS::Serverless::Api``.

    :cloudformationResource: AWS::Serverless::Api
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sam as sam
        
        # authorizers: Any
        # definition_body: Any
        # gateway_responses: Any
        # method_settings: Any
        # models: Any
        
        cfn_api = sam.CfnApi(self, "MyCfnApi",
            stage_name="stageName",
        
            # the properties below are optional
            access_log_setting=sam.CfnApi.AccessLogSettingProperty(
                destination_arn="destinationArn",
                format="format"
            ),
            auth=sam.CfnApi.AuthProperty(
                add_default_authorizer_to_cors_preflight=False,
                authorizers=authorizers,
                default_authorizer="defaultAuthorizer"
            ),
            binary_media_types=["binaryMediaTypes"],
            cache_cluster_enabled=False,
            cache_cluster_size="cacheClusterSize",
            canary_setting=sam.CfnApi.CanarySettingProperty(
                deployment_id="deploymentId",
                percent_traffic=123,
                stage_variable_overrides={
                    "stage_variable_overrides_key": "stageVariableOverrides"
                },
                use_stage_cache=False
            ),
            cors="cors",
            definition_body=definition_body,
            definition_uri="definitionUri",
            description="description",
            domain=sam.CfnApi.DomainConfigurationProperty(
                certificate_arn="certificateArn",
                domain_name="domainName",
        
                # the properties below are optional
                base_path=["basePath"],
                endpoint_configuration="endpointConfiguration",
                mutual_tls_authentication=sam.CfnApi.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version="truststoreVersion"
                ),
                ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                route53=sam.CfnApi.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                ),
                security_policy="securityPolicy"
            ),
            endpoint_configuration="endpointConfiguration",
            gateway_responses=gateway_responses,
            method_settings=[method_settings],
            minimum_compression_size=123,
            models=models,
            name="name",
            open_api_version="openApiVersion",
            tags={
                "tags_key": "tags"
            },
            tracing_enabled=False,
            variables={
                "variables_key": "variables"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        stage_name: builtins.str,
        access_log_setting: typing.Optional[typing.Union[typing.Union["CfnApi.AccessLogSettingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        auth: typing.Optional[typing.Union[typing.Union["CfnApi.AuthProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        cache_cluster_size: typing.Optional[builtins.str] = None,
        canary_setting: typing.Optional[typing.Union[typing.Union["CfnApi.CanarySettingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cors: typing.Optional[typing.Union[builtins.str, typing.Union["CfnApi.CorsConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union["CfnApi.S3LocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        domain: typing.Optional[typing.Union[typing.Union["CfnApi.DomainConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        endpoint_configuration: typing.Optional[typing.Union[builtins.str, typing.Union["CfnApi.EndpointConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        gateway_responses: typing.Any = None,
        method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_a771d0ef]] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        models: typing.Any = None,
        name: typing.Optional[builtins.str] = None,
        open_api_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::Api``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param stage_name: ``AWS::Serverless::Api.StageName``.
        :param access_log_setting: ``AWS::Serverless::Api.AccessLogSetting``.
        :param auth: ``AWS::Serverless::Api.Auth``.
        :param binary_media_types: ``AWS::Serverless::Api.BinaryMediaTypes``.
        :param cache_cluster_enabled: ``AWS::Serverless::Api.CacheClusterEnabled``.
        :param cache_cluster_size: ``AWS::Serverless::Api.CacheClusterSize``.
        :param canary_setting: ``AWS::Serverless::Api.CanarySetting``.
        :param cors: ``AWS::Serverless::Api.Cors``.
        :param definition_body: ``AWS::Serverless::Api.DefinitionBody``.
        :param definition_uri: ``AWS::Serverless::Api.DefinitionUri``.
        :param description: ``AWS::Serverless::Api.Description``.
        :param domain: ``AWS::Serverless::Api.Domain``.
        :param endpoint_configuration: ``AWS::Serverless::Api.EndpointConfiguration``.
        :param gateway_responses: ``AWS::Serverless::Api.GatewayResponses``.
        :param method_settings: ``AWS::Serverless::Api.MethodSettings``.
        :param minimum_compression_size: ``AWS::Serverless::Api.MinimumCompressionSize``.
        :param models: ``AWS::Serverless::Api.Models``.
        :param name: ``AWS::Serverless::Api.Name``.
        :param open_api_version: ``AWS::Serverless::Api.OpenApiVersion``.
        :param tags: ``AWS::Serverless::Api.Tags``.
        :param tracing_enabled: ``AWS::Serverless::Api.TracingEnabled``.
        :param variables: ``AWS::Serverless::Api.Variables``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d335580439b2be96b6739327fa014ceb07f1e8a3e2b5336958a004f4356a9c0a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApiProps(
            stage_name=stage_name,
            access_log_setting=access_log_setting,
            auth=auth,
            binary_media_types=binary_media_types,
            cache_cluster_enabled=cache_cluster_enabled,
            cache_cluster_size=cache_cluster_size,
            canary_setting=canary_setting,
            cors=cors,
            definition_body=definition_body,
            definition_uri=definition_uri,
            description=description,
            domain=domain,
            endpoint_configuration=endpoint_configuration,
            gateway_responses=gateway_responses,
            method_settings=method_settings,
            minimum_compression_size=minimum_compression_size,
            models=models,
            name=name,
            open_api_version=open_api_version,
            tags=tags,
            tracing_enabled=tracing_enabled,
            variables=variables,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599e37cc9f0b898583181cb5e3c590ec879259471ad4a4ad7485a0354da7e130)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c7a54026d53491b3a9f3b7ce470eedd1a095c55bf1b5e2b889200bb0c3c720d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Serverless::Api.Tags``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="definitionBody")
    def definition_body(self) -> typing.Any:
        '''``AWS::Serverless::Api.DefinitionBody``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Any, jsii.get(self, "definitionBody"))

    @definition_body.setter
    def definition_body(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a311296130c0aaa489a0b107cabf03aa7536b7a1ba38852c587ab82a4782d1ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionBody", value)

    @builtins.property
    @jsii.member(jsii_name="gatewayResponses")
    def gateway_responses(self) -> typing.Any:
        '''``AWS::Serverless::Api.GatewayResponses``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-gatewayresponses
        '''
        return typing.cast(typing.Any, jsii.get(self, "gatewayResponses"))

    @gateway_responses.setter
    def gateway_responses(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a835ed5badbf94a7491f74fa3debc004afe21892bef705c066632f467cb342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayResponses", value)

    @builtins.property
    @jsii.member(jsii_name="models")
    def models(self) -> typing.Any:
        '''``AWS::Serverless::Api.Models``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-models
        '''
        return typing.cast(typing.Any, jsii.get(self, "models"))

    @models.setter
    def models(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea5de8ac34b118315e689d139eca91cba2d4e9673d110822451218448f812fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "models", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        '''``AWS::Serverless::Api.StageName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(builtins.str, jsii.get(self, "stageName"))

    @stage_name.setter
    def stage_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55aa4934945655485cc2b7868d00ec4fcad6e1e5929fdb6cf522246f8b08170c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageName", value)

    @builtins.property
    @jsii.member(jsii_name="accessLogSetting")
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union["CfnApi.AccessLogSettingProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.AccessLogSetting``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApi.AccessLogSettingProperty", _IResolvable_a771d0ef]], jsii.get(self, "accessLogSetting"))

    @access_log_setting.setter
    def access_log_setting(
        self,
        value: typing.Optional[typing.Union["CfnApi.AccessLogSettingProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9baae6f1fa6931f3806e1c4d83a6c1314e1bc7d0c3d7ef981d168adef46efb3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLogSetting", value)

    @builtins.property
    @jsii.member(jsii_name="auth")
    def auth(
        self,
    ) -> typing.Optional[typing.Union["CfnApi.AuthProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.Auth``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApi.AuthProperty", _IResolvable_a771d0ef]], jsii.get(self, "auth"))

    @auth.setter
    def auth(
        self,
        value: typing.Optional[typing.Union["CfnApi.AuthProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a509f93a43137b3d78d240835dbe09b3a32e1e689665db3a5d793ad524627347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auth", value)

    @builtins.property
    @jsii.member(jsii_name="binaryMediaTypes")
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Api.BinaryMediaTypes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "binaryMediaTypes"))

    @binary_media_types.setter
    def binary_media_types(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6968388745dbc358c2ed9ef87e6c806ce847c391a3ed212e4cb8744ecff4cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryMediaTypes", value)

    @builtins.property
    @jsii.member(jsii_name="cacheClusterEnabled")
    def cache_cluster_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.CacheClusterEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "cacheClusterEnabled"))

    @cache_cluster_enabled.setter
    def cache_cluster_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26576406457c4387225108951ff87ea49c0a2adc5194bbbd1095b88e01a40dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheClusterEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cacheClusterSize")
    def cache_cluster_size(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.CacheClusterSize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheClusterSize"))

    @cache_cluster_size.setter
    def cache_cluster_size(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d67fb7fe4bd03c8bffa3a932ff5928fec3b6cd37aac618cbf3d9a8a4b69286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheClusterSize", value)

    @builtins.property
    @jsii.member(jsii_name="canarySetting")
    def canary_setting(
        self,
    ) -> typing.Optional[typing.Union["CfnApi.CanarySettingProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.CanarySetting``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-canarysetting
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApi.CanarySettingProperty", _IResolvable_a771d0ef]], jsii.get(self, "canarySetting"))

    @canary_setting.setter
    def canary_setting(
        self,
        value: typing.Optional[typing.Union["CfnApi.CanarySettingProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c283bcd8c826280aaa07c8827f3ab44b562a4202c68e8ac08ece8be25601e8df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canarySetting", value)

    @builtins.property
    @jsii.member(jsii_name="cors")
    def cors(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnApi.CorsConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.Cors``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnApi.CorsConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "cors"))

    @cors.setter
    def cors(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnApi.CorsConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf7631e195781ecf396795a9ebdc478d3a81125bfb22c3de1d3ddb876a55a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cors", value)

    @builtins.property
    @jsii.member(jsii_name="definitionUri")
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnApi.S3LocationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.DefinitionUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnApi.S3LocationProperty", _IResolvable_a771d0ef]], jsii.get(self, "definitionUri"))

    @definition_uri.setter
    def definition_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnApi.S3LocationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e7ed62f63ed9152ae2ac81e4f1c9423100b0ad8c2369be869cfa550ebf74431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionUri", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.Description``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7e87f0a766e830ba1078dbe9a867b14d26bc19e6cef4ebb791ccbd69c3387d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(
        self,
    ) -> typing.Optional[typing.Union["CfnApi.DomainConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.Domain``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-domain
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApi.DomainConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "domain"))

    @domain.setter
    def domain(
        self,
        value: typing.Optional[typing.Union["CfnApi.DomainConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9abdc627cc7739ccbd2adbeb03cf55b6312cded59c672d96d179bbe161c601c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="endpointConfiguration")
    def endpoint_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnApi.EndpointConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.EndpointConfiguration``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnApi.EndpointConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "endpointConfiguration"))

    @endpoint_configuration.setter
    def endpoint_configuration(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnApi.EndpointConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b432cfef1b40e146c6759ba2d948aa980ac4f5b55420b2177c26131f2de51e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="methodSettings")
    def method_settings(
        self,
    ) -> typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.MethodSettings``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef]], jsii.get(self, "methodSettings"))

    @method_settings.setter
    def method_settings(
        self,
        value: typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a997e2cb1239fc2f833d20acb1f2b61edbdc00232a55c840dbb561910e6a3b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methodSettings", value)

    @builtins.property
    @jsii.member(jsii_name="minimumCompressionSize")
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Api.MinimumCompressionSize``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-minimumcompressionsize
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumCompressionSize"))

    @minimum_compression_size.setter
    def minimum_compression_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7bcacc949c68bcdccbbd16ab1ff46e84d7fb6e68152c0ff8ec8c4903859de4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumCompressionSize", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.Name``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8064bae7c53341f04ffd95e911e57d020bb57ab1172f4f9a3bece47c8a6385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="openApiVersion")
    def open_api_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.OpenApiVersion``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "openApiVersion"))

    @open_api_version.setter
    def open_api_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091f9b9754b8fd289b004c55e21a03a3bb150b9e616d48b3e96a8b64e0b896f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "openApiVersion", value)

    @builtins.property
    @jsii.member(jsii_name="tracingEnabled")
    def tracing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.TracingEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "tracingEnabled"))

    @tracing_enabled.setter
    def tracing_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0707e368c9b45be13971289c3fb51db0d8fc0fb36f6dac387a251ee2d9599e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tracingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Api.Variables``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "variables"))

    @variables.setter
    def variables(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51cfa5503c330e2143ad6b91761b656b2e541538a510912704db7d6350c9211b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variables", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnApi.AccessLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_arn: ``CfnApi.AccessLogSettingProperty.DestinationArn``.
            :param format: ``CfnApi.AccessLogSettingProperty.Format``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                access_log_setting_property = sam.CfnApi.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c1fd6cfc9b13d3412afe13981524f5ddb575bc1450eb5d384df0607e078ce87c)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.AccessLogSettingProperty.DestinationArn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.AccessLogSettingProperty.Format``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnApi.AuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_default_authorizer_to_cors_preflight": "addDefaultAuthorizerToCorsPreflight",
            "authorizers": "authorizers",
            "default_authorizer": "defaultAuthorizer",
        },
    )
    class AuthProperty:
        def __init__(
            self,
            *,
            add_default_authorizer_to_cors_preflight: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            authorizers: typing.Any = None,
            default_authorizer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param add_default_authorizer_to_cors_preflight: ``CfnApi.AuthProperty.AddDefaultAuthorizerToCorsPreflight``.
            :param authorizers: ``CfnApi.AuthProperty.Authorizers``.
            :param default_authorizer: ``CfnApi.AuthProperty.DefaultAuthorizer``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api-auth-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                # authorizers: Any
                
                auth_property = sam.CfnApi.AuthProperty(
                    add_default_authorizer_to_cors_preflight=False,
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d80f1d235e5871d0bf3254e0466b4857fbdee758bbb96838a3774a33f9a33284)
                check_type(argname="argument add_default_authorizer_to_cors_preflight", value=add_default_authorizer_to_cors_preflight, expected_type=type_hints["add_default_authorizer_to_cors_preflight"])
                check_type(argname="argument authorizers", value=authorizers, expected_type=type_hints["authorizers"])
                check_type(argname="argument default_authorizer", value=default_authorizer, expected_type=type_hints["default_authorizer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_default_authorizer_to_cors_preflight is not None:
                self._values["add_default_authorizer_to_cors_preflight"] = add_default_authorizer_to_cors_preflight
            if authorizers is not None:
                self._values["authorizers"] = authorizers
            if default_authorizer is not None:
                self._values["default_authorizer"] = default_authorizer

        @builtins.property
        def add_default_authorizer_to_cors_preflight(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnApi.AuthProperty.AddDefaultAuthorizerToCorsPreflight``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api-auth-object
            '''
            result = self._values.get("add_default_authorizer_to_cors_preflight")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def authorizers(self) -> typing.Any:
            '''``CfnApi.AuthProperty.Authorizers``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api-auth-object
            '''
            result = self._values.get("authorizers")
            return typing.cast(typing.Any, result)

        @builtins.property
        def default_authorizer(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.AuthProperty.DefaultAuthorizer``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api-auth-object
            '''
            result = self._values.get("default_authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnApi.CanarySettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_id": "deploymentId",
            "percent_traffic": "percentTraffic",
            "stage_variable_overrides": "stageVariableOverrides",
            "use_stage_cache": "useStageCache",
        },
    )
    class CanarySettingProperty:
        def __init__(
            self,
            *,
            deployment_id: typing.Optional[builtins.str] = None,
            percent_traffic: typing.Optional[jsii.Number] = None,
            stage_variable_overrides: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
            use_stage_cache: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param deployment_id: ``CfnApi.CanarySettingProperty.DeploymentId``.
            :param percent_traffic: ``CfnApi.CanarySettingProperty.PercentTraffic``.
            :param stage_variable_overrides: ``CfnApi.CanarySettingProperty.StageVariableOverrides``.
            :param use_stage_cache: ``CfnApi.CanarySettingProperty.UseStageCache``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                canary_setting_property = sam.CfnApi.CanarySettingProperty(
                    deployment_id="deploymentId",
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90803c6a90da1622ea8804fee25a6d4ffb0f08bf5c0ae66e21ca3fd6cb4688c1)
                check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
                check_type(argname="argument percent_traffic", value=percent_traffic, expected_type=type_hints["percent_traffic"])
                check_type(argname="argument stage_variable_overrides", value=stage_variable_overrides, expected_type=type_hints["stage_variable_overrides"])
                check_type(argname="argument use_stage_cache", value=use_stage_cache, expected_type=type_hints["use_stage_cache"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deployment_id is not None:
                self._values["deployment_id"] = deployment_id
            if percent_traffic is not None:
                self._values["percent_traffic"] = percent_traffic
            if stage_variable_overrides is not None:
                self._values["stage_variable_overrides"] = stage_variable_overrides
            if use_stage_cache is not None:
                self._values["use_stage_cache"] = use_stage_cache

        @builtins.property
        def deployment_id(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.CanarySettingProperty.DeploymentId``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-deploymentid
            '''
            result = self._values.get("deployment_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def percent_traffic(self) -> typing.Optional[jsii.Number]:
            '''``CfnApi.CanarySettingProperty.PercentTraffic``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-percenttraffic
            '''
            result = self._values.get("percent_traffic")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stage_variable_overrides(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnApi.CanarySettingProperty.StageVariableOverrides``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-stagevariableoverrides
            '''
            result = self._values.get("stage_variable_overrides")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def use_stage_cache(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnApi.CanarySettingProperty.UseStageCache``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-usestagecache
            '''
            result = self._values.get("use_stage_cache")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CanarySettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnApi.CorsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_origin": "allowOrigin",
            "allow_credentials": "allowCredentials",
            "allow_headers": "allowHeaders",
            "allow_methods": "allowMethods",
            "max_age": "maxAge",
        },
    )
    class CorsConfigurationProperty:
        def __init__(
            self,
            *,
            allow_origin: builtins.str,
            allow_credentials: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            allow_headers: typing.Optional[builtins.str] = None,
            allow_methods: typing.Optional[builtins.str] = None,
            max_age: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param allow_origin: ``CfnApi.CorsConfigurationProperty.AllowOrigin``.
            :param allow_credentials: ``CfnApi.CorsConfigurationProperty.AllowCredentials``.
            :param allow_headers: ``CfnApi.CorsConfigurationProperty.AllowHeaders``.
            :param allow_methods: ``CfnApi.CorsConfigurationProperty.AllowMethods``.
            :param max_age: ``CfnApi.CorsConfigurationProperty.MaxAge``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                cors_configuration_property = sam.CfnApi.CorsConfigurationProperty(
                    allow_origin="allowOrigin",
                
                    # the properties below are optional
                    allow_credentials=False,
                    allow_headers="allowHeaders",
                    allow_methods="allowMethods",
                    max_age="maxAge"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c33c10e79774a3454838e6e5a5f9f99fd894e3e9d829cc8cc6afb8b66a912ec4)
                check_type(argname="argument allow_origin", value=allow_origin, expected_type=type_hints["allow_origin"])
                check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
                check_type(argname="argument allow_headers", value=allow_headers, expected_type=type_hints["allow_headers"])
                check_type(argname="argument allow_methods", value=allow_methods, expected_type=type_hints["allow_methods"])
                check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "allow_origin": allow_origin,
            }
            if allow_credentials is not None:
                self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None:
                self._values["allow_headers"] = allow_headers
            if allow_methods is not None:
                self._values["allow_methods"] = allow_methods
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allow_origin(self) -> builtins.str:
            '''``CfnApi.CorsConfigurationProperty.AllowOrigin``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_origin")
            assert result is not None, "Required property 'allow_origin' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allow_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnApi.CorsConfigurationProperty.AllowCredentials``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def allow_headers(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.CorsConfigurationProperty.AllowHeaders``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_headers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def allow_methods(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.CorsConfigurationProperty.AllowMethods``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_methods")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_age(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.CorsConfigurationProperty.MaxAge``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("max_age")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnApi.DomainConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "domain_name": "domainName",
            "base_path": "basePath",
            "endpoint_configuration": "endpointConfiguration",
            "mutual_tls_authentication": "mutualTlsAuthentication",
            "ownership_verification_certificate_arn": "ownershipVerificationCertificateArn",
            "route53": "route53",
            "security_policy": "securityPolicy",
        },
    )
    class DomainConfigurationProperty:
        def __init__(
            self,
            *,
            certificate_arn: builtins.str,
            domain_name: builtins.str,
            base_path: typing.Optional[typing.Sequence[builtins.str]] = None,
            endpoint_configuration: typing.Optional[builtins.str] = None,
            mutual_tls_authentication: typing.Optional[typing.Union[typing.Union["CfnApi.MutualTlsAuthenticationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            ownership_verification_certificate_arn: typing.Optional[builtins.str] = None,
            route53: typing.Optional[typing.Union[typing.Union["CfnApi.Route53ConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param certificate_arn: ``CfnApi.DomainConfigurationProperty.CertificateArn``.
            :param domain_name: ``CfnApi.DomainConfigurationProperty.DomainName``.
            :param base_path: ``CfnApi.DomainConfigurationProperty.BasePath``.
            :param endpoint_configuration: ``CfnApi.DomainConfigurationProperty.EndpointConfiguration``.
            :param mutual_tls_authentication: ``CfnApi.DomainConfigurationProperty.MutualTlsAuthentication``.
            :param ownership_verification_certificate_arn: ``CfnApi.DomainConfigurationProperty.OwnershipVerificationCertificateArn``.
            :param route53: ``CfnApi.DomainConfigurationProperty.Route53``.
            :param security_policy: ``CfnApi.DomainConfigurationProperty.SecurityPolicy``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                domain_configuration_property = sam.CfnApi.DomainConfigurationProperty(
                    certificate_arn="certificateArn",
                    domain_name="domainName",
                
                    # the properties below are optional
                    base_path=["basePath"],
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam.CfnApi.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version="truststoreVersion"
                    ),
                    ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                    route53=sam.CfnApi.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93b7a68f7c676c2aa3d43136780d961b44db8f0f647dec485730b4f44a40d187)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument base_path", value=base_path, expected_type=type_hints["base_path"])
                check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
                check_type(argname="argument mutual_tls_authentication", value=mutual_tls_authentication, expected_type=type_hints["mutual_tls_authentication"])
                check_type(argname="argument ownership_verification_certificate_arn", value=ownership_verification_certificate_arn, expected_type=type_hints["ownership_verification_certificate_arn"])
                check_type(argname="argument route53", value=route53, expected_type=type_hints["route53"])
                check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "certificate_arn": certificate_arn,
                "domain_name": domain_name,
            }
            if base_path is not None:
                self._values["base_path"] = base_path
            if endpoint_configuration is not None:
                self._values["endpoint_configuration"] = endpoint_configuration
            if mutual_tls_authentication is not None:
                self._values["mutual_tls_authentication"] = mutual_tls_authentication
            if ownership_verification_certificate_arn is not None:
                self._values["ownership_verification_certificate_arn"] = ownership_verification_certificate_arn
            if route53 is not None:
                self._values["route53"] = route53
            if security_policy is not None:
                self._values["security_policy"] = security_policy

        @builtins.property
        def certificate_arn(self) -> builtins.str:
            '''``CfnApi.DomainConfigurationProperty.CertificateArn``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-certificatearn
            '''
            result = self._values.get("certificate_arn")
            assert result is not None, "Required property 'certificate_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def domain_name(self) -> builtins.str:
            '''``CfnApi.DomainConfigurationProperty.DomainName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-domainname
            '''
            result = self._values.get("domain_name")
            assert result is not None, "Required property 'domain_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def base_path(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnApi.DomainConfigurationProperty.BasePath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-basepath
            '''
            result = self._values.get("base_path")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def endpoint_configuration(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.DomainConfigurationProperty.EndpointConfiguration``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-endpointconfiguration
            '''
            result = self._values.get("endpoint_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mutual_tls_authentication(
            self,
        ) -> typing.Optional[typing.Union["CfnApi.MutualTlsAuthenticationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApi.DomainConfigurationProperty.MutualTlsAuthentication``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-mutualtlsauthentication
            '''
            result = self._values.get("mutual_tls_authentication")
            return typing.cast(typing.Optional[typing.Union["CfnApi.MutualTlsAuthenticationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ownership_verification_certificate_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''``CfnApi.DomainConfigurationProperty.OwnershipVerificationCertificateArn``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-ownershipverificationcertificatearn
            '''
            result = self._values.get("ownership_verification_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def route53(
            self,
        ) -> typing.Optional[typing.Union["CfnApi.Route53ConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApi.DomainConfigurationProperty.Route53``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-route53
            '''
            result = self._values.get("route53")
            return typing.cast(typing.Optional[typing.Union["CfnApi.Route53ConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def security_policy(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.DomainConfigurationProperty.SecurityPolicy``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-securitypolicy
            '''
            result = self._values.get("security_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnApi.EndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "vpc_endpoint_ids": "vpcEndpointIds"},
    )
    class EndpointConfigurationProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            vpc_endpoint_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param type: ``CfnApi.EndpointConfigurationProperty.Type``.
            :param vpc_endpoint_ids: ``CfnApi.EndpointConfigurationProperty.VpcEndpointIds``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-endpointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                endpoint_configuration_property = sam.CfnApi.EndpointConfigurationProperty(
                    type="type",
                    vpc_endpoint_ids=["vpcEndpointIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc6a6fc1266becaea79c116e24134e07f3d9a2b7f41bf971d23eb382e847e55a)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument vpc_endpoint_ids", value=vpc_endpoint_ids, expected_type=type_hints["vpc_endpoint_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if vpc_endpoint_ids is not None:
                self._values["vpc_endpoint_ids"] = vpc_endpoint_ids

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.EndpointConfigurationProperty.Type``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-endpointconfiguration.html#sam-api-endpointconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_endpoint_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnApi.EndpointConfigurationProperty.VpcEndpointIds``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-endpointconfiguration.html#sam-api-endpointconfiguration-vpcendpointids
            '''
            result = self._values.get("vpc_endpoint_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnApi.MutualTlsAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "truststore_uri": "truststoreUri",
            "truststore_version": "truststoreVersion",
        },
    )
    class MutualTlsAuthenticationProperty:
        def __init__(
            self,
            *,
            truststore_uri: typing.Optional[builtins.str] = None,
            truststore_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param truststore_uri: ``CfnApi.MutualTlsAuthenticationProperty.TruststoreUri``.
            :param truststore_version: ``CfnApi.MutualTlsAuthenticationProperty.TruststoreVersion``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-mutualtlsauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                mutual_tls_authentication_property = sam.CfnApi.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version="truststoreVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d6477d62bdd979ffe7878b5a7a317c990ed4621773d918a6e6c1da373af72fc)
                check_type(argname="argument truststore_uri", value=truststore_uri, expected_type=type_hints["truststore_uri"])
                check_type(argname="argument truststore_version", value=truststore_version, expected_type=type_hints["truststore_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if truststore_uri is not None:
                self._values["truststore_uri"] = truststore_uri
            if truststore_version is not None:
                self._values["truststore_version"] = truststore_version

        @builtins.property
        def truststore_uri(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.MutualTlsAuthenticationProperty.TruststoreUri``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-mutualtlsauthentication.html#cfn-apigateway-domainname-mutualtlsauthentication-truststoreuri
            '''
            result = self._values.get("truststore_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def truststore_version(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.MutualTlsAuthenticationProperty.TruststoreVersion``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-mutualtlsauthentication.html#cfn-apigateway-domainname-mutualtlsauthentication-truststoreversion
            '''
            result = self._values.get("truststore_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutualTlsAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnApi.Route53ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "distributed_domain_name": "distributedDomainName",
            "evaluate_target_health": "evaluateTargetHealth",
            "hosted_zone_id": "hostedZoneId",
            "hosted_zone_name": "hostedZoneName",
            "ip_v6": "ipV6",
        },
    )
    class Route53ConfigurationProperty:
        def __init__(
            self,
            *,
            distributed_domain_name: typing.Optional[builtins.str] = None,
            evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
            hosted_zone_name: typing.Optional[builtins.str] = None,
            ip_v6: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param distributed_domain_name: ``CfnApi.Route53ConfigurationProperty.DistributedDomainName``.
            :param evaluate_target_health: ``CfnApi.Route53ConfigurationProperty.EvaluateTargetHealth``.
            :param hosted_zone_id: ``CfnApi.Route53ConfigurationProperty.HostedZoneId``.
            :param hosted_zone_name: ``CfnApi.Route53ConfigurationProperty.HostedZoneName``.
            :param ip_v6: ``CfnApi.Route53ConfigurationProperty.IpV6``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                route53_configuration_property = sam.CfnApi.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fe3511583218c761d12aeabdb8c65c92f14917564e966bf7159fcbe3d7b6956)
                check_type(argname="argument distributed_domain_name", value=distributed_domain_name, expected_type=type_hints["distributed_domain_name"])
                check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
                check_type(argname="argument hosted_zone_name", value=hosted_zone_name, expected_type=type_hints["hosted_zone_name"])
                check_type(argname="argument ip_v6", value=ip_v6, expected_type=type_hints["ip_v6"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if distributed_domain_name is not None:
                self._values["distributed_domain_name"] = distributed_domain_name
            if evaluate_target_health is not None:
                self._values["evaluate_target_health"] = evaluate_target_health
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id
            if hosted_zone_name is not None:
                self._values["hosted_zone_name"] = hosted_zone_name
            if ip_v6 is not None:
                self._values["ip_v6"] = ip_v6

        @builtins.property
        def distributed_domain_name(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.Route53ConfigurationProperty.DistributedDomainName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html#sam-api-route53configuration-distributiondomainname
            '''
            result = self._values.get("distributed_domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def evaluate_target_health(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnApi.Route53ConfigurationProperty.EvaluateTargetHealth``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html#sam-api-route53configuration-evaluatetargethealth
            '''
            result = self._values.get("evaluate_target_health")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.Route53ConfigurationProperty.HostedZoneId``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html#sam-api-route53configuration-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_name(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.Route53ConfigurationProperty.HostedZoneName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html#sam-api-route53configuration-hostedzonename
            '''
            result = self._values.get("hosted_zone_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ip_v6(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnApi.Route53ConfigurationProperty.IpV6``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html#sam-api-route53configuration-ipv6
            '''
            result = self._values.get("ip_v6")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Route53ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnApi.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: jsii.Number,
        ) -> None:
            '''
            :param bucket: ``CfnApi.S3LocationProperty.Bucket``.
            :param key: ``CfnApi.S3LocationProperty.Key``.
            :param version: ``CfnApi.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s3_location_property = sam.CfnApi.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__891165367931c3c6b349c85239a964e708cd75b86160dc7cb7e19c74559572a4)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
                "version": version,
            }

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnApi.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnApi.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> jsii.Number:
            '''``CfnApi.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_sam.CfnApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "stage_name": "stageName",
        "access_log_setting": "accessLogSetting",
        "auth": "auth",
        "binary_media_types": "binaryMediaTypes",
        "cache_cluster_enabled": "cacheClusterEnabled",
        "cache_cluster_size": "cacheClusterSize",
        "canary_setting": "canarySetting",
        "cors": "cors",
        "definition_body": "definitionBody",
        "definition_uri": "definitionUri",
        "description": "description",
        "domain": "domain",
        "endpoint_configuration": "endpointConfiguration",
        "gateway_responses": "gatewayResponses",
        "method_settings": "methodSettings",
        "minimum_compression_size": "minimumCompressionSize",
        "models": "models",
        "name": "name",
        "open_api_version": "openApiVersion",
        "tags": "tags",
        "tracing_enabled": "tracingEnabled",
        "variables": "variables",
    },
)
class CfnApiProps:
    def __init__(
        self,
        *,
        stage_name: builtins.str,
        access_log_setting: typing.Optional[typing.Union[typing.Union[CfnApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        auth: typing.Optional[typing.Union[typing.Union[CfnApi.AuthProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        cache_cluster_size: typing.Optional[builtins.str] = None,
        canary_setting: typing.Optional[typing.Union[typing.Union[CfnApi.CanarySettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cors: typing.Optional[typing.Union[builtins.str, typing.Union[CfnApi.CorsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        domain: typing.Optional[typing.Union[typing.Union[CfnApi.DomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        endpoint_configuration: typing.Optional[typing.Union[builtins.str, typing.Union[CfnApi.EndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        gateway_responses: typing.Any = None,
        method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_a771d0ef]] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        models: typing.Any = None,
        name: typing.Optional[builtins.str] = None,
        open_api_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApi``.

        :param stage_name: ``AWS::Serverless::Api.StageName``.
        :param access_log_setting: ``AWS::Serverless::Api.AccessLogSetting``.
        :param auth: ``AWS::Serverless::Api.Auth``.
        :param binary_media_types: ``AWS::Serverless::Api.BinaryMediaTypes``.
        :param cache_cluster_enabled: ``AWS::Serverless::Api.CacheClusterEnabled``.
        :param cache_cluster_size: ``AWS::Serverless::Api.CacheClusterSize``.
        :param canary_setting: ``AWS::Serverless::Api.CanarySetting``.
        :param cors: ``AWS::Serverless::Api.Cors``.
        :param definition_body: ``AWS::Serverless::Api.DefinitionBody``.
        :param definition_uri: ``AWS::Serverless::Api.DefinitionUri``.
        :param description: ``AWS::Serverless::Api.Description``.
        :param domain: ``AWS::Serverless::Api.Domain``.
        :param endpoint_configuration: ``AWS::Serverless::Api.EndpointConfiguration``.
        :param gateway_responses: ``AWS::Serverless::Api.GatewayResponses``.
        :param method_settings: ``AWS::Serverless::Api.MethodSettings``.
        :param minimum_compression_size: ``AWS::Serverless::Api.MinimumCompressionSize``.
        :param models: ``AWS::Serverless::Api.Models``.
        :param name: ``AWS::Serverless::Api.Name``.
        :param open_api_version: ``AWS::Serverless::Api.OpenApiVersion``.
        :param tags: ``AWS::Serverless::Api.Tags``.
        :param tracing_enabled: ``AWS::Serverless::Api.TracingEnabled``.
        :param variables: ``AWS::Serverless::Api.Variables``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sam as sam
            
            # authorizers: Any
            # definition_body: Any
            # gateway_responses: Any
            # method_settings: Any
            # models: Any
            
            cfn_api_props = sam.CfnApiProps(
                stage_name="stageName",
            
                # the properties below are optional
                access_log_setting=sam.CfnApi.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                ),
                auth=sam.CfnApi.AuthProperty(
                    add_default_authorizer_to_cors_preflight=False,
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                ),
                binary_media_types=["binaryMediaTypes"],
                cache_cluster_enabled=False,
                cache_cluster_size="cacheClusterSize",
                canary_setting=sam.CfnApi.CanarySettingProperty(
                    deployment_id="deploymentId",
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                ),
                cors="cors",
                definition_body=definition_body,
                definition_uri="definitionUri",
                description="description",
                domain=sam.CfnApi.DomainConfigurationProperty(
                    certificate_arn="certificateArn",
                    domain_name="domainName",
            
                    # the properties below are optional
                    base_path=["basePath"],
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam.CfnApi.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version="truststoreVersion"
                    ),
                    ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                    route53=sam.CfnApi.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                ),
                endpoint_configuration="endpointConfiguration",
                gateway_responses=gateway_responses,
                method_settings=[method_settings],
                minimum_compression_size=123,
                models=models,
                name="name",
                open_api_version="openApiVersion",
                tags={
                    "tags_key": "tags"
                },
                tracing_enabled=False,
                variables={
                    "variables_key": "variables"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7eb533facf31131a127d9d307a95eb6aa4dd79e860550198f9dc8dde110133)
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument access_log_setting", value=access_log_setting, expected_type=type_hints["access_log_setting"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument binary_media_types", value=binary_media_types, expected_type=type_hints["binary_media_types"])
            check_type(argname="argument cache_cluster_enabled", value=cache_cluster_enabled, expected_type=type_hints["cache_cluster_enabled"])
            check_type(argname="argument cache_cluster_size", value=cache_cluster_size, expected_type=type_hints["cache_cluster_size"])
            check_type(argname="argument canary_setting", value=canary_setting, expected_type=type_hints["canary_setting"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument definition_body", value=definition_body, expected_type=type_hints["definition_body"])
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
            check_type(argname="argument gateway_responses", value=gateway_responses, expected_type=type_hints["gateway_responses"])
            check_type(argname="argument method_settings", value=method_settings, expected_type=type_hints["method_settings"])
            check_type(argname="argument minimum_compression_size", value=minimum_compression_size, expected_type=type_hints["minimum_compression_size"])
            check_type(argname="argument models", value=models, expected_type=type_hints["models"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument open_api_version", value=open_api_version, expected_type=type_hints["open_api_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tracing_enabled", value=tracing_enabled, expected_type=type_hints["tracing_enabled"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stage_name": stage_name,
        }
        if access_log_setting is not None:
            self._values["access_log_setting"] = access_log_setting
        if auth is not None:
            self._values["auth"] = auth
        if binary_media_types is not None:
            self._values["binary_media_types"] = binary_media_types
        if cache_cluster_enabled is not None:
            self._values["cache_cluster_enabled"] = cache_cluster_enabled
        if cache_cluster_size is not None:
            self._values["cache_cluster_size"] = cache_cluster_size
        if canary_setting is not None:
            self._values["canary_setting"] = canary_setting
        if cors is not None:
            self._values["cors"] = cors
        if definition_body is not None:
            self._values["definition_body"] = definition_body
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if description is not None:
            self._values["description"] = description
        if domain is not None:
            self._values["domain"] = domain
        if endpoint_configuration is not None:
            self._values["endpoint_configuration"] = endpoint_configuration
        if gateway_responses is not None:
            self._values["gateway_responses"] = gateway_responses
        if method_settings is not None:
            self._values["method_settings"] = method_settings
        if minimum_compression_size is not None:
            self._values["minimum_compression_size"] = minimum_compression_size
        if models is not None:
            self._values["models"] = models
        if name is not None:
            self._values["name"] = name
        if open_api_version is not None:
            self._values["open_api_version"] = open_api_version
        if tags is not None:
            self._values["tags"] = tags
        if tracing_enabled is not None:
            self._values["tracing_enabled"] = tracing_enabled
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''``AWS::Serverless::Api.StageName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union[CfnApi.AccessLogSettingProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.AccessLogSetting``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("access_log_setting")
        return typing.cast(typing.Optional[typing.Union[CfnApi.AccessLogSettingProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def auth(
        self,
    ) -> typing.Optional[typing.Union[CfnApi.AuthProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.Auth``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[typing.Union[CfnApi.AuthProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Api.BinaryMediaTypes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("binary_media_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache_cluster_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.CacheClusterEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("cache_cluster_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cache_cluster_size(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.CacheClusterSize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("cache_cluster_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def canary_setting(
        self,
    ) -> typing.Optional[typing.Union[CfnApi.CanarySettingProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.CanarySetting``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-canarysetting
        '''
        result = self._values.get("canary_setting")
        return typing.cast(typing.Optional[typing.Union[CfnApi.CanarySettingProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cors(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnApi.CorsConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.Cors``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnApi.CorsConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def definition_body(self) -> typing.Any:
        '''``AWS::Serverless::Api.DefinitionBody``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("definition_body")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnApi.S3LocationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.DefinitionUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnApi.S3LocationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.Description``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain(
        self,
    ) -> typing.Optional[typing.Union[CfnApi.DomainConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.Domain``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[typing.Union[CfnApi.DomainConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def endpoint_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnApi.EndpointConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.EndpointConfiguration``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("endpoint_configuration")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnApi.EndpointConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def gateway_responses(self) -> typing.Any:
        '''``AWS::Serverless::Api.GatewayResponses``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-gatewayresponses
        '''
        result = self._values.get("gateway_responses")
        return typing.cast(typing.Any, result)

    @builtins.property
    def method_settings(
        self,
    ) -> typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.MethodSettings``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("method_settings")
        return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef]], result)

    @builtins.property
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Api.MinimumCompressionSize``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-minimumcompressionsize
        '''
        result = self._values.get("minimum_compression_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def models(self) -> typing.Any:
        '''``AWS::Serverless::Api.Models``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-models
        '''
        result = self._values.get("models")
        return typing.cast(typing.Any, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.Name``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_api_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.OpenApiVersion``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("open_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::Api.Tags``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tracing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Api.TracingEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("tracing_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Api.Variables``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sam.CfnApplication",
):
    '''A CloudFormation ``AWS::Serverless::Application``.

    :cloudformationResource: AWS::Serverless::Application
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sam as sam
        
        cfn_application = sam.CfnApplication(self, "MyCfnApplication",
            location="location",
        
            # the properties below are optional
            notification_arns=["notificationArns"],
            parameters={
                "parameters_key": "parameters"
            },
            tags={
                "tags_key": "tags"
            },
            timeout_in_minutes=123
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        location: typing.Union[builtins.str, typing.Union["CfnApplication.ApplicationLocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param location: ``AWS::Serverless::Application.Location``.
        :param notification_arns: ``AWS::Serverless::Application.NotificationArns``.
        :param parameters: ``AWS::Serverless::Application.Parameters``.
        :param tags: ``AWS::Serverless::Application.Tags``.
        :param timeout_in_minutes: ``AWS::Serverless::Application.TimeoutInMinutes``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e391f6e060fd4265ded810eaa6d5fa75a8893d957b8d3d42c360f5d5188bda0a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(
            location=location,
            notification_arns=notification_arns,
            parameters=parameters,
            tags=tags,
            timeout_in_minutes=timeout_in_minutes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ba6853b05b0e3295f8df18d55b56fbeb194338450ec4a66a0f85419bd7aae0)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe091b2dd8b63bb3489cb00a4b31286a2c607f4d1297170cb83a9fde9d10b16)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Serverless::Application.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(
        self,
    ) -> typing.Union[builtins.str, "CfnApplication.ApplicationLocationProperty", _IResolvable_a771d0ef]:
        '''``AWS::Serverless::Application.Location``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Union[builtins.str, "CfnApplication.ApplicationLocationProperty", _IResolvable_a771d0ef], jsii.get(self, "location"))

    @location.setter
    def location(
        self,
        value: typing.Union[builtins.str, "CfnApplication.ApplicationLocationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7f648169f50a5b84af67e5b83167efc28457190510099ea093d81740db52c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Application.NotificationArns``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationArns"))

    @notification_arns.setter
    def notification_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45542ebea6247b01691ff27d7fa164c8d0c244846034beff30254651aadcb21e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationArns", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Application.Parameters``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0359fb53a9fdd4f16ee731485f8901e11dc89bb98d01103313e6a5efcf61624b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Application.TimeoutInMinutes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInMinutes"))

    @timeout_in_minutes.setter
    def timeout_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e434a496a1676f20e55f92cf9bcea893a5e84f1287e7323b79a0bb7a153b5b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInMinutes", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnApplication.ApplicationLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_id": "applicationId",
            "semantic_version": "semanticVersion",
        },
    )
    class ApplicationLocationProperty:
        def __init__(
            self,
            *,
            application_id: builtins.str,
            semantic_version: builtins.str,
        ) -> None:
            '''
            :param application_id: ``CfnApplication.ApplicationLocationProperty.ApplicationId``.
            :param semantic_version: ``CfnApplication.ApplicationLocationProperty.SemanticVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                application_location_property = sam.CfnApplication.ApplicationLocationProperty(
                    application_id="applicationId",
                    semantic_version="semanticVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__475d934ea3b3aac2469b7bbb982cc0c2d630261ef3f81be745d9224ecfb3f331)
                check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
                check_type(argname="argument semantic_version", value=semantic_version, expected_type=type_hints["semantic_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "application_id": application_id,
                "semantic_version": semantic_version,
            }

        @builtins.property
        def application_id(self) -> builtins.str:
            '''``CfnApplication.ApplicationLocationProperty.ApplicationId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
            '''
            result = self._values.get("application_id")
            assert result is not None, "Required property 'application_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def semantic_version(self) -> builtins.str:
            '''``CfnApplication.ApplicationLocationProperty.SemanticVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
            '''
            result = self._values.get("semantic_version")
            assert result is not None, "Required property 'semantic_version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_sam.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "notification_arns": "notificationArns",
        "parameters": "parameters",
        "tags": "tags",
        "timeout_in_minutes": "timeoutInMinutes",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        location: typing.Union[builtins.str, typing.Union[CfnApplication.ApplicationLocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param location: ``AWS::Serverless::Application.Location``.
        :param notification_arns: ``AWS::Serverless::Application.NotificationArns``.
        :param parameters: ``AWS::Serverless::Application.Parameters``.
        :param tags: ``AWS::Serverless::Application.Tags``.
        :param timeout_in_minutes: ``AWS::Serverless::Application.TimeoutInMinutes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sam as sam
            
            cfn_application_props = sam.CfnApplicationProps(
                location="location",
            
                # the properties below are optional
                notification_arns=["notificationArns"],
                parameters={
                    "parameters_key": "parameters"
                },
                tags={
                    "tags_key": "tags"
                },
                timeout_in_minutes=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15e85ab5ce25f0c53a2cf55d1edf0649c0f83c03f775da6a2945d1ba1efb8b0)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout_in_minutes", value=timeout_in_minutes, expected_type=type_hints["timeout_in_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes

    @builtins.property
    def location(
        self,
    ) -> typing.Union[builtins.str, CfnApplication.ApplicationLocationProperty, _IResolvable_a771d0ef]:
        '''``AWS::Serverless::Application.Location``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(typing.Union[builtins.str, CfnApplication.ApplicationLocationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Application.NotificationArns``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Application.Parameters``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::Application.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Application.TimeoutInMinutes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFunction(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sam.CfnFunction",
):
    '''A CloudFormation ``AWS::Serverless::Function``.

    :cloudformationResource: AWS::Serverless::Function
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sam as sam
        
        # assume_role_policy_document: Any
        
        cfn_function = sam.CfnFunction(self, "MyCfnFunction",
            architectures=["architectures"],
            assume_role_policy_document=assume_role_policy_document,
            auto_publish_alias="autoPublishAlias",
            auto_publish_code_sha256="autoPublishCodeSha256",
            code_signing_config_arn="codeSigningConfigArn",
            code_uri="codeUri",
            dead_letter_queue=sam.CfnFunction.DeadLetterQueueProperty(
                target_arn="targetArn",
                type="type"
            ),
            deployment_preference=sam.CfnFunction.DeploymentPreferenceProperty(
                enabled=False,
                type="type",
        
                # the properties below are optional
                alarms=["alarms"],
                hooks=sam.CfnFunction.HooksProperty(
                    post_traffic="postTraffic",
                    pre_traffic="preTraffic"
                )
            ),
            description="description",
            environment=sam.CfnFunction.FunctionEnvironmentProperty(
                variables={
                    "variables_key": "variables"
                }
            ),
            event_invoke_config=sam.CfnFunction.EventInvokeConfigProperty(
                destination_config=sam.CfnFunction.EventInvokeDestinationConfigProperty(
                    on_failure=sam.CfnFunction.DestinationProperty(
                        destination="destination",
        
                        # the properties below are optional
                        type="type"
                    ),
                    on_success=sam.CfnFunction.DestinationProperty(
                        destination="destination",
        
                        # the properties below are optional
                        type="type"
                    )
                ),
                maximum_event_age_in_seconds=123,
                maximum_retry_attempts=123
            ),
            events={
                "events_key": sam.CfnFunction.EventSourceProperty(
                    properties=sam.CfnFunction.S3EventProperty(
                        variables={
                            "variables_key": "variables"
                        }
                    ),
                    type="type"
                )
            },
            file_system_configs=[sam.CfnFunction.FileSystemConfigProperty(
                arn="arn",
                local_mount_path="localMountPath"
            )],
            function_name="functionName",
            handler="handler",
            image_config=sam.CfnFunction.ImageConfigProperty(
                command=["command"],
                entry_point=["entryPoint"],
                working_directory="workingDirectory"
            ),
            image_uri="imageUri",
            inline_code="inlineCode",
            kms_key_arn="kmsKeyArn",
            layers=["layers"],
            memory_size=123,
            package_type="packageType",
            permissions_boundary="permissionsBoundary",
            policies="policies",
            provisioned_concurrency_config=sam.CfnFunction.ProvisionedConcurrencyConfigProperty(
                provisioned_concurrent_executions="provisionedConcurrentExecutions"
            ),
            reserved_concurrent_executions=123,
            role="role",
            runtime="runtime",
            tags={
                "tags_key": "tags"
            },
            timeout=123,
            tracing="tracing",
            version_description="versionDescription",
            vpc_config=sam.CfnFunction.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role_policy_document: typing.Any = None,
        auto_publish_alias: typing.Optional[builtins.str] = None,
        auto_publish_code_sha256: typing.Optional[builtins.str] = None,
        code_signing_config_arn: typing.Optional[builtins.str] = None,
        code_uri: typing.Optional[typing.Union[builtins.str, typing.Union["CfnFunction.S3LocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        dead_letter_queue: typing.Optional[typing.Union[typing.Union["CfnFunction.DeadLetterQueueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        deployment_preference: typing.Optional[typing.Union[typing.Union["CfnFunction.DeploymentPreferenceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union[typing.Union["CfnFunction.FunctionEnvironmentProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        event_invoke_config: typing.Optional[typing.Union[typing.Union["CfnFunction.EventInvokeConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnFunction.EventSourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        file_system_configs: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFunction.FileSystemConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        function_name: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        image_config: typing.Optional[typing.Union[typing.Union["CfnFunction.ImageConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        inline_code: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        layers: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        package_type: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, typing.Union["CfnFunction.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef, typing.Sequence[typing.Union[builtins.str, typing.Union["CfnFunction.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.SAMPolicyTemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        provisioned_concurrency_config: typing.Optional[typing.Union[typing.Union["CfnFunction.ProvisionedConcurrencyConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        tracing: typing.Optional[builtins.str] = None,
        version_description: typing.Optional[builtins.str] = None,
        vpc_config: typing.Optional[typing.Union[typing.Union["CfnFunction.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::Function``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param architectures: ``AWS::Serverless::Function.Architectures``.
        :param assume_role_policy_document: ``AWS::Serverless::Function.AssumeRolePolicyDocument``.
        :param auto_publish_alias: ``AWS::Serverless::Function.AutoPublishAlias``.
        :param auto_publish_code_sha256: ``AWS::Serverless::Function.AutoPublishCodeSha256``.
        :param code_signing_config_arn: ``AWS::Serverless::Function.CodeSigningConfigArn``.
        :param code_uri: ``AWS::Serverless::Function.CodeUri``.
        :param dead_letter_queue: ``AWS::Serverless::Function.DeadLetterQueue``.
        :param deployment_preference: ``AWS::Serverless::Function.DeploymentPreference``.
        :param description: ``AWS::Serverless::Function.Description``.
        :param environment: ``AWS::Serverless::Function.Environment``.
        :param event_invoke_config: ``AWS::Serverless::Function.EventInvokeConfig``.
        :param events: ``AWS::Serverless::Function.Events``.
        :param file_system_configs: ``AWS::Serverless::Function.FileSystemConfigs``.
        :param function_name: ``AWS::Serverless::Function.FunctionName``.
        :param handler: ``AWS::Serverless::Function.Handler``.
        :param image_config: ``AWS::Serverless::Function.ImageConfig``.
        :param image_uri: ``AWS::Serverless::Function.ImageUri``.
        :param inline_code: ``AWS::Serverless::Function.InlineCode``.
        :param kms_key_arn: ``AWS::Serverless::Function.KmsKeyArn``.
        :param layers: ``AWS::Serverless::Function.Layers``.
        :param memory_size: ``AWS::Serverless::Function.MemorySize``.
        :param package_type: ``AWS::Serverless::Function.PackageType``.
        :param permissions_boundary: ``AWS::Serverless::Function.PermissionsBoundary``.
        :param policies: ``AWS::Serverless::Function.Policies``.
        :param provisioned_concurrency_config: ``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.
        :param reserved_concurrent_executions: ``AWS::Serverless::Function.ReservedConcurrentExecutions``.
        :param role: ``AWS::Serverless::Function.Role``.
        :param runtime: ``AWS::Serverless::Function.Runtime``.
        :param tags: ``AWS::Serverless::Function.Tags``.
        :param timeout: ``AWS::Serverless::Function.Timeout``.
        :param tracing: ``AWS::Serverless::Function.Tracing``.
        :param version_description: ``AWS::Serverless::Function.VersionDescription``.
        :param vpc_config: ``AWS::Serverless::Function.VpcConfig``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0de068acf685722560ef730ee4ff2068f39bb26acda2f602b73a5de06853743)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFunctionProps(
            architectures=architectures,
            assume_role_policy_document=assume_role_policy_document,
            auto_publish_alias=auto_publish_alias,
            auto_publish_code_sha256=auto_publish_code_sha256,
            code_signing_config_arn=code_signing_config_arn,
            code_uri=code_uri,
            dead_letter_queue=dead_letter_queue,
            deployment_preference=deployment_preference,
            description=description,
            environment=environment,
            event_invoke_config=event_invoke_config,
            events=events,
            file_system_configs=file_system_configs,
            function_name=function_name,
            handler=handler,
            image_config=image_config,
            image_uri=image_uri,
            inline_code=inline_code,
            kms_key_arn=kms_key_arn,
            layers=layers,
            memory_size=memory_size,
            package_type=package_type,
            permissions_boundary=permissions_boundary,
            policies=policies,
            provisioned_concurrency_config=provisioned_concurrency_config,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            runtime=runtime,
            tags=tags,
            timeout=timeout,
            tracing=tracing,
            version_description=version_description,
            vpc_config=vpc_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e12a05469b93683a5f9531392ce66303e6c17d75e57f2f7658e7f5e776c3e8)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b68051667412141943a3bb2a7ac0192c89299775ec6889d9a1768274e2414ff)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Serverless::Function.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="assumeRolePolicyDocument")
    def assume_role_policy_document(self) -> typing.Any:
        '''``AWS::Serverless::Function.AssumeRolePolicyDocument``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-assumerolepolicydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "assumeRolePolicyDocument"))

    @assume_role_policy_document.setter
    def assume_role_policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375a12290ea6a1d63cc5a5cd0342a6885b337b5dd379801c28e3035d1d1fbbad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assumeRolePolicyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="architectures")
    def architectures(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Function.Architectures``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-architectures
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "architectures"))

    @architectures.setter
    def architectures(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__804275fc6da7514ecdac419882f2fef9a024d6e1d8895fa5dd54fe69da1f71db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architectures", value)

    @builtins.property
    @jsii.member(jsii_name="autoPublishAlias")
    def auto_publish_alias(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.AutoPublishAlias``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoPublishAlias"))

    @auto_publish_alias.setter
    def auto_publish_alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1991c5255aaad02611e8bedc1c8c2630a4d79c53875681aea075e4371391f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoPublishAlias", value)

    @builtins.property
    @jsii.member(jsii_name="autoPublishCodeSha256")
    def auto_publish_code_sha256(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.AutoPublishCodeSha256``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-autopublishcodesha256
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoPublishCodeSha256"))

    @auto_publish_code_sha256.setter
    def auto_publish_code_sha256(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d9afbfaecc38c523a20fd85a1db54f16430f710f70a360532b65bb1f08e0cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoPublishCodeSha256", value)

    @builtins.property
    @jsii.member(jsii_name="codeSigningConfigArn")
    def code_signing_config_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.CodeSigningConfigArn``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-codesigningconfigarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeSigningConfigArn"))

    @code_signing_config_arn.setter
    def code_signing_config_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a711c21d186a725f05bd0413466740097825e43d4bdd018d3e53fb9c2dc610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeSigningConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="codeUri")
    def code_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnFunction.S3LocationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.CodeUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnFunction.S3LocationProperty", _IResolvable_a771d0ef]], jsii.get(self, "codeUri"))

    @code_uri.setter
    def code_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnFunction.S3LocationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19dfe64e8a3347aed5bc2299b53c7bd2897871d4a646bfc6b7f0a106133b4c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeUri", value)

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.DeadLetterQueueProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.DeadLetterQueue``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.DeadLetterQueueProperty", _IResolvable_a771d0ef]], jsii.get(self, "deadLetterQueue"))

    @dead_letter_queue.setter
    def dead_letter_queue(
        self,
        value: typing.Optional[typing.Union["CfnFunction.DeadLetterQueueProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e119b59cd6d479aa69e5c52e781ea7676c97f3e3de3155de930aa9f991fd96d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deadLetterQueue", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentPreference")
    def deployment_preference(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.DeploymentPreferenceProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.DeploymentPreference``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.DeploymentPreferenceProperty", _IResolvable_a771d0ef]], jsii.get(self, "deploymentPreference"))

    @deployment_preference.setter
    def deployment_preference(
        self,
        value: typing.Optional[typing.Union["CfnFunction.DeploymentPreferenceProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a85f4e49e2f14ccf2f87b3fc9b627f69774ccc7891831d66c18517c443cb270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentPreference", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7494b2253e36226f39ddc446bd11ed5fd8c29090148170bbddd551c249784c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.FunctionEnvironmentProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.Environment``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.FunctionEnvironmentProperty", _IResolvable_a771d0ef]], jsii.get(self, "environment"))

    @environment.setter
    def environment(
        self,
        value: typing.Optional[typing.Union["CfnFunction.FunctionEnvironmentProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b02434c1938c553c5da9bbe591e782f909ac2ee738fb60454ce5ca3c38c273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value)

    @builtins.property
    @jsii.member(jsii_name="eventInvokeConfig")
    def event_invoke_config(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.EventInvokeConfigProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.EventInvokeConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.EventInvokeConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "eventInvokeConfig"))

    @event_invoke_config.setter
    def event_invoke_config(
        self,
        value: typing.Optional[typing.Union["CfnFunction.EventInvokeConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be023c816fc0668bda8c01cbcf330c514b85a3661f68eaecf6d2e56c94a189a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventInvokeConfig", value)

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnFunction.EventSourceProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Serverless::Function.Events``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnFunction.EventSourceProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "events"))

    @events.setter
    def events(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnFunction.EventSourceProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db239217b9a2443dc9d9350daffc0f690256e2daa2b4edfe8e0b330eec55ec49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value)

    @builtins.property
    @jsii.member(jsii_name="fileSystemConfigs")
    def file_system_configs(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFunction.FileSystemConfigProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Serverless::Function.FileSystemConfigs``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFunction.FileSystemConfigProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "fileSystemConfigs"))

    @file_system_configs.setter
    def file_system_configs(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFunction.FileSystemConfigProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701d77cb40ebcfeaeaf68383cdd250a6a81ff6b1bbeb35056602056c77bc0c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemConfigs", value)

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.FunctionName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5567c9f81687721aa7f6c56ed2406db4357288a7abffb019aedbbebfafb5ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Handler``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "handler"))

    @handler.setter
    def handler(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f3e4f69582686f638a74b50e9ce063581a1776db0c07c05f7fd39bb4becc57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handler", value)

    @builtins.property
    @jsii.member(jsii_name="imageConfig")
    def image_config(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.ImageConfigProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.ImageConfig``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-imageconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.ImageConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "imageConfig"))

    @image_config.setter
    def image_config(
        self,
        value: typing.Optional[typing.Union["CfnFunction.ImageConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377a1c2f1f0d78eefde5673d2e91399d440afcd850c8e527f5a55b2922f12c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageConfig", value)

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.ImageUri``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-imageuri
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373f070366098e1c79b4e5b51746473f50a0061473ad7f20c8f9363644c77885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value)

    @builtins.property
    @jsii.member(jsii_name="inlineCode")
    def inline_code(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.InlineCode``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inlineCode"))

    @inline_code.setter
    def inline_code(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe7fe7e959912ca8a56a9559b7432fdc9e681cbd25f66163b5e505613987c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inlineCode", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.KmsKeyArn``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48864df81d24b13a6a8203001089c190adae74b9771418407b3d45ce93de386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="layers")
    def layers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Function.Layers``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "layers"))

    @layers.setter
    def layers(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018472eb15e47b9349b6acb0048fe63db14477badd1289d3f0ff97ab426c532f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "layers", value)

    @builtins.property
    @jsii.member(jsii_name="memorySize")
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.MemorySize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySize"))

    @memory_size.setter
    def memory_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518b7770acda94ce3f04ba56d322586e9250bcd5d65fa7d1c30c019fdf49ca61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySize", value)

    @builtins.property
    @jsii.member(jsii_name="packageType")
    def package_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.PackageType``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-packagetype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "packageType"))

    @package_type.setter
    def package_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48db0d17bdb739c2f462f00a940c910e4ba4a03913877f8495ce709167d9cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageType", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.PermissionsBoundary``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundary"))

    @permissions_boundary.setter
    def permissions_boundary(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e630fe0f30a4505f0ca3a54d558d69661b469aea8d7b1d91730c73462b854cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundary", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", "CfnFunction.SAMPolicyTemplateProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Serverless::Function.Policies``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", "CfnFunction.SAMPolicyTemplateProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", "CfnFunction.SAMPolicyTemplateProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f3c6c961e23ba32c743496e32aed532d9a9f1bec87d22b6a28b2c136158451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrencyConfig")
    def provisioned_concurrency_config(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.ProvisionedConcurrencyConfigProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.ProvisionedConcurrencyConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "provisionedConcurrencyConfig"))

    @provisioned_concurrency_config.setter
    def provisioned_concurrency_config(
        self,
        value: typing.Optional[typing.Union["CfnFunction.ProvisionedConcurrencyConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89ee2cb8bde087ab40ecd2282d8780671c26576117d2ab6556a197de94d34eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedConcurrencyConfig", value)

    @builtins.property
    @jsii.member(jsii_name="reservedConcurrentExecutions")
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.ReservedConcurrentExecutions``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "reservedConcurrentExecutions"))

    @reserved_concurrent_executions.setter
    def reserved_concurrent_executions(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb1be95e48307dab1757f159e46ac4bdfb0c23d9332c0c03655d42f37b32fd8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedConcurrentExecutions", value)

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Role``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "role"))

    @role.setter
    def role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebab6fd8f10a58329519b09eb2d52a1fbe304ff28dc2ce852574def51a5bf0d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Runtime``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ffeb4aa04c9a78b83a16b4c52bb3a08d40437baa39328b925fcd9e535252b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.Timeout``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf59ecf8b986eb5768efac087337f966cf3e400e67f759f4fd2f4d316f00878c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)

    @builtins.property
    @jsii.member(jsii_name="tracing")
    def tracing(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Tracing``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tracing"))

    @tracing.setter
    def tracing(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf88c1925f2553a764c9fceb65343ce9672135350d771ef7cb6526beda99af3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tracing", value)

    @builtins.property
    @jsii.member(jsii_name="versionDescription")
    def version_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.VersionDescription``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionDescription"))

    @version_description.setter
    def version_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10da312f626a7017a11eea94a16d491c4a06dc796fd47c2fe4cc183d1314c1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionDescription", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.VpcConfigProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.VpcConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.VpcConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "vpcConfig"))

    @vpc_config.setter
    def vpc_config(
        self,
        value: typing.Optional[typing.Union["CfnFunction.VpcConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6defe318c0cef4d532cf2a1dec729a806c163d7589fec000b097257352b210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.AlexaSkillEventProperty",
        jsii_struct_bases=[],
        name_mapping={"variables": "variables"},
    )
    class AlexaSkillEventProperty:
        def __init__(
            self,
            *,
            variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''
            :param variables: ``CfnFunction.AlexaSkillEventProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#alexaskill
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                alexa_skill_event_property = sam.CfnFunction.AlexaSkillEventProperty(
                    variables={
                        "variables_key": "variables"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a7df05c26bf2d41d501512f754453c47c9702b430e9d9a4cae86e5491cc32be)
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def variables(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnFunction.AlexaSkillEventProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#alexaskill
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlexaSkillEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.ApiEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "method": "method",
            "path": "path",
            "auth": "auth",
            "request_model": "requestModel",
            "request_parameters": "requestParameters",
            "rest_api_id": "restApiId",
        },
    )
    class ApiEventProperty:
        def __init__(
            self,
            *,
            method: builtins.str,
            path: builtins.str,
            auth: typing.Optional[typing.Union[typing.Union["CfnFunction.AuthProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            request_model: typing.Optional[typing.Union[typing.Union["CfnFunction.RequestModelProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            request_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[builtins.str, typing.Union["CfnFunction.RequestParameterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            rest_api_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param method: ``CfnFunction.ApiEventProperty.Method``.
            :param path: ``CfnFunction.ApiEventProperty.Path``.
            :param auth: ``CfnFunction.ApiEventProperty.Auth``.
            :param request_model: ``CfnFunction.ApiEventProperty.RequestModel``.
            :param request_parameters: ``CfnFunction.ApiEventProperty.RequestParameters``.
            :param rest_api_id: ``CfnFunction.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                # custom_statements: Any
                
                api_event_property = sam.CfnFunction.ApiEventProperty(
                    method="method",
                    path="path",
                
                    # the properties below are optional
                    auth=sam.CfnFunction.AuthProperty(
                        api_key_required=False,
                        authorization_scopes=["authorizationScopes"],
                        authorizer="authorizer",
                        resource_policy=sam.CfnFunction.AuthResourcePolicyProperty(
                            aws_account_blacklist=["awsAccountBlacklist"],
                            aws_account_whitelist=["awsAccountWhitelist"],
                            custom_statements=[custom_statements],
                            intrinsic_vpc_blacklist=["intrinsicVpcBlacklist"],
                            intrinsic_vpce_blacklist=["intrinsicVpceBlacklist"],
                            intrinsic_vpce_whitelist=["intrinsicVpceWhitelist"],
                            intrinsic_vpc_whitelist=["intrinsicVpcWhitelist"],
                            ip_range_blacklist=["ipRangeBlacklist"],
                            ip_range_whitelist=["ipRangeWhitelist"],
                            source_vpc_blacklist=["sourceVpcBlacklist"],
                            source_vpc_whitelist=["sourceVpcWhitelist"]
                        )
                    ),
                    request_model=sam.CfnFunction.RequestModelProperty(
                        model="model",
                
                        # the properties below are optional
                        required=False,
                        validate_body=False,
                        validate_parameters=False
                    ),
                    request_parameters=["requestParameters"],
                    rest_api_id="restApiId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15ab38ee5864bebb8cb1499634450e772d4c5416aa150d1c2a536c700192dad9)
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
                check_type(argname="argument request_model", value=request_model, expected_type=type_hints["request_model"])
                check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
                check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "method": method,
                "path": path,
            }
            if auth is not None:
                self._values["auth"] = auth
            if request_model is not None:
                self._values["request_model"] = request_model
            if request_parameters is not None:
                self._values["request_parameters"] = request_parameters
            if rest_api_id is not None:
                self._values["rest_api_id"] = rest_api_id

        @builtins.property
        def method(self) -> builtins.str:
            '''``CfnFunction.ApiEventProperty.Method``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("method")
            assert result is not None, "Required property 'method' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def path(self) -> builtins.str:
            '''``CfnFunction.ApiEventProperty.Path``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("path")
            assert result is not None, "Required property 'path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def auth(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.AuthProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.ApiEventProperty.Auth``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("auth")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.AuthProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def request_model(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.RequestModelProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.ApiEventProperty.RequestModel``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("request_model")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.RequestModelProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def request_parameters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, "CfnFunction.RequestParameterProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnFunction.ApiEventProperty.RequestParameters``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("request_parameters")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, "CfnFunction.RequestParameterProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def rest_api_id(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("rest_api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.AuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_key_required": "apiKeyRequired",
            "authorization_scopes": "authorizationScopes",
            "authorizer": "authorizer",
            "resource_policy": "resourcePolicy",
        },
    )
    class AuthProperty:
        def __init__(
            self,
            *,
            api_key_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
            authorizer: typing.Optional[builtins.str] = None,
            resource_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.AuthResourcePolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param api_key_required: ``CfnFunction.AuthProperty.ApiKeyRequired``.
            :param authorization_scopes: ``CfnFunction.AuthProperty.AuthorizationScopes``.
            :param authorizer: ``CfnFunction.AuthProperty.Authorizer``.
            :param resource_policy: ``CfnFunction.AuthProperty.ResourcePolicy``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                # custom_statements: Any
                
                auth_property = sam.CfnFunction.AuthProperty(
                    api_key_required=False,
                    authorization_scopes=["authorizationScopes"],
                    authorizer="authorizer",
                    resource_policy=sam.CfnFunction.AuthResourcePolicyProperty(
                        aws_account_blacklist=["awsAccountBlacklist"],
                        aws_account_whitelist=["awsAccountWhitelist"],
                        custom_statements=[custom_statements],
                        intrinsic_vpc_blacklist=["intrinsicVpcBlacklist"],
                        intrinsic_vpce_blacklist=["intrinsicVpceBlacklist"],
                        intrinsic_vpce_whitelist=["intrinsicVpceWhitelist"],
                        intrinsic_vpc_whitelist=["intrinsicVpcWhitelist"],
                        ip_range_blacklist=["ipRangeBlacklist"],
                        ip_range_whitelist=["ipRangeWhitelist"],
                        source_vpc_blacklist=["sourceVpcBlacklist"],
                        source_vpc_whitelist=["sourceVpcWhitelist"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c534500bb3f39e60558efb77528ec3b161f64dbaa91ff1ee304d4d0c96b234c5)
                check_type(argname="argument api_key_required", value=api_key_required, expected_type=type_hints["api_key_required"])
                check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
                check_type(argname="argument authorizer", value=authorizer, expected_type=type_hints["authorizer"])
                check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_key_required is not None:
                self._values["api_key_required"] = api_key_required
            if authorization_scopes is not None:
                self._values["authorization_scopes"] = authorization_scopes
            if authorizer is not None:
                self._values["authorizer"] = authorizer
            if resource_policy is not None:
                self._values["resource_policy"] = resource_policy

        @builtins.property
        def api_key_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFunction.AuthProperty.ApiKeyRequired``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("api_key_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthProperty.AuthorizationScopes``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("authorization_scopes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def authorizer(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.AuthProperty.Authorizer``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.AuthResourcePolicyProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.AuthProperty.ResourcePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("resource_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.AuthResourcePolicyProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.AuthResourcePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_account_blacklist": "awsAccountBlacklist",
            "aws_account_whitelist": "awsAccountWhitelist",
            "custom_statements": "customStatements",
            "intrinsic_vpc_blacklist": "intrinsicVpcBlacklist",
            "intrinsic_vpce_blacklist": "intrinsicVpceBlacklist",
            "intrinsic_vpce_whitelist": "intrinsicVpceWhitelist",
            "intrinsic_vpc_whitelist": "intrinsicVpcWhitelist",
            "ip_range_blacklist": "ipRangeBlacklist",
            "ip_range_whitelist": "ipRangeWhitelist",
            "source_vpc_blacklist": "sourceVpcBlacklist",
            "source_vpc_whitelist": "sourceVpcWhitelist",
        },
    )
    class AuthResourcePolicyProperty:
        def __init__(
            self,
            *,
            aws_account_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            aws_account_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            custom_statements: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_a771d0ef]] = None,
            intrinsic_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            intrinsic_vpce_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            intrinsic_vpce_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            intrinsic_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            ip_range_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            ip_range_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            source_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            source_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param aws_account_blacklist: ``CfnFunction.AuthResourcePolicyProperty.AwsAccountBlacklist``.
            :param aws_account_whitelist: ``CfnFunction.AuthResourcePolicyProperty.AwsAccountWhitelist``.
            :param custom_statements: ``CfnFunction.AuthResourcePolicyProperty.CustomStatements``.
            :param intrinsic_vpc_blacklist: ``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpcBlacklist``.
            :param intrinsic_vpce_blacklist: ``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpceBlacklist``.
            :param intrinsic_vpce_whitelist: ``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpceWhitelist``.
            :param intrinsic_vpc_whitelist: ``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpcWhitelist``.
            :param ip_range_blacklist: ``CfnFunction.AuthResourcePolicyProperty.IpRangeBlacklist``.
            :param ip_range_whitelist: ``CfnFunction.AuthResourcePolicyProperty.IpRangeWhitelist``.
            :param source_vpc_blacklist: ``CfnFunction.AuthResourcePolicyProperty.SourceVpcBlacklist``.
            :param source_vpc_whitelist: ``CfnFunction.AuthResourcePolicyProperty.SourceVpcWhitelist``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                # custom_statements: Any
                
                auth_resource_policy_property = sam.CfnFunction.AuthResourcePolicyProperty(
                    aws_account_blacklist=["awsAccountBlacklist"],
                    aws_account_whitelist=["awsAccountWhitelist"],
                    custom_statements=[custom_statements],
                    intrinsic_vpc_blacklist=["intrinsicVpcBlacklist"],
                    intrinsic_vpce_blacklist=["intrinsicVpceBlacklist"],
                    intrinsic_vpce_whitelist=["intrinsicVpceWhitelist"],
                    intrinsic_vpc_whitelist=["intrinsicVpcWhitelist"],
                    ip_range_blacklist=["ipRangeBlacklist"],
                    ip_range_whitelist=["ipRangeWhitelist"],
                    source_vpc_blacklist=["sourceVpcBlacklist"],
                    source_vpc_whitelist=["sourceVpcWhitelist"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80c1fa1f37de885add91037ec07163a77c8cbdbd40f0b7799b22d44133a7a8ad)
                check_type(argname="argument aws_account_blacklist", value=aws_account_blacklist, expected_type=type_hints["aws_account_blacklist"])
                check_type(argname="argument aws_account_whitelist", value=aws_account_whitelist, expected_type=type_hints["aws_account_whitelist"])
                check_type(argname="argument custom_statements", value=custom_statements, expected_type=type_hints["custom_statements"])
                check_type(argname="argument intrinsic_vpc_blacklist", value=intrinsic_vpc_blacklist, expected_type=type_hints["intrinsic_vpc_blacklist"])
                check_type(argname="argument intrinsic_vpce_blacklist", value=intrinsic_vpce_blacklist, expected_type=type_hints["intrinsic_vpce_blacklist"])
                check_type(argname="argument intrinsic_vpce_whitelist", value=intrinsic_vpce_whitelist, expected_type=type_hints["intrinsic_vpce_whitelist"])
                check_type(argname="argument intrinsic_vpc_whitelist", value=intrinsic_vpc_whitelist, expected_type=type_hints["intrinsic_vpc_whitelist"])
                check_type(argname="argument ip_range_blacklist", value=ip_range_blacklist, expected_type=type_hints["ip_range_blacklist"])
                check_type(argname="argument ip_range_whitelist", value=ip_range_whitelist, expected_type=type_hints["ip_range_whitelist"])
                check_type(argname="argument source_vpc_blacklist", value=source_vpc_blacklist, expected_type=type_hints["source_vpc_blacklist"])
                check_type(argname="argument source_vpc_whitelist", value=source_vpc_whitelist, expected_type=type_hints["source_vpc_whitelist"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_account_blacklist is not None:
                self._values["aws_account_blacklist"] = aws_account_blacklist
            if aws_account_whitelist is not None:
                self._values["aws_account_whitelist"] = aws_account_whitelist
            if custom_statements is not None:
                self._values["custom_statements"] = custom_statements
            if intrinsic_vpc_blacklist is not None:
                self._values["intrinsic_vpc_blacklist"] = intrinsic_vpc_blacklist
            if intrinsic_vpce_blacklist is not None:
                self._values["intrinsic_vpce_blacklist"] = intrinsic_vpce_blacklist
            if intrinsic_vpce_whitelist is not None:
                self._values["intrinsic_vpce_whitelist"] = intrinsic_vpce_whitelist
            if intrinsic_vpc_whitelist is not None:
                self._values["intrinsic_vpc_whitelist"] = intrinsic_vpc_whitelist
            if ip_range_blacklist is not None:
                self._values["ip_range_blacklist"] = ip_range_blacklist
            if ip_range_whitelist is not None:
                self._values["ip_range_whitelist"] = ip_range_whitelist
            if source_vpc_blacklist is not None:
                self._values["source_vpc_blacklist"] = source_vpc_blacklist
            if source_vpc_whitelist is not None:
                self._values["source_vpc_whitelist"] = source_vpc_whitelist

        @builtins.property
        def aws_account_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.AwsAccountBlacklist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("aws_account_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def aws_account_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.AwsAccountWhitelist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("aws_account_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def custom_statements(
            self,
        ) -> typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef]]:
            '''``CfnFunction.AuthResourcePolicyProperty.CustomStatements``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("custom_statements")
            return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef]], result)

        @builtins.property
        def intrinsic_vpc_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpcBlacklist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("intrinsic_vpc_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def intrinsic_vpce_blacklist(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpceBlacklist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("intrinsic_vpce_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def intrinsic_vpce_whitelist(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpceWhitelist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("intrinsic_vpce_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def intrinsic_vpc_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpcWhitelist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("intrinsic_vpc_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def ip_range_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IpRangeBlacklist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("ip_range_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def ip_range_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IpRangeWhitelist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("ip_range_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source_vpc_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.SourceVpcBlacklist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("source_vpc_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source_vpc_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.SourceVpcWhitelist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("source_vpc_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthResourcePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.BucketSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName"},
    )
    class BucketSAMPTProperty:
        def __init__(self, *, bucket_name: builtins.str) -> None:
            '''
            :param bucket_name: ``CfnFunction.BucketSAMPTProperty.BucketName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                bucket_sAMPTProperty = sam.CfnFunction.BucketSAMPTProperty(
                    bucket_name="bucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b6cc77d8345ad124348a1a1b1f59474e377a0c721e0dca532acade7d18097a1)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
            }

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''``CfnFunction.BucketSAMPTProperty.BucketName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BucketSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.CloudWatchEventEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class CloudWatchEventEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnFunction.CloudWatchEventEventProperty.Pattern``.
            :param input: ``CfnFunction.CloudWatchEventEventProperty.Input``.
            :param input_path: ``CfnFunction.CloudWatchEventEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                # pattern: Any
                
                cloud_watch_event_event_property = sam.CfnFunction.CloudWatchEventEventProperty(
                    pattern=pattern,
                
                    # the properties below are optional
                    input="input",
                    input_path="inputPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd1adf6783f3a17e48227575af8e4f52a2a73165a8a8383ddc167d379dfaa6f4)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "pattern": pattern,
            }
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnFunction.CloudWatchEventEventProperty.Pattern``.

            :link: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.CloudWatchEventEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.CloudWatchEventEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchEventEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.CloudWatchLogsEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "filter_pattern": "filterPattern",
            "log_group_name": "logGroupName",
        },
    )
    class CloudWatchLogsEventProperty:
        def __init__(
            self,
            *,
            filter_pattern: builtins.str,
            log_group_name: builtins.str,
        ) -> None:
            '''
            :param filter_pattern: ``CfnFunction.CloudWatchLogsEventProperty.FilterPattern``.
            :param log_group_name: ``CfnFunction.CloudWatchLogsEventProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                cloud_watch_logs_event_property = sam.CfnFunction.CloudWatchLogsEventProperty(
                    filter_pattern="filterPattern",
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2943ed1df7fdbfc76cbecefb386bf6fe4281986e4406a33b157de638c464e6b)
                check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "filter_pattern": filter_pattern,
                "log_group_name": log_group_name,
            }

        @builtins.property
        def filter_pattern(self) -> builtins.str:
            '''``CfnFunction.CloudWatchLogsEventProperty.FilterPattern``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchlogs
            '''
            result = self._values.get("filter_pattern")
            assert result is not None, "Required property 'filter_pattern' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_group_name(self) -> builtins.str:
            '''``CfnFunction.CloudWatchLogsEventProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchlogs
            '''
            result = self._values.get("log_group_name")
            assert result is not None, "Required property 'log_group_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.CollectionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"collection_id": "collectionId"},
    )
    class CollectionSAMPTProperty:
        def __init__(self, *, collection_id: builtins.str) -> None:
            '''
            :param collection_id: ``CfnFunction.CollectionSAMPTProperty.CollectionId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                collection_sAMPTProperty = sam.CfnFunction.CollectionSAMPTProperty(
                    collection_id="collectionId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a722d45eb35303595002dea40acebe21f27a4a78b02a373806d2edcf79ff5ae)
                check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "collection_id": collection_id,
            }

        @builtins.property
        def collection_id(self) -> builtins.str:
            '''``CfnFunction.CollectionSAMPTProperty.CollectionId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("collection_id")
            assert result is not None, "Required property 'collection_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CollectionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.DeadLetterQueueProperty",
        jsii_struct_bases=[],
        name_mapping={"target_arn": "targetArn", "type": "type"},
    )
    class DeadLetterQueueProperty:
        def __init__(self, *, target_arn: builtins.str, type: builtins.str) -> None:
            '''
            :param target_arn: ``CfnFunction.DeadLetterQueueProperty.TargetArn``.
            :param type: ``CfnFunction.DeadLetterQueueProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deadletterqueue-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                dead_letter_queue_property = sam.CfnFunction.DeadLetterQueueProperty(
                    target_arn="targetArn",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb9621a4710099a7ee6a6aff484ed86576d597341996d5b2342f67c28ff5e00d)
                check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_arn": target_arn,
                "type": type,
            }

        @builtins.property
        def target_arn(self) -> builtins.str:
            '''``CfnFunction.DeadLetterQueueProperty.TargetArn``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("target_arn")
            assert result is not None, "Required property 'target_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnFunction.DeadLetterQueueProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeadLetterQueueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.DeploymentPreferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "type": "type",
            "alarms": "alarms",
            "hooks": "hooks",
        },
    )
    class DeploymentPreferenceProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            type: builtins.str,
            alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
            hooks: typing.Optional[typing.Union[typing.Union["CfnFunction.HooksProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnFunction.DeploymentPreferenceProperty.Enabled``.
            :param type: ``CfnFunction.DeploymentPreferenceProperty.Type``.
            :param alarms: ``CfnFunction.DeploymentPreferenceProperty.Alarms``.
            :param hooks: ``CfnFunction.DeploymentPreferenceProperty.Hooks``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/safe_lambda_deployments.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                deployment_preference_property = sam.CfnFunction.DeploymentPreferenceProperty(
                    enabled=False,
                    type="type",
                
                    # the properties below are optional
                    alarms=["alarms"],
                    hooks=sam.CfnFunction.HooksProperty(
                        post_traffic="postTraffic",
                        pre_traffic="preTraffic"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1ed46c5ebbd769808717492c1986de9da633e053265e65a470ca1abf8e972c1)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
                check_type(argname="argument hooks", value=hooks, expected_type=type_hints["hooks"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
                "type": type,
            }
            if alarms is not None:
                self._values["alarms"] = alarms
            if hooks is not None:
                self._values["hooks"] = hooks

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnFunction.DeploymentPreferenceProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnFunction.DeploymentPreferenceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def alarms(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.DeploymentPreferenceProperty.Alarms``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("alarms")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def hooks(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.HooksProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.DeploymentPreferenceProperty.Hooks``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("hooks")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.HooksProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentPreferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.DestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"on_failure": "onFailure"},
    )
    class DestinationConfigProperty:
        def __init__(
            self,
            *,
            on_failure: typing.Union[typing.Union["CfnFunction.DestinationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param on_failure: ``CfnFunction.DestinationConfigProperty.OnFailure``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                destination_config_property = sam.CfnFunction.DestinationConfigProperty(
                    on_failure=sam.CfnFunction.DestinationProperty(
                        destination="destination",
                
                        # the properties below are optional
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ad528993e60b85172808cfbd39ff1ae91cf5791b5be958de66e3d73c9d7262fc)
                check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "on_failure": on_failure,
            }

        @builtins.property
        def on_failure(
            self,
        ) -> typing.Union["CfnFunction.DestinationProperty", _IResolvable_a771d0ef]:
            '''``CfnFunction.DestinationConfigProperty.OnFailure``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            '''
            result = self._values.get("on_failure")
            assert result is not None, "Required property 'on_failure' is missing"
            return typing.cast(typing.Union["CfnFunction.DestinationProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "type": "type"},
    )
    class DestinationProperty:
        def __init__(
            self,
            *,
            destination: builtins.str,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination: ``CfnFunction.DestinationProperty.Destination``.
            :param type: ``CfnFunction.DestinationProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                destination_property = sam.CfnFunction.DestinationProperty(
                    destination="destination",
                
                    # the properties below are optional
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3075edb20a46edbf9e5c848415719c2fb409c26085d7d49ae8f9839b7b9f48d)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination": destination,
            }
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def destination(self) -> builtins.str:
            '''``CfnFunction.DestinationProperty.Destination``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.DestinationProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.DomainSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName"},
    )
    class DomainSAMPTProperty:
        def __init__(self, *, domain_name: builtins.str) -> None:
            '''
            :param domain_name: ``CfnFunction.DomainSAMPTProperty.DomainName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                domain_sAMPTProperty = sam.CfnFunction.DomainSAMPTProperty(
                    domain_name="domainName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e7c9fcb29aa8589419e9a8986d540e9f09e79b505427984ab72821be3e8f7fd)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "domain_name": domain_name,
            }

        @builtins.property
        def domain_name(self) -> builtins.str:
            '''``CfnFunction.DomainSAMPTProperty.DomainName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("domain_name")
            assert result is not None, "Required property 'domain_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.DynamoDBEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "starting_position": "startingPosition",
            "stream": "stream",
            "batch_size": "batchSize",
            "bisect_batch_on_function_error": "bisectBatchOnFunctionError",
            "destination_config": "destinationConfig",
            "enabled": "enabled",
            "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
            "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
            "parallelization_factor": "parallelizationFactor",
        },
    )
    class DynamoDBEventProperty:
        def __init__(
            self,
            *,
            starting_position: builtins.str,
            stream: builtins.str,
            batch_size: typing.Optional[jsii.Number] = None,
            bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            destination_config: typing.Optional[typing.Union[typing.Union["CfnFunction.DestinationConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
            parallelization_factor: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param starting_position: ``CfnFunction.DynamoDBEventProperty.StartingPosition``.
            :param stream: ``CfnFunction.DynamoDBEventProperty.Stream``.
            :param batch_size: ``CfnFunction.DynamoDBEventProperty.BatchSize``.
            :param bisect_batch_on_function_error: ``CfnFunction.DynamoDBEventProperty.BisectBatchOnFunctionError``.
            :param destination_config: ``CfnFunction.DynamoDBEventProperty.DestinationConfig``.
            :param enabled: ``CfnFunction.DynamoDBEventProperty.Enabled``.
            :param maximum_batching_window_in_seconds: ``CfnFunction.DynamoDBEventProperty.MaximumBatchingWindowInSeconds``.
            :param maximum_record_age_in_seconds: ``CfnFunction.DynamoDBEventProperty.MaximumRecordAgeInSeconds``.
            :param maximum_retry_attempts: ``CfnFunction.DynamoDBEventProperty.MaximumRetryAttempts``.
            :param parallelization_factor: ``CfnFunction.DynamoDBEventProperty.ParallelizationFactor``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                dynamo_dBEvent_property = sam.CfnFunction.DynamoDBEventProperty(
                    starting_position="startingPosition",
                    stream="stream",
                
                    # the properties below are optional
                    batch_size=123,
                    bisect_batch_on_function_error=False,
                    destination_config=sam.CfnFunction.DestinationConfigProperty(
                        on_failure=sam.CfnFunction.DestinationProperty(
                            destination="destination",
                
                            # the properties below are optional
                            type="type"
                        )
                    ),
                    enabled=False,
                    maximum_batching_window_in_seconds=123,
                    maximum_record_age_in_seconds=123,
                    maximum_retry_attempts=123,
                    parallelization_factor=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e71bd9ca43af2cdbb04cbe8bf9a32728e966d77b67ff70f10f4d7998aebbcbc0)
                check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
                check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument bisect_batch_on_function_error", value=bisect_batch_on_function_error, expected_type=type_hints["bisect_batch_on_function_error"])
                check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
                check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
                check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
                check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "starting_position": starting_position,
                "stream": stream,
            }
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if bisect_batch_on_function_error is not None:
                self._values["bisect_batch_on_function_error"] = bisect_batch_on_function_error
            if destination_config is not None:
                self._values["destination_config"] = destination_config
            if enabled is not None:
                self._values["enabled"] = enabled
            if maximum_batching_window_in_seconds is not None:
                self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
            if maximum_record_age_in_seconds is not None:
                self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts
            if parallelization_factor is not None:
                self._values["parallelization_factor"] = parallelization_factor

        @builtins.property
        def starting_position(self) -> builtins.str:
            '''``CfnFunction.DynamoDBEventProperty.StartingPosition``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("starting_position")
            assert result is not None, "Required property 'starting_position' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def stream(self) -> builtins.str:
            '''``CfnFunction.DynamoDBEventProperty.Stream``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("stream")
            assert result is not None, "Required property 'stream' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.BatchSize``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def bisect_batch_on_function_error(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFunction.DynamoDBEventProperty.BisectBatchOnFunctionError``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("bisect_batch_on_function_error")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def destination_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.DestinationConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.DynamoDBEventProperty.DestinationConfig``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("destination_config")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.DestinationConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFunction.DynamoDBEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.MaximumBatchingWindowInSeconds``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("maximum_batching_window_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.MaximumRecordAgeInSeconds``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("maximum_record_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.MaximumRetryAttempts``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def parallelization_factor(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.ParallelizationFactor``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("parallelization_factor")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.EmptySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class EmptySAMPTProperty:
        def __init__(self) -> None:
            '''
            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                empty_sAMPTProperty = sam.CfnFunction.EmptySAMPTProperty()
            '''
            self._values: typing.Dict[builtins.str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmptySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.EventBridgeRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class EventBridgeRuleEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnFunction.EventBridgeRuleEventProperty.Pattern``.
            :param event_bus_name: ``CfnFunction.EventBridgeRuleEventProperty.EventBusName``.
            :param input: ``CfnFunction.EventBridgeRuleEventProperty.Input``.
            :param input_path: ``CfnFunction.EventBridgeRuleEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                # pattern: Any
                
                event_bridge_rule_event_property = sam.CfnFunction.EventBridgeRuleEventProperty(
                    pattern=pattern,
                
                    # the properties below are optional
                    event_bus_name="eventBusName",
                    input="input",
                    input_path="inputPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b30d870ab1ae35a9ed02e4d6b319250cdc4bfe14c413a3ac88c0ffdff5026d18)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
                check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "pattern": pattern,
            }
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnFunction.EventBridgeRuleEventProperty.Pattern``.

            :link: https://docs.aws.amazon.com/eventbridge/latest/userguide/filtering-examples-structure.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.EventBridgeRuleEventProperty.EventBusName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.EventBridgeRuleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.EventBridgeRuleEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.EventInvokeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_config": "destinationConfig",
            "maximum_event_age_in_seconds": "maximumEventAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
        },
    )
    class EventInvokeConfigProperty:
        def __init__(
            self,
            *,
            destination_config: typing.Optional[typing.Union[typing.Union["CfnFunction.EventInvokeDestinationConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param destination_config: ``CfnFunction.EventInvokeConfigProperty.DestinationConfig``.
            :param maximum_event_age_in_seconds: ``CfnFunction.EventInvokeConfigProperty.MaximumEventAgeInSeconds``.
            :param maximum_retry_attempts: ``CfnFunction.EventInvokeConfigProperty.MaximumRetryAttempts``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-config-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                event_invoke_config_property = sam.CfnFunction.EventInvokeConfigProperty(
                    destination_config=sam.CfnFunction.EventInvokeDestinationConfigProperty(
                        on_failure=sam.CfnFunction.DestinationProperty(
                            destination="destination",
                
                            # the properties below are optional
                            type="type"
                        ),
                        on_success=sam.CfnFunction.DestinationProperty(
                            destination="destination",
                
                            # the properties below are optional
                            type="type"
                        )
                    ),
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__06f95edaebe61be780428f489b76fb5fc9f40a224066d242676cffa7772c149b)
                check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
                check_type(argname="argument maximum_event_age_in_seconds", value=maximum_event_age_in_seconds, expected_type=type_hints["maximum_event_age_in_seconds"])
                check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_config is not None:
                self._values["destination_config"] = destination_config
            if maximum_event_age_in_seconds is not None:
                self._values["maximum_event_age_in_seconds"] = maximum_event_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts

        @builtins.property
        def destination_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EventInvokeDestinationConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.EventInvokeConfigProperty.DestinationConfig``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-config-object
            '''
            result = self._values.get("destination_config")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EventInvokeDestinationConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def maximum_event_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.EventInvokeConfigProperty.MaximumEventAgeInSeconds``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-config-object
            '''
            result = self._values.get("maximum_event_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.EventInvokeConfigProperty.MaximumRetryAttempts``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-config-object
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventInvokeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.EventInvokeDestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"on_failure": "onFailure", "on_success": "onSuccess"},
    )
    class EventInvokeDestinationConfigProperty:
        def __init__(
            self,
            *,
            on_failure: typing.Union[typing.Union["CfnFunction.DestinationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            on_success: typing.Union[typing.Union["CfnFunction.DestinationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param on_failure: ``CfnFunction.EventInvokeDestinationConfigProperty.OnFailure``.
            :param on_success: ``CfnFunction.EventInvokeDestinationConfigProperty.OnSuccess``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-destination-config-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                event_invoke_destination_config_property = sam.CfnFunction.EventInvokeDestinationConfigProperty(
                    on_failure=sam.CfnFunction.DestinationProperty(
                        destination="destination",
                
                        # the properties below are optional
                        type="type"
                    ),
                    on_success=sam.CfnFunction.DestinationProperty(
                        destination="destination",
                
                        # the properties below are optional
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0c7f8d2257400f6650cd91dd60b0f27ffeb5c6e37dfdbc3f0629b8b2ecf29d0)
                check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
                check_type(argname="argument on_success", value=on_success, expected_type=type_hints["on_success"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "on_failure": on_failure,
                "on_success": on_success,
            }

        @builtins.property
        def on_failure(
            self,
        ) -> typing.Union["CfnFunction.DestinationProperty", _IResolvable_a771d0ef]:
            '''``CfnFunction.EventInvokeDestinationConfigProperty.OnFailure``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-destination-config-object
            '''
            result = self._values.get("on_failure")
            assert result is not None, "Required property 'on_failure' is missing"
            return typing.cast(typing.Union["CfnFunction.DestinationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def on_success(
            self,
        ) -> typing.Union["CfnFunction.DestinationProperty", _IResolvable_a771d0ef]:
            '''``CfnFunction.EventInvokeDestinationConfigProperty.OnSuccess``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-destination-config-object
            '''
            result = self._values.get("on_success")
            assert result is not None, "Required property 'on_success' is missing"
            return typing.cast(typing.Union["CfnFunction.DestinationProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventInvokeDestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.EventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"properties": "properties", "type": "type"},
    )
    class EventSourceProperty:
        def __init__(
            self,
            *,
            properties: typing.Union[typing.Union["CfnFunction.AlexaSkillEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.ApiEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.CloudWatchEventEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.CloudWatchLogsEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.DynamoDBEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.EventBridgeRuleEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.IoTRuleEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.KinesisEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.S3EventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.SNSEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.SQSEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.ScheduleEventProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            type: builtins.str,
        ) -> None:
            '''
            :param properties: ``CfnFunction.EventSourceProperty.Properties``.
            :param type: ``CfnFunction.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                event_source_property = sam.CfnFunction.EventSourceProperty(
                    properties=sam.CfnFunction.S3EventProperty(
                        variables={
                            "variables_key": "variables"
                        }
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea52d536f6a79bb2a00a85d54edbc2e6745cacf6a7249113ff29084f28d29762)
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "properties": properties,
                "type": type,
            }

        @builtins.property
        def properties(
            self,
        ) -> typing.Union["CfnFunction.AlexaSkillEventProperty", "CfnFunction.ApiEventProperty", "CfnFunction.CloudWatchEventEventProperty", "CfnFunction.CloudWatchLogsEventProperty", "CfnFunction.DynamoDBEventProperty", "CfnFunction.EventBridgeRuleEventProperty", "CfnFunction.IoTRuleEventProperty", "CfnFunction.KinesisEventProperty", "CfnFunction.S3EventProperty", "CfnFunction.SNSEventProperty", "CfnFunction.SQSEventProperty", "CfnFunction.ScheduleEventProperty", _IResolvable_a771d0ef]:
            '''``CfnFunction.EventSourceProperty.Properties``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-types
            '''
            result = self._values.get("properties")
            assert result is not None, "Required property 'properties' is missing"
            return typing.cast(typing.Union["CfnFunction.AlexaSkillEventProperty", "CfnFunction.ApiEventProperty", "CfnFunction.CloudWatchEventEventProperty", "CfnFunction.CloudWatchLogsEventProperty", "CfnFunction.DynamoDBEventProperty", "CfnFunction.EventBridgeRuleEventProperty", "CfnFunction.IoTRuleEventProperty", "CfnFunction.KinesisEventProperty", "CfnFunction.S3EventProperty", "CfnFunction.SNSEventProperty", "CfnFunction.SQSEventProperty", "CfnFunction.ScheduleEventProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnFunction.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.FileSystemConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "local_mount_path": "localMountPath"},
    )
    class FileSystemConfigProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            local_mount_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param arn: ``CfnFunction.FileSystemConfigProperty.Arn``.
            :param local_mount_path: ``CfnFunction.FileSystemConfigProperty.LocalMountPath``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html#cfn-lambda-function-filesystemconfig-localmountpath
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                file_system_config_property = sam.CfnFunction.FileSystemConfigProperty(
                    arn="arn",
                    local_mount_path="localMountPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a61ec2c7bb73b664df38f125555576bb30fc2268956b8e0969fd943615c2cbe)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument local_mount_path", value=local_mount_path, expected_type=type_hints["local_mount_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if local_mount_path is not None:
                self._values["local_mount_path"] = local_mount_path

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.FileSystemConfigProperty.Arn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html#cfn-lambda-function-filesystemconfig-localmountpath
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def local_mount_path(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.FileSystemConfigProperty.LocalMountPath``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html#cfn-lambda-function-filesystemconfig-localmountpath
            '''
            result = self._values.get("local_mount_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileSystemConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.FunctionEnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={"variables": "variables"},
    )
    class FunctionEnvironmentProperty:
        def __init__(
            self,
            *,
            variables: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]],
        ) -> None:
            '''
            :param variables: ``CfnFunction.FunctionEnvironmentProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#environment-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                function_environment_property = sam.CfnFunction.FunctionEnvironmentProperty(
                    variables={
                        "variables_key": "variables"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11ddecf71d5b106da79c787c3b30275499ddf30459d7c840f702fb238d4acbac)
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "variables": variables,
            }

        @builtins.property
        def variables(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]:
            '''``CfnFunction.FunctionEnvironmentProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#environment-object
            '''
            result = self._values.get("variables")
            assert result is not None, "Required property 'variables' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionEnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.FunctionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"function_name": "functionName"},
    )
    class FunctionSAMPTProperty:
        def __init__(self, *, function_name: builtins.str) -> None:
            '''
            :param function_name: ``CfnFunction.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                function_sAMPTProperty = sam.CfnFunction.FunctionSAMPTProperty(
                    function_name="functionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71c23fab1970d3079a076a370635a9d09cc06d56d15b3ffb02d3d9bb2a798041)
                check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "function_name": function_name,
            }

        @builtins.property
        def function_name(self) -> builtins.str:
            '''``CfnFunction.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("function_name")
            assert result is not None, "Required property 'function_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.HooksProperty",
        jsii_struct_bases=[],
        name_mapping={"post_traffic": "postTraffic", "pre_traffic": "preTraffic"},
    )
    class HooksProperty:
        def __init__(
            self,
            *,
            post_traffic: typing.Optional[builtins.str] = None,
            pre_traffic: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param post_traffic: ``CfnFunction.HooksProperty.PostTraffic``.
            :param pre_traffic: ``CfnFunction.HooksProperty.PreTraffic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/safe_lambda_deployments.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                hooks_property = sam.CfnFunction.HooksProperty(
                    post_traffic="postTraffic",
                    pre_traffic="preTraffic"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__12c3f0667e75b9bc2c45dc4e7d6b2ee2a6138e392041c355eeda88d18a8384e4)
                check_type(argname="argument post_traffic", value=post_traffic, expected_type=type_hints["post_traffic"])
                check_type(argname="argument pre_traffic", value=pre_traffic, expected_type=type_hints["pre_traffic"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if post_traffic is not None:
                self._values["post_traffic"] = post_traffic
            if pre_traffic is not None:
                self._values["pre_traffic"] = pre_traffic

        @builtins.property
        def post_traffic(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.HooksProperty.PostTraffic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("post_traffic")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pre_traffic(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.HooksProperty.PreTraffic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("pre_traffic")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HooksProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.IAMPolicyDocumentProperty",
        jsii_struct_bases=[],
        name_mapping={"statement": "statement", "version": "version"},
    )
    class IAMPolicyDocumentProperty:
        def __init__(
            self,
            *,
            statement: typing.Any,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param statement: ``CfnFunction.IAMPolicyDocumentProperty.Statement``.
            :param version: ``CfnFunction.IAMPolicyDocumentProperty.Version``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                # statement: Any
                
                i_aMPolicy_document_property = {
                    "statement": statement,
                
                    # the properties below are optional
                    "version": "version"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3bdf32f1b1e8a4a536505b65dbe578e887bf27c908cd5386ba85b7b044a64b2)
                check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "statement": statement,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def statement(self) -> typing.Any:
            '''``CfnFunction.IAMPolicyDocumentProperty.Statement``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            result = self._values.get("statement")
            assert result is not None, "Required property 'statement' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.IAMPolicyDocumentProperty.Version``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IAMPolicyDocumentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.IdentitySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"identity_name": "identityName"},
    )
    class IdentitySAMPTProperty:
        def __init__(self, *, identity_name: builtins.str) -> None:
            '''
            :param identity_name: ``CfnFunction.IdentitySAMPTProperty.IdentityName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                identity_sAMPTProperty = sam.CfnFunction.IdentitySAMPTProperty(
                    identity_name="identityName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3cedf8c3360513df2b0f3ba2b39bdcfb7904eddac0008c5b37d016f9aa5fd7a)
                check_type(argname="argument identity_name", value=identity_name, expected_type=type_hints["identity_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "identity_name": identity_name,
            }

        @builtins.property
        def identity_name(self) -> builtins.str:
            '''``CfnFunction.IdentitySAMPTProperty.IdentityName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("identity_name")
            assert result is not None, "Required property 'identity_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentitySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.ImageConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "command": "command",
            "entry_point": "entryPoint",
            "working_directory": "workingDirectory",
        },
    )
    class ImageConfigProperty:
        def __init__(
            self,
            *,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
            working_directory: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param command: ``CfnFunction.ImageConfigProperty.Command``.
            :param entry_point: ``CfnFunction.ImageConfigProperty.EntryPoint``.
            :param working_directory: ``CfnFunction.ImageConfigProperty.WorkingDirectory``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                image_config_property = sam.CfnFunction.ImageConfigProperty(
                    command=["command"],
                    entry_point=["entryPoint"],
                    working_directory="workingDirectory"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__232ecaef435e6878fe68947f571bfbfeb4694b29e759635268d752bab436026b)
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument entry_point", value=entry_point, expected_type=type_hints["entry_point"])
                check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if command is not None:
                self._values["command"] = command
            if entry_point is not None:
                self._values["entry_point"] = entry_point
            if working_directory is not None:
                self._values["working_directory"] = working_directory

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.ImageConfigProperty.Command``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html#cfn-lambda-function-imageconfig-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def entry_point(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.ImageConfigProperty.EntryPoint``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html#cfn-lambda-function-imageconfig-entrypoint
            '''
            result = self._values.get("entry_point")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def working_directory(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ImageConfigProperty.WorkingDirectory``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html#cfn-lambda-function-imageconfig-workingdirectory
            '''
            result = self._values.get("working_directory")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.IoTRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={"sql": "sql", "aws_iot_sql_version": "awsIotSqlVersion"},
    )
    class IoTRuleEventProperty:
        def __init__(
            self,
            *,
            sql: builtins.str,
            aws_iot_sql_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param sql: ``CfnFunction.IoTRuleEventProperty.Sql``.
            :param aws_iot_sql_version: ``CfnFunction.IoTRuleEventProperty.AwsIotSqlVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#iotrule
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                io_tRule_event_property = sam.CfnFunction.IoTRuleEventProperty(
                    sql="sql",
                
                    # the properties below are optional
                    aws_iot_sql_version="awsIotSqlVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f16a8c649ec5f9e447c10019acecaddd129ad45a6a45040c3f73488fbdfebc9)
                check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
                check_type(argname="argument aws_iot_sql_version", value=aws_iot_sql_version, expected_type=type_hints["aws_iot_sql_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "sql": sql,
            }
            if aws_iot_sql_version is not None:
                self._values["aws_iot_sql_version"] = aws_iot_sql_version

        @builtins.property
        def sql(self) -> builtins.str:
            '''``CfnFunction.IoTRuleEventProperty.Sql``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#iotrule
            '''
            result = self._values.get("sql")
            assert result is not None, "Required property 'sql' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def aws_iot_sql_version(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.IoTRuleEventProperty.AwsIotSqlVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#iotrule
            '''
            result = self._values.get("aws_iot_sql_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.KeySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"key_id": "keyId"},
    )
    class KeySAMPTProperty:
        def __init__(self, *, key_id: builtins.str) -> None:
            '''
            :param key_id: ``CfnFunction.KeySAMPTProperty.KeyId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                key_sAMPTProperty = sam.CfnFunction.KeySAMPTProperty(
                    key_id="keyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__670a3f3d405a39c92fea391f7fbaafb3c7217bacdbed026b6acd8b0c7a4c63df)
                check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key_id": key_id,
            }

        @builtins.property
        def key_id(self) -> builtins.str:
            '''``CfnFunction.KeySAMPTProperty.KeyId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("key_id")
            assert result is not None, "Required property 'key_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.KinesisEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "starting_position": "startingPosition",
            "stream": "stream",
            "batch_size": "batchSize",
            "enabled": "enabled",
        },
    )
    class KinesisEventProperty:
        def __init__(
            self,
            *,
            starting_position: builtins.str,
            stream: builtins.str,
            batch_size: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param starting_position: ``CfnFunction.KinesisEventProperty.StartingPosition``.
            :param stream: ``CfnFunction.KinesisEventProperty.Stream``.
            :param batch_size: ``CfnFunction.KinesisEventProperty.BatchSize``.
            :param enabled: ``CfnFunction.KinesisEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                kinesis_event_property = sam.CfnFunction.KinesisEventProperty(
                    starting_position="startingPosition",
                    stream="stream",
                
                    # the properties below are optional
                    batch_size=123,
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a2f39bca540600fcb83759b376489168b314d5b654bde65e559a34cea6b0888)
                check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
                check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "starting_position": starting_position,
                "stream": stream,
            }
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def starting_position(self) -> builtins.str:
            '''``CfnFunction.KinesisEventProperty.StartingPosition``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("starting_position")
            assert result is not None, "Required property 'starting_position' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def stream(self) -> builtins.str:
            '''``CfnFunction.KinesisEventProperty.Stream``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("stream")
            assert result is not None, "Required property 'stream' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.KinesisEventProperty.BatchSize``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFunction.KinesisEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.LogGroupSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName"},
    )
    class LogGroupSAMPTProperty:
        def __init__(self, *, log_group_name: builtins.str) -> None:
            '''
            :param log_group_name: ``CfnFunction.LogGroupSAMPTProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                log_group_sAMPTProperty = sam.CfnFunction.LogGroupSAMPTProperty(
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57bf8c40ca26e976ae703c815e0d5d6eb912f82ef63469a4308c8c05f404ac44)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_group_name": log_group_name,
            }

        @builtins.property
        def log_group_name(self) -> builtins.str:
            '''``CfnFunction.LogGroupSAMPTProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("log_group_name")
            assert result is not None, "Required property 'log_group_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogGroupSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.ParameterNameSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"parameter_name": "parameterName"},
    )
    class ParameterNameSAMPTProperty:
        def __init__(self, *, parameter_name: builtins.str) -> None:
            '''
            :param parameter_name: ``CfnFunction.ParameterNameSAMPTProperty.ParameterName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                parameter_name_sAMPTProperty = sam.CfnFunction.ParameterNameSAMPTProperty(
                    parameter_name="parameterName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3bff9afa411607f2d768f5cc6afc724b84626eae4b65660aac9c9b3fccbbdb7f)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "parameter_name": parameter_name,
            }

        @builtins.property
        def parameter_name(self) -> builtins.str:
            '''``CfnFunction.ParameterNameSAMPTProperty.ParameterName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("parameter_name")
            assert result is not None, "Required property 'parameter_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterNameSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.ProvisionedConcurrencyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "provisioned_concurrent_executions": "provisionedConcurrentExecutions",
        },
    )
    class ProvisionedConcurrencyConfigProperty:
        def __init__(self, *, provisioned_concurrent_executions: builtins.str) -> None:
            '''
            :param provisioned_concurrent_executions: ``CfnFunction.ProvisionedConcurrencyConfigProperty.ProvisionedConcurrentExecutions``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#provisioned-concurrency-config-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                provisioned_concurrency_config_property = sam.CfnFunction.ProvisionedConcurrencyConfigProperty(
                    provisioned_concurrent_executions="provisionedConcurrentExecutions"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11b794589fea6427a02b47c345278125621d90ba663013f08e28f70242b80e9e)
                check_type(argname="argument provisioned_concurrent_executions", value=provisioned_concurrent_executions, expected_type=type_hints["provisioned_concurrent_executions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "provisioned_concurrent_executions": provisioned_concurrent_executions,
            }

        @builtins.property
        def provisioned_concurrent_executions(self) -> builtins.str:
            '''``CfnFunction.ProvisionedConcurrencyConfigProperty.ProvisionedConcurrentExecutions``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#provisioned-concurrency-config-object
            '''
            result = self._values.get("provisioned_concurrent_executions")
            assert result is not None, "Required property 'provisioned_concurrent_executions' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedConcurrencyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.QueueSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"queue_name": "queueName"},
    )
    class QueueSAMPTProperty:
        def __init__(self, *, queue_name: builtins.str) -> None:
            '''
            :param queue_name: ``CfnFunction.QueueSAMPTProperty.QueueName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                queue_sAMPTProperty = sam.CfnFunction.QueueSAMPTProperty(
                    queue_name="queueName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6637cb5af07936531c635c412fa5b51265ff073e4e6562ff60c01fc5b8742707)
                check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "queue_name": queue_name,
            }

        @builtins.property
        def queue_name(self) -> builtins.str:
            '''``CfnFunction.QueueSAMPTProperty.QueueName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("queue_name")
            assert result is not None, "Required property 'queue_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueueSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.RequestModelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "model": "model",
            "required": "required",
            "validate_body": "validateBody",
            "validate_parameters": "validateParameters",
        },
    )
    class RequestModelProperty:
        def __init__(
            self,
            *,
            model: builtins.str,
            required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            validate_body: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            validate_parameters: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param model: ``CfnFunction.RequestModelProperty.Model``.
            :param required: ``CfnFunction.RequestModelProperty.Required``.
            :param validate_body: ``CfnFunction.RequestModelProperty.ValidateBody``.
            :param validate_parameters: ``CfnFunction.RequestModelProperty.ValidateParameters``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestmodel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                request_model_property = sam.CfnFunction.RequestModelProperty(
                    model="model",
                
                    # the properties below are optional
                    required=False,
                    validate_body=False,
                    validate_parameters=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__527081aabc5dbbac6ee5b0777ec3a39fbd25365ab15b8a774be3307b0ef69331)
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
                check_type(argname="argument validate_body", value=validate_body, expected_type=type_hints["validate_body"])
                check_type(argname="argument validate_parameters", value=validate_parameters, expected_type=type_hints["validate_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "model": model,
            }
            if required is not None:
                self._values["required"] = required
            if validate_body is not None:
                self._values["validate_body"] = validate_body
            if validate_parameters is not None:
                self._values["validate_parameters"] = validate_parameters

        @builtins.property
        def model(self) -> builtins.str:
            '''``CfnFunction.RequestModelProperty.Model``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestmodel.html#sam-function-requestmodel-model
            '''
            result = self._values.get("model")
            assert result is not None, "Required property 'model' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFunction.RequestModelProperty.Required``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestmodel.html#sam-function-requestmodel-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def validate_body(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFunction.RequestModelProperty.ValidateBody``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestmodel.html#sam-function-requestmodel-validatebody
            '''
            result = self._values.get("validate_body")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def validate_parameters(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFunction.RequestModelProperty.ValidateParameters``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestmodel.html#sam-function-requestmodel-validateparameters
            '''
            result = self._values.get("validate_parameters")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequestModelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.RequestParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"caching": "caching", "required": "required"},
    )
    class RequestParameterProperty:
        def __init__(
            self,
            *,
            caching: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param caching: ``CfnFunction.RequestParameterProperty.Caching``.
            :param required: ``CfnFunction.RequestParameterProperty.Required``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                request_parameter_property = sam.CfnFunction.RequestParameterProperty(
                    caching=False,
                    required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4808a4ac5d444e4da34872ad607e0cdd2a0f8a3e405e424b9b772e788e9d283f)
                check_type(argname="argument caching", value=caching, expected_type=type_hints["caching"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if caching is not None:
                self._values["caching"] = caching
            if required is not None:
                self._values["required"] = required

        @builtins.property
        def caching(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFunction.RequestParameterProperty.Caching``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestparameter.html#sam-function-requestparameter-caching
            '''
            result = self._values.get("caching")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFunction.RequestParameterProperty.Required``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestparameter.html#sam-function-requestparameter-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequestParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.S3EventProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "events": "events", "filter": "filter"},
    )
    class S3EventProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            events: typing.Union[builtins.str, _IResolvable_a771d0ef, typing.Sequence[builtins.str]],
            filter: typing.Optional[typing.Union[typing.Union["CfnFunction.S3NotificationFilterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param bucket: ``CfnFunction.S3EventProperty.Bucket``.
            :param events: ``CfnFunction.S3EventProperty.Events``.
            :param filter: ``CfnFunction.S3EventProperty.Filter``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s3_event_property = sam.CfnFunction.S3EventProperty(
                    bucket="bucket",
                    events="events",
                
                    # the properties below are optional
                    filter=sam.CfnFunction.S3NotificationFilterProperty(
                        s3_key=sam.CfnFunction.S3KeyFilterProperty(
                            rules=[sam.CfnFunction.S3KeyFilterRuleProperty(
                                name="name",
                                value="value"
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f152fab2b6a730c21df47b3710b913f9ca0fa433e1075487890918ca9a32a6ff)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "events": events,
            }
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnFunction.S3EventProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def events(
            self,
        ) -> typing.Union[builtins.str, _IResolvable_a771d0ef, typing.List[builtins.str]]:
            '''``CfnFunction.S3EventProperty.Events``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            '''
            result = self._values.get("events")
            assert result is not None, "Required property 'events' is missing"
            return typing.cast(typing.Union[builtins.str, _IResolvable_a771d0ef, typing.List[builtins.str]], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.S3NotificationFilterProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.S3EventProperty.Filter``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.S3NotificationFilterProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3EventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.S3KeyFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class S3KeyFilterProperty:
        def __init__(
            self,
            *,
            rules: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFunction.S3KeyFilterRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param rules: ``CfnFunction.S3KeyFilterProperty.Rules``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s3_key_filter_property = sam.CfnFunction.S3KeyFilterProperty(
                    rules=[sam.CfnFunction.S3KeyFilterRuleProperty(
                        name="name",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__28e114dc8f885e4ab5d9b9cddc2cfc1a732a2171a49e831cb57afc990b05b9fb)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "rules": rules,
            }

        @builtins.property
        def rules(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFunction.S3KeyFilterRuleProperty", _IResolvable_a771d0ef]]]:
            '''``CfnFunction.S3KeyFilterProperty.Rules``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            '''
            result = self._values.get("rules")
            assert result is not None, "Required property 'rules' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFunction.S3KeyFilterRuleProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3KeyFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.S3KeyFilterRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class S3KeyFilterRuleProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''
            :param name: ``CfnFunction.S3KeyFilterRuleProperty.Name``.
            :param value: ``CfnFunction.S3KeyFilterRuleProperty.Value``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s3_key_filter_rule_property = sam.CfnFunction.S3KeyFilterRuleProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5981d9f68fe76f0220b2be9cecfd3031b29e6055b56a0364a7e687399d56ed8d)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnFunction.S3KeyFilterRuleProperty.Name``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnFunction.S3KeyFilterRuleProperty.Value``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3KeyFilterRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: ``CfnFunction.S3LocationProperty.Bucket``.
            :param key: ``CfnFunction.S3LocationProperty.Key``.
            :param version: ``CfnFunction.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s3_location_property = sam.CfnFunction.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                
                    # the properties below are optional
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3045e650e513ab46e5c8cc7b2aa7eaace1c14468e6dda188d6ab7a9daad01cbf)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnFunction.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnFunction.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.S3NotificationFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_key": "s3Key"},
    )
    class S3NotificationFilterProperty:
        def __init__(
            self,
            *,
            s3_key: typing.Union[typing.Union["CfnFunction.S3KeyFilterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param s3_key: ``CfnFunction.S3NotificationFilterProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s3_notification_filter_property = sam.CfnFunction.S3NotificationFilterProperty(
                    s3_key=sam.CfnFunction.S3KeyFilterProperty(
                        rules=[sam.CfnFunction.S3KeyFilterRuleProperty(
                            name="name",
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1087f415a49886c06d99add9e196924788ac0b29dbd089ade319d2ac539e2e35)
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_key": s3_key,
            }

        @builtins.property
        def s3_key(
            self,
        ) -> typing.Union["CfnFunction.S3KeyFilterProperty", _IResolvable_a771d0ef]:
            '''``CfnFunction.S3NotificationFilterProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(typing.Union["CfnFunction.S3KeyFilterProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3NotificationFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.SAMPolicyTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ami_describe_policy": "amiDescribePolicy",
            "aws_secrets_manager_get_secret_value_policy": "awsSecretsManagerGetSecretValuePolicy",
            "cloud_formation_describe_stacks_policy": "cloudFormationDescribeStacksPolicy",
            "cloud_watch_put_metric_policy": "cloudWatchPutMetricPolicy",
            "dynamo_db_crud_policy": "dynamoDbCrudPolicy",
            "dynamo_db_read_policy": "dynamoDbReadPolicy",
            "dynamo_db_stream_read_policy": "dynamoDbStreamReadPolicy",
            "dynamo_db_write_policy": "dynamoDbWritePolicy",
            "ec2_describe_policy": "ec2DescribePolicy",
            "elasticsearch_http_post_policy": "elasticsearchHttpPostPolicy",
            "filter_log_events_policy": "filterLogEventsPolicy",
            "kinesis_crud_policy": "kinesisCrudPolicy",
            "kinesis_stream_read_policy": "kinesisStreamReadPolicy",
            "kms_decrypt_policy": "kmsDecryptPolicy",
            "lambda_invoke_policy": "lambdaInvokePolicy",
            "rekognition_detect_only_policy": "rekognitionDetectOnlyPolicy",
            "rekognition_labels_policy": "rekognitionLabelsPolicy",
            "rekognition_no_data_access_policy": "rekognitionNoDataAccessPolicy",
            "rekognition_read_policy": "rekognitionReadPolicy",
            "rekognition_write_only_access_policy": "rekognitionWriteOnlyAccessPolicy",
            "s3_crud_policy": "s3CrudPolicy",
            "s3_read_policy": "s3ReadPolicy",
            "s3_write_policy": "s3WritePolicy",
            "ses_bulk_templated_crud_policy": "sesBulkTemplatedCrudPolicy",
            "ses_crud_policy": "sesCrudPolicy",
            "ses_email_template_crud_policy": "sesEmailTemplateCrudPolicy",
            "ses_send_bounce_policy": "sesSendBouncePolicy",
            "sns_crud_policy": "snsCrudPolicy",
            "sns_publish_message_policy": "snsPublishMessagePolicy",
            "sqs_poller_policy": "sqsPollerPolicy",
            "sqs_send_message_policy": "sqsSendMessagePolicy",
            "ssm_parameter_read_policy": "ssmParameterReadPolicy",
            "step_functions_execution_policy": "stepFunctionsExecutionPolicy",
            "vpc_access_policy": "vpcAccessPolicy",
        },
    )
    class SAMPolicyTemplateProperty:
        def __init__(
            self,
            *,
            ami_describe_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            aws_secrets_manager_get_secret_value_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.SecretArnSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            cloud_formation_describe_stacks_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            cloud_watch_put_metric_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            dynamo_db_crud_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.TableSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            dynamo_db_read_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.TableSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            dynamo_db_stream_read_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.TableStreamSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            dynamo_db_write_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.TableSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            ec2_describe_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            elasticsearch_http_post_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.DomainSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            filter_log_events_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.LogGroupSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            kinesis_crud_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.StreamSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            kinesis_stream_read_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.StreamSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            kms_decrypt_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.KeySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            lambda_invoke_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.FunctionSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            rekognition_detect_only_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            rekognition_labels_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            rekognition_no_data_access_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.CollectionSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            rekognition_read_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.CollectionSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            rekognition_write_only_access_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.CollectionSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            s3_crud_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.BucketSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            s3_read_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.BucketSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            s3_write_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.BucketSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            ses_bulk_templated_crud_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.IdentitySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            ses_crud_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.IdentitySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            ses_email_template_crud_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            ses_send_bounce_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.IdentitySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sns_crud_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.TopicSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sns_publish_message_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.TopicSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sqs_poller_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.QueueSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sqs_send_message_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.QueueSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            ssm_parameter_read_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.ParameterNameSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            step_functions_execution_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.StateMachineSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            vpc_access_policy: typing.Optional[typing.Union[typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param ami_describe_policy: ``CfnFunction.SAMPolicyTemplateProperty.AMIDescribePolicy``.
            :param aws_secrets_manager_get_secret_value_policy: ``CfnFunction.SAMPolicyTemplateProperty.AWSSecretsManagerGetSecretValuePolicy``.
            :param cloud_formation_describe_stacks_policy: ``CfnFunction.SAMPolicyTemplateProperty.CloudFormationDescribeStacksPolicy``.
            :param cloud_watch_put_metric_policy: ``CfnFunction.SAMPolicyTemplateProperty.CloudWatchPutMetricPolicy``.
            :param dynamo_db_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.DynamoDBCrudPolicy``.
            :param dynamo_db_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.DynamoDBReadPolicy``.
            :param dynamo_db_stream_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.DynamoDBStreamReadPolicy``.
            :param dynamo_db_write_policy: ``CfnFunction.SAMPolicyTemplateProperty.DynamoDBWritePolicy``.
            :param ec2_describe_policy: ``CfnFunction.SAMPolicyTemplateProperty.EC2DescribePolicy``.
            :param elasticsearch_http_post_policy: ``CfnFunction.SAMPolicyTemplateProperty.ElasticsearchHttpPostPolicy``.
            :param filter_log_events_policy: ``CfnFunction.SAMPolicyTemplateProperty.FilterLogEventsPolicy``.
            :param kinesis_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.KinesisCrudPolicy``.
            :param kinesis_stream_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.KinesisStreamReadPolicy``.
            :param kms_decrypt_policy: ``CfnFunction.SAMPolicyTemplateProperty.KMSDecryptPolicy``.
            :param lambda_invoke_policy: ``CfnFunction.SAMPolicyTemplateProperty.LambdaInvokePolicy``.
            :param rekognition_detect_only_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionDetectOnlyPolicy``.
            :param rekognition_labels_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionLabelsPolicy``.
            :param rekognition_no_data_access_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionNoDataAccessPolicy``.
            :param rekognition_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionReadPolicy``.
            :param rekognition_write_only_access_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionWriteOnlyAccessPolicy``.
            :param s3_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.S3CrudPolicy``.
            :param s3_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.S3ReadPolicy``.
            :param s3_write_policy: ``CfnFunction.SAMPolicyTemplateProperty.S3WritePolicy``.
            :param ses_bulk_templated_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESBulkTemplatedCrudPolicy``.
            :param ses_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESCrudPolicy``.
            :param ses_email_template_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESEmailTemplateCrudPolicy``.
            :param ses_send_bounce_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESSendBouncePolicy``.
            :param sns_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SNSCrudPolicy``.
            :param sns_publish_message_policy: ``CfnFunction.SAMPolicyTemplateProperty.SNSPublishMessagePolicy``.
            :param sqs_poller_policy: ``CfnFunction.SAMPolicyTemplateProperty.SQSPollerPolicy``.
            :param sqs_send_message_policy: ``CfnFunction.SAMPolicyTemplateProperty.SQSSendMessagePolicy``.
            :param ssm_parameter_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.SSMParameterReadPolicy``.
            :param step_functions_execution_policy: ``CfnFunction.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.
            :param vpc_access_policy: ``CfnFunction.SAMPolicyTemplateProperty.VPCAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s_aMPolicy_template_property = sam.CfnFunction.SAMPolicyTemplateProperty(
                    ami_describe_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    aws_secrets_manager_get_secret_value_policy=sam.CfnFunction.SecretArnSAMPTProperty(
                        secret_arn="secretArn"
                    ),
                    cloud_formation_describe_stacks_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    cloud_watch_put_metric_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    dynamo_db_crud_policy=sam.CfnFunction.TableSAMPTProperty(
                        table_name="tableName"
                    ),
                    dynamo_db_read_policy=sam.CfnFunction.TableSAMPTProperty(
                        table_name="tableName"
                    ),
                    dynamo_db_stream_read_policy=sam.CfnFunction.TableStreamSAMPTProperty(
                        stream_name="streamName",
                        table_name="tableName"
                    ),
                    dynamo_db_write_policy=sam.CfnFunction.TableSAMPTProperty(
                        table_name="tableName"
                    ),
                    ec2_describe_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    elasticsearch_http_post_policy=sam.CfnFunction.DomainSAMPTProperty(
                        domain_name="domainName"
                    ),
                    filter_log_events_policy=sam.CfnFunction.LogGroupSAMPTProperty(
                        log_group_name="logGroupName"
                    ),
                    kinesis_crud_policy=sam.CfnFunction.StreamSAMPTProperty(
                        stream_name="streamName"
                    ),
                    kinesis_stream_read_policy=sam.CfnFunction.StreamSAMPTProperty(
                        stream_name="streamName"
                    ),
                    kms_decrypt_policy=sam.CfnFunction.KeySAMPTProperty(
                        key_id="keyId"
                    ),
                    lambda_invoke_policy=sam.CfnFunction.FunctionSAMPTProperty(
                        function_name="functionName"
                    ),
                    rekognition_detect_only_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    rekognition_labels_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    rekognition_no_data_access_policy=sam.CfnFunction.CollectionSAMPTProperty(
                        collection_id="collectionId"
                    ),
                    rekognition_read_policy=sam.CfnFunction.CollectionSAMPTProperty(
                        collection_id="collectionId"
                    ),
                    rekognition_write_only_access_policy=sam.CfnFunction.CollectionSAMPTProperty(
                        collection_id="collectionId"
                    ),
                    s3_crud_policy=sam.CfnFunction.BucketSAMPTProperty(
                        bucket_name="bucketName"
                    ),
                    s3_read_policy=sam.CfnFunction.BucketSAMPTProperty(
                        bucket_name="bucketName"
                    ),
                    s3_write_policy=sam.CfnFunction.BucketSAMPTProperty(
                        bucket_name="bucketName"
                    ),
                    ses_bulk_templated_crud_policy=sam.CfnFunction.IdentitySAMPTProperty(
                        identity_name="identityName"
                    ),
                    ses_crud_policy=sam.CfnFunction.IdentitySAMPTProperty(
                        identity_name="identityName"
                    ),
                    ses_email_template_crud_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    ses_send_bounce_policy=sam.CfnFunction.IdentitySAMPTProperty(
                        identity_name="identityName"
                    ),
                    sns_crud_policy=sam.CfnFunction.TopicSAMPTProperty(
                        topic_name="topicName"
                    ),
                    sns_publish_message_policy=sam.CfnFunction.TopicSAMPTProperty(
                        topic_name="topicName"
                    ),
                    sqs_poller_policy=sam.CfnFunction.QueueSAMPTProperty(
                        queue_name="queueName"
                    ),
                    sqs_send_message_policy=sam.CfnFunction.QueueSAMPTProperty(
                        queue_name="queueName"
                    ),
                    ssm_parameter_read_policy=sam.CfnFunction.ParameterNameSAMPTProperty(
                        parameter_name="parameterName"
                    ),
                    step_functions_execution_policy=sam.CfnFunction.StateMachineSAMPTProperty(
                        state_machine_name="stateMachineName"
                    ),
                    vpc_access_policy=sam.CfnFunction.EmptySAMPTProperty()
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f818379b2f41b3e45a592087f1d682e06e83c6c10d2ca331a0a7209e534c729)
                check_type(argname="argument ami_describe_policy", value=ami_describe_policy, expected_type=type_hints["ami_describe_policy"])
                check_type(argname="argument aws_secrets_manager_get_secret_value_policy", value=aws_secrets_manager_get_secret_value_policy, expected_type=type_hints["aws_secrets_manager_get_secret_value_policy"])
                check_type(argname="argument cloud_formation_describe_stacks_policy", value=cloud_formation_describe_stacks_policy, expected_type=type_hints["cloud_formation_describe_stacks_policy"])
                check_type(argname="argument cloud_watch_put_metric_policy", value=cloud_watch_put_metric_policy, expected_type=type_hints["cloud_watch_put_metric_policy"])
                check_type(argname="argument dynamo_db_crud_policy", value=dynamo_db_crud_policy, expected_type=type_hints["dynamo_db_crud_policy"])
                check_type(argname="argument dynamo_db_read_policy", value=dynamo_db_read_policy, expected_type=type_hints["dynamo_db_read_policy"])
                check_type(argname="argument dynamo_db_stream_read_policy", value=dynamo_db_stream_read_policy, expected_type=type_hints["dynamo_db_stream_read_policy"])
                check_type(argname="argument dynamo_db_write_policy", value=dynamo_db_write_policy, expected_type=type_hints["dynamo_db_write_policy"])
                check_type(argname="argument ec2_describe_policy", value=ec2_describe_policy, expected_type=type_hints["ec2_describe_policy"])
                check_type(argname="argument elasticsearch_http_post_policy", value=elasticsearch_http_post_policy, expected_type=type_hints["elasticsearch_http_post_policy"])
                check_type(argname="argument filter_log_events_policy", value=filter_log_events_policy, expected_type=type_hints["filter_log_events_policy"])
                check_type(argname="argument kinesis_crud_policy", value=kinesis_crud_policy, expected_type=type_hints["kinesis_crud_policy"])
                check_type(argname="argument kinesis_stream_read_policy", value=kinesis_stream_read_policy, expected_type=type_hints["kinesis_stream_read_policy"])
                check_type(argname="argument kms_decrypt_policy", value=kms_decrypt_policy, expected_type=type_hints["kms_decrypt_policy"])
                check_type(argname="argument lambda_invoke_policy", value=lambda_invoke_policy, expected_type=type_hints["lambda_invoke_policy"])
                check_type(argname="argument rekognition_detect_only_policy", value=rekognition_detect_only_policy, expected_type=type_hints["rekognition_detect_only_policy"])
                check_type(argname="argument rekognition_labels_policy", value=rekognition_labels_policy, expected_type=type_hints["rekognition_labels_policy"])
                check_type(argname="argument rekognition_no_data_access_policy", value=rekognition_no_data_access_policy, expected_type=type_hints["rekognition_no_data_access_policy"])
                check_type(argname="argument rekognition_read_policy", value=rekognition_read_policy, expected_type=type_hints["rekognition_read_policy"])
                check_type(argname="argument rekognition_write_only_access_policy", value=rekognition_write_only_access_policy, expected_type=type_hints["rekognition_write_only_access_policy"])
                check_type(argname="argument s3_crud_policy", value=s3_crud_policy, expected_type=type_hints["s3_crud_policy"])
                check_type(argname="argument s3_read_policy", value=s3_read_policy, expected_type=type_hints["s3_read_policy"])
                check_type(argname="argument s3_write_policy", value=s3_write_policy, expected_type=type_hints["s3_write_policy"])
                check_type(argname="argument ses_bulk_templated_crud_policy", value=ses_bulk_templated_crud_policy, expected_type=type_hints["ses_bulk_templated_crud_policy"])
                check_type(argname="argument ses_crud_policy", value=ses_crud_policy, expected_type=type_hints["ses_crud_policy"])
                check_type(argname="argument ses_email_template_crud_policy", value=ses_email_template_crud_policy, expected_type=type_hints["ses_email_template_crud_policy"])
                check_type(argname="argument ses_send_bounce_policy", value=ses_send_bounce_policy, expected_type=type_hints["ses_send_bounce_policy"])
                check_type(argname="argument sns_crud_policy", value=sns_crud_policy, expected_type=type_hints["sns_crud_policy"])
                check_type(argname="argument sns_publish_message_policy", value=sns_publish_message_policy, expected_type=type_hints["sns_publish_message_policy"])
                check_type(argname="argument sqs_poller_policy", value=sqs_poller_policy, expected_type=type_hints["sqs_poller_policy"])
                check_type(argname="argument sqs_send_message_policy", value=sqs_send_message_policy, expected_type=type_hints["sqs_send_message_policy"])
                check_type(argname="argument ssm_parameter_read_policy", value=ssm_parameter_read_policy, expected_type=type_hints["ssm_parameter_read_policy"])
                check_type(argname="argument step_functions_execution_policy", value=step_functions_execution_policy, expected_type=type_hints["step_functions_execution_policy"])
                check_type(argname="argument vpc_access_policy", value=vpc_access_policy, expected_type=type_hints["vpc_access_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ami_describe_policy is not None:
                self._values["ami_describe_policy"] = ami_describe_policy
            if aws_secrets_manager_get_secret_value_policy is not None:
                self._values["aws_secrets_manager_get_secret_value_policy"] = aws_secrets_manager_get_secret_value_policy
            if cloud_formation_describe_stacks_policy is not None:
                self._values["cloud_formation_describe_stacks_policy"] = cloud_formation_describe_stacks_policy
            if cloud_watch_put_metric_policy is not None:
                self._values["cloud_watch_put_metric_policy"] = cloud_watch_put_metric_policy
            if dynamo_db_crud_policy is not None:
                self._values["dynamo_db_crud_policy"] = dynamo_db_crud_policy
            if dynamo_db_read_policy is not None:
                self._values["dynamo_db_read_policy"] = dynamo_db_read_policy
            if dynamo_db_stream_read_policy is not None:
                self._values["dynamo_db_stream_read_policy"] = dynamo_db_stream_read_policy
            if dynamo_db_write_policy is not None:
                self._values["dynamo_db_write_policy"] = dynamo_db_write_policy
            if ec2_describe_policy is not None:
                self._values["ec2_describe_policy"] = ec2_describe_policy
            if elasticsearch_http_post_policy is not None:
                self._values["elasticsearch_http_post_policy"] = elasticsearch_http_post_policy
            if filter_log_events_policy is not None:
                self._values["filter_log_events_policy"] = filter_log_events_policy
            if kinesis_crud_policy is not None:
                self._values["kinesis_crud_policy"] = kinesis_crud_policy
            if kinesis_stream_read_policy is not None:
                self._values["kinesis_stream_read_policy"] = kinesis_stream_read_policy
            if kms_decrypt_policy is not None:
                self._values["kms_decrypt_policy"] = kms_decrypt_policy
            if lambda_invoke_policy is not None:
                self._values["lambda_invoke_policy"] = lambda_invoke_policy
            if rekognition_detect_only_policy is not None:
                self._values["rekognition_detect_only_policy"] = rekognition_detect_only_policy
            if rekognition_labels_policy is not None:
                self._values["rekognition_labels_policy"] = rekognition_labels_policy
            if rekognition_no_data_access_policy is not None:
                self._values["rekognition_no_data_access_policy"] = rekognition_no_data_access_policy
            if rekognition_read_policy is not None:
                self._values["rekognition_read_policy"] = rekognition_read_policy
            if rekognition_write_only_access_policy is not None:
                self._values["rekognition_write_only_access_policy"] = rekognition_write_only_access_policy
            if s3_crud_policy is not None:
                self._values["s3_crud_policy"] = s3_crud_policy
            if s3_read_policy is not None:
                self._values["s3_read_policy"] = s3_read_policy
            if s3_write_policy is not None:
                self._values["s3_write_policy"] = s3_write_policy
            if ses_bulk_templated_crud_policy is not None:
                self._values["ses_bulk_templated_crud_policy"] = ses_bulk_templated_crud_policy
            if ses_crud_policy is not None:
                self._values["ses_crud_policy"] = ses_crud_policy
            if ses_email_template_crud_policy is not None:
                self._values["ses_email_template_crud_policy"] = ses_email_template_crud_policy
            if ses_send_bounce_policy is not None:
                self._values["ses_send_bounce_policy"] = ses_send_bounce_policy
            if sns_crud_policy is not None:
                self._values["sns_crud_policy"] = sns_crud_policy
            if sns_publish_message_policy is not None:
                self._values["sns_publish_message_policy"] = sns_publish_message_policy
            if sqs_poller_policy is not None:
                self._values["sqs_poller_policy"] = sqs_poller_policy
            if sqs_send_message_policy is not None:
                self._values["sqs_send_message_policy"] = sqs_send_message_policy
            if ssm_parameter_read_policy is not None:
                self._values["ssm_parameter_read_policy"] = ssm_parameter_read_policy
            if step_functions_execution_policy is not None:
                self._values["step_functions_execution_policy"] = step_functions_execution_policy
            if vpc_access_policy is not None:
                self._values["vpc_access_policy"] = vpc_access_policy

        @builtins.property
        def ami_describe_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.AMIDescribePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ami_describe_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def aws_secrets_manager_get_secret_value_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.SecretArnSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.AWSSecretsManagerGetSecretValuePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("aws_secrets_manager_get_secret_value_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.SecretArnSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def cloud_formation_describe_stacks_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.CloudFormationDescribeStacksPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("cloud_formation_describe_stacks_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def cloud_watch_put_metric_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.CloudWatchPutMetricPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("cloud_watch_put_metric_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynamo_db_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.DynamoDBCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("dynamo_db_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynamo_db_read_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.DynamoDBReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("dynamo_db_read_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynamo_db_stream_read_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.TableStreamSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.DynamoDBStreamReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("dynamo_db_stream_read_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.TableStreamSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynamo_db_write_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.DynamoDBWritePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("dynamo_db_write_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ec2_describe_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.EC2DescribePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ec2_describe_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def elasticsearch_http_post_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.DomainSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.ElasticsearchHttpPostPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("elasticsearch_http_post_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.DomainSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def filter_log_events_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.LogGroupSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.FilterLogEventsPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("filter_log_events_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.LogGroupSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kinesis_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.StreamSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.KinesisCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("kinesis_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.StreamSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kinesis_stream_read_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.StreamSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.KinesisStreamReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("kinesis_stream_read_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.StreamSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kms_decrypt_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.KeySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.KMSDecryptPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("kms_decrypt_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.KeySAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def lambda_invoke_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.FunctionSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.LambdaInvokePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("lambda_invoke_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.FunctionSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rekognition_detect_only_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionDetectOnlyPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_detect_only_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rekognition_labels_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionLabelsPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_labels_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rekognition_no_data_access_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionNoDataAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_no_data_access_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rekognition_read_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_read_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rekognition_write_only_access_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionWriteOnlyAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_write_only_access_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def s3_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.S3CrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("s3_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def s3_read_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.S3ReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("s3_read_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def s3_write_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.S3WritePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("s3_write_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ses_bulk_templated_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESBulkTemplatedCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_bulk_templated_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ses_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ses_email_template_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESEmailTemplateCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_email_template_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ses_send_bounce_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESSendBouncePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_send_bounce_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sns_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.TopicSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SNSCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sns_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.TopicSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sns_publish_message_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.TopicSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SNSPublishMessagePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sns_publish_message_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.TopicSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqs_poller_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.QueueSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SQSPollerPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sqs_poller_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.QueueSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqs_send_message_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.QueueSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SQSSendMessagePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sqs_send_message_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.QueueSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ssm_parameter_read_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.ParameterNameSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SSMParameterReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ssm_parameter_read_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.ParameterNameSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def step_functions_execution_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.StateMachineSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("step_functions_execution_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.StateMachineSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def vpc_access_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.VPCAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("vpc_access_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAMPolicyTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.SNSEventProperty",
        jsii_struct_bases=[],
        name_mapping={"topic": "topic"},
    )
    class SNSEventProperty:
        def __init__(self, *, topic: builtins.str) -> None:
            '''
            :param topic: ``CfnFunction.SNSEventProperty.Topic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sns
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s_nSEvent_property = sam.CfnFunction.SNSEventProperty(
                    topic="topic"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e105fcb25392badbc729d3a8382809a14713d54d9fd75f4b75716b7e804f1b19)
                check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "topic": topic,
            }

        @builtins.property
        def topic(self) -> builtins.str:
            '''``CfnFunction.SNSEventProperty.Topic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sns
            '''
            result = self._values.get("topic")
            assert result is not None, "Required property 'topic' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SNSEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.SQSEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "queue": "queue",
            "batch_size": "batchSize",
            "enabled": "enabled",
        },
    )
    class SQSEventProperty:
        def __init__(
            self,
            *,
            queue: builtins.str,
            batch_size: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param queue: ``CfnFunction.SQSEventProperty.Queue``.
            :param batch_size: ``CfnFunction.SQSEventProperty.BatchSize``.
            :param enabled: ``CfnFunction.SQSEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s_qSEvent_property = sam.CfnFunction.SQSEventProperty(
                    queue="queue",
                
                    # the properties below are optional
                    batch_size=123,
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__596cf9e3422e5ea0dd247e44e4068e9f0fc2925fc7e5f35683c9215878343004)
                check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "queue": queue,
            }
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def queue(self) -> builtins.str:
            '''``CfnFunction.SQSEventProperty.Queue``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            '''
            result = self._values.get("queue")
            assert result is not None, "Required property 'queue' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.SQSEventProperty.BatchSize``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFunction.SQSEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SQSEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.ScheduleEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "schedule": "schedule",
            "description": "description",
            "enabled": "enabled",
            "input": "input",
            "name": "name",
        },
    )
    class ScheduleEventProperty:
        def __init__(
            self,
            *,
            schedule: builtins.str,
            description: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            input: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param schedule: ``CfnFunction.ScheduleEventProperty.Schedule``.
            :param description: ``CfnFunction.ScheduleEventProperty.Description``.
            :param enabled: ``CfnFunction.ScheduleEventProperty.Enabled``.
            :param input: ``CfnFunction.ScheduleEventProperty.Input``.
            :param name: ``CfnFunction.ScheduleEventProperty.Name``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                schedule_event_property = sam.CfnFunction.ScheduleEventProperty(
                    schedule="schedule",
                
                    # the properties below are optional
                    description="description",
                    enabled=False,
                    input="input",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0120579ea2c654e37a7bb81cb13416de265beb4c07976cff5edae031ee76e994)
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "schedule": schedule,
            }
            if description is not None:
                self._values["description"] = description
            if enabled is not None:
                self._values["enabled"] = enabled
            if input is not None:
                self._values["input"] = input
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def schedule(self) -> builtins.str:
            '''``CfnFunction.ScheduleEventProperty.Schedule``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("schedule")
            assert result is not None, "Required property 'schedule' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ScheduleEventProperty.Description``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFunction.ScheduleEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ScheduleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ScheduleEventProperty.Name``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.SecretArnSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_arn": "secretArn"},
    )
    class SecretArnSAMPTProperty:
        def __init__(self, *, secret_arn: builtins.str) -> None:
            '''
            :param secret_arn: ``CfnFunction.SecretArnSAMPTProperty.SecretArn``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                secret_arn_sAMPTProperty = sam.CfnFunction.SecretArnSAMPTProperty(
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ff72985ffaf6a1cf38ac2cef403c54fefd6c7d084ae3f5f2c890b709e749589)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "secret_arn": secret_arn,
            }

        @builtins.property
        def secret_arn(self) -> builtins.str:
            '''``CfnFunction.SecretArnSAMPTProperty.SecretArn``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("secret_arn")
            assert result is not None, "Required property 'secret_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretArnSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.StateMachineSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"state_machine_name": "stateMachineName"},
    )
    class StateMachineSAMPTProperty:
        def __init__(self, *, state_machine_name: builtins.str) -> None:
            '''
            :param state_machine_name: ``CfnFunction.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                state_machine_sAMPTProperty = sam.CfnFunction.StateMachineSAMPTProperty(
                    state_machine_name="stateMachineName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2b5e5c2c25ff1b829ff00639fa4ca49a5a7f9892d0cab9380abdc66796a2601)
                check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "state_machine_name": state_machine_name,
            }

        @builtins.property
        def state_machine_name(self) -> builtins.str:
            '''``CfnFunction.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("state_machine_name")
            assert result is not None, "Required property 'state_machine_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateMachineSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.StreamSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_name": "streamName"},
    )
    class StreamSAMPTProperty:
        def __init__(self, *, stream_name: builtins.str) -> None:
            '''
            :param stream_name: ``CfnFunction.StreamSAMPTProperty.StreamName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                stream_sAMPTProperty = sam.CfnFunction.StreamSAMPTProperty(
                    stream_name="streamName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__500797e41a4ad71c1d4c15d245e70caddf9578565e3078ba2629ef04bb6a0e51)
                check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stream_name": stream_name,
            }

        @builtins.property
        def stream_name(self) -> builtins.str:
            '''``CfnFunction.StreamSAMPTProperty.StreamName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("stream_name")
            assert result is not None, "Required property 'stream_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.TableSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"table_name": "tableName"},
    )
    class TableSAMPTProperty:
        def __init__(self, *, table_name: builtins.str) -> None:
            '''
            :param table_name: ``CfnFunction.TableSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                table_sAMPTProperty = sam.CfnFunction.TableSAMPTProperty(
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4dde8a927b347c63b74b3d2be8c98295198e1f321cd62fcf1df4cbbe730849d1)
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "table_name": table_name,
            }

        @builtins.property
        def table_name(self) -> builtins.str:
            '''``CfnFunction.TableSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.TableStreamSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_name": "streamName", "table_name": "tableName"},
    )
    class TableStreamSAMPTProperty:
        def __init__(
            self,
            *,
            stream_name: builtins.str,
            table_name: builtins.str,
        ) -> None:
            '''
            :param stream_name: ``CfnFunction.TableStreamSAMPTProperty.StreamName``.
            :param table_name: ``CfnFunction.TableStreamSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                table_stream_sAMPTProperty = sam.CfnFunction.TableStreamSAMPTProperty(
                    stream_name="streamName",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a16f56f3ae85cc6db5aca5a8978363a8f92dcf1dd950a159e5cec6b3897bc0a)
                check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stream_name": stream_name,
                "table_name": table_name,
            }

        @builtins.property
        def stream_name(self) -> builtins.str:
            '''``CfnFunction.TableStreamSAMPTProperty.StreamName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("stream_name")
            assert result is not None, "Required property 'stream_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def table_name(self) -> builtins.str:
            '''``CfnFunction.TableStreamSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableStreamSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.TopicSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_name": "topicName"},
    )
    class TopicSAMPTProperty:
        def __init__(self, *, topic_name: builtins.str) -> None:
            '''
            :param topic_name: ``CfnFunction.TopicSAMPTProperty.TopicName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                topic_sAMPTProperty = sam.CfnFunction.TopicSAMPTProperty(
                    topic_name="topicName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1977a80f2c3a568e7fddc8854834b5f4d012f0060364531a1df65cfc67e37b1b)
                check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "topic_name": topic_name,
            }

        @builtins.property
        def topic_name(self) -> builtins.str:
            '''``CfnFunction.TopicSAMPTProperty.TopicName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("topic_name")
            assert result is not None, "Required property 'topic_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TopicSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnFunction.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Sequence[builtins.str],
            subnet_ids: typing.Sequence[builtins.str],
        ) -> None:
            '''
            :param security_group_ids: ``CfnFunction.VpcConfigProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnFunction.VpcConfigProperty.SubnetIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                vpc_config_property = sam.CfnFunction.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__043a5c7053a5d62211a19843451af327cf2033b2fdb160b805adb5ed3a1b726f)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "security_group_ids": security_group_ids,
                "subnet_ids": subnet_ids,
            }

        @builtins.property
        def security_group_ids(self) -> typing.List[builtins.str]:
            '''``CfnFunction.VpcConfigProperty.SecurityGroupIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html
            '''
            result = self._values.get("security_group_ids")
            assert result is not None, "Required property 'security_group_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def subnet_ids(self) -> typing.List[builtins.str]:
            '''``CfnFunction.VpcConfigProperty.SubnetIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html
            '''
            result = self._values.get("subnet_ids")
            assert result is not None, "Required property 'subnet_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_sam.CfnFunctionProps",
    jsii_struct_bases=[],
    name_mapping={
        "architectures": "architectures",
        "assume_role_policy_document": "assumeRolePolicyDocument",
        "auto_publish_alias": "autoPublishAlias",
        "auto_publish_code_sha256": "autoPublishCodeSha256",
        "code_signing_config_arn": "codeSigningConfigArn",
        "code_uri": "codeUri",
        "dead_letter_queue": "deadLetterQueue",
        "deployment_preference": "deploymentPreference",
        "description": "description",
        "environment": "environment",
        "event_invoke_config": "eventInvokeConfig",
        "events": "events",
        "file_system_configs": "fileSystemConfigs",
        "function_name": "functionName",
        "handler": "handler",
        "image_config": "imageConfig",
        "image_uri": "imageUri",
        "inline_code": "inlineCode",
        "kms_key_arn": "kmsKeyArn",
        "layers": "layers",
        "memory_size": "memorySize",
        "package_type": "packageType",
        "permissions_boundary": "permissionsBoundary",
        "policies": "policies",
        "provisioned_concurrency_config": "provisionedConcurrencyConfig",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "runtime": "runtime",
        "tags": "tags",
        "timeout": "timeout",
        "tracing": "tracing",
        "version_description": "versionDescription",
        "vpc_config": "vpcConfig",
    },
)
class CfnFunctionProps:
    def __init__(
        self,
        *,
        architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role_policy_document: typing.Any = None,
        auto_publish_alias: typing.Optional[builtins.str] = None,
        auto_publish_code_sha256: typing.Optional[builtins.str] = None,
        code_signing_config_arn: typing.Optional[builtins.str] = None,
        code_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnFunction.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        dead_letter_queue: typing.Optional[typing.Union[typing.Union[CfnFunction.DeadLetterQueueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        deployment_preference: typing.Optional[typing.Union[typing.Union[CfnFunction.DeploymentPreferenceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union[typing.Union[CfnFunction.FunctionEnvironmentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        event_invoke_config: typing.Optional[typing.Union[typing.Union[CfnFunction.EventInvokeConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnFunction.EventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        file_system_configs: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFunction.FileSystemConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        function_name: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        image_config: typing.Optional[typing.Union[typing.Union[CfnFunction.ImageConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        inline_code: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        layers: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        package_type: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef, typing.Sequence[typing.Union[builtins.str, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        provisioned_concurrency_config: typing.Optional[typing.Union[typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        tracing: typing.Optional[builtins.str] = None,
        version_description: typing.Optional[builtins.str] = None,
        vpc_config: typing.Optional[typing.Union[typing.Union[CfnFunction.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFunction``.

        :param architectures: ``AWS::Serverless::Function.Architectures``.
        :param assume_role_policy_document: ``AWS::Serverless::Function.AssumeRolePolicyDocument``.
        :param auto_publish_alias: ``AWS::Serverless::Function.AutoPublishAlias``.
        :param auto_publish_code_sha256: ``AWS::Serverless::Function.AutoPublishCodeSha256``.
        :param code_signing_config_arn: ``AWS::Serverless::Function.CodeSigningConfigArn``.
        :param code_uri: ``AWS::Serverless::Function.CodeUri``.
        :param dead_letter_queue: ``AWS::Serverless::Function.DeadLetterQueue``.
        :param deployment_preference: ``AWS::Serverless::Function.DeploymentPreference``.
        :param description: ``AWS::Serverless::Function.Description``.
        :param environment: ``AWS::Serverless::Function.Environment``.
        :param event_invoke_config: ``AWS::Serverless::Function.EventInvokeConfig``.
        :param events: ``AWS::Serverless::Function.Events``.
        :param file_system_configs: ``AWS::Serverless::Function.FileSystemConfigs``.
        :param function_name: ``AWS::Serverless::Function.FunctionName``.
        :param handler: ``AWS::Serverless::Function.Handler``.
        :param image_config: ``AWS::Serverless::Function.ImageConfig``.
        :param image_uri: ``AWS::Serverless::Function.ImageUri``.
        :param inline_code: ``AWS::Serverless::Function.InlineCode``.
        :param kms_key_arn: ``AWS::Serverless::Function.KmsKeyArn``.
        :param layers: ``AWS::Serverless::Function.Layers``.
        :param memory_size: ``AWS::Serverless::Function.MemorySize``.
        :param package_type: ``AWS::Serverless::Function.PackageType``.
        :param permissions_boundary: ``AWS::Serverless::Function.PermissionsBoundary``.
        :param policies: ``AWS::Serverless::Function.Policies``.
        :param provisioned_concurrency_config: ``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.
        :param reserved_concurrent_executions: ``AWS::Serverless::Function.ReservedConcurrentExecutions``.
        :param role: ``AWS::Serverless::Function.Role``.
        :param runtime: ``AWS::Serverless::Function.Runtime``.
        :param tags: ``AWS::Serverless::Function.Tags``.
        :param timeout: ``AWS::Serverless::Function.Timeout``.
        :param tracing: ``AWS::Serverless::Function.Tracing``.
        :param version_description: ``AWS::Serverless::Function.VersionDescription``.
        :param vpc_config: ``AWS::Serverless::Function.VpcConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sam as sam
            
            # assume_role_policy_document: Any
            
            cfn_function_props = sam.CfnFunctionProps(
                architectures=["architectures"],
                assume_role_policy_document=assume_role_policy_document,
                auto_publish_alias="autoPublishAlias",
                auto_publish_code_sha256="autoPublishCodeSha256",
                code_signing_config_arn="codeSigningConfigArn",
                code_uri="codeUri",
                dead_letter_queue=sam.CfnFunction.DeadLetterQueueProperty(
                    target_arn="targetArn",
                    type="type"
                ),
                deployment_preference=sam.CfnFunction.DeploymentPreferenceProperty(
                    enabled=False,
                    type="type",
            
                    # the properties below are optional
                    alarms=["alarms"],
                    hooks=sam.CfnFunction.HooksProperty(
                        post_traffic="postTraffic",
                        pre_traffic="preTraffic"
                    )
                ),
                description="description",
                environment=sam.CfnFunction.FunctionEnvironmentProperty(
                    variables={
                        "variables_key": "variables"
                    }
                ),
                event_invoke_config=sam.CfnFunction.EventInvokeConfigProperty(
                    destination_config=sam.CfnFunction.EventInvokeDestinationConfigProperty(
                        on_failure=sam.CfnFunction.DestinationProperty(
                            destination="destination",
            
                            # the properties below are optional
                            type="type"
                        ),
                        on_success=sam.CfnFunction.DestinationProperty(
                            destination="destination",
            
                            # the properties below are optional
                            type="type"
                        )
                    ),
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                ),
                events={
                    "events_key": sam.CfnFunction.EventSourceProperty(
                        properties=sam.CfnFunction.S3EventProperty(
                            variables={
                                "variables_key": "variables"
                            }
                        ),
                        type="type"
                    )
                },
                file_system_configs=[sam.CfnFunction.FileSystemConfigProperty(
                    arn="arn",
                    local_mount_path="localMountPath"
                )],
                function_name="functionName",
                handler="handler",
                image_config=sam.CfnFunction.ImageConfigProperty(
                    command=["command"],
                    entry_point=["entryPoint"],
                    working_directory="workingDirectory"
                ),
                image_uri="imageUri",
                inline_code="inlineCode",
                kms_key_arn="kmsKeyArn",
                layers=["layers"],
                memory_size=123,
                package_type="packageType",
                permissions_boundary="permissionsBoundary",
                policies="policies",
                provisioned_concurrency_config=sam.CfnFunction.ProvisionedConcurrencyConfigProperty(
                    provisioned_concurrent_executions="provisionedConcurrentExecutions"
                ),
                reserved_concurrent_executions=123,
                role="role",
                runtime="runtime",
                tags={
                    "tags_key": "tags"
                },
                timeout=123,
                tracing="tracing",
                version_description="versionDescription",
                vpc_config=sam.CfnFunction.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b941aecdc76dca88e7aa52761ece48d840c2b00504960660dfc97c3340c3fdec)
            check_type(argname="argument architectures", value=architectures, expected_type=type_hints["architectures"])
            check_type(argname="argument assume_role_policy_document", value=assume_role_policy_document, expected_type=type_hints["assume_role_policy_document"])
            check_type(argname="argument auto_publish_alias", value=auto_publish_alias, expected_type=type_hints["auto_publish_alias"])
            check_type(argname="argument auto_publish_code_sha256", value=auto_publish_code_sha256, expected_type=type_hints["auto_publish_code_sha256"])
            check_type(argname="argument code_signing_config_arn", value=code_signing_config_arn, expected_type=type_hints["code_signing_config_arn"])
            check_type(argname="argument code_uri", value=code_uri, expected_type=type_hints["code_uri"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument deployment_preference", value=deployment_preference, expected_type=type_hints["deployment_preference"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument event_invoke_config", value=event_invoke_config, expected_type=type_hints["event_invoke_config"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument file_system_configs", value=file_system_configs, expected_type=type_hints["file_system_configs"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument image_config", value=image_config, expected_type=type_hints["image_config"])
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument inline_code", value=inline_code, expected_type=type_hints["inline_code"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument layers", value=layers, expected_type=type_hints["layers"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument package_type", value=package_type, expected_type=type_hints["package_type"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument provisioned_concurrency_config", value=provisioned_concurrency_config, expected_type=type_hints["provisioned_concurrency_config"])
            check_type(argname="argument reserved_concurrent_executions", value=reserved_concurrent_executions, expected_type=type_hints["reserved_concurrent_executions"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
            check_type(argname="argument version_description", value=version_description, expected_type=type_hints["version_description"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architectures is not None:
            self._values["architectures"] = architectures
        if assume_role_policy_document is not None:
            self._values["assume_role_policy_document"] = assume_role_policy_document
        if auto_publish_alias is not None:
            self._values["auto_publish_alias"] = auto_publish_alias
        if auto_publish_code_sha256 is not None:
            self._values["auto_publish_code_sha256"] = auto_publish_code_sha256
        if code_signing_config_arn is not None:
            self._values["code_signing_config_arn"] = code_signing_config_arn
        if code_uri is not None:
            self._values["code_uri"] = code_uri
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if deployment_preference is not None:
            self._values["deployment_preference"] = deployment_preference
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if event_invoke_config is not None:
            self._values["event_invoke_config"] = event_invoke_config
        if events is not None:
            self._values["events"] = events
        if file_system_configs is not None:
            self._values["file_system_configs"] = file_system_configs
        if function_name is not None:
            self._values["function_name"] = function_name
        if handler is not None:
            self._values["handler"] = handler
        if image_config is not None:
            self._values["image_config"] = image_config
        if image_uri is not None:
            self._values["image_uri"] = image_uri
        if inline_code is not None:
            self._values["inline_code"] = inline_code
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if layers is not None:
            self._values["layers"] = layers
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if package_type is not None:
            self._values["package_type"] = package_type
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policies is not None:
            self._values["policies"] = policies
        if provisioned_concurrency_config is not None:
            self._values["provisioned_concurrency_config"] = provisioned_concurrency_config
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if runtime is not None:
            self._values["runtime"] = runtime
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if version_description is not None:
            self._values["version_description"] = version_description
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def architectures(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Function.Architectures``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-architectures
        '''
        result = self._values.get("architectures")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assume_role_policy_document(self) -> typing.Any:
        '''``AWS::Serverless::Function.AssumeRolePolicyDocument``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-assumerolepolicydocument
        '''
        result = self._values.get("assume_role_policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def auto_publish_alias(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.AutoPublishAlias``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("auto_publish_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_publish_code_sha256(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.AutoPublishCodeSha256``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-autopublishcodesha256
        '''
        result = self._values.get("auto_publish_code_sha256")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_signing_config_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.CodeSigningConfigArn``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-codesigningconfigarn
        '''
        result = self._values.get("code_signing_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnFunction.S3LocationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.CodeUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("code_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnFunction.S3LocationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def dead_letter_queue(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.DeadLetterQueueProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.DeadLetterQueue``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.DeadLetterQueueProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def deployment_preference(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.DeploymentPreferenceProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.DeploymentPreference``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
        '''
        result = self._values.get("deployment_preference")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.DeploymentPreferenceProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.FunctionEnvironmentProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.Environment``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.FunctionEnvironmentProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def event_invoke_config(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.EventInvokeConfigProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.EventInvokeConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("event_invoke_config")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.EventInvokeConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnFunction.EventSourceProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Serverless::Function.Events``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnFunction.EventSourceProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def file_system_configs(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFunction.FileSystemConfigProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Serverless::Function.FileSystemConfigs``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html
        '''
        result = self._values.get("file_system_configs")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFunction.FileSystemConfigProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.FunctionName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Handler``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_config(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.ImageConfigProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.ImageConfig``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-imageconfig
        '''
        result = self._values.get("image_config")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.ImageConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.ImageUri``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-imageuri
        '''
        result = self._values.get("image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_code(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.InlineCode``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("inline_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.KmsKeyArn``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Function.Layers``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.MemorySize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def package_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.PackageType``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-packagetype
        '''
        result = self._values.get("package_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.PermissionsBoundary``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, CfnFunction.SAMPolicyTemplateProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Serverless::Function.Policies``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, CfnFunction.SAMPolicyTemplateProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def provisioned_concurrency_config(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("provisioned_concurrency_config")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.ReservedConcurrentExecutions``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Role``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Runtime``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::Function.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.Timeout``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tracing(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Tracing``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.VersionDescription``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("version_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.VpcConfigProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::Function.VpcConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.VpcConfigProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnHttpApi(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sam.CfnHttpApi",
):
    '''A CloudFormation ``AWS::Serverless::HttpApi``.

    :cloudformationResource: AWS::Serverless::HttpApi
    :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sam as sam
        
        # authorizers: Any
        # definition_body: Any
        
        cfn_http_api = sam.CfnHttpApi(self, "MyCfnHttpApi",
            access_log_setting=sam.CfnHttpApi.AccessLogSettingProperty(
                destination_arn="destinationArn",
                format="format"
            ),
            auth=sam.CfnHttpApi.HttpApiAuthProperty(
                authorizers=authorizers,
                default_authorizer="defaultAuthorizer"
            ),
            cors_configuration=False,
            default_route_settings=sam.CfnHttpApi.RouteSettingsProperty(
                data_trace_enabled=False,
                detailed_metrics_enabled=False,
                logging_level="loggingLevel",
                throttling_burst_limit=123,
                throttling_rate_limit=123
            ),
            definition_body=definition_body,
            definition_uri="definitionUri",
            description="description",
            disable_execute_api_endpoint=False,
            domain=sam.CfnHttpApi.HttpApiDomainConfigurationProperty(
                certificate_arn="certificateArn",
                domain_name="domainName",
        
                # the properties below are optional
                base_path="basePath",
                endpoint_configuration="endpointConfiguration",
                mutual_tls_authentication=sam.CfnHttpApi.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version=False
                ),
                route53=sam.CfnHttpApi.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                ),
                security_policy="securityPolicy"
            ),
            fail_on_warnings=False,
            route_settings=sam.CfnHttpApi.RouteSettingsProperty(
                data_trace_enabled=False,
                detailed_metrics_enabled=False,
                logging_level="loggingLevel",
                throttling_burst_limit=123,
                throttling_rate_limit=123
            ),
            stage_name="stageName",
            stage_variables={
                "stage_variables_key": "stageVariables"
            },
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        access_log_setting: typing.Optional[typing.Union[typing.Union["CfnHttpApi.AccessLogSettingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        auth: typing.Optional[typing.Union[typing.Union["CfnHttpApi.HttpApiAuthProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cors_configuration: typing.Optional[typing.Union[builtins.bool, typing.Union["CfnHttpApi.CorsConfigurationObjectProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        default_route_settings: typing.Optional[typing.Union[typing.Union["CfnHttpApi.RouteSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union["CfnHttpApi.S3LocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        domain: typing.Optional[typing.Union[typing.Union["CfnHttpApi.HttpApiDomainConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        route_settings: typing.Optional[typing.Union[typing.Union["CfnHttpApi.RouteSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stage_name: typing.Optional[builtins.str] = None,
        stage_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::HttpApi``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_log_setting: ``AWS::Serverless::HttpApi.AccessLogSetting``.
        :param auth: ``AWS::Serverless::HttpApi.Auth``.
        :param cors_configuration: ``AWS::Serverless::HttpApi.CorsConfiguration``.
        :param default_route_settings: ``AWS::Serverless::HttpApi.DefaultRouteSettings``.
        :param definition_body: ``AWS::Serverless::HttpApi.DefinitionBody``.
        :param definition_uri: ``AWS::Serverless::HttpApi.DefinitionUri``.
        :param description: ``AWS::Serverless::HttpApi.Description``.
        :param disable_execute_api_endpoint: ``AWS::Serverless::HttpApi.DisableExecuteApiEndpoint``.
        :param domain: ``AWS::Serverless::HttpApi.Domain``.
        :param fail_on_warnings: ``AWS::Serverless::HttpApi.FailOnWarnings``.
        :param route_settings: ``AWS::Serverless::HttpApi.RouteSettings``.
        :param stage_name: ``AWS::Serverless::HttpApi.StageName``.
        :param stage_variables: ``AWS::Serverless::HttpApi.StageVariables``.
        :param tags: ``AWS::Serverless::HttpApi.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa411e01d6f778480833823e15735ca25e6c504034269114833c9ede4a91f793)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHttpApiProps(
            access_log_setting=access_log_setting,
            auth=auth,
            cors_configuration=cors_configuration,
            default_route_settings=default_route_settings,
            definition_body=definition_body,
            definition_uri=definition_uri,
            description=description,
            disable_execute_api_endpoint=disable_execute_api_endpoint,
            domain=domain,
            fail_on_warnings=fail_on_warnings,
            route_settings=route_settings,
            stage_name=stage_name,
            stage_variables=stage_variables,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6886d79181036dd31ae97b82804a3d16e2c5e78427ee5b1b13f0674123d95027)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6d5fceb7fd25fd6dfe9c0993cacacf85da75f54399f68a5e75a0d50f7e9948)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Serverless::HttpApi.Tags``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="definitionBody")
    def definition_body(self) -> typing.Any:
        '''``AWS::Serverless::HttpApi.DefinitionBody``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Any, jsii.get(self, "definitionBody"))

    @definition_body.setter
    def definition_body(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f716a57d72cc5d708ef2a675264e5e950b1c58b0d9a728ca4675d45840d41ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionBody", value)

    @builtins.property
    @jsii.member(jsii_name="accessLogSetting")
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union["CfnHttpApi.AccessLogSettingProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.AccessLogSetting``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union["CfnHttpApi.AccessLogSettingProperty", _IResolvable_a771d0ef]], jsii.get(self, "accessLogSetting"))

    @access_log_setting.setter
    def access_log_setting(
        self,
        value: typing.Optional[typing.Union["CfnHttpApi.AccessLogSettingProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed21829d9947e92445298a702d845a10b7c2e3f1ba938c5d0314ccc96a2d61e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLogSetting", value)

    @builtins.property
    @jsii.member(jsii_name="auth")
    def auth(
        self,
    ) -> typing.Optional[typing.Union["CfnHttpApi.HttpApiAuthProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.Auth``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union["CfnHttpApi.HttpApiAuthProperty", _IResolvable_a771d0ef]], jsii.get(self, "auth"))

    @auth.setter
    def auth(
        self,
        value: typing.Optional[typing.Union["CfnHttpApi.HttpApiAuthProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1511b652cc6e4c48460c8eb538d3930e04246822b874e2dce1d3745e5f71a7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auth", value)

    @builtins.property
    @jsii.member(jsii_name="corsConfiguration")
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "CfnHttpApi.CorsConfigurationObjectProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.CorsConfiguration``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "CfnHttpApi.CorsConfigurationObjectProperty", _IResolvable_a771d0ef]], jsii.get(self, "corsConfiguration"))

    @cors_configuration.setter
    def cors_configuration(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "CfnHttpApi.CorsConfigurationObjectProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66059a9ea73a2046b9491850fd60e7278e1871a43514a4a9fa339ab2157679d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "corsConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="defaultRouteSettings")
    def default_route_settings(
        self,
    ) -> typing.Optional[typing.Union["CfnHttpApi.RouteSettingsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.DefaultRouteSettings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union["CfnHttpApi.RouteSettingsProperty", _IResolvable_a771d0ef]], jsii.get(self, "defaultRouteSettings"))

    @default_route_settings.setter
    def default_route_settings(
        self,
        value: typing.Optional[typing.Union["CfnHttpApi.RouteSettingsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e62e8b6936488580a3663d80dff4572681025aa8fddb7b068050a1e0c9be617a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRouteSettings", value)

    @builtins.property
    @jsii.member(jsii_name="definitionUri")
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnHttpApi.S3LocationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.DefinitionUri``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnHttpApi.S3LocationProperty", _IResolvable_a771d0ef]], jsii.get(self, "definitionUri"))

    @definition_uri.setter
    def definition_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnHttpApi.S3LocationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea0e9d7f4bf5ffa369ae58f3ce273cf2e859bc897406e83de8af76970500ae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionUri", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::HttpApi.Description``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfecb38222254b2fa0d1c29fcd691fb9b0d727082ed13a8f0ba6405dd342b9a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="disableExecuteApiEndpoint")
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.DisableExecuteApiEndpoint``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-httpapi.html#sam-httpapi-disableexecuteapiendpoint
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "disableExecuteApiEndpoint"))

    @disable_execute_api_endpoint.setter
    def disable_execute_api_endpoint(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98665acacadba691cc71fb95891fcf43748d2b33e3297f10c184d14c38c132b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableExecuteApiEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(
        self,
    ) -> typing.Optional[typing.Union["CfnHttpApi.HttpApiDomainConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.Domain``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union["CfnHttpApi.HttpApiDomainConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "domain"))

    @domain.setter
    def domain(
        self,
        value: typing.Optional[typing.Union["CfnHttpApi.HttpApiDomainConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930c1cef7d89795a70d6197f4ebe1ec4d3a1ddbe0e27917e41cf149fb092e953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="failOnWarnings")
    def fail_on_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.FailOnWarnings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "failOnWarnings"))

    @fail_on_warnings.setter
    def fail_on_warnings(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e1095fdf65eccde40910464056400475ae2e95854dd7ad1d86c6ad121cd438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnWarnings", value)

    @builtins.property
    @jsii.member(jsii_name="routeSettings")
    def route_settings(
        self,
    ) -> typing.Optional[typing.Union["CfnHttpApi.RouteSettingsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.RouteSettings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union["CfnHttpApi.RouteSettingsProperty", _IResolvable_a771d0ef]], jsii.get(self, "routeSettings"))

    @route_settings.setter
    def route_settings(
        self,
        value: typing.Optional[typing.Union["CfnHttpApi.RouteSettingsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88d4ff97b0401e0229cbe78b6f3fb8cb0dc0a4a4415c1eb2f5ee41ee86136fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeSettings", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::HttpApi.StageName``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stageName"))

    @stage_name.setter
    def stage_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e714a934d23cae1c5398836c8ffa6b9cffb2061790d90790a735156010ffbc7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageName", value)

    @builtins.property
    @jsii.member(jsii_name="stageVariables")
    def stage_variables(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::HttpApi.StageVariables``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "stageVariables"))

    @stage_variables.setter
    def stage_variables(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd02bcccb457b1b113468c76500e5e2c1ee07f7124ab8fa68557580bc7dda61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageVariables", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnHttpApi.AccessLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_arn: ``CfnHttpApi.AccessLogSettingProperty.DestinationArn``.
            :param format: ``CfnHttpApi.AccessLogSettingProperty.Format``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                access_log_setting_property = sam.CfnHttpApi.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0dad4a8088a9148e5f5fa0ea961af819c0ffda34a3215a756b1acb3dca152172)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.AccessLogSettingProperty.DestinationArn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.AccessLogSettingProperty.Format``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnHttpApi.CorsConfigurationObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_credentials": "allowCredentials",
            "allow_headers": "allowHeaders",
            "allow_methods": "allowMethods",
            "allow_origins": "allowOrigins",
            "expose_headers": "exposeHeaders",
            "max_age": "maxAge",
        },
    )
    class CorsConfigurationObjectProperty:
        def __init__(
            self,
            *,
            allow_credentials: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
            allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
            expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            max_age: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param allow_credentials: ``CfnHttpApi.CorsConfigurationObjectProperty.AllowCredentials``.
            :param allow_headers: ``CfnHttpApi.CorsConfigurationObjectProperty.AllowHeaders``.
            :param allow_methods: ``CfnHttpApi.CorsConfigurationObjectProperty.AllowMethods``.
            :param allow_origins: ``CfnHttpApi.CorsConfigurationObjectProperty.AllowOrigins``.
            :param expose_headers: ``CfnHttpApi.CorsConfigurationObjectProperty.ExposeHeaders``.
            :param max_age: ``CfnHttpApi.CorsConfigurationObjectProperty.MaxAge``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                cors_configuration_object_property = sam.CfnHttpApi.CorsConfigurationObjectProperty(
                    allow_credentials=False,
                    allow_headers=["allowHeaders"],
                    allow_methods=["allowMethods"],
                    allow_origins=["allowOrigins"],
                    expose_headers=["exposeHeaders"],
                    max_age=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__35e31f5a654409fd70ef66a72719eea79042efda9e9638b13959d8491bf5a126)
                check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
                check_type(argname="argument allow_headers", value=allow_headers, expected_type=type_hints["allow_headers"])
                check_type(argname="argument allow_methods", value=allow_methods, expected_type=type_hints["allow_methods"])
                check_type(argname="argument allow_origins", value=allow_origins, expected_type=type_hints["allow_origins"])
                check_type(argname="argument expose_headers", value=expose_headers, expected_type=type_hints["expose_headers"])
                check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_credentials is not None:
                self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None:
                self._values["allow_headers"] = allow_headers
            if allow_methods is not None:
                self._values["allow_methods"] = allow_methods
            if allow_origins is not None:
                self._values["allow_origins"] = allow_origins
            if expose_headers is not None:
                self._values["expose_headers"] = expose_headers
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allow_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.AllowCredentials``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("allow_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.AllowHeaders``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("allow_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.AllowMethods``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("allow_methods")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.AllowOrigins``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("allow_origins")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.ExposeHeaders``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("expose_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_age(self) -> typing.Optional[jsii.Number]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.MaxAge``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("max_age")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsConfigurationObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnHttpApi.HttpApiAuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorizers": "authorizers",
            "default_authorizer": "defaultAuthorizer",
        },
    )
    class HttpApiAuthProperty:
        def __init__(
            self,
            *,
            authorizers: typing.Any = None,
            default_authorizer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param authorizers: ``CfnHttpApi.HttpApiAuthProperty.Authorizers``.
            :param default_authorizer: ``CfnHttpApi.HttpApiAuthProperty.DefaultAuthorizer``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-httpapiauth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                # authorizers: Any
                
                http_api_auth_property = sam.CfnHttpApi.HttpApiAuthProperty(
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89a86596b352487f89c525f791c68cbe025b53e26ae84f933d3e8bdf93890670)
                check_type(argname="argument authorizers", value=authorizers, expected_type=type_hints["authorizers"])
                check_type(argname="argument default_authorizer", value=default_authorizer, expected_type=type_hints["default_authorizer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorizers is not None:
                self._values["authorizers"] = authorizers
            if default_authorizer is not None:
                self._values["default_authorizer"] = default_authorizer

        @builtins.property
        def authorizers(self) -> typing.Any:
            '''``CfnHttpApi.HttpApiAuthProperty.Authorizers``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-httpapiauth.html#sam-httpapi-httpapiauth-defaultauthorizer
            '''
            result = self._values.get("authorizers")
            return typing.cast(typing.Any, result)

        @builtins.property
        def default_authorizer(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.HttpApiAuthProperty.DefaultAuthorizer``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-httpapiauth.html#sam-httpapi-httpapiauth-authorizers
            '''
            result = self._values.get("default_authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpApiAuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnHttpApi.HttpApiDomainConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "domain_name": "domainName",
            "base_path": "basePath",
            "endpoint_configuration": "endpointConfiguration",
            "mutual_tls_authentication": "mutualTlsAuthentication",
            "route53": "route53",
            "security_policy": "securityPolicy",
        },
    )
    class HttpApiDomainConfigurationProperty:
        def __init__(
            self,
            *,
            certificate_arn: builtins.str,
            domain_name: builtins.str,
            base_path: typing.Optional[builtins.str] = None,
            endpoint_configuration: typing.Optional[builtins.str] = None,
            mutual_tls_authentication: typing.Optional[typing.Union[typing.Union["CfnHttpApi.MutualTlsAuthenticationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            route53: typing.Optional[typing.Union[typing.Union["CfnHttpApi.Route53ConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param certificate_arn: ``CfnHttpApi.HttpApiDomainConfigurationProperty.CertificateArn``.
            :param domain_name: ``CfnHttpApi.HttpApiDomainConfigurationProperty.DomainName``.
            :param base_path: ``CfnHttpApi.HttpApiDomainConfigurationProperty.BasePath``.
            :param endpoint_configuration: ``CfnHttpApi.HttpApiDomainConfigurationProperty.EndpointConfiguration``.
            :param mutual_tls_authentication: ``CfnHttpApi.HttpApiDomainConfigurationProperty.MutualTlsAuthentication``.
            :param route53: ``CfnHttpApi.HttpApiDomainConfigurationProperty.Route53``.
            :param security_policy: ``CfnHttpApi.HttpApiDomainConfigurationProperty.SecurityPolicy``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                http_api_domain_configuration_property = sam.CfnHttpApi.HttpApiDomainConfigurationProperty(
                    certificate_arn="certificateArn",
                    domain_name="domainName",
                
                    # the properties below are optional
                    base_path="basePath",
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam.CfnHttpApi.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version=False
                    ),
                    route53=sam.CfnHttpApi.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b199fc60d229a44bf29ace65240e9ab15b093f42646e5c5a8abe1e44fde8e1cd)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument base_path", value=base_path, expected_type=type_hints["base_path"])
                check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
                check_type(argname="argument mutual_tls_authentication", value=mutual_tls_authentication, expected_type=type_hints["mutual_tls_authentication"])
                check_type(argname="argument route53", value=route53, expected_type=type_hints["route53"])
                check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "certificate_arn": certificate_arn,
                "domain_name": domain_name,
            }
            if base_path is not None:
                self._values["base_path"] = base_path
            if endpoint_configuration is not None:
                self._values["endpoint_configuration"] = endpoint_configuration
            if mutual_tls_authentication is not None:
                self._values["mutual_tls_authentication"] = mutual_tls_authentication
            if route53 is not None:
                self._values["route53"] = route53
            if security_policy is not None:
                self._values["security_policy"] = security_policy

        @builtins.property
        def certificate_arn(self) -> builtins.str:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.CertificateArn``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("certificate_arn")
            assert result is not None, "Required property 'certificate_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def domain_name(self) -> builtins.str:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.DomainName``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("domain_name")
            assert result is not None, "Required property 'domain_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def base_path(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.BasePath``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("base_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_configuration(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.EndpointConfiguration``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("endpoint_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mutual_tls_authentication(
            self,
        ) -> typing.Optional[typing.Union["CfnHttpApi.MutualTlsAuthenticationProperty", _IResolvable_a771d0ef]]:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.MutualTlsAuthentication``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-httpapidomainconfiguration.html#sam-httpapi-httpapidomainconfiguration-mutualtlsauthentication
            '''
            result = self._values.get("mutual_tls_authentication")
            return typing.cast(typing.Optional[typing.Union["CfnHttpApi.MutualTlsAuthenticationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def route53(
            self,
        ) -> typing.Optional[typing.Union["CfnHttpApi.Route53ConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.Route53``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("route53")
            return typing.cast(typing.Optional[typing.Union["CfnHttpApi.Route53ConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def security_policy(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.SecurityPolicy``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("security_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpApiDomainConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnHttpApi.MutualTlsAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "truststore_uri": "truststoreUri",
            "truststore_version": "truststoreVersion",
        },
    )
    class MutualTlsAuthenticationProperty:
        def __init__(
            self,
            *,
            truststore_uri: typing.Optional[builtins.str] = None,
            truststore_version: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param truststore_uri: ``CfnHttpApi.MutualTlsAuthenticationProperty.TruststoreUri``.
            :param truststore_version: ``CfnHttpApi.MutualTlsAuthenticationProperty.TruststoreVersion``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                mutual_tls_authentication_property = sam.CfnHttpApi.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afbe6b7ec59fd65ed1d4807e7497231a6c1f376026f290932f82b02ce818bd6e)
                check_type(argname="argument truststore_uri", value=truststore_uri, expected_type=type_hints["truststore_uri"])
                check_type(argname="argument truststore_version", value=truststore_version, expected_type=type_hints["truststore_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if truststore_uri is not None:
                self._values["truststore_uri"] = truststore_uri
            if truststore_version is not None:
                self._values["truststore_version"] = truststore_version

        @builtins.property
        def truststore_uri(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.MutualTlsAuthenticationProperty.TruststoreUri``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html#cfn-apigatewayv2-domainname-mutualtlsauthentication-truststoreuri
            '''
            result = self._values.get("truststore_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def truststore_version(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnHttpApi.MutualTlsAuthenticationProperty.TruststoreVersion``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html#cfn-apigatewayv2-domainname-mutualtlsauthentication-truststoreversion
            '''
            result = self._values.get("truststore_version")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutualTlsAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnHttpApi.Route53ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "distributed_domain_name": "distributedDomainName",
            "evaluate_target_health": "evaluateTargetHealth",
            "hosted_zone_id": "hostedZoneId",
            "hosted_zone_name": "hostedZoneName",
            "ip_v6": "ipV6",
        },
    )
    class Route53ConfigurationProperty:
        def __init__(
            self,
            *,
            distributed_domain_name: typing.Optional[builtins.str] = None,
            evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
            hosted_zone_name: typing.Optional[builtins.str] = None,
            ip_v6: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param distributed_domain_name: ``CfnHttpApi.Route53ConfigurationProperty.DistributedDomainName``.
            :param evaluate_target_health: ``CfnHttpApi.Route53ConfigurationProperty.EvaluateTargetHealth``.
            :param hosted_zone_id: ``CfnHttpApi.Route53ConfigurationProperty.HostedZoneId``.
            :param hosted_zone_name: ``CfnHttpApi.Route53ConfigurationProperty.HostedZoneName``.
            :param ip_v6: ``CfnHttpApi.Route53ConfigurationProperty.IpV6``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                route53_configuration_property = sam.CfnHttpApi.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e07d70bf7a7dc668a1a657f1b794d64732cfa45204ec84297fc27a3dfb4e31d)
                check_type(argname="argument distributed_domain_name", value=distributed_domain_name, expected_type=type_hints["distributed_domain_name"])
                check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
                check_type(argname="argument hosted_zone_name", value=hosted_zone_name, expected_type=type_hints["hosted_zone_name"])
                check_type(argname="argument ip_v6", value=ip_v6, expected_type=type_hints["ip_v6"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if distributed_domain_name is not None:
                self._values["distributed_domain_name"] = distributed_domain_name
            if evaluate_target_health is not None:
                self._values["evaluate_target_health"] = evaluate_target_health
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id
            if hosted_zone_name is not None:
                self._values["hosted_zone_name"] = hosted_zone_name
            if ip_v6 is not None:
                self._values["ip_v6"] = ip_v6

        @builtins.property
        def distributed_domain_name(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.Route53ConfigurationProperty.DistributedDomainName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html#sam-httpapi-route53configuration-distributiondomainname
            '''
            result = self._values.get("distributed_domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def evaluate_target_health(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnHttpApi.Route53ConfigurationProperty.EvaluateTargetHealth``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html#sam-httpapi-route53configuration-evaluatetargethealth
            '''
            result = self._values.get("evaluate_target_health")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.Route53ConfigurationProperty.HostedZoneId``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html#sam-httpapi-route53configuration-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_name(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.Route53ConfigurationProperty.HostedZoneName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html#sam-httpapi-route53configuration-hostedzonename
            '''
            result = self._values.get("hosted_zone_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ip_v6(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnHttpApi.Route53ConfigurationProperty.IpV6``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html#sam-httpapi-route53configuration-ipv6
            '''
            result = self._values.get("ip_v6")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Route53ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnHttpApi.RouteSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_trace_enabled": "dataTraceEnabled",
            "detailed_metrics_enabled": "detailedMetricsEnabled",
            "logging_level": "loggingLevel",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
        },
    )
    class RouteSettingsProperty:
        def __init__(
            self,
            *,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            logging_level: typing.Optional[builtins.str] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param data_trace_enabled: ``CfnHttpApi.RouteSettingsProperty.DataTraceEnabled``.
            :param detailed_metrics_enabled: ``CfnHttpApi.RouteSettingsProperty.DetailedMetricsEnabled``.
            :param logging_level: ``CfnHttpApi.RouteSettingsProperty.LoggingLevel``.
            :param throttling_burst_limit: ``CfnHttpApi.RouteSettingsProperty.ThrottlingBurstLimit``.
            :param throttling_rate_limit: ``CfnHttpApi.RouteSettingsProperty.ThrottlingRateLimit``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                route_settings_property = sam.CfnHttpApi.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c470fee9a95389a07991e47206b0f93fc029de7d632375269557f84e11fe5ebf)
                check_type(argname="argument data_trace_enabled", value=data_trace_enabled, expected_type=type_hints["data_trace_enabled"])
                check_type(argname="argument detailed_metrics_enabled", value=detailed_metrics_enabled, expected_type=type_hints["detailed_metrics_enabled"])
                check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
                check_type(argname="argument throttling_burst_limit", value=throttling_burst_limit, expected_type=type_hints["throttling_burst_limit"])
                check_type(argname="argument throttling_rate_limit", value=throttling_rate_limit, expected_type=type_hints["throttling_rate_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if detailed_metrics_enabled is not None:
                self._values["detailed_metrics_enabled"] = detailed_metrics_enabled
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnHttpApi.RouteSettingsProperty.DataTraceEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-datatraceenabled
            '''
            result = self._values.get("data_trace_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def detailed_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnHttpApi.RouteSettingsProperty.DetailedMetricsEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-detailedmetricsenabled
            '''
            result = self._values.get("detailed_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.RouteSettingsProperty.LoggingLevel``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-logginglevel
            '''
            result = self._values.get("logging_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            '''``CfnHttpApi.RouteSettingsProperty.ThrottlingBurstLimit``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingburstlimit
            '''
            result = self._values.get("throttling_burst_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            '''``CfnHttpApi.RouteSettingsProperty.ThrottlingRateLimit``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingratelimit
            '''
            result = self._values.get("throttling_rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnHttpApi.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: jsii.Number,
        ) -> None:
            '''
            :param bucket: ``CfnHttpApi.S3LocationProperty.Bucket``.
            :param key: ``CfnHttpApi.S3LocationProperty.Key``.
            :param version: ``CfnHttpApi.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s3_location_property = sam.CfnHttpApi.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__230a3845c48f75035abe656bccaf360b24fe16b1264ce6b5c703f27803ba694b)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
                "version": version,
            }

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnHttpApi.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnHttpApi.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> jsii.Number:
            '''``CfnHttpApi.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_sam.CfnHttpApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_log_setting": "accessLogSetting",
        "auth": "auth",
        "cors_configuration": "corsConfiguration",
        "default_route_settings": "defaultRouteSettings",
        "definition_body": "definitionBody",
        "definition_uri": "definitionUri",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
        "domain": "domain",
        "fail_on_warnings": "failOnWarnings",
        "route_settings": "routeSettings",
        "stage_name": "stageName",
        "stage_variables": "stageVariables",
        "tags": "tags",
    },
)
class CfnHttpApiProps:
    def __init__(
        self,
        *,
        access_log_setting: typing.Optional[typing.Union[typing.Union[CfnHttpApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        auth: typing.Optional[typing.Union[typing.Union[CfnHttpApi.HttpApiAuthProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cors_configuration: typing.Optional[typing.Union[builtins.bool, typing.Union[CfnHttpApi.CorsConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        default_route_settings: typing.Optional[typing.Union[typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnHttpApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        domain: typing.Optional[typing.Union[typing.Union[CfnHttpApi.HttpApiDomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        route_settings: typing.Optional[typing.Union[typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stage_name: typing.Optional[builtins.str] = None,
        stage_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnHttpApi``.

        :param access_log_setting: ``AWS::Serverless::HttpApi.AccessLogSetting``.
        :param auth: ``AWS::Serverless::HttpApi.Auth``.
        :param cors_configuration: ``AWS::Serverless::HttpApi.CorsConfiguration``.
        :param default_route_settings: ``AWS::Serverless::HttpApi.DefaultRouteSettings``.
        :param definition_body: ``AWS::Serverless::HttpApi.DefinitionBody``.
        :param definition_uri: ``AWS::Serverless::HttpApi.DefinitionUri``.
        :param description: ``AWS::Serverless::HttpApi.Description``.
        :param disable_execute_api_endpoint: ``AWS::Serverless::HttpApi.DisableExecuteApiEndpoint``.
        :param domain: ``AWS::Serverless::HttpApi.Domain``.
        :param fail_on_warnings: ``AWS::Serverless::HttpApi.FailOnWarnings``.
        :param route_settings: ``AWS::Serverless::HttpApi.RouteSettings``.
        :param stage_name: ``AWS::Serverless::HttpApi.StageName``.
        :param stage_variables: ``AWS::Serverless::HttpApi.StageVariables``.
        :param tags: ``AWS::Serverless::HttpApi.Tags``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sam as sam
            
            # authorizers: Any
            # definition_body: Any
            
            cfn_http_api_props = sam.CfnHttpApiProps(
                access_log_setting=sam.CfnHttpApi.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                ),
                auth=sam.CfnHttpApi.HttpApiAuthProperty(
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                ),
                cors_configuration=False,
                default_route_settings=sam.CfnHttpApi.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                ),
                definition_body=definition_body,
                definition_uri="definitionUri",
                description="description",
                disable_execute_api_endpoint=False,
                domain=sam.CfnHttpApi.HttpApiDomainConfigurationProperty(
                    certificate_arn="certificateArn",
                    domain_name="domainName",
            
                    # the properties below are optional
                    base_path="basePath",
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam.CfnHttpApi.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version=False
                    ),
                    route53=sam.CfnHttpApi.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                ),
                fail_on_warnings=False,
                route_settings=sam.CfnHttpApi.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                ),
                stage_name="stageName",
                stage_variables={
                    "stage_variables_key": "stageVariables"
                },
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2b433bf42e48d668ae6e9a2311b15e7e56d8122e2976fefded5e15bb97c10d)
            check_type(argname="argument access_log_setting", value=access_log_setting, expected_type=type_hints["access_log_setting"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument cors_configuration", value=cors_configuration, expected_type=type_hints["cors_configuration"])
            check_type(argname="argument default_route_settings", value=default_route_settings, expected_type=type_hints["default_route_settings"])
            check_type(argname="argument definition_body", value=definition_body, expected_type=type_hints["definition_body"])
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_execute_api_endpoint", value=disable_execute_api_endpoint, expected_type=type_hints["disable_execute_api_endpoint"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument fail_on_warnings", value=fail_on_warnings, expected_type=type_hints["fail_on_warnings"])
            check_type(argname="argument route_settings", value=route_settings, expected_type=type_hints["route_settings"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument stage_variables", value=stage_variables, expected_type=type_hints["stage_variables"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_log_setting is not None:
            self._values["access_log_setting"] = access_log_setting
        if auth is not None:
            self._values["auth"] = auth
        if cors_configuration is not None:
            self._values["cors_configuration"] = cors_configuration
        if default_route_settings is not None:
            self._values["default_route_settings"] = default_route_settings
        if definition_body is not None:
            self._values["definition_body"] = definition_body
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint
        if domain is not None:
            self._values["domain"] = domain
        if fail_on_warnings is not None:
            self._values["fail_on_warnings"] = fail_on_warnings
        if route_settings is not None:
            self._values["route_settings"] = route_settings
        if stage_name is not None:
            self._values["stage_name"] = stage_name
        if stage_variables is not None:
            self._values["stage_variables"] = stage_variables
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union[CfnHttpApi.AccessLogSettingProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.AccessLogSetting``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("access_log_setting")
        return typing.cast(typing.Optional[typing.Union[CfnHttpApi.AccessLogSettingProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def auth(
        self,
    ) -> typing.Optional[typing.Union[CfnHttpApi.HttpApiAuthProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.Auth``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[typing.Union[CfnHttpApi.HttpApiAuthProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, CfnHttpApi.CorsConfigurationObjectProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.CorsConfiguration``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("cors_configuration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, CfnHttpApi.CorsConfigurationObjectProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def default_route_settings(
        self,
    ) -> typing.Optional[typing.Union[CfnHttpApi.RouteSettingsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.DefaultRouteSettings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("default_route_settings")
        return typing.cast(typing.Optional[typing.Union[CfnHttpApi.RouteSettingsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def definition_body(self) -> typing.Any:
        '''``AWS::Serverless::HttpApi.DefinitionBody``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("definition_body")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnHttpApi.S3LocationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.DefinitionUri``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnHttpApi.S3LocationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::HttpApi.Description``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.DisableExecuteApiEndpoint``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-httpapi.html#sam-httpapi-disableexecuteapiendpoint
        '''
        result = self._values.get("disable_execute_api_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def domain(
        self,
    ) -> typing.Optional[typing.Union[CfnHttpApi.HttpApiDomainConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.Domain``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[typing.Union[CfnHttpApi.HttpApiDomainConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def fail_on_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.FailOnWarnings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("fail_on_warnings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def route_settings(
        self,
    ) -> typing.Optional[typing.Union[CfnHttpApi.RouteSettingsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::HttpApi.RouteSettings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("route_settings")
        return typing.cast(typing.Optional[typing.Union[CfnHttpApi.RouteSettingsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::HttpApi.StageName``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_variables(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::HttpApi.StageVariables``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("stage_variables")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::HttpApi.Tags``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHttpApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLayerVersion(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sam.CfnLayerVersion",
):
    '''A CloudFormation ``AWS::Serverless::LayerVersion``.

    :cloudformationResource: AWS::Serverless::LayerVersion
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sam as sam
        
        cfn_layer_version = sam.CfnLayerVersion(self, "MyCfnLayerVersion",
            compatible_runtimes=["compatibleRuntimes"],
            content_uri="contentUri",
            description="description",
            layer_name="layerName",
            license_info="licenseInfo",
            retention_policy="retentionPolicy"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_uri: typing.Optional[typing.Union[builtins.str, typing.Union["CfnLayerVersion.S3LocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        layer_name: typing.Optional[builtins.str] = None,
        license_info: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::LayerVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param compatible_runtimes: ``AWS::Serverless::LayerVersion.CompatibleRuntimes``.
        :param content_uri: ``AWS::Serverless::LayerVersion.ContentUri``.
        :param description: ``AWS::Serverless::LayerVersion.Description``.
        :param layer_name: ``AWS::Serverless::LayerVersion.LayerName``.
        :param license_info: ``AWS::Serverless::LayerVersion.LicenseInfo``.
        :param retention_policy: ``AWS::Serverless::LayerVersion.RetentionPolicy``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b6f04ed630f026d1734622d5cc0611ac0426a3f336979a0b71887ad86ee023)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLayerVersionProps(
            compatible_runtimes=compatible_runtimes,
            content_uri=content_uri,
            description=description,
            layer_name=layer_name,
            license_info=license_info,
            retention_policy=retention_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57aee27769c12f67ea279db56364a802378867a2330bb5d56b86ef90fa624ed)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83693e2df7267062d72e9c94d16092495ec930ee2ca168f435f0f61c7de5b65f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::LayerVersion.CompatibleRuntimes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "compatibleRuntimes"))

    @compatible_runtimes.setter
    def compatible_runtimes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfcc02ce98180060e8b7f66e34c9f926075d3825d38ed0960d6903e62a050c97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compatibleRuntimes", value)

    @builtins.property
    @jsii.member(jsii_name="contentUri")
    def content_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnLayerVersion.S3LocationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::LayerVersion.ContentUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnLayerVersion.S3LocationProperty", _IResolvable_a771d0ef]], jsii.get(self, "contentUri"))

    @content_uri.setter
    def content_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnLayerVersion.S3LocationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b453a6454c1eda610298aad694ae21322a6aa6e05a49bb0f344baefc483a9030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentUri", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d68189436f9b0d210a08d61a3825b5d4dedacc07abdddd3ffa119d46058163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="layerName")
    def layer_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LayerName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "layerName"))

    @layer_name.setter
    def layer_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a75d064fe11d7e462efbc3d00da1078c3e19e248052ecbc72f3709be5090eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "layerName", value)

    @builtins.property
    @jsii.member(jsii_name="licenseInfo")
    def license_info(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LicenseInfo``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseInfo"))

    @license_info.setter
    def license_info(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b596565df284c23053142763389419202c17a44c7121b4454175b56c5f134878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseInfo", value)

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.RetentionPolicy``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionPolicy"))

    @retention_policy.setter
    def retention_policy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e3b80f431b7cdeae00d85a8972746955695df6b9589698d9b5e83207fc7381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicy", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnLayerVersion.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: ``CfnLayerVersion.S3LocationProperty.Bucket``.
            :param key: ``CfnLayerVersion.S3LocationProperty.Key``.
            :param version: ``CfnLayerVersion.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s3_location_property = sam.CfnLayerVersion.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                
                    # the properties below are optional
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b9772b9ebbe1caf9d00a3636b7e71d9cf78b74056dcc80b8485f5c65f74f9eb2)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnLayerVersion.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnLayerVersion.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''``CfnLayerVersion.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_sam.CfnLayerVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "compatible_runtimes": "compatibleRuntimes",
        "content_uri": "contentUri",
        "description": "description",
        "layer_name": "layerName",
        "license_info": "licenseInfo",
        "retention_policy": "retentionPolicy",
    },
)
class CfnLayerVersionProps:
    def __init__(
        self,
        *,
        compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnLayerVersion.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        layer_name: typing.Optional[builtins.str] = None,
        license_info: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLayerVersion``.

        :param compatible_runtimes: ``AWS::Serverless::LayerVersion.CompatibleRuntimes``.
        :param content_uri: ``AWS::Serverless::LayerVersion.ContentUri``.
        :param description: ``AWS::Serverless::LayerVersion.Description``.
        :param layer_name: ``AWS::Serverless::LayerVersion.LayerName``.
        :param license_info: ``AWS::Serverless::LayerVersion.LicenseInfo``.
        :param retention_policy: ``AWS::Serverless::LayerVersion.RetentionPolicy``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sam as sam
            
            cfn_layer_version_props = sam.CfnLayerVersionProps(
                compatible_runtimes=["compatibleRuntimes"],
                content_uri="contentUri",
                description="description",
                layer_name="layerName",
                license_info="licenseInfo",
                retention_policy="retentionPolicy"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc739a3bfb10e84da9ff4deea2213e663e0a9dc646e4fbb7ce13b214e32fdae)
            check_type(argname="argument compatible_runtimes", value=compatible_runtimes, expected_type=type_hints["compatible_runtimes"])
            check_type(argname="argument content_uri", value=content_uri, expected_type=type_hints["content_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument layer_name", value=layer_name, expected_type=type_hints["layer_name"])
            check_type(argname="argument license_info", value=license_info, expected_type=type_hints["license_info"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compatible_runtimes is not None:
            self._values["compatible_runtimes"] = compatible_runtimes
        if content_uri is not None:
            self._values["content_uri"] = content_uri
        if description is not None:
            self._values["description"] = description
        if layer_name is not None:
            self._values["layer_name"] = layer_name
        if license_info is not None:
            self._values["license_info"] = license_info
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy

    @builtins.property
    def compatible_runtimes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::LayerVersion.CompatibleRuntimes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("compatible_runtimes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def content_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnLayerVersion.S3LocationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::LayerVersion.ContentUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("content_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnLayerVersion.S3LocationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layer_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LayerName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("layer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_info(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LicenseInfo``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("license_info")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.RetentionPolicy``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLayerVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSimpleTable(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sam.CfnSimpleTable",
):
    '''A CloudFormation ``AWS::Serverless::SimpleTable``.

    :cloudformationResource: AWS::Serverless::SimpleTable
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sam as sam
        
        cfn_simple_table = sam.CfnSimpleTable(self, "MyCfnSimpleTable",
            primary_key=sam.CfnSimpleTable.PrimaryKeyProperty(
                type="type",
        
                # the properties below are optional
                name="name"
            ),
            provisioned_throughput=sam.CfnSimpleTable.ProvisionedThroughputProperty(
                write_capacity_units=123,
        
                # the properties below are optional
                read_capacity_units=123
            ),
            sse_specification=sam.CfnSimpleTable.SSESpecificationProperty(
                sse_enabled=False
            ),
            table_name="tableName",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        primary_key: typing.Optional[typing.Union[typing.Union["CfnSimpleTable.PrimaryKeyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        provisioned_throughput: typing.Optional[typing.Union[typing.Union["CfnSimpleTable.ProvisionedThroughputProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sse_specification: typing.Optional[typing.Union[typing.Union["CfnSimpleTable.SSESpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::SimpleTable``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param primary_key: ``AWS::Serverless::SimpleTable.PrimaryKey``.
        :param provisioned_throughput: ``AWS::Serverless::SimpleTable.ProvisionedThroughput``.
        :param sse_specification: ``AWS::Serverless::SimpleTable.SSESpecification``.
        :param table_name: ``AWS::Serverless::SimpleTable.TableName``.
        :param tags: ``AWS::Serverless::SimpleTable.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44d23bbd962691797648c10128ff0090ac41bfa06558cdbc76920ea818bfc7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSimpleTableProps(
            primary_key=primary_key,
            provisioned_throughput=provisioned_throughput,
            sse_specification=sse_specification,
            table_name=table_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7bc8998ec79f64c212ffc00232a5ebaf9c513a6b11e4efda7292d9a69691c8)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae7c4bce351d0b7f6de3229fbc4b9d614777e9ad21ad34c2daa62778234eae9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Serverless::SimpleTable.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union["CfnSimpleTable.PrimaryKeyProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::SimpleTable.PrimaryKey``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSimpleTable.PrimaryKeyProperty", _IResolvable_a771d0ef]], jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(
        self,
        value: typing.Optional[typing.Union["CfnSimpleTable.PrimaryKeyProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846f3714de353ef22bad0fb130478210893e73cf99bb7d30d4372ea32d1328f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughput")
    def provisioned_throughput(
        self,
    ) -> typing.Optional[typing.Union["CfnSimpleTable.ProvisionedThroughputProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::SimpleTable.ProvisionedThroughput``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSimpleTable.ProvisionedThroughputProperty", _IResolvable_a771d0ef]], jsii.get(self, "provisionedThroughput"))

    @provisioned_throughput.setter
    def provisioned_throughput(
        self,
        value: typing.Optional[typing.Union["CfnSimpleTable.ProvisionedThroughputProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75bb119576bfc8e2295756d5ca76b923671f26be0ad39fb48a587d67ad15707d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedThroughput", value)

    @builtins.property
    @jsii.member(jsii_name="sseSpecification")
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnSimpleTable.SSESpecificationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::SimpleTable.SSESpecification``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSimpleTable.SSESpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "sseSpecification"))

    @sse_specification.setter
    def sse_specification(
        self,
        value: typing.Optional[typing.Union["CfnSimpleTable.SSESpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7894a16a6821788d3ad385df5331aa2f170a254b680dc1a83d24e0b1edfe36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::SimpleTable.TableName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0a5fd537a53d2f88667e33bfe747ea6254dc5cd2c3c4a814336511cac7a649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnSimpleTable.PrimaryKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "name": "name"},
    )
    class PrimaryKeyProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param type: ``CfnSimpleTable.PrimaryKeyProperty.Type``.
            :param name: ``CfnSimpleTable.PrimaryKeyProperty.Name``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                primary_key_property = sam.CfnSimpleTable.PrimaryKeyProperty(
                    type="type",
                
                    # the properties below are optional
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c39f460fee285d965b5d5ace9481d479ab5d07043ef03a78ebdb620b509c87f)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnSimpleTable.PrimaryKeyProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnSimpleTable.PrimaryKeyProperty.Name``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrimaryKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnSimpleTable.ProvisionedThroughputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "write_capacity_units": "writeCapacityUnits",
            "read_capacity_units": "readCapacityUnits",
        },
    )
    class ProvisionedThroughputProperty:
        def __init__(
            self,
            *,
            write_capacity_units: jsii.Number,
            read_capacity_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param write_capacity_units: ``CfnSimpleTable.ProvisionedThroughputProperty.WriteCapacityUnits``.
            :param read_capacity_units: ``CfnSimpleTable.ProvisionedThroughputProperty.ReadCapacityUnits``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                provisioned_throughput_property = sam.CfnSimpleTable.ProvisionedThroughputProperty(
                    write_capacity_units=123,
                
                    # the properties below are optional
                    read_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ac88047acc8e01622c99d653e2a0504d82a054a24cef371572734385a06f064)
                check_type(argname="argument write_capacity_units", value=write_capacity_units, expected_type=type_hints["write_capacity_units"])
                check_type(argname="argument read_capacity_units", value=read_capacity_units, expected_type=type_hints["read_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "write_capacity_units": write_capacity_units,
            }
            if read_capacity_units is not None:
                self._values["read_capacity_units"] = read_capacity_units

        @builtins.property
        def write_capacity_units(self) -> jsii.Number:
            '''``CfnSimpleTable.ProvisionedThroughputProperty.WriteCapacityUnits``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
            '''
            result = self._values.get("write_capacity_units")
            assert result is not None, "Required property 'write_capacity_units' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def read_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''``CfnSimpleTable.ProvisionedThroughputProperty.ReadCapacityUnits``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
            '''
            result = self._values.get("read_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedThroughputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnSimpleTable.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"sse_enabled": "sseEnabled"},
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            sse_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param sse_enabled: ``CfnSimpleTable.SSESpecificationProperty.SSEEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s_sESpecification_property = sam.CfnSimpleTable.SSESpecificationProperty(
                    sse_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72e3a74ff254a07b2e0d05ed197d48744c7d07e8042df0f7ae44c2dd4dd3856f)
                check_type(argname="argument sse_enabled", value=sse_enabled, expected_type=type_hints["sse_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sse_enabled is not None:
                self._values["sse_enabled"] = sse_enabled

        @builtins.property
        def sse_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnSimpleTable.SSESpecificationProperty.SSEEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html
            '''
            result = self._values.get("sse_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_sam.CfnSimpleTableProps",
    jsii_struct_bases=[],
    name_mapping={
        "primary_key": "primaryKey",
        "provisioned_throughput": "provisionedThroughput",
        "sse_specification": "sseSpecification",
        "table_name": "tableName",
        "tags": "tags",
    },
)
class CfnSimpleTableProps:
    def __init__(
        self,
        *,
        primary_key: typing.Optional[typing.Union[typing.Union[CfnSimpleTable.PrimaryKeyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        provisioned_throughput: typing.Optional[typing.Union[typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sse_specification: typing.Optional[typing.Union[typing.Union[CfnSimpleTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSimpleTable``.

        :param primary_key: ``AWS::Serverless::SimpleTable.PrimaryKey``.
        :param provisioned_throughput: ``AWS::Serverless::SimpleTable.ProvisionedThroughput``.
        :param sse_specification: ``AWS::Serverless::SimpleTable.SSESpecification``.
        :param table_name: ``AWS::Serverless::SimpleTable.TableName``.
        :param tags: ``AWS::Serverless::SimpleTable.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sam as sam
            
            cfn_simple_table_props = sam.CfnSimpleTableProps(
                primary_key=sam.CfnSimpleTable.PrimaryKeyProperty(
                    type="type",
            
                    # the properties below are optional
                    name="name"
                ),
                provisioned_throughput=sam.CfnSimpleTable.ProvisionedThroughputProperty(
                    write_capacity_units=123,
            
                    # the properties below are optional
                    read_capacity_units=123
                ),
                sse_specification=sam.CfnSimpleTable.SSESpecificationProperty(
                    sse_enabled=False
                ),
                table_name="tableName",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e367d7231cd973a844124a4129768a224ad6f5aa81749af11fe8e0a676a8aa1c)
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
            check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            check_type(argname="argument sse_specification", value=sse_specification, expected_type=type_hints["sse_specification"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if primary_key is not None:
            self._values["primary_key"] = primary_key
        if provisioned_throughput is not None:
            self._values["provisioned_throughput"] = provisioned_throughput
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union[CfnSimpleTable.PrimaryKeyProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::SimpleTable.PrimaryKey``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional[typing.Union[CfnSimpleTable.PrimaryKeyProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def provisioned_throughput(
        self,
    ) -> typing.Optional[typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::SimpleTable.ProvisionedThroughput``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnSimpleTable.SSESpecificationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::SimpleTable.SSESpecification``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        result = self._values.get("sse_specification")
        return typing.cast(typing.Optional[typing.Union[CfnSimpleTable.SSESpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::SimpleTable.TableName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::SimpleTable.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSimpleTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnStateMachine(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sam.CfnStateMachine",
):
    '''A CloudFormation ``AWS::Serverless::StateMachine``.

    :cloudformationResource: AWS::Serverless::StateMachine
    :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_sam as sam
        
        # definition: Any
        
        cfn_state_machine = sam.CfnStateMachine(self, "MyCfnStateMachine",
            definition=definition,
            definition_substitutions={
                "definition_substitutions_key": "definitionSubstitutions"
            },
            definition_uri="definitionUri",
            events={
                "events_key": sam.CfnStateMachine.EventSourceProperty(
                    properties=sam.CfnStateMachine.CloudWatchEventEventProperty(
                        method="method",
                        path="path",
        
                        # the properties below are optional
                        rest_api_id="restApiId"
                    ),
                    type="type"
                )
            },
            logging=sam.CfnStateMachine.LoggingConfigurationProperty(
                destinations=[sam.CfnStateMachine.LogDestinationProperty(
                    cloud_watch_logs_log_group=sam.CfnStateMachine.CloudWatchLogsLogGroupProperty(
                        log_group_arn="logGroupArn"
                    )
                )],
                include_execution_data=False,
                level="level"
            ),
            name="name",
            permissions_boundaries="permissionsBoundaries",
            policies="policies",
            role="role",
            tags={
                "tags_key": "tags"
            },
            tracing=sam.CfnStateMachine.TracingConfigurationProperty(
                enabled=False
            ),
            type="type"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        definition: typing.Any = None,
        definition_substitutions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union["CfnStateMachine.S3LocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnStateMachine.EventSourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        logging: typing.Optional[typing.Union[typing.Union["CfnStateMachine.LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions_boundaries: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, typing.Union["CfnStateMachine.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef, typing.Sequence[typing.Union[builtins.str, typing.Union["CfnStateMachine.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachine.SAMPolicyTemplateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing: typing.Optional[typing.Union[typing.Union["CfnStateMachine.TracingConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::StateMachine``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param definition: ``AWS::Serverless::StateMachine.Definition``.
        :param definition_substitutions: ``AWS::Serverless::StateMachine.DefinitionSubstitutions``.
        :param definition_uri: ``AWS::Serverless::StateMachine.DefinitionUri``.
        :param events: ``AWS::Serverless::StateMachine.Events``.
        :param logging: ``AWS::Serverless::StateMachine.Logging``.
        :param name: ``AWS::Serverless::StateMachine.Name``.
        :param permissions_boundaries: ``AWS::Serverless::StateMachine.PermissionsBoundaries``.
        :param policies: ``AWS::Serverless::StateMachine.Policies``.
        :param role: ``AWS::Serverless::StateMachine.Role``.
        :param tags: ``AWS::Serverless::StateMachine.Tags``.
        :param tracing: ``AWS::Serverless::StateMachine.Tracing``.
        :param type: ``AWS::Serverless::StateMachine.Type``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f261dd0ab90ba2d0f9dfd9bc6dbef41aa183f6a6dfe59a926fb7a7b7c818a1be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStateMachineProps(
            definition=definition,
            definition_substitutions=definition_substitutions,
            definition_uri=definition_uri,
            events=events,
            logging=logging,
            name=name,
            permissions_boundaries=permissions_boundaries,
            policies=policies,
            role=role,
            tags=tags,
            tracing=tracing,
            type=type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07216c550a6c258f33e2f0440d2a653fffebfcb7a79604cbae35c9c6357993f7)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882af4bdf2ad713e6e9888d2815595b660b11326524d98d23691271be53499d8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Serverless::StateMachine.Tags``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Any:
        '''``AWS::Serverless::StateMachine.Definition``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Any, jsii.get(self, "definition"))

    @definition.setter
    def definition(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc26613798481b6eb804cabd70e6611bafd59b7fccd9e8e25017e170f6b5ef75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value)

    @builtins.property
    @jsii.member(jsii_name="definitionSubstitutions")
    def definition_substitutions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::StateMachine.DefinitionSubstitutions``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "definitionSubstitutions"))

    @definition_substitutions.setter
    def definition_substitutions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6d09fb960474f623d643f4ba812981b38ac75aa6548b1f642309d3c2662a98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionSubstitutions", value)

    @builtins.property
    @jsii.member(jsii_name="definitionUri")
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnStateMachine.S3LocationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::StateMachine.DefinitionUri``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnStateMachine.S3LocationProperty", _IResolvable_a771d0ef]], jsii.get(self, "definitionUri"))

    @definition_uri.setter
    def definition_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnStateMachine.S3LocationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c0355ff6b86cc77af6e396b98cd849b46fd8c90501b03eac3c55050464bdc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionUri", value)

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnStateMachine.EventSourceProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Serverless::StateMachine.Events``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnStateMachine.EventSourceProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "events"))

    @events.setter
    def events(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnStateMachine.EventSourceProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b889372b331f3d912cf0e70a79e10bfe1f3c54a6a99f9249eb8c4adad829b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value)

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(
        self,
    ) -> typing.Optional[typing.Union["CfnStateMachine.LoggingConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::StateMachine.Logging``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStateMachine.LoggingConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "logging"))

    @logging.setter
    def logging(
        self,
        value: typing.Optional[typing.Union["CfnStateMachine.LoggingConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4772c2e9f4530d01c63f88be4fadeee1ccc85325804f7e13a730ba4241cf8608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Name``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876774c3ef2ce660773bbb5c87ddc5b7d16335b8c6fec81bc79150d9ee971bbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundaries")
    def permissions_boundaries(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.PermissionsBoundaries``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html#sam-statemachine-permissionsboundary
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundaries"))

    @permissions_boundaries.setter
    def permissions_boundaries(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd96db9a00098d42372e7c4c10581ad2de390cba6ba8d5f1bafead7075a5e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundaries", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", "CfnStateMachine.SAMPolicyTemplateProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Serverless::StateMachine.Policies``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", "CfnStateMachine.SAMPolicyTemplateProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", "CfnStateMachine.SAMPolicyTemplateProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c9a4acf3364986a2fde3dd2cd8b52b0a3db758a5a1019c80862415c4e7c2ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Role``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "role"))

    @role.setter
    def role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880d6a7456d03c49121155c029d2c524510dc6237be7843c7ed8381ac07f4bbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="tracing")
    def tracing(
        self,
    ) -> typing.Optional[typing.Union["CfnStateMachine.TracingConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::StateMachine.Tracing``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html#sam-statemachine-tracing
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStateMachine.TracingConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "tracing"))

    @tracing.setter
    def tracing(
        self,
        value: typing.Optional[typing.Union["CfnStateMachine.TracingConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00bd6f8184fd1f118e4a2c58c2c2927aa176b09bb35d479620f1f865a8cdf184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tracing", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Type``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ff39f278f3f850d6b003762d8170bbd5151dc7757728080e64e730891e7bc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.ApiEventProperty",
        jsii_struct_bases=[],
        name_mapping={"method": "method", "path": "path", "rest_api_id": "restApiId"},
    )
    class ApiEventProperty:
        def __init__(
            self,
            *,
            method: builtins.str,
            path: builtins.str,
            rest_api_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param method: ``CfnStateMachine.ApiEventProperty.Method``.
            :param path: ``CfnStateMachine.ApiEventProperty.Path``.
            :param rest_api_id: ``CfnStateMachine.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                api_event_property = sam.CfnStateMachine.ApiEventProperty(
                    method="method",
                    path="path",
                
                    # the properties below are optional
                    rest_api_id="restApiId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be2293073e212958f35b7dc2d0b78008219049e094cc382f7dc02c15358bfce2)
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "method": method,
                "path": path,
            }
            if rest_api_id is not None:
                self._values["rest_api_id"] = rest_api_id

        @builtins.property
        def method(self) -> builtins.str:
            '''``CfnStateMachine.ApiEventProperty.Method``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("method")
            assert result is not None, "Required property 'method' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def path(self) -> builtins.str:
            '''``CfnStateMachine.ApiEventProperty.Path``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("path")
            assert result is not None, "Required property 'path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def rest_api_id(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("rest_api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.CloudWatchEventEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class CloudWatchEventEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnStateMachine.CloudWatchEventEventProperty.Pattern``.
            :param event_bus_name: ``CfnStateMachine.CloudWatchEventEventProperty.EventBusName``.
            :param input: ``CfnStateMachine.CloudWatchEventEventProperty.Input``.
            :param input_path: ``CfnStateMachine.CloudWatchEventEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                # pattern: Any
                
                cloud_watch_event_event_property = sam.CfnStateMachine.CloudWatchEventEventProperty(
                    pattern=pattern,
                
                    # the properties below are optional
                    event_bus_name="eventBusName",
                    input="input",
                    input_path="inputPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__626533df1a46e4afb94d528358bc617c1e624690bbc09deb2c2e873066785ec0)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
                check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "pattern": pattern,
            }
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnStateMachine.CloudWatchEventEventProperty.Pattern``.

            :link: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.CloudWatchEventEventProperty.EventBusName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.CloudWatchEventEventProperty.Input``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.CloudWatchEventEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchEventEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.CloudWatchLogsLogGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class CloudWatchLogsLogGroupProperty:
        def __init__(self, *, log_group_arn: builtins.str) -> None:
            '''
            :param log_group_arn: ``CfnStateMachine.CloudWatchLogsLogGroupProperty.LogGroupArn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                cloud_watch_logs_log_group_property = sam.CfnStateMachine.CloudWatchLogsLogGroupProperty(
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee2d018eb508c04f2196cc80cdd11a377faf08bbab21144edb462d731007bf93)
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_group_arn": log_group_arn,
            }

        @builtins.property
        def log_group_arn(self) -> builtins.str:
            '''``CfnStateMachine.CloudWatchLogsLogGroupProperty.LogGroupArn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup.html
            '''
            result = self._values.get("log_group_arn")
            assert result is not None, "Required property 'log_group_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsLogGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.EventBridgeRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class EventBridgeRuleEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnStateMachine.EventBridgeRuleEventProperty.Pattern``.
            :param event_bus_name: ``CfnStateMachine.EventBridgeRuleEventProperty.EventBusName``.
            :param input: ``CfnStateMachine.EventBridgeRuleEventProperty.Input``.
            :param input_path: ``CfnStateMachine.EventBridgeRuleEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                # pattern: Any
                
                event_bridge_rule_event_property = sam.CfnStateMachine.EventBridgeRuleEventProperty(
                    pattern=pattern,
                
                    # the properties below are optional
                    event_bus_name="eventBusName",
                    input="input",
                    input_path="inputPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5ddfc96f6bb05b471d2dd4be91f276425fc70c8fad46ba1bac4db60f59da035)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
                check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "pattern": pattern,
            }
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.Pattern``.

            :link: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.EventBusName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.Input``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.EventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"properties": "properties", "type": "type"},
    )
    class EventSourceProperty:
        def __init__(
            self,
            *,
            properties: typing.Union[typing.Union["CfnStateMachine.ApiEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachine.CloudWatchEventEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachine.EventBridgeRuleEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachine.ScheduleEventProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            type: builtins.str,
        ) -> None:
            '''
            :param properties: ``CfnStateMachine.EventSourceProperty.Properties``.
            :param type: ``CfnStateMachine.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                event_source_property = sam.CfnStateMachine.EventSourceProperty(
                    properties=sam.CfnStateMachine.CloudWatchEventEventProperty(
                        method="method",
                        path="path",
                
                        # the properties below are optional
                        rest_api_id="restApiId"
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__31cdb34c93059c6355e5b545938269220da13fc651b40f6564346a207ee2fd8d)
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "properties": properties,
                "type": type,
            }

        @builtins.property
        def properties(
            self,
        ) -> typing.Union["CfnStateMachine.ApiEventProperty", "CfnStateMachine.CloudWatchEventEventProperty", "CfnStateMachine.EventBridgeRuleEventProperty", "CfnStateMachine.ScheduleEventProperty", _IResolvable_a771d0ef]:
            '''``CfnStateMachine.EventSourceProperty.Properties``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-types
            '''
            result = self._values.get("properties")
            assert result is not None, "Required property 'properties' is missing"
            return typing.cast(typing.Union["CfnStateMachine.ApiEventProperty", "CfnStateMachine.CloudWatchEventEventProperty", "CfnStateMachine.EventBridgeRuleEventProperty", "CfnStateMachine.ScheduleEventProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnStateMachine.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.FunctionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"function_name": "functionName"},
    )
    class FunctionSAMPTProperty:
        def __init__(self, *, function_name: builtins.str) -> None:
            '''
            :param function_name: ``CfnStateMachine.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                function_sAMPTProperty = sam.CfnStateMachine.FunctionSAMPTProperty(
                    function_name="functionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__52e7e889b7e2ea44115a1baddb54719b5ccf53e1257e5e6ab545bebef09f9463)
                check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "function_name": function_name,
            }

        @builtins.property
        def function_name(self) -> builtins.str:
            '''``CfnStateMachine.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("function_name")
            assert result is not None, "Required property 'function_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.IAMPolicyDocumentProperty",
        jsii_struct_bases=[],
        name_mapping={"statement": "statement", "version": "version"},
    )
    class IAMPolicyDocumentProperty:
        def __init__(self, *, statement: typing.Any, version: builtins.str) -> None:
            '''
            :param statement: ``CfnStateMachine.IAMPolicyDocumentProperty.Statement``.
            :param version: ``CfnStateMachine.IAMPolicyDocumentProperty.Version``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                # statement: Any
                
                i_aMPolicy_document_property = {
                    "statement": statement,
                    "version": "version"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b13e69a5b6a4d4b7ede5996edf77e7f2247fb74af351b33f4501b96f8f839e9)
                check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "statement": statement,
                "version": version,
            }

        @builtins.property
        def statement(self) -> typing.Any:
            '''``CfnStateMachine.IAMPolicyDocumentProperty.Statement``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            result = self._values.get("statement")
            assert result is not None, "Required property 'statement' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def version(self) -> builtins.str:
            '''``CfnStateMachine.IAMPolicyDocumentProperty.Version``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IAMPolicyDocumentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.LogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs_log_group": "cloudWatchLogsLogGroup"},
    )
    class LogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group: typing.Union[typing.Union["CfnStateMachine.CloudWatchLogsLogGroupProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param cloud_watch_logs_log_group: ``CfnStateMachine.LogDestinationProperty.CloudWatchLogsLogGroup``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html#cfn-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                log_destination_property = sam.CfnStateMachine.LogDestinationProperty(
                    cloud_watch_logs_log_group=sam.CfnStateMachine.CloudWatchLogsLogGroupProperty(
                        log_group_arn="logGroupArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7647230b6f50304a7ceda85cf1a565f99966b488a7ee409040d85a8f8db5483d)
                check_type(argname="argument cloud_watch_logs_log_group", value=cloud_watch_logs_log_group, expected_type=type_hints["cloud_watch_logs_log_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cloud_watch_logs_log_group": cloud_watch_logs_log_group,
            }

        @builtins.property
        def cloud_watch_logs_log_group(
            self,
        ) -> typing.Union["CfnStateMachine.CloudWatchLogsLogGroupProperty", _IResolvable_a771d0ef]:
            '''``CfnStateMachine.LogDestinationProperty.CloudWatchLogsLogGroup``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html#cfn-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup
            '''
            result = self._values.get("cloud_watch_logs_log_group")
            assert result is not None, "Required property 'cloud_watch_logs_log_group' is missing"
            return typing.cast(typing.Union["CfnStateMachine.CloudWatchLogsLogGroupProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destinations": "destinations",
            "include_execution_data": "includeExecutionData",
            "level": "level",
        },
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            destinations: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnStateMachine.LogDestinationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            include_execution_data: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            level: builtins.str,
        ) -> None:
            '''
            :param destinations: ``CfnStateMachine.LoggingConfigurationProperty.Destinations``.
            :param include_execution_data: ``CfnStateMachine.LoggingConfigurationProperty.IncludeExecutionData``.
            :param level: ``CfnStateMachine.LoggingConfigurationProperty.Level``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                logging_configuration_property = sam.CfnStateMachine.LoggingConfigurationProperty(
                    destinations=[sam.CfnStateMachine.LogDestinationProperty(
                        cloud_watch_logs_log_group=sam.CfnStateMachine.CloudWatchLogsLogGroupProperty(
                            log_group_arn="logGroupArn"
                        )
                    )],
                    include_execution_data=False,
                    level="level"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9394a19a79c6f80932de0dae180f7c0655d650bdfa30024947488cc50be70c2e)
                check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
                check_type(argname="argument include_execution_data", value=include_execution_data, expected_type=type_hints["include_execution_data"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destinations": destinations,
                "include_execution_data": include_execution_data,
                "level": level,
            }

        @builtins.property
        def destinations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStateMachine.LogDestinationProperty", _IResolvable_a771d0ef]]]:
            '''``CfnStateMachine.LoggingConfigurationProperty.Destinations``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            '''
            result = self._values.get("destinations")
            assert result is not None, "Required property 'destinations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStateMachine.LogDestinationProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def include_execution_data(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnStateMachine.LoggingConfigurationProperty.IncludeExecutionData``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            '''
            result = self._values.get("include_execution_data")
            assert result is not None, "Required property 'include_execution_data' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def level(self) -> builtins.str:
            '''``CfnStateMachine.LoggingConfigurationProperty.Level``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            '''
            result = self._values.get("level")
            assert result is not None, "Required property 'level' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: ``CfnStateMachine.S3LocationProperty.Bucket``.
            :param key: ``CfnStateMachine.S3LocationProperty.Key``.
            :param version: ``CfnStateMachine.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s3_location_property = sam.CfnStateMachine.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                
                    # the properties below are optional
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4155b9df3c5b781536b1680b03fd7fa43f056a49a9724fb3faafa9da7172aa87)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnStateMachine.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnStateMachine.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''``CfnStateMachine.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.SAMPolicyTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_invoke_policy": "lambdaInvokePolicy",
            "step_functions_execution_policy": "stepFunctionsExecutionPolicy",
        },
    )
    class SAMPolicyTemplateProperty:
        def __init__(
            self,
            *,
            lambda_invoke_policy: typing.Optional[typing.Union[typing.Union["CfnStateMachine.FunctionSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            step_functions_execution_policy: typing.Optional[typing.Union[typing.Union["CfnStateMachine.StateMachineSAMPTProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param lambda_invoke_policy: ``CfnStateMachine.SAMPolicyTemplateProperty.LambdaInvokePolicy``.
            :param step_functions_execution_policy: ``CfnStateMachine.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                s_aMPolicy_template_property = sam.CfnStateMachine.SAMPolicyTemplateProperty(
                    lambda_invoke_policy=sam.CfnStateMachine.FunctionSAMPTProperty(
                        function_name="functionName"
                    ),
                    step_functions_execution_policy=sam.CfnStateMachine.StateMachineSAMPTProperty(
                        state_machine_name="stateMachineName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__900d97ed7047a8926d5afdf95a530da25b5a17541730d6341bb925b834336194)
                check_type(argname="argument lambda_invoke_policy", value=lambda_invoke_policy, expected_type=type_hints["lambda_invoke_policy"])
                check_type(argname="argument step_functions_execution_policy", value=step_functions_execution_policy, expected_type=type_hints["step_functions_execution_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_invoke_policy is not None:
                self._values["lambda_invoke_policy"] = lambda_invoke_policy
            if step_functions_execution_policy is not None:
                self._values["step_functions_execution_policy"] = step_functions_execution_policy

        @builtins.property
        def lambda_invoke_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnStateMachine.FunctionSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnStateMachine.SAMPolicyTemplateProperty.LambdaInvokePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("lambda_invoke_policy")
            return typing.cast(typing.Optional[typing.Union["CfnStateMachine.FunctionSAMPTProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def step_functions_execution_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnStateMachine.StateMachineSAMPTProperty", _IResolvable_a771d0ef]]:
            '''``CfnStateMachine.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("step_functions_execution_policy")
            return typing.cast(typing.Optional[typing.Union["CfnStateMachine.StateMachineSAMPTProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAMPolicyTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.ScheduleEventProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule": "schedule", "input": "input"},
    )
    class ScheduleEventProperty:
        def __init__(
            self,
            *,
            schedule: builtins.str,
            input: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param schedule: ``CfnStateMachine.ScheduleEventProperty.Schedule``.
            :param input: ``CfnStateMachine.ScheduleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                schedule_event_property = sam.CfnStateMachine.ScheduleEventProperty(
                    schedule="schedule",
                
                    # the properties below are optional
                    input="input"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6692ae7dcfc8a332fcfc1f51c9546dfee12346baca761ea1181f597571701bf)
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "schedule": schedule,
            }
            if input is not None:
                self._values["input"] = input

        @builtins.property
        def schedule(self) -> builtins.str:
            '''``CfnStateMachine.ScheduleEventProperty.Schedule``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("schedule")
            assert result is not None, "Required property 'schedule' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.ScheduleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.StateMachineSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"state_machine_name": "stateMachineName"},
    )
    class StateMachineSAMPTProperty:
        def __init__(self, *, state_machine_name: builtins.str) -> None:
            '''
            :param state_machine_name: ``CfnStateMachine.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                state_machine_sAMPTProperty = sam.CfnStateMachine.StateMachineSAMPTProperty(
                    state_machine_name="stateMachineName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b62dacde000a760a0c2215db364a7b0571a4ecd661abe84c37da374d3aa5a9e)
                check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "state_machine_name": state_machine_name,
            }

        @builtins.property
        def state_machine_name(self) -> builtins.str:
            '''``CfnStateMachine.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("state_machine_name")
            assert result is not None, "Required property 'state_machine_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateMachineSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_sam.CfnStateMachine.TracingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class TracingConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnStateMachine.TracingConfigurationProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_sam as sam
                
                tracing_configuration_property = sam.CfnStateMachine.TracingConfigurationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa8430214daa5bfd3d59048144f188d3254406152a8bf8db1c31c606db29fc61)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnStateMachine.TracingConfigurationProperty.Enabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tracingconfiguration.html
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TracingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_sam.CfnStateMachineProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "definition_substitutions": "definitionSubstitutions",
        "definition_uri": "definitionUri",
        "events": "events",
        "logging": "logging",
        "name": "name",
        "permissions_boundaries": "permissionsBoundaries",
        "policies": "policies",
        "role": "role",
        "tags": "tags",
        "tracing": "tracing",
        "type": "type",
    },
)
class CfnStateMachineProps:
    def __init__(
        self,
        *,
        definition: typing.Any = None,
        definition_substitutions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnStateMachine.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnStateMachine.EventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        logging: typing.Optional[typing.Union[typing.Union[CfnStateMachine.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions_boundaries: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef, typing.Sequence[typing.Union[builtins.str, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing: typing.Optional[typing.Union[typing.Union[CfnStateMachine.TracingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnStateMachine``.

        :param definition: ``AWS::Serverless::StateMachine.Definition``.
        :param definition_substitutions: ``AWS::Serverless::StateMachine.DefinitionSubstitutions``.
        :param definition_uri: ``AWS::Serverless::StateMachine.DefinitionUri``.
        :param events: ``AWS::Serverless::StateMachine.Events``.
        :param logging: ``AWS::Serverless::StateMachine.Logging``.
        :param name: ``AWS::Serverless::StateMachine.Name``.
        :param permissions_boundaries: ``AWS::Serverless::StateMachine.PermissionsBoundaries``.
        :param policies: ``AWS::Serverless::StateMachine.Policies``.
        :param role: ``AWS::Serverless::StateMachine.Role``.
        :param tags: ``AWS::Serverless::StateMachine.Tags``.
        :param tracing: ``AWS::Serverless::StateMachine.Tracing``.
        :param type: ``AWS::Serverless::StateMachine.Type``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sam as sam
            
            # definition: Any
            
            cfn_state_machine_props = sam.CfnStateMachineProps(
                definition=definition,
                definition_substitutions={
                    "definition_substitutions_key": "definitionSubstitutions"
                },
                definition_uri="definitionUri",
                events={
                    "events_key": sam.CfnStateMachine.EventSourceProperty(
                        properties=sam.CfnStateMachine.CloudWatchEventEventProperty(
                            method="method",
                            path="path",
            
                            # the properties below are optional
                            rest_api_id="restApiId"
                        ),
                        type="type"
                    )
                },
                logging=sam.CfnStateMachine.LoggingConfigurationProperty(
                    destinations=[sam.CfnStateMachine.LogDestinationProperty(
                        cloud_watch_logs_log_group=sam.CfnStateMachine.CloudWatchLogsLogGroupProperty(
                            log_group_arn="logGroupArn"
                        )
                    )],
                    include_execution_data=False,
                    level="level"
                ),
                name="name",
                permissions_boundaries="permissionsBoundaries",
                policies="policies",
                role="role",
                tags={
                    "tags_key": "tags"
                },
                tracing=sam.CfnStateMachine.TracingConfigurationProperty(
                    enabled=False
                ),
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80311e231e4568de61f027208a83dac0d2246d793c7508ae6f6307a984d79fb2)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument definition_substitutions", value=definition_substitutions, expected_type=type_hints["definition_substitutions"])
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions_boundaries", value=permissions_boundaries, expected_type=type_hints["permissions_boundaries"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if definition is not None:
            self._values["definition"] = definition
        if definition_substitutions is not None:
            self._values["definition_substitutions"] = definition_substitutions
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if events is not None:
            self._values["events"] = events
        if logging is not None:
            self._values["logging"] = logging
        if name is not None:
            self._values["name"] = name
        if permissions_boundaries is not None:
            self._values["permissions_boundaries"] = permissions_boundaries
        if policies is not None:
            self._values["policies"] = policies
        if role is not None:
            self._values["role"] = role
        if tags is not None:
            self._values["tags"] = tags
        if tracing is not None:
            self._values["tracing"] = tracing
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def definition(self) -> typing.Any:
        '''``AWS::Serverless::StateMachine.Definition``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_substitutions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::StateMachine.DefinitionSubstitutions``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("definition_substitutions")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnStateMachine.S3LocationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::StateMachine.DefinitionUri``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnStateMachine.S3LocationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnStateMachine.EventSourceProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Serverless::StateMachine.Events``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnStateMachine.EventSourceProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[CfnStateMachine.LoggingConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::StateMachine.Logging``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[CfnStateMachine.LoggingConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Name``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundaries(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.PermissionsBoundaries``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html#sam-statemachine-permissionsboundary
        '''
        result = self._values.get("permissions_boundaries")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, CfnStateMachine.SAMPolicyTemplateProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Serverless::StateMachine.Policies``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, CfnStateMachine.SAMPolicyTemplateProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Role``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::StateMachine.Tags``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tracing(
        self,
    ) -> typing.Optional[typing.Union[CfnStateMachine.TracingConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Serverless::StateMachine.Tracing``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html#sam-statemachine-tracing
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[typing.Union[CfnStateMachine.TracingConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Type``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApi",
    "CfnApiProps",
    "CfnApplication",
    "CfnApplicationProps",
    "CfnFunction",
    "CfnFunctionProps",
    "CfnHttpApi",
    "CfnHttpApiProps",
    "CfnLayerVersion",
    "CfnLayerVersionProps",
    "CfnSimpleTable",
    "CfnSimpleTableProps",
    "CfnStateMachine",
    "CfnStateMachineProps",
]

publication.publish()

def _typecheckingstub__d335580439b2be96b6739327fa014ceb07f1e8a3e2b5336958a004f4356a9c0a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    stage_name: builtins.str,
    access_log_setting: typing.Optional[typing.Union[typing.Union[CfnApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    auth: typing.Optional[typing.Union[typing.Union[CfnApi.AuthProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    cache_cluster_size: typing.Optional[builtins.str] = None,
    canary_setting: typing.Optional[typing.Union[typing.Union[CfnApi.CanarySettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cors: typing.Optional[typing.Union[builtins.str, typing.Union[CfnApi.CorsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    definition_body: typing.Any = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    domain: typing.Optional[typing.Union[typing.Union[CfnApi.DomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    endpoint_configuration: typing.Optional[typing.Union[builtins.str, typing.Union[CfnApi.EndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    gateway_responses: typing.Any = None,
    method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_a771d0ef]] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    models: typing.Any = None,
    name: typing.Optional[builtins.str] = None,
    open_api_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599e37cc9f0b898583181cb5e3c590ec879259471ad4a4ad7485a0354da7e130(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7a54026d53491b3a9f3b7ce470eedd1a095c55bf1b5e2b889200bb0c3c720d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a311296130c0aaa489a0b107cabf03aa7536b7a1ba38852c587ab82a4782d1ab(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a835ed5badbf94a7491f74fa3debc004afe21892bef705c066632f467cb342(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea5de8ac34b118315e689d139eca91cba2d4e9673d110822451218448f812fe(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55aa4934945655485cc2b7868d00ec4fcad6e1e5929fdb6cf522246f8b08170c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9baae6f1fa6931f3806e1c4d83a6c1314e1bc7d0c3d7ef981d168adef46efb3f(
    value: typing.Optional[typing.Union[CfnApi.AccessLogSettingProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a509f93a43137b3d78d240835dbe09b3a32e1e689665db3a5d793ad524627347(
    value: typing.Optional[typing.Union[CfnApi.AuthProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6968388745dbc358c2ed9ef87e6c806ce847c391a3ed212e4cb8744ecff4cd(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26576406457c4387225108951ff87ea49c0a2adc5194bbbd1095b88e01a40dd(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d67fb7fe4bd03c8bffa3a932ff5928fec3b6cd37aac618cbf3d9a8a4b69286(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c283bcd8c826280aaa07c8827f3ab44b562a4202c68e8ac08ece8be25601e8df(
    value: typing.Optional[typing.Union[CfnApi.CanarySettingProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf7631e195781ecf396795a9ebdc478d3a81125bfb22c3de1d3ddb876a55a02(
    value: typing.Optional[typing.Union[builtins.str, CfnApi.CorsConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7ed62f63ed9152ae2ac81e4f1c9423100b0ad8c2369be869cfa550ebf74431(
    value: typing.Optional[typing.Union[builtins.str, CfnApi.S3LocationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7e87f0a766e830ba1078dbe9a867b14d26bc19e6cef4ebb791ccbd69c3387d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abdc627cc7739ccbd2adbeb03cf55b6312cded59c672d96d179bbe161c601c0(
    value: typing.Optional[typing.Union[CfnApi.DomainConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b432cfef1b40e146c6759ba2d948aa980ac4f5b55420b2177c26131f2de51e2(
    value: typing.Optional[typing.Union[builtins.str, CfnApi.EndpointConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a997e2cb1239fc2f833d20acb1f2b61edbdc00232a55c840dbb561910e6a3b89(
    value: typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bcacc949c68bcdccbbd16ab1ff46e84d7fb6e68152c0ff8ec8c4903859de4c(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8064bae7c53341f04ffd95e911e57d020bb57ab1172f4f9a3bece47c8a6385(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091f9b9754b8fd289b004c55e21a03a3bb150b9e616d48b3e96a8b64e0b896f4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0707e368c9b45be13971289c3fb51db0d8fc0fb36f6dac387a251ee2d9599e3d(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cfa5503c330e2143ad6b91761b656b2e541538a510912704db7d6350c9211b(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fd6cfc9b13d3412afe13981524f5ddb575bc1450eb5d384df0607e078ce87c(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80f1d235e5871d0bf3254e0466b4857fbdee758bbb96838a3774a33f9a33284(
    *,
    add_default_authorizer_to_cors_preflight: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    authorizers: typing.Any = None,
    default_authorizer: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90803c6a90da1622ea8804fee25a6d4ffb0f08bf5c0ae66e21ca3fd6cb4688c1(
    *,
    deployment_id: typing.Optional[builtins.str] = None,
    percent_traffic: typing.Optional[jsii.Number] = None,
    stage_variable_overrides: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    use_stage_cache: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33c10e79774a3454838e6e5a5f9f99fd894e3e9d829cc8cc6afb8b66a912ec4(
    *,
    allow_origin: builtins.str,
    allow_credentials: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    allow_headers: typing.Optional[builtins.str] = None,
    allow_methods: typing.Optional[builtins.str] = None,
    max_age: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b7a68f7c676c2aa3d43136780d961b44db8f0f647dec485730b4f44a40d187(
    *,
    certificate_arn: builtins.str,
    domain_name: builtins.str,
    base_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    endpoint_configuration: typing.Optional[builtins.str] = None,
    mutual_tls_authentication: typing.Optional[typing.Union[typing.Union[CfnApi.MutualTlsAuthenticationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ownership_verification_certificate_arn: typing.Optional[builtins.str] = None,
    route53: typing.Optional[typing.Union[typing.Union[CfnApi.Route53ConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    security_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6a6fc1266becaea79c116e24134e07f3d9a2b7f41bf971d23eb382e847e55a(
    *,
    type: typing.Optional[builtins.str] = None,
    vpc_endpoint_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d6477d62bdd979ffe7878b5a7a317c990ed4621773d918a6e6c1da373af72fc(
    *,
    truststore_uri: typing.Optional[builtins.str] = None,
    truststore_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe3511583218c761d12aeabdb8c65c92f14917564e966bf7159fcbe3d7b6956(
    *,
    distributed_domain_name: typing.Optional[builtins.str] = None,
    evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    hosted_zone_name: typing.Optional[builtins.str] = None,
    ip_v6: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891165367931c3c6b349c85239a964e708cd75b86160dc7cb7e19c74559572a4(
    *,
    bucket: builtins.str,
    key: builtins.str,
    version: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7eb533facf31131a127d9d307a95eb6aa4dd79e860550198f9dc8dde110133(
    *,
    stage_name: builtins.str,
    access_log_setting: typing.Optional[typing.Union[typing.Union[CfnApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    auth: typing.Optional[typing.Union[typing.Union[CfnApi.AuthProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    cache_cluster_size: typing.Optional[builtins.str] = None,
    canary_setting: typing.Optional[typing.Union[typing.Union[CfnApi.CanarySettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cors: typing.Optional[typing.Union[builtins.str, typing.Union[CfnApi.CorsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    definition_body: typing.Any = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    domain: typing.Optional[typing.Union[typing.Union[CfnApi.DomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    endpoint_configuration: typing.Optional[typing.Union[builtins.str, typing.Union[CfnApi.EndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    gateway_responses: typing.Any = None,
    method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_a771d0ef]] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    models: typing.Any = None,
    name: typing.Optional[builtins.str] = None,
    open_api_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e391f6e060fd4265ded810eaa6d5fa75a8893d957b8d3d42c360f5d5188bda0a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    location: typing.Union[builtins.str, typing.Union[CfnApplication.ApplicationLocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ba6853b05b0e3295f8df18d55b56fbeb194338450ec4a66a0f85419bd7aae0(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe091b2dd8b63bb3489cb00a4b31286a2c607f4d1297170cb83a9fde9d10b16(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7f648169f50a5b84af67e5b83167efc28457190510099ea093d81740db52c7(
    value: typing.Union[builtins.str, CfnApplication.ApplicationLocationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45542ebea6247b01691ff27d7fa164c8d0c244846034beff30254651aadcb21e(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0359fb53a9fdd4f16ee731485f8901e11dc89bb98d01103313e6a5efcf61624b(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e434a496a1676f20e55f92cf9bcea893a5e84f1287e7323b79a0bb7a153b5b75(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475d934ea3b3aac2469b7bbb982cc0c2d630261ef3f81be745d9224ecfb3f331(
    *,
    application_id: builtins.str,
    semantic_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15e85ab5ce25f0c53a2cf55d1edf0649c0f83c03f775da6a2945d1ba1efb8b0(
    *,
    location: typing.Union[builtins.str, typing.Union[CfnApplication.ApplicationLocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0de068acf685722560ef730ee4ff2068f39bb26acda2f602b73a5de06853743(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    assume_role_policy_document: typing.Any = None,
    auto_publish_alias: typing.Optional[builtins.str] = None,
    auto_publish_code_sha256: typing.Optional[builtins.str] = None,
    code_signing_config_arn: typing.Optional[builtins.str] = None,
    code_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnFunction.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dead_letter_queue: typing.Optional[typing.Union[typing.Union[CfnFunction.DeadLetterQueueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    deployment_preference: typing.Optional[typing.Union[typing.Union[CfnFunction.DeploymentPreferenceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[typing.Union[CfnFunction.FunctionEnvironmentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    event_invoke_config: typing.Optional[typing.Union[typing.Union[CfnFunction.EventInvokeConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnFunction.EventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    file_system_configs: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFunction.FileSystemConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    function_name: typing.Optional[builtins.str] = None,
    handler: typing.Optional[builtins.str] = None,
    image_config: typing.Optional[typing.Union[typing.Union[CfnFunction.ImageConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    inline_code: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    layers: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    package_type: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[builtins.str, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef, typing.Sequence[typing.Union[builtins.str, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    provisioned_concurrency_config: typing.Optional[typing.Union[typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    tracing: typing.Optional[builtins.str] = None,
    version_description: typing.Optional[builtins.str] = None,
    vpc_config: typing.Optional[typing.Union[typing.Union[CfnFunction.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e12a05469b93683a5f9531392ce66303e6c17d75e57f2f7658e7f5e776c3e8(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b68051667412141943a3bb2a7ac0192c89299775ec6889d9a1768274e2414ff(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375a12290ea6a1d63cc5a5cd0342a6885b337b5dd379801c28e3035d1d1fbbad(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804275fc6da7514ecdac419882f2fef9a024d6e1d8895fa5dd54fe69da1f71db(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1991c5255aaad02611e8bedc1c8c2630a4d79c53875681aea075e4371391f5a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d9afbfaecc38c523a20fd85a1db54f16430f710f70a360532b65bb1f08e0cf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a711c21d186a725f05bd0413466740097825e43d4bdd018d3e53fb9c2dc610(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19dfe64e8a3347aed5bc2299b53c7bd2897871d4a646bfc6b7f0a106133b4c5(
    value: typing.Optional[typing.Union[builtins.str, CfnFunction.S3LocationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e119b59cd6d479aa69e5c52e781ea7676c97f3e3de3155de930aa9f991fd96d1(
    value: typing.Optional[typing.Union[CfnFunction.DeadLetterQueueProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a85f4e49e2f14ccf2f87b3fc9b627f69774ccc7891831d66c18517c443cb270(
    value: typing.Optional[typing.Union[CfnFunction.DeploymentPreferenceProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7494b2253e36226f39ddc446bd11ed5fd8c29090148170bbddd551c249784c5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b02434c1938c553c5da9bbe591e782f909ac2ee738fb60454ce5ca3c38c273(
    value: typing.Optional[typing.Union[CfnFunction.FunctionEnvironmentProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be023c816fc0668bda8c01cbcf330c514b85a3661f68eaecf6d2e56c94a189a2(
    value: typing.Optional[typing.Union[CfnFunction.EventInvokeConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db239217b9a2443dc9d9350daffc0f690256e2daa2b4edfe8e0b330eec55ec49(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnFunction.EventSourceProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701d77cb40ebcfeaeaf68383cdd250a6a81ff6b1bbeb35056602056c77bc0c5e(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFunction.FileSystemConfigProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5567c9f81687721aa7f6c56ed2406db4357288a7abffb019aedbbebfafb5ae(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f3e4f69582686f638a74b50e9ce063581a1776db0c07c05f7fd39bb4becc57(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377a1c2f1f0d78eefde5673d2e91399d440afcd850c8e527f5a55b2922f12c8c(
    value: typing.Optional[typing.Union[CfnFunction.ImageConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373f070366098e1c79b4e5b51746473f50a0061473ad7f20c8f9363644c77885(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe7fe7e959912ca8a56a9559b7432fdc9e681cbd25f66163b5e505613987c52(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48864df81d24b13a6a8203001089c190adae74b9771418407b3d45ce93de386(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018472eb15e47b9349b6acb0048fe63db14477badd1289d3f0ff97ab426c532f(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518b7770acda94ce3f04ba56d322586e9250bcd5d65fa7d1c30c019fdf49ca61(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48db0d17bdb739c2f462f00a940c910e4ba4a03913877f8495ce709167d9cac(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e630fe0f30a4505f0ca3a54d558d69661b469aea8d7b1d91730c73462b854cdc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f3c6c961e23ba32c743496e32aed532d9a9f1bec87d22b6a28b2c136158451(
    value: typing.Optional[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, CfnFunction.SAMPolicyTemplateProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89ee2cb8bde087ab40ecd2282d8780671c26576117d2ab6556a197de94d34eb(
    value: typing.Optional[typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1be95e48307dab1757f159e46ac4bdfb0c23d9332c0c03655d42f37b32fd8c(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebab6fd8f10a58329519b09eb2d52a1fbe304ff28dc2ce852574def51a5bf0d8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ffeb4aa04c9a78b83a16b4c52bb3a08d40437baa39328b925fcd9e535252b8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf59ecf8b986eb5768efac087337f966cf3e400e67f759f4fd2f4d316f00878c(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf88c1925f2553a764c9fceb65343ce9672135350d771ef7cb6526beda99af3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10da312f626a7017a11eea94a16d491c4a06dc796fd47c2fe4cc183d1314c1fc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6defe318c0cef4d532cf2a1dec729a806c163d7589fec000b097257352b210(
    value: typing.Optional[typing.Union[CfnFunction.VpcConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7df05c26bf2d41d501512f754453c47c9702b430e9d9a4cae86e5491cc32be(
    *,
    variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ab38ee5864bebb8cb1499634450e772d4c5416aa150d1c2a536c700192dad9(
    *,
    method: builtins.str,
    path: builtins.str,
    auth: typing.Optional[typing.Union[typing.Union[CfnFunction.AuthProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    request_model: typing.Optional[typing.Union[typing.Union[CfnFunction.RequestModelProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    request_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[builtins.str, typing.Union[CfnFunction.RequestParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c534500bb3f39e60558efb77528ec3b161f64dbaa91ff1ee304d4d0c96b234c5(
    *,
    api_key_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    authorizer: typing.Optional[builtins.str] = None,
    resource_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.AuthResourcePolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c1fa1f37de885add91037ec07163a77c8cbdbd40f0b7799b22d44133a7a8ad(
    *,
    aws_account_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    aws_account_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_statements: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_a771d0ef]] = None,
    intrinsic_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    intrinsic_vpce_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    intrinsic_vpce_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    intrinsic_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_range_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_range_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6cc77d8345ad124348a1a1b1f59474e377a0c721e0dca532acade7d18097a1(
    *,
    bucket_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1adf6783f3a17e48227575af8e4f52a2a73165a8a8383ddc167d379dfaa6f4(
    *,
    pattern: typing.Any,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2943ed1df7fdbfc76cbecefb386bf6fe4281986e4406a33b157de638c464e6b(
    *,
    filter_pattern: builtins.str,
    log_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a722d45eb35303595002dea40acebe21f27a4a78b02a373806d2edcf79ff5ae(
    *,
    collection_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9621a4710099a7ee6a6aff484ed86576d597341996d5b2342f67c28ff5e00d(
    *,
    target_arn: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ed46c5ebbd769808717492c1986de9da633e053265e65a470ca1abf8e972c1(
    *,
    enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    type: builtins.str,
    alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
    hooks: typing.Optional[typing.Union[typing.Union[CfnFunction.HooksProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad528993e60b85172808cfbd39ff1ae91cf5791b5be958de66e3d73c9d7262fc(
    *,
    on_failure: typing.Union[typing.Union[CfnFunction.DestinationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3075edb20a46edbf9e5c848415719c2fb409c26085d7d49ae8f9839b7b9f48d(
    *,
    destination: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7c9fcb29aa8589419e9a8986d540e9f09e79b505427984ab72821be3e8f7fd(
    *,
    domain_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71bd9ca43af2cdbb04cbe8bf9a32728e966d77b67ff70f10f4d7998aebbcbc0(
    *,
    starting_position: builtins.str,
    stream: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    destination_config: typing.Optional[typing.Union[typing.Union[CfnFunction.DestinationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30d870ab1ae35a9ed02e4d6b319250cdc4bfe14c413a3ac88c0ffdff5026d18(
    *,
    pattern: typing.Any,
    event_bus_name: typing.Optional[builtins.str] = None,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f95edaebe61be780428f489b76fb5fc9f40a224066d242676cffa7772c149b(
    *,
    destination_config: typing.Optional[typing.Union[typing.Union[CfnFunction.EventInvokeDestinationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c7f8d2257400f6650cd91dd60b0f27ffeb5c6e37dfdbc3f0629b8b2ecf29d0(
    *,
    on_failure: typing.Union[typing.Union[CfnFunction.DestinationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    on_success: typing.Union[typing.Union[CfnFunction.DestinationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea52d536f6a79bb2a00a85d54edbc2e6745cacf6a7249113ff29084f28d29762(
    *,
    properties: typing.Union[typing.Union[CfnFunction.AlexaSkillEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.ApiEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.CloudWatchEventEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.CloudWatchLogsEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.DynamoDBEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.EventBridgeRuleEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.IoTRuleEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.KinesisEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.S3EventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.SNSEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.SQSEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.ScheduleEventProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a61ec2c7bb73b664df38f125555576bb30fc2268956b8e0969fd943615c2cbe(
    *,
    arn: typing.Optional[builtins.str] = None,
    local_mount_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ddecf71d5b106da79c787c3b30275499ddf30459d7c840f702fb238d4acbac(
    *,
    variables: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c23fab1970d3079a076a370635a9d09cc06d56d15b3ffb02d3d9bb2a798041(
    *,
    function_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c3f0667e75b9bc2c45dc4e7d6b2ee2a6138e392041c355eeda88d18a8384e4(
    *,
    post_traffic: typing.Optional[builtins.str] = None,
    pre_traffic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bdf32f1b1e8a4a536505b65dbe578e887bf27c908cd5386ba85b7b044a64b2(
    *,
    statement: typing.Any,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3cedf8c3360513df2b0f3ba2b39bdcfb7904eddac0008c5b37d016f9aa5fd7a(
    *,
    identity_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232ecaef435e6878fe68947f571bfbfeb4694b29e759635268d752bab436026b(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f16a8c649ec5f9e447c10019acecaddd129ad45a6a45040c3f73488fbdfebc9(
    *,
    sql: builtins.str,
    aws_iot_sql_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670a3f3d405a39c92fea391f7fbaafb3c7217bacdbed026b6acd8b0c7a4c63df(
    *,
    key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2f39bca540600fcb83759b376489168b314d5b654bde65e559a34cea6b0888(
    *,
    starting_position: builtins.str,
    stream: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57bf8c40ca26e976ae703c815e0d5d6eb912f82ef63469a4308c8c05f404ac44(
    *,
    log_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bff9afa411607f2d768f5cc6afc724b84626eae4b65660aac9c9b3fccbbdb7f(
    *,
    parameter_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b794589fea6427a02b47c345278125621d90ba663013f08e28f70242b80e9e(
    *,
    provisioned_concurrent_executions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6637cb5af07936531c635c412fa5b51265ff073e4e6562ff60c01fc5b8742707(
    *,
    queue_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527081aabc5dbbac6ee5b0777ec3a39fbd25365ab15b8a774be3307b0ef69331(
    *,
    model: builtins.str,
    required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    validate_body: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    validate_parameters: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4808a4ac5d444e4da34872ad607e0cdd2a0f8a3e405e424b9b772e788e9d283f(
    *,
    caching: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f152fab2b6a730c21df47b3710b913f9ca0fa433e1075487890918ca9a32a6ff(
    *,
    bucket: builtins.str,
    events: typing.Union[builtins.str, _IResolvable_a771d0ef, typing.Sequence[builtins.str]],
    filter: typing.Optional[typing.Union[typing.Union[CfnFunction.S3NotificationFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e114dc8f885e4ab5d9b9cddc2cfc1a732a2171a49e831cb57afc990b05b9fb(
    *,
    rules: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFunction.S3KeyFilterRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5981d9f68fe76f0220b2be9cecfd3031b29e6055b56a0364a7e687399d56ed8d(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3045e650e513ab46e5c8cc7b2aa7eaace1c14468e6dda188d6ab7a9daad01cbf(
    *,
    bucket: builtins.str,
    key: builtins.str,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1087f415a49886c06d99add9e196924788ac0b29dbd089ade319d2ac539e2e35(
    *,
    s3_key: typing.Union[typing.Union[CfnFunction.S3KeyFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f818379b2f41b3e45a592087f1d682e06e83c6c10d2ca331a0a7209e534c729(
    *,
    ami_describe_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    aws_secrets_manager_get_secret_value_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.SecretArnSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cloud_formation_describe_stacks_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cloud_watch_put_metric_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dynamo_db_crud_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.TableSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dynamo_db_read_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.TableSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dynamo_db_stream_read_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.TableStreamSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dynamo_db_write_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.TableSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ec2_describe_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    elasticsearch_http_post_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.DomainSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    filter_log_events_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.LogGroupSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_crud_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.StreamSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_stream_read_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.StreamSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kms_decrypt_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.KeySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    lambda_invoke_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.FunctionSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    rekognition_detect_only_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    rekognition_labels_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    rekognition_no_data_access_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.CollectionSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    rekognition_read_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.CollectionSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    rekognition_write_only_access_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.CollectionSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    s3_crud_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.BucketSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    s3_read_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.BucketSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    s3_write_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.BucketSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ses_bulk_templated_crud_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.IdentitySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ses_crud_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.IdentitySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ses_email_template_crud_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ses_send_bounce_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.IdentitySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sns_crud_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.TopicSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sns_publish_message_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.TopicSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sqs_poller_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.QueueSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sqs_send_message_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.QueueSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ssm_parameter_read_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.ParameterNameSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    step_functions_execution_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.StateMachineSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    vpc_access_policy: typing.Optional[typing.Union[typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e105fcb25392badbc729d3a8382809a14713d54d9fd75f4b75716b7e804f1b19(
    *,
    topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596cf9e3422e5ea0dd247e44e4068e9f0fc2925fc7e5f35683c9215878343004(
    *,
    queue: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0120579ea2c654e37a7bb81cb13416de265beb4c07976cff5edae031ee76e994(
    *,
    schedule: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    input: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff72985ffaf6a1cf38ac2cef403c54fefd6c7d084ae3f5f2c890b709e749589(
    *,
    secret_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b5e5c2c25ff1b829ff00639fa4ca49a5a7f9892d0cab9380abdc66796a2601(
    *,
    state_machine_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500797e41a4ad71c1d4c15d245e70caddf9578565e3078ba2629ef04bb6a0e51(
    *,
    stream_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dde8a927b347c63b74b3d2be8c98295198e1f321cd62fcf1df4cbbe730849d1(
    *,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a16f56f3ae85cc6db5aca5a8978363a8f92dcf1dd950a159e5cec6b3897bc0a(
    *,
    stream_name: builtins.str,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1977a80f2c3a568e7fddc8854834b5f4d012f0060364531a1df65cfc67e37b1b(
    *,
    topic_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043a5c7053a5d62211a19843451af327cf2033b2fdb160b805adb5ed3a1b726f(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnet_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b941aecdc76dca88e7aa52761ece48d840c2b00504960660dfc97c3340c3fdec(
    *,
    architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    assume_role_policy_document: typing.Any = None,
    auto_publish_alias: typing.Optional[builtins.str] = None,
    auto_publish_code_sha256: typing.Optional[builtins.str] = None,
    code_signing_config_arn: typing.Optional[builtins.str] = None,
    code_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnFunction.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dead_letter_queue: typing.Optional[typing.Union[typing.Union[CfnFunction.DeadLetterQueueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    deployment_preference: typing.Optional[typing.Union[typing.Union[CfnFunction.DeploymentPreferenceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[typing.Union[CfnFunction.FunctionEnvironmentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    event_invoke_config: typing.Optional[typing.Union[typing.Union[CfnFunction.EventInvokeConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnFunction.EventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    file_system_configs: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFunction.FileSystemConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    function_name: typing.Optional[builtins.str] = None,
    handler: typing.Optional[builtins.str] = None,
    image_config: typing.Optional[typing.Union[typing.Union[CfnFunction.ImageConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    inline_code: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    layers: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    package_type: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[builtins.str, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef, typing.Sequence[typing.Union[builtins.str, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    provisioned_concurrency_config: typing.Optional[typing.Union[typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    tracing: typing.Optional[builtins.str] = None,
    version_description: typing.Optional[builtins.str] = None,
    vpc_config: typing.Optional[typing.Union[typing.Union[CfnFunction.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa411e01d6f778480833823e15735ca25e6c504034269114833c9ede4a91f793(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    access_log_setting: typing.Optional[typing.Union[typing.Union[CfnHttpApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    auth: typing.Optional[typing.Union[typing.Union[CfnHttpApi.HttpApiAuthProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cors_configuration: typing.Optional[typing.Union[builtins.bool, typing.Union[CfnHttpApi.CorsConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default_route_settings: typing.Optional[typing.Union[typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    definition_body: typing.Any = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnHttpApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    domain: typing.Optional[typing.Union[typing.Union[CfnHttpApi.HttpApiDomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    route_settings: typing.Optional[typing.Union[typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stage_name: typing.Optional[builtins.str] = None,
    stage_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6886d79181036dd31ae97b82804a3d16e2c5e78427ee5b1b13f0674123d95027(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6d5fceb7fd25fd6dfe9c0993cacacf85da75f54399f68a5e75a0d50f7e9948(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f716a57d72cc5d708ef2a675264e5e950b1c58b0d9a728ca4675d45840d41ce(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed21829d9947e92445298a702d845a10b7c2e3f1ba938c5d0314ccc96a2d61e8(
    value: typing.Optional[typing.Union[CfnHttpApi.AccessLogSettingProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1511b652cc6e4c48460c8eb538d3930e04246822b874e2dce1d3745e5f71a7c(
    value: typing.Optional[typing.Union[CfnHttpApi.HttpApiAuthProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66059a9ea73a2046b9491850fd60e7278e1871a43514a4a9fa339ab2157679d(
    value: typing.Optional[typing.Union[builtins.bool, CfnHttpApi.CorsConfigurationObjectProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62e8b6936488580a3663d80dff4572681025aa8fddb7b068050a1e0c9be617a(
    value: typing.Optional[typing.Union[CfnHttpApi.RouteSettingsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea0e9d7f4bf5ffa369ae58f3ce273cf2e859bc897406e83de8af76970500ae8(
    value: typing.Optional[typing.Union[builtins.str, CfnHttpApi.S3LocationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfecb38222254b2fa0d1c29fcd691fb9b0d727082ed13a8f0ba6405dd342b9a7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98665acacadba691cc71fb95891fcf43748d2b33e3297f10c184d14c38c132b5(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930c1cef7d89795a70d6197f4ebe1ec4d3a1ddbe0e27917e41cf149fb092e953(
    value: typing.Optional[typing.Union[CfnHttpApi.HttpApiDomainConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e1095fdf65eccde40910464056400475ae2e95854dd7ad1d86c6ad121cd438(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88d4ff97b0401e0229cbe78b6f3fb8cb0dc0a4a4415c1eb2f5ee41ee86136fa(
    value: typing.Optional[typing.Union[CfnHttpApi.RouteSettingsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e714a934d23cae1c5398836c8ffa6b9cffb2061790d90790a735156010ffbc7c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd02bcccb457b1b113468c76500e5e2c1ee07f7124ab8fa68557580bc7dda61(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dad4a8088a9148e5f5fa0ea961af819c0ffda34a3215a756b1acb3dca152172(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e31f5a654409fd70ef66a72719eea79042efda9e9638b13959d8491bf5a126(
    *,
    allow_credentials: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_age: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a86596b352487f89c525f791c68cbe025b53e26ae84f933d3e8bdf93890670(
    *,
    authorizers: typing.Any = None,
    default_authorizer: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b199fc60d229a44bf29ace65240e9ab15b093f42646e5c5a8abe1e44fde8e1cd(
    *,
    certificate_arn: builtins.str,
    domain_name: builtins.str,
    base_path: typing.Optional[builtins.str] = None,
    endpoint_configuration: typing.Optional[builtins.str] = None,
    mutual_tls_authentication: typing.Optional[typing.Union[typing.Union[CfnHttpApi.MutualTlsAuthenticationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    route53: typing.Optional[typing.Union[typing.Union[CfnHttpApi.Route53ConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    security_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbe6b7ec59fd65ed1d4807e7497231a6c1f376026f290932f82b02ce818bd6e(
    *,
    truststore_uri: typing.Optional[builtins.str] = None,
    truststore_version: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e07d70bf7a7dc668a1a657f1b794d64732cfa45204ec84297fc27a3dfb4e31d(
    *,
    distributed_domain_name: typing.Optional[builtins.str] = None,
    evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    hosted_zone_name: typing.Optional[builtins.str] = None,
    ip_v6: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c470fee9a95389a07991e47206b0f93fc029de7d632375269557f84e11fe5ebf(
    *,
    data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    logging_level: typing.Optional[builtins.str] = None,
    throttling_burst_limit: typing.Optional[jsii.Number] = None,
    throttling_rate_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230a3845c48f75035abe656bccaf360b24fe16b1264ce6b5c703f27803ba694b(
    *,
    bucket: builtins.str,
    key: builtins.str,
    version: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2b433bf42e48d668ae6e9a2311b15e7e56d8122e2976fefded5e15bb97c10d(
    *,
    access_log_setting: typing.Optional[typing.Union[typing.Union[CfnHttpApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    auth: typing.Optional[typing.Union[typing.Union[CfnHttpApi.HttpApiAuthProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cors_configuration: typing.Optional[typing.Union[builtins.bool, typing.Union[CfnHttpApi.CorsConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default_route_settings: typing.Optional[typing.Union[typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    definition_body: typing.Any = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnHttpApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    domain: typing.Optional[typing.Union[typing.Union[CfnHttpApi.HttpApiDomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    route_settings: typing.Optional[typing.Union[typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stage_name: typing.Optional[builtins.str] = None,
    stage_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b6f04ed630f026d1734622d5cc0611ac0426a3f336979a0b71887ad86ee023(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnLayerVersion.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    layer_name: typing.Optional[builtins.str] = None,
    license_info: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57aee27769c12f67ea279db56364a802378867a2330bb5d56b86ef90fa624ed(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83693e2df7267062d72e9c94d16092495ec930ee2ca168f435f0f61c7de5b65f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfcc02ce98180060e8b7f66e34c9f926075d3825d38ed0960d6903e62a050c97(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b453a6454c1eda610298aad694ae21322a6aa6e05a49bb0f344baefc483a9030(
    value: typing.Optional[typing.Union[builtins.str, CfnLayerVersion.S3LocationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d68189436f9b0d210a08d61a3825b5d4dedacc07abdddd3ffa119d46058163(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a75d064fe11d7e462efbc3d00da1078c3e19e248052ecbc72f3709be5090eaa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b596565df284c23053142763389419202c17a44c7121b4454175b56c5f134878(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e3b80f431b7cdeae00d85a8972746955695df6b9589698d9b5e83207fc7381(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9772b9ebbe1caf9d00a3636b7e71d9cf78b74056dcc80b8485f5c65f74f9eb2(
    *,
    bucket: builtins.str,
    key: builtins.str,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc739a3bfb10e84da9ff4deea2213e663e0a9dc646e4fbb7ce13b214e32fdae(
    *,
    compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnLayerVersion.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    layer_name: typing.Optional[builtins.str] = None,
    license_info: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44d23bbd962691797648c10128ff0090ac41bfa06558cdbc76920ea818bfc7a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    primary_key: typing.Optional[typing.Union[typing.Union[CfnSimpleTable.PrimaryKeyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    provisioned_throughput: typing.Optional[typing.Union[typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sse_specification: typing.Optional[typing.Union[typing.Union[CfnSimpleTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7bc8998ec79f64c212ffc00232a5ebaf9c513a6b11e4efda7292d9a69691c8(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae7c4bce351d0b7f6de3229fbc4b9d614777e9ad21ad34c2daa62778234eae9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846f3714de353ef22bad0fb130478210893e73cf99bb7d30d4372ea32d1328f8(
    value: typing.Optional[typing.Union[CfnSimpleTable.PrimaryKeyProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bb119576bfc8e2295756d5ca76b923671f26be0ad39fb48a587d67ad15707d(
    value: typing.Optional[typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7894a16a6821788d3ad385df5331aa2f170a254b680dc1a83d24e0b1edfe36(
    value: typing.Optional[typing.Union[CfnSimpleTable.SSESpecificationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0a5fd537a53d2f88667e33bfe747ea6254dc5cd2c3c4a814336511cac7a649(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c39f460fee285d965b5d5ace9481d479ab5d07043ef03a78ebdb620b509c87f(
    *,
    type: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac88047acc8e01622c99d653e2a0504d82a054a24cef371572734385a06f064(
    *,
    write_capacity_units: jsii.Number,
    read_capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e3a74ff254a07b2e0d05ed197d48744c7d07e8042df0f7ae44c2dd4dd3856f(
    *,
    sse_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e367d7231cd973a844124a4129768a224ad6f5aa81749af11fe8e0a676a8aa1c(
    *,
    primary_key: typing.Optional[typing.Union[typing.Union[CfnSimpleTable.PrimaryKeyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    provisioned_throughput: typing.Optional[typing.Union[typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sse_specification: typing.Optional[typing.Union[typing.Union[CfnSimpleTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f261dd0ab90ba2d0f9dfd9bc6dbef41aa183f6a6dfe59a926fb7a7b7c818a1be(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    definition: typing.Any = None,
    definition_substitutions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnStateMachine.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnStateMachine.EventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    logging: typing.Optional[typing.Union[typing.Union[CfnStateMachine.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions_boundaries: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[builtins.str, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef, typing.Sequence[typing.Union[builtins.str, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing: typing.Optional[typing.Union[typing.Union[CfnStateMachine.TracingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07216c550a6c258f33e2f0440d2a653fffebfcb7a79604cbae35c9c6357993f7(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882af4bdf2ad713e6e9888d2815595b660b11326524d98d23691271be53499d8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc26613798481b6eb804cabd70e6611bafd59b7fccd9e8e25017e170f6b5ef75(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6d09fb960474f623d643f4ba812981b38ac75aa6548b1f642309d3c2662a98(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c0355ff6b86cc77af6e396b98cd849b46fd8c90501b03eac3c55050464bdc9(
    value: typing.Optional[typing.Union[builtins.str, CfnStateMachine.S3LocationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b889372b331f3d912cf0e70a79e10bfe1f3c54a6a99f9249eb8c4adad829b00(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnStateMachine.EventSourceProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4772c2e9f4530d01c63f88be4fadeee1ccc85325804f7e13a730ba4241cf8608(
    value: typing.Optional[typing.Union[CfnStateMachine.LoggingConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876774c3ef2ce660773bbb5c87ddc5b7d16335b8c6fec81bc79150d9ee971bbb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd96db9a00098d42372e7c4c10581ad2de390cba6ba8d5f1bafead7075a5e37(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c9a4acf3364986a2fde3dd2cd8b52b0a3db758a5a1019c80862415c4e7c2ed(
    value: typing.Optional[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, _IResolvable_a771d0ef, typing.List[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, CfnStateMachine.SAMPolicyTemplateProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880d6a7456d03c49121155c029d2c524510dc6237be7843c7ed8381ac07f4bbb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00bd6f8184fd1f118e4a2c58c2c2927aa176b09bb35d479620f1f865a8cdf184(
    value: typing.Optional[typing.Union[CfnStateMachine.TracingConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ff39f278f3f850d6b003762d8170bbd5151dc7757728080e64e730891e7bc2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2293073e212958f35b7dc2d0b78008219049e094cc382f7dc02c15358bfce2(
    *,
    method: builtins.str,
    path: builtins.str,
    rest_api_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626533df1a46e4afb94d528358bc617c1e624690bbc09deb2c2e873066785ec0(
    *,
    pattern: typing.Any,
    event_bus_name: typing.Optional[builtins.str] = None,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2d018eb508c04f2196cc80cdd11a377faf08bbab21144edb462d731007bf93(
    *,
    log_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ddfc96f6bb05b471d2dd4be91f276425fc70c8fad46ba1bac4db60f59da035(
    *,
    pattern: typing.Any,
    event_bus_name: typing.Optional[builtins.str] = None,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cdb34c93059c6355e5b545938269220da13fc651b40f6564346a207ee2fd8d(
    *,
    properties: typing.Union[typing.Union[CfnStateMachine.ApiEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.CloudWatchEventEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.EventBridgeRuleEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.ScheduleEventProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e7e889b7e2ea44115a1baddb54719b5ccf53e1257e5e6ab545bebef09f9463(
    *,
    function_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b13e69a5b6a4d4b7ede5996edf77e7f2247fb74af351b33f4501b96f8f839e9(
    *,
    statement: typing.Any,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7647230b6f50304a7ceda85cf1a565f99966b488a7ee409040d85a8f8db5483d(
    *,
    cloud_watch_logs_log_group: typing.Union[typing.Union[CfnStateMachine.CloudWatchLogsLogGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9394a19a79c6f80932de0dae180f7c0655d650bdfa30024947488cc50be70c2e(
    *,
    destinations: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStateMachine.LogDestinationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    include_execution_data: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    level: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4155b9df3c5b781536b1680b03fd7fa43f056a49a9724fb3faafa9da7172aa87(
    *,
    bucket: builtins.str,
    key: builtins.str,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900d97ed7047a8926d5afdf95a530da25b5a17541730d6341bb925b834336194(
    *,
    lambda_invoke_policy: typing.Optional[typing.Union[typing.Union[CfnStateMachine.FunctionSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    step_functions_execution_policy: typing.Optional[typing.Union[typing.Union[CfnStateMachine.StateMachineSAMPTProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6692ae7dcfc8a332fcfc1f51c9546dfee12346baca761ea1181f597571701bf(
    *,
    schedule: builtins.str,
    input: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b62dacde000a760a0c2215db364a7b0571a4ecd661abe84c37da374d3aa5a9e(
    *,
    state_machine_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8430214daa5bfd3d59048144f188d3254406152a8bf8db1c31c606db29fc61(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80311e231e4568de61f027208a83dac0d2246d793c7508ae6f6307a984d79fb2(
    *,
    definition: typing.Any = None,
    definition_substitutions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, typing.Union[CfnStateMachine.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnStateMachine.EventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    logging: typing.Optional[typing.Union[typing.Union[CfnStateMachine.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions_boundaries: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[builtins.str, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef, typing.Sequence[typing.Union[builtins.str, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing: typing.Optional[typing.Union[typing.Union[CfnStateMachine.TracingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
